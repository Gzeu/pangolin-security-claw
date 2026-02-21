import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pangolin_guard.db")

def get_connection():
    """Returns a raw sqlite3 connection. No ORM, no attack surface."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates all tables if they do not exist yet (no migrations needed)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS encrypted_scales (
            id          TEXT PRIMARY KEY,
            filename    TEXT NOT NULL,
            total_chunks INTEGER NOT NULL,
            status      TEXT DEFAULT 'ARMORED',
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS threat_radar (
            id          TEXT PRIMARY KEY,
            entity_type TEXT NOT NULL,
            identifier  TEXT NOT NULL,
            scent_level INTEGER DEFAULT 0,
            status      TEXT DEFAULT 'ACTIVE',
            last_seen   TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS data_leaks (
            id               TEXT PRIMARY KEY,
            file_path        TEXT NOT NULL,
            leak_type        TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            resolved         INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()
    print("[DB] SQLite initialized successfully (stdlib only, no ORM).")
