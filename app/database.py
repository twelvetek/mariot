import sqlite3
from pathlib import Path
from flask import g

def get_db_path():
    return Path(__file__).resolve().parent.parent / "instance" / "app.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(get_db_path())
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(get_db_path())
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    db.commit()
    db.close()