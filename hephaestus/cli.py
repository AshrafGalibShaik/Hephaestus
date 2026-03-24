"""
 ▉ HEPHAESTUS — Financial Intelligence Terminal ▉

 Entry point for the CLI.
"""

import os
import sys
import glob

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

def get_db_path():
    hephaestus_dir = os.path.expanduser("~/.hephaestus")
    return os.path.join(hephaestus_dir, "revenue_leak.db")

def has_data():
    """Check if the database has data loaded."""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        return False
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='raw_data'")
        if not cursor.fetchone():
            conn.close()
            return False
        cursor.execute("SELECT COUNT(*) FROM raw_data")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False

def get_row_count():
    """Get number of rows in the database."""
    try:
        import sqlite3
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM raw_data")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0

def scan_for_csvs():
    """Find CSV files in common locations from current working directory."""
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
    banner = Text(justify="center")
    banner.append("▉ H E P H A E S T U S ▉\n", style="bold cyan")
    banner.append("Financial Intelligence Terminal\n", style="dim orange1")
    console.print(Panel(banner, border_style="cyan", style="on black", padding=(1, 4)))

def import_flow():
    """Guide user through importing a CSV."""
    console.print("\n[bold cyan]── DATA IMPORT ──[/bold cyan]\n")
    
    csvs = scan_for_csvs()
    
    if csvs:
        console.print("[bold orange1]CSV files found nearby:[/bold orange1]\n")
        table = Table(show_header=True, border_style="cyan", style="on black")
        table.add_column("#", style="cyan", width=4)
        table.add_column("File", style="orange1")
        table.add_column("Size", style="dim")
        
        for i, f in enumerate(csvs, 1):
            size = os.path.getsize(f)
            size_str = f"{size/1024:.0f} KB" if size > 1024 else f"{size} B"
            # Show relative path if possible
            try:
                rel_path = os.path.relpath(f, os.getcwd())
            except ValueError:
                rel_path = f
            table.add_row(str(i), rel_path, size_str)
        
        console.print(table)
        console.print()
        
        choice = Prompt.ask(
            f"[cyan]Pick a file (1-{len(csvs)}) or type a custom external path[/cyan]",
            default="1"
        )
        
        if choice.isdigit() and 1 <= int(choice) <= len(csvs):
            filepath = csvs[int(choice) - 1]
        else:
            filepath = choice.strip().strip('"').strip("'")
    else:
        filepath = Prompt.ask("[cyan]Enter the path to your CSV file[/cyan]")
        filepath = filepath.strip().strip('"').strip("'")
    
    # Resolve relative paths relative to CWD
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
        
    if not os.path.isfile(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        return
    
    console.print(f"\n[dim]Importing: {filepath}[/dim]\n")
    
    # Run the import
    from hephaestus.import_data import import_csv
    import_csv(filepath)

def dashboard_flow():
    """Launch the Bloomberg terminal dashboard."""
    console.print("\n[dim]Launching terminal...[/dim]\n")
    from hephaestus.main import main as run_dashboard
    run_dashboard()

def main():
    show_banner()
    
    data_loaded = has_data()
    
    if data_loaded:
        rows = get_row_count()
        console.print(f"[green]✓ Database loaded:[/green] [bold]{rows}[/bold] records\n")
    else:
        console.print("[yellow]⚠ No data loaded yet.[/yellow] Import a CSV to get started.\n")
    
    # Menu
    table = Table(show_header=False, border_style="cyan", style="on black", padding=(0, 2))
    table.add_column("Key", style="bold cyan", width=6)
    table.add_column("Action", style="orange1")
    
    if data_loaded:
        table.add_row("[1]", "Launch Dashboard")
        table.add_row("[2]", "Import New Data (CSV)")
        table.add_row("[3]", "Exit")
    else:
        table.add_row("[1]", "Import Data (CSV)")
        table.add_row("[2]", "Exit")
    
    console.print(table)
    console.print()
    
    choice = Prompt.ask("[cyan]Select[/cyan]", choices=["1", "2", "3"] if data_loaded else ["1", "2"], default="1")
    
    if data_loaded:
        if choice == "1":
            dashboard_flow()
        elif choice == "2":
            import_flow()
            if has_data():
                if Confirm.ask("\n[cyan]Launch dashboard now?[/cyan]", default=True):
                    dashboard_flow()
        else:
            console.print("[dim]Goodbye.[/dim]")
    else:
        if choice == "1":
            import_flow()
            if has_data():
                if Confirm.ask("\n[cyan]Launch dashboard now?[/cyan]", default=True):
                    dashboard_flow()
        else:
            console.print("[dim]Goodbye.[/dim]")

if __name__ == "__main__":
    main()
