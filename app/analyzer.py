import pandas as pd
import numpy as np
import sqlite3
from database import get_connection

class RevenueAnalyzer:
    def __init__(self):
        self.conn = get_connection()
        
    def get_funnel_metrics(self):
        """Calculates conversion rates through the funnel."""
        query = """
        SELECT event_type, COUNT(DISTINCT user_id) as users 
        FROM events 
        GROUP BY event_type
        """
        df = pd.read_sql_query(query, self.conn)
        
        # Order the funnel
        funnel_order = ['visit', 'product_view', 'add_to_cart', 'checkout_start', 'purchase']
        df['event_type'] = pd.Categorical(df['event_type'], categories=funnel_order, ordered=True)
        df = df.sort_values('event_type').reset_index(drop=True)
        
        # Calculate rates
        df['conversion_rate'] = (df['users'] / df['users'].shift(1) * 100).fillna(100).round(2)
        df['dropoff_rate'] = (100 - df['conversion_rate']).round(2)
        df.loc[0, 'dropoff_rate'] = 0.0 # First step has no dropoff
        
        return df
        
    def get_revenue_loss(self, funnel_df):
        """Quantifies the loss in revenue."""
        # Get Average Order Value
        query = "SELECT AVG(revenue) as aov FROM orders"
        cursor = self.conn.cursor()
        cursor.execute(query)
        aov_row = cursor.fetchone()
        aov = aov_row['aov'] if aov_row and aov_row['aov'] else 0
        
        # Calculate impact if we improved each step by recovering 15% of dropped users
        loss_analysis = []
        visitors = funnel_df.loc[0, 'users'] if not funnel_df.empty else 0
        
        for i in range(1, len(funnel_df)):
            step = funnel_df.loc[i, 'event_type']
            current_users = funnel_df.loc[i, 'users']
            prev_users = funnel_df.loc[i-1, 'users']
            
            # If we converted 15% more users who dropped off at this stage
            dropped = prev_users - current_users
            recovered = int(dropped * 0.15)
            
            # Probability that a user AT this step eventually purchases
            purchasers = funnel_df.loc[len(funnel_df)-1, 'users']
            if current_users > 0:
                prob_purchase = purchasers / current_users
            else:
                prob_purchase = 0
                
            est_recovered_purchases = recovered * prob_purchase
            est_monthly_upside = est_recovered_purchases * aov
            
            loss_analysis.append({
                'stage': step,
                'dropoff_count': int(dropped),
                'recovered_target': int(recovered),
                'est_revenue_upside': float(est_monthly_upside)
            })
            
        return pd.DataFrame(loss_analysis), aov
        
    def get_device_breakdown(self):
        """Segments cart to checkout drop-off by device."""
        query = """
        SELECT u.device_type, 
               COUNT(DISTINCT e1.user_id) as cart_users,
               COUNT(DISTINCT e2.user_id) as checkout_users
        FROM events e1
        JOIN users u ON e1.user_id = u.user_id
        LEFT JOIN events e2 ON e1.user_id = e2.user_id AND e2.event_type = 'checkout_start'
        WHERE e1.event_type = 'add_to_cart'
        GROUP BY u.device_type
        """
        df = pd.read_sql_query(query, self.conn)
        df['conversion'] = (df['checkout_users'] / df['cart_users'] * 100).round(2)
        df['dropoff'] = (100 - df['conversion']).round(2)
        return df
        
    def get_marketing_roi(self):
        query = """
        SELECT c.source, 
               c.cost,
               COALESCE(SUM(o.revenue), 0) as total_revenue
        FROM campaigns c
        LEFT JOIN users u ON c.source = u.source
        LEFT JOIN orders o ON u.user_id = o.user_id
        GROUP BY c.source
        """
        df = pd.read_sql_query(query, self.conn)
        df['roi_percent'] = np.where(df['cost'] > 0, 
                                     ((df['total_revenue'] - df['cost']) / df['cost'] * 100).round(2), 
                                     np.where(df['total_revenue'] > 0, float('inf'), 0.0))
        return df
        
    def get_summary_metrics(self):
        funnel = self.get_funnel_metrics()
        loss, aov = self.get_revenue_loss(funnel)
        device = self.get_device_breakdown()
        roi = self.get_marketing_roi()
        
        biggest_leak = loss.loc[loss['est_revenue_upside'].idxmax()] if not loss.empty else None
        
        return {
            'funnel': funnel.to_dict(orient='records'),
            'loss_analysis': loss.to_dict(orient='records'),
            'device_breakdown': device.to_dict(orient='records'),
            'roi': roi.to_dict(orient='records'),
            'aov': round(aov, 2),
            'top_leak_stage': biggest_leak['stage'] if biggest_leak is not None else 'N/A',
            'top_leak_value': round(biggest_leak['est_revenue_upside'], 2) if biggest_leak is not None else 0
        }

if __name__ == "__main__":
    analyzer = RevenueAnalyzer()
    metrics = analyzer.get_summary_metrics()
    import json
    print(json.dumps(metrics, indent=2))
