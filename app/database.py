import sqlite3
from pathlib import Path
from flask import g
from config import Config   

def get_db_path():
    return Path(__file__).resolve().parent.parent / "database" / "app.db"

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
CREATE TABLE sensors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    legacy_id   INTEGER UNIQUE,
    external_id TEXT    UNIQUE,
    type        TEXT    NOT NULL,
    name        TEXT    NOT NULL,
    location    TEXT    NOT NULL
                        DEFAULT '',
    unit        TEXT    NOT NULL
                        DEFAULT '',
    state       TEXT    NOT NULL
                        DEFAULT 'inconnu',
    last_seen   TEXT
);

    """)
    db.commit()
    db.close()