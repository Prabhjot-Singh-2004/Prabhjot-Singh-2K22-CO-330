import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "boostly.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance INTEGER NOT NULL DEFAULT 100,
        sent_this_month INTEGER NOT NULL DEFAULT 0,
        month_key TEXT NOT NULL DEFAULT ''
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recognitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        message TEXT,
        timestamp TEXT,
        endorsements_count INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(sender_id) REFERENCES students(id),
        FOREIGN KEY(receiver_id) REFERENCES students(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS endorsements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recognition_id INTEGER NOT NULL,
        endorser_id INTEGER NOT NULL,
        timestamp TEXT,
        UNIQUE(recognition_id, endorser_id),
        FOREIGN KEY(recognition_id) REFERENCES recognitions(id),
        FOREIGN KEY(endorser_id) REFERENCES students(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS redemptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        credits INTEGER NOT NULL,
        value INTEGER NOT NULL,
        timestamp TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    );
    """)

    conn.commit()
    conn.close()
