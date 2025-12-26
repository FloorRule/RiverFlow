import sqlite3

DB_PATH = "ocean.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS workflow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    service TEXT NOT NULL,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    is_threat BOOLEAN DEFAULT FALSE
);
"""

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.close()
    
def get_connection():
    return sqlite3.connect(DB_PATH)