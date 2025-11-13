from database import get_db
from datetime import datetime

def create_student(name):
    db = get_db()
    now = datetime.utcnow().isoformat()
    cur = db.cursor()
    cur.execute("INSERT INTO students (name, month_key) VALUES (?, ?)", (name, now[:7]))
    db.commit()
    return cur.lastrowid

def get_student(sid):
    db = get_db()
    return db.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()

def update_student(sid, **kwargs):
    db = get_db()
    cols = []
    vals = []
    for k, v in kwargs.items():
        cols.append(f"{k} = ?")
        vals.append(v)
    vals.append(sid)
    db.execute(f"UPDATE students SET {', '.join(cols)} WHERE id = ?", vals)
    db.commit()

def insert_recognition(sender_id, receiver_id, amount, message):
    db = get_db()
    ts = datetime.utcnow().isoformat()
    cur = db.cursor()
    cur.execute("INSERT INTO recognitions (sender_id, receiver_id, amount, message, timestamp) VALUES (?, ?, ?, ?, ?)",
                (sender_id, receiver_id, amount, message, ts))
    db.commit()
    return cur.lastrowid

def get_recognition(rid):
    db = get_db()
    return db.execute("SELECT * FROM recognitions WHERE id = ?", (rid,)).fetchone()

def increment_recognition_endorsements(rid):
    db = get_db()
    db.execute("UPDATE recognitions SET endorsements_count = endorsements_count + 1 WHERE id = ?", (rid,))
    db.commit()

def insert_endorsement(recognition_id, endorser_id):
    db = get_db()
    ts = datetime.utcnow().isoformat()
    cur = db.cursor()
    cur.execute("INSERT INTO endorsements (recognition_id, endorser_id, timestamp) VALUES (?, ?, ?)",
                (recognition_id, endorser_id, ts))
    db.commit()
    return cur.lastrowid

def sum_redemptions(student_id):
    db = get_db()
    row = db.execute("SELECT COALESCE(SUM(credits),0) as s FROM redemptions WHERE student_id = ?", (student_id,)).fetchone()
    return row["s"] if row else 0

def insert_redemption(student_id, credits, value):
    db = get_db()
    ts = datetime.utcnow().isoformat()
    cur = db.cursor()
    cur.execute("INSERT INTO redemptions (student_id, credits, value, timestamp) VALUES (?, ?, ?, ?)",
                (student_id, credits, value, ts))
    db.commit()
    return cur.lastrowid

def get_top_students(limit=10):
    db = get_db()
    rows = db.execute("""
        SELECT s.id, s.name, s.balance, s.sent_this_month, s.month_key,
               (SELECT COALESCE(SUM(amount),0) FROM recognitions r WHERE r.receiver_id = s.id) as total_received,
               (SELECT COUNT(*) FROM recognitions r WHERE r.receiver_id = s.id) as recognitions_count,
               (SELECT COALESCE(SUM(r.endorsements_count),0) FROM recognitions r WHERE r.receiver_id = s.id) as endorsements_total
        FROM students s
        ORDER BY total_received DESC, s.id ASC
        LIMIT ?
    """, (limit,)).fetchall()
    return rows
