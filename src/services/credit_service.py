from datetime import date
from models import update_student, get_student

MONTHLY_ISSUE = 100
MONTHLY_SEND_LIMIT = 100
CARRY_FORWARD_LIMIT = 50

def current_month_key():
    today = date.today()
    return f"{today.year}-{today.month:02d}"

def ensure_monthly_state(student):
    key = current_month_key()
    if not student:
        return
    if student["month_key"] != key:
        carry = min(student["balance"], CARRY_FORWARD_LIMIT)
        new_balance = MONTHLY_ISSUE + carry
        update_student(student["id"], balance=new_balance, sent_this_month=0, month_key=key)
