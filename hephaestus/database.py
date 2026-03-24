import sqlite3
import os

def get_db_path():
    """Get the path to the Hephaestus user database in the home directory."""
    hephaestus_dir = os.path.expanduser("~/.hephaestus")
    os.makedirs(hephaestus_dir, exist_ok=True)
    return os.path.join(hephaestus_dir, "revenue_leak.db")

def get_connection():
    """Returns a database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    # This allows us to access columns by name (e.g., row['user_id'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    pass

def reset_db():
    pass
