"""
 ▉ HEPHAESTUS — Financial Intelligence Terminal ▉
"""

import os
import sys
import glob
import sqlite3
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich.align import Align

console = Console()

# Bloomberg palette — amber on black, nothing else
A = "orange1"       # Amber — primary text
D = "dim"           # Dimmed — secondary/muted
B = "bright_white"  # Bright — emphasis
BD = "orange1 dim"  # Dim amber

def get_db_path():
    return os.path.join(os.path.expanduser("~/.hephaestus"), "revenue_leak.db")

def has_data():
    db = get_db_path()
    if not os.path.exists(db):
        return False
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='raw_data'")
        if not cur.fetchone():
            conn.close()
            return False
        cur.execute("SELECT COUNT(*) FROM raw_data")
        n = cur.fetchone()[0]
        conn.close()
        return n > 0
    except Exception:
        return False

def get_row_count():
    try:
        conn = sqlite3.connect(get_db_path())
        n = conn.cursor().execute("SELECT COUNT(*) FROM raw_data").fetchone()[0]
        conn.close()
        return n
    except Exception:
        return 0

def scan_for_csvs():
    cwd = os.getcwd()
    found = []
    for pattern in [
        os.path.join(cwd, '*.csv'),
        os.path.join(cwd, 'data', '*.csv'),
        os.path.join(cwd, 'sample data', '*.csv'),
    ]:
        found.extend(glob.glob(pattern))
    return found

def show_banner():
    console.clear()
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    
    # Top bar — like a Bloomberg header
    header = Text(justify="center")
    header.append("H E P H A E S T U S", style=f"bold {A}")
    
    console.print(Panel(
        header,
        border_style=A,
        style="on black",
        padding=(1, 2),
        subtitle=f"[{D}]{now}[/{D}]",
        subtitle_align="right"
    ))
    
    console.print(
        Text("  FINANCIAL INTELLIGENCE TERMINAL", style=f"{D}"),
        justify="center"
    )
    console.print()

def import_flow():
    console.print(Rule(f"[{A}]DATA IMPORT[/{A}]", style=D))
    console.print()
    
    csvs = scan_for_csvs()
    
    if csvs:
        console.print(f"  [{D}]CSV files detected:[/{D}]\n")
        
        for i, f in enumerate(csvs, 1):
            size = os.path.getsize(f)
            size_str = f"{size/1024:.0f}KB" if size > 1024 else f"{size}B"
            try:
                rel = os.path.relpath(f, os.getcwd())
            except ValueError:
                rel = f
            console.print(f"  [{A}]{i}[/{A}]  [{D}]│[/{D}]  {rel}  [{D}]{size_str}[/{D}]")
        
        console.print()
        choice = Prompt.ask(
            f"  [{A}]SELECT FILE[/{A}] [{D}](1-{len(csvs)} or path)[/{D}]",
            default="1"
        )
        
        if choice.isdigit() and 1 <= int(choice) <= len(csvs):
            filepath = csvs[int(choice) - 1]
        else:
            filepath = choice.strip().strip('"').strip("'")
    else:
        filepath = Prompt.ask(f"  [{A}]FILE PATH[/{A}]")
        filepath = filepath.strip().strip('"').strip("'")
    
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
        
    if not os.path.isfile(filepath):
        console.print(f"\n  [red]ERROR  File not found[/red]")
        return
    
    console.print(f"\n  [{D}]Loading {os.path.basename(filepath)}...[/{D}]\n")
    
    from hephaestus.import_data import import_csv
    import_csv(filepath)

def dashboard_flow():
    console.print(f"\n  [{D}]Initializing terminal...[/{D}]\n")
    from hephaestus.main import main as run_dashboard
    run_dashboard()

def main():
    show_banner()
    
    data_loaded = has_data()
    
    if data_loaded:
        rows = get_row_count()
        console.print(f"  [{A}]●[/{A}]  [{D}]DATABASE[/{D}]  [{B}]{rows:,}[/{B}] [{D}]records loaded[/{D}]")
    else:
        console.print(f"  [{D}]○  DATABASE  No data loaded[/{D}]")
    
    console.print()
    console.print(Rule(style=D))
    console.print()
    
    if data_loaded:
        console.print(f"  [{A}]1[/{A}]  [{D}]│[/{D}]  Launch Terminal")
        console.print(f"  [{A}]2[/{A}]  [{D}]│[/{D}]  Import Data")
        console.print(f"  [{A}]3[/{A}]  [{D}]│[/{D}]  Exit")
        console.print()
        choice = Prompt.ask(f"  [{A}]>[/{A}]", choices=["1", "2", "3"], default="1", show_choices=False)
    else:
        console.print(f"  [{A}]1[/{A}]  [{D}]│[/{D}]  Import Data")
        console.print(f"  [{A}]2[/{A}]  [{D}]│[/{D}]  Exit")
        console.print()
        choice = Prompt.ask(f"  [{A}]>[/{A}]", choices=["1", "2"], default="1", show_choices=False)
    
    if data_loaded:
        if choice == "1":
            dashboard_flow()
        elif choice == "2":
            import_flow()
            if has_data() and Confirm.ask(f"\n  [{A}]Launch terminal?[/{A}]", default=True):
                dashboard_flow()
        else:
            console.print(f"\n  [{D}]Session terminated.[/{D}]\n")
    else:
        if choice == "1":
            import_flow()
            if has_data() and Confirm.ask(f"\n  [{A}]Launch terminal?[/{A}]", default=True):
                dashboard_flow()
        else:
            console.print(f"\n  [{D}]Session terminated.[/{D}]\n")

if __name__ == "__main__":
    main()
