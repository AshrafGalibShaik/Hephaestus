-- Generic data table (auto-populated from any CSV)
-- Columns are created dynamically at import time.
-- This schema is just a placeholder; import_data.py builds the real table.
CREATE TABLE IF NOT EXISTS raw_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
