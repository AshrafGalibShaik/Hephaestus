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

from hephaestus.config import (
    load_config, save_config, is_configured,
    SUPPORTED_MODELS, CONFIG_DIR
)

console = Console()

# Bloomberg palette
A = "orange1"
D = "dim"
B = "bright_white"

def get_db_path():
    return os.path.join(CONFIG_DIR, "revenue_leak.db")

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
    console.print(Text("  FINANCIAL INTELLIGENCE TERMINAL", style=D), justify="center")
    console.print()

# ── First-Run Setup ──────────────────────────────────────────────

def first_run_setup():
    """First-time setup wizard: model selection + API key."""
    show_banner()
    
    console.print(Rule(f"[{A}]FIRST-TIME SETUP[/{A}]", style=D))
    console.print()
    console.print(f"  [{D}]Welcome. Let's configure your AI engine.[/{D}]")
    console.print()
    
    # Model selection
    console.print(f"  [{A}]Select your AI model:[/{A}]")
    console.print()
    
    console.print(f"  [{D}]── Google Gemini ──[/{D}]")
    for key in ["1", "2", "3"]:
        m = SUPPORTED_MODELS[key]
        console.print(f"  [{A}]{key}[/{A}]  [{D}]│[/{D}]  {m['name']}")
    
    console.print()
    console.print(f"  [{D}]── OpenAI ──[/{D}]")
    for key in ["4", "5", "6"]:
        m = SUPPORTED_MODELS[key]
        console.print(f"  [{A}]{key}[/{A}]  [{D}]│[/{D}]  {m['name']}")
    
    console.print()
    choice = Prompt.ask(
        f"  [{A}]MODEL[/{A}]",
        choices=list(SUPPORTED_MODELS.keys()),
        default="1"
    )
    
    model = SUPPORTED_MODELS[choice]
    console.print(f"\n  [{D}]Selected:[/{D}]  [{B}]{model['name']}[/{B}]")
    
    # API key
    console.print()
    
    if model['provider'] == 'google':
        console.print(f"  [{D}]Get your key at: https://aistudio.google.com/apikey[/{D}]")
    else:
        console.print(f"  [{D}]Get your key at: https://platform.openai.com/api-keys[/{D}]")
    
    console.print()
    api_key = Prompt.ask(f"  [{A}]{model['key_env']}[/{A}]")
    
    if not api_key.strip():
        console.print(f"\n  [{D}]No key provided. You can configure later.[/{D}]")
        api_key = ""
    
    # Save
    config = {
        "model_id": model['id'],
        "model_name": model['name'],
        "provider": model['provider'],
        "api_key": api_key.strip()
    }
    save_config(config)
    
    console.print(f"\n  [{A}]●[/{A}]  [{D}]Configuration saved to[/{D}]  [{D}]~/.hephaestus/config.json[/{D}]")
    console.print()
    
    return config

# ── Data Import ──────────────────────────────────────────────────

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
        console.print(f"  [{D}]Or type a full path to any CSV on your machine.[/{D}]")
        console.print()
        choice = Prompt.ask(
            f"  [{A}]SELECT[/{A}] [{D}](1-{len(csvs)} or path)[/{D}]",
            default="1"
        )
        
        if choice.isdigit() and 1 <= int(choice) <= len(csvs):
            filepath = csvs[int(choice) - 1]
        else:
            filepath = choice.strip().strip('"').strip("'")
    else:
        console.print(f"  [{D}]No CSV files found in this directory.[/{D}]")
        console.print(f"  [{D}]Enter the full path to any CSV file on your machine:[/{D}]")
        console.print()
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

# ── Settings ─────────────────────────────────────────────────────

def settings_flow():
    """Reconfigure AI model and API key."""
    console.print(Rule(f"[{A}]SETTINGS[/{A}]", style=D))
    console.print()
    
    config = load_config()
    console.print(f"  [{D}]Current model:[/{D}]  [{B}]{config.get('model_name', 'Not set')}[/{B}]")
    console.print(f"  [{D}]API key:[/{D}]       [{B}]{'••••' + config.get('api_key', '')[-4:] if config.get('api_key') else 'Not set'}[/{B}]")
    console.print()
    
    if Confirm.ask(f"  [{A}]Reconfigure?[/{A}]", default=False):
        first_run_setup()

# ── Main ─────────────────────────────────────────────────────────

def main():
    # First-run: setup wizard
    if not is_configured():
        config = first_run_setup()
        
        # After setup, prompt for data import
        console.print(Rule(f"[{A}]LOAD YOUR DATA[/{A}]", style=D))
        console.print()
        console.print(f"  [{D}]Now import a CSV file to get started.[/{D}]")
        console.print()
        import_flow()
        
        if has_data() and Confirm.ask(f"\n  [{A}]Launch terminal?[/{A}]", default=True):
            dashboard_flow()
        return
    
    # Normal flow
    show_banner()
    
    config = load_config()
    console.print(f"  [{A}]●[/{A}]  [{D}]AI[/{D}]     [{B}]{config.get('model_name', 'Not configured')}[/{B}]")
    
    data_loaded = has_data()
    if data_loaded:
        rows = get_row_count()
        console.print(f"  [{A}]●[/{A}]  [{D}]DATA[/{D}]   [{B}]{rows:,}[/{B}] [{D}]records[/{D}]")
    else:
        console.print(f"  [{D}]○  DATA   No data loaded[/{D}]")
    
    console.print()
    console.print(Rule(style=D))
    console.print()
    
    if data_loaded:
        console.print(f"  [{A}]1[/{A}]  [{D}]│[/{D}]  Launch Terminal")
        console.print(f"  [{A}]2[/{A}]  [{D}]│[/{D}]  Import Data")
        console.print(f"  [{A}]3[/{A}]  [{D}]│[/{D}]  Settings")
        console.print(f"  [{A}]4[/{A}]  [{D}]│[/{D}]  Exit")
        console.print()
        choice = Prompt.ask(f"  [{A}]>[/{A}]", choices=["1","2","3","4"], default="1", show_choices=False)
    else:
        console.print(f"  [{A}]1[/{A}]  [{D}]│[/{D}]  Import Data")
        console.print(f"  [{A}]2[/{A}]  [{D}]│[/{D}]  Settings")
        console.print(f"  [{A}]3[/{A}]  [{D}]│[/{D}]  Exit")
        console.print()
        choice = Prompt.ask(f"  [{A}]>[/{A}]", choices=["1","2","3"], default="1", show_choices=False)
    
    if data_loaded:
        if choice == "1":
            dashboard_flow()
        elif choice == "2":
            import_flow()
            if has_data() and Confirm.ask(f"\n  [{A}]Launch terminal?[/{A}]", default=True):
                dashboard_flow()
        elif choice == "3":
            settings_flow()
        else:
            console.print(f"\n  [{D}]Session terminated.[/{D}]\n")
    else:
        if choice == "1":
            import_flow()
            if has_data() and Confirm.ask(f"\n  [{A}]Launch terminal?[/{A}]", default=True):
                dashboard_flow()
        elif choice == "2":
            settings_flow()
        else:
            console.print(f"\n  [{D}]Session terminated.[/{D}]\n")

if __name__ == "__main__":
    main()
