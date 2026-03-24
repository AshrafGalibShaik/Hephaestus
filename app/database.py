import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'revenue_leak.db')
SCHEMA_PATH = os.path.join(PROJECT_ROOT, 'data', 'schema.sql')

def get_connection():
    """Returns a database connection."""
    conn = sqlite3.connect(DB_PATH)
    # This allows us to access columns by name (e.g., row['user_id'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the schema."""
    conn = get_connection()
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, 'r') as f:
            try:
                conn.executescript(f.read())
                print(f"[success] Initialized tables from {SCHEMA_PATH}")
            except sqlite3.Error as e:
                print(f"[error] SQLite error: {e}")
    else:
        print(f"[error] {SCHEMA_PATH} not found.")
    
    conn.commit()
    conn.close()

def reset_db():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except OSError:
            pass
    init_db()

if __name__ == "__main__":
    reset_db()
