import sqlite3
import pandas as pd
from hephaestus.database import get_connection

class RevenueAnalyzer:
    """Universal analyzer — auto-detects columns and builds insights from any CSV."""
    
    def __init__(self):
        self.conn = get_connection()
        self.df = pd.read_sql_query("SELECT * FROM raw_data", self.conn)
        self.num_cols = self.df.select_dtypes(include='number').columns.tolist()
        self.cat_cols = self.df.select_dtypes(exclude='number').columns.tolist()
        
        # Auto-detect key columns
        self._detect_key_columns()
    
    def _detect_key_columns(self):
        """Heuristically identify the most important columns."""
        # Find the best "value" column (likely revenue, sales, profit, amount, etc.)
        value_keywords = ['profit', 'revenue', 'sales', 'amount', 'total', 'income', 'value', 'price']
        self.value_col = self._find_best_col(self.num_cols, value_keywords, fallback_to_largest=True)
        
        # Find the best "cost" column
        cost_keywords = ['cost', 'cogs', 'expense', 'spend', 'manufacturing']
        self.cost_col = self._find_best_col(self.num_cols, cost_keywords)
        
        # Find discount/loss column
        loss_keywords = ['discount', 'loss', 'deduction', 'write']
        self.loss_col = self._find_best_col(self.num_cols, loss_keywords)
        
        # Find secondary value (gross sales, revenue if value is profit, etc.)
        secondary_keywords = ['gross', 'revenue', 'sales']
        candidates = [c for c in self.num_cols if c != self.value_col]
        self.secondary_col = self._find_best_col(candidates, secondary_keywords)
        
        # Find category columns (for grouping) — pick top 3 by cardinality
        self.group_cols = []
        for col in self.cat_cols:
            nunique = self.df[col].nunique()
            if 2 <= nunique <= 20:  # Good range for chart labels
                self.group_cols.append((col, nunique))
        self.group_cols.sort(key=lambda x: x[1])
        self.group_cols = [c[0] for c in self.group_cols[:3]]
    
    def _find_best_col(self, columns, keywords, fallback_to_largest=False):
        """Find column matching keywords, with optional fallback."""
        for kw in keywords:
            for col in columns:
                if kw in col.lower():
                    return col
        if fallback_to_largest and columns:
            # Pick the numeric column with the largest absolute values
            max_col = max(columns, key=lambda c: self.df[c].abs().sum())
            return max_col
        return None
    
    def get_grouped_analysis(self, group_col):
        """Aggregate the value column by a category column."""
        if not self.value_col or not group_col:
            return pd.DataFrame()
        
        agg_dict = {self.value_col: ['sum', 'mean', 'count']}
        if self.cost_col:
            agg_dict[self.cost_col] = 'sum'
        if self.loss_col:
            agg_dict[self.loss_col] = 'sum'
        
        result = self.df.groupby(group_col).agg(agg_dict).reset_index()
        result.columns = ['_'.join(col).strip('_') for col in result.columns]
        result = result.sort_values(f'{self.value_col}_sum', ascending=False)
        return result
    
    def get_top_leaks(self, n=10):
        """Find records with the worst (most negative) value."""
        if not self.value_col:
            return pd.DataFrame()
        neg = self.df[self.df[self.value_col] < 0].copy()
        if neg.empty:
            # If no negative values, find lowest performers
            neg = self.df.nsmallest(n, self.value_col)
        else:
            neg = neg.nsmallest(n, self.value_col)
        return neg
    
    def get_summary_metrics(self):
        """Build a universal summary dict for the dashboard."""
        metrics = {
            'total_rows': len(self.df),
            'value_col': self.value_col or 'N/A',
            'cost_col': self.cost_col or 'N/A',
            'loss_col': self.loss_col or 'N/A',
            'group_cols': self.group_cols,
        }
        
        if self.value_col:
            metrics['total_value'] = round(float(self.df[self.value_col].sum()), 2)
            metrics['avg_value'] = round(float(self.df[self.value_col].mean()), 2)
            metrics['min_value'] = round(float(self.df[self.value_col].min()), 2)
            metrics['max_value'] = round(float(self.df[self.value_col].max()), 2)
        
        if self.cost_col:
            metrics['total_cost'] = round(float(self.df[self.cost_col].sum()), 2)
        
        if self.loss_col:
            metrics['total_loss'] = round(float(self.df[self.loss_col].sum()), 2)
        
        if self.value_col and self.secondary_col:
            sec_total = self.df[self.secondary_col].sum()
            if sec_total != 0:
                metrics['margin_pct'] = round(float(self.df[self.value_col].sum()) / float(sec_total) * 100, 2)
            else:
                metrics['margin_pct'] = 0.0
            metrics['secondary_col'] = self.secondary_col
            metrics['total_secondary'] = round(float(sec_total), 2)
        
        # Build grouped data for each category
        metrics['groups'] = {}
        for gc in self.group_cols:
            grouped = self.get_grouped_analysis(gc)
            metrics['groups'][gc] = grouped.to_dict(orient='records')
        
        # Leaks
        leaks = self.get_top_leaks()
        if not leaks.empty:
            neg_sum = leaks[leaks[self.value_col] < 0][self.value_col].sum() if self.value_col else 0
            metrics['total_leak_value'] = round(abs(float(neg_sum)), 2)
            # Find worst category
            if self.group_cols:
                worst_gc = self.group_cols[0]
                grouped = self.get_grouped_analysis(worst_gc)
                if not grouped.empty:
                    worst_row = grouped.iloc[-1]
                    metrics['worst_category'] = f"{worst_row[worst_gc]} ({worst_gc})"
                else:
                    metrics['worst_category'] = 'N/A'
            else:
                metrics['worst_category'] = 'N/A'
        else:
            metrics['total_leak_value'] = 0
            metrics['worst_category'] = 'N/A'
        
        return metrics

if __name__ == "__main__":
    analyzer = RevenueAnalyzer()
    metrics = analyzer.get_summary_metrics()
    import json
    print(json.dumps(metrics, indent=2, default=str))
