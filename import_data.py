"""
import_data.py — Import ANY CSV into Hephaestus.

Usage:
    python import_data.py                      # Interactive prompt
    python import_data.py "path/to/data.csv"   # Direct path

The system auto-detects your CSV columns, identifies numeric vs categorical,
and stores everything in a universal 'raw_data' table for analysis.
"""

import sys
import os
import re
import sqlite3
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from app.database import get_connection

console = Console()

def clean_currency(val):
    """Strip $, commas, parens (negative), and whitespace from currency strings."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    # If it doesn't look like a currency/number string, return as-is
    if not re.search(r'[\d$]', s):
        return s
    negative = s.startswith('(') or s.startswith('$(')
    s = re.sub(r'[$(),\s]', '', s)
    if s == '' or s == '-':
        return 0.0
    try:
        result = float(s)
        return -result if negative else result
    except ValueError:
        return val

def detect_and_clean(df):
    """Auto-detect column types and clean currency values."""
    for col in df.columns:
        sample = df[col].dropna().head(20)
        if sample.empty:
            continue
        # Check if column looks like currency/numeric
        currency_pattern = re.compile(r'^\s*\$?\s*[\d,]+\.?\d*\s*$|^\s*\(\$?[\d,]+\.?\d*\)\s*$|^\s*\$\s*-\s*$')
        matches = sample.astype(str).apply(lambda x: bool(currency_pattern.match(x))).sum()
        if matches > len(sample) * 0.5:
            df[col] = df[col].apply(clean_currency)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def import_csv(filepath):
    """Import any CSV into the database."""
    # Get DB path and delete the old database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'revenue_leak.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[orange1][progress.description]{task.description}[/orange1]"),
        transient=True
    ) as progress:
        task = progress.add_task(description="Reading CSV...", total=None)
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip()
        
        progress.update(task, description=f"Loaded {len(df)} rows, {len(df.columns)} columns. Detecting types...")
        
        # Strip text columns
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip()
        
        # Auto-detect and clean currency
        df = detect_and_clean(df)
        
        progress.update(task, description="Creating table and inserting data...")
        
        # Use pandas to write directly — it auto-creates the table
        df.to_sql('raw_data', conn, if_exists='replace', index=False)
        
        conn.commit()
        conn.close()
        
        progress.update(task, description=f"Import complete — {len(df)} records loaded.")
    
    # Show column summary
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()
    
    summary = Table(title="Detected Columns", border_style="cyan", style="on black")
    summary.add_column("Type", style="cyan")
    summary.add_column("Columns", style="orange1")
    summary.add_row("Numeric", ", ".join(num_cols) if num_cols else "None")
    summary.add_row("Categorical", ", ".join(cat_cols) if cat_cols else "None")
    console.print(summary)
    
    console.print(Panel(
        Text(f"Imported {len(df)} records from {os.path.basename(filepath)}.\nRun 'python app/main.py' to launch the terminal.", 
             style="bold green"),
        border_style="green",
        title="[bold green]IMPORT COMPLETE[/bold green]"
    ))

def main():
    console.print(Panel(
        Text(" HEPHAESTUS DATA IMPORT ", style="bold cyan on black", justify="center"),
        border_style="cyan"
    ))
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        console.print("\n[bold cyan]Enter the path to your CSV file:[/bold cyan]")
        console.print("[dim](Any CSV format is supported — columns are auto-detected)[/dim]\n")
        filepath = input("  > File path: ").strip()
    
    if not filepath or not os.path.isfile(filepath):
        console.print(f"[bold red]ERROR:[/bold red] '{filepath}' not found.")
        sys.exit(1)
    
    import_csv(filepath)

if __name__ == "__main__":
    main()
