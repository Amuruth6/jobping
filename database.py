import sqlite3
from datetime import datetime

DB_PATH = "jobping.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS postings (
            id TEXT PRIMARY KEY,
            company TEXT,
            title TEXT,
            url TEXT,
            first_seen TEXT
        )
    """)
    conn.commit()
    conn.close()


def is_new_posting(posting_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM postings WHERE id = ?", (posting_id,))
    result = cur.fetchone()
    conn.close()
    return result is None


def save_posting(posting_id, company, title, url):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO postings (id, company, title, url, first_seen) VALUES (?, ?, ?, ?, ?)",
        (posting_id, company, title, url, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()