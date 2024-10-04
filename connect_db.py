import sqlite3
from datetime import datetime

def create_user_table():
    with sqlite3.connect("bencodex.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS login_user (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                name TEXT,
                email TEXT,
                password TEXT,
                setting_login INTEGER,
                status INTEGER,
                modified_by TEXT,
                modified_at DATETIME
            )
        """)
        conn.commit()

def add_user(id, user_id, name, email, password, setting_login, status, modified_by, modified_at):
    with sqlite3.connect("bencodex.db") as conn:
        modified_at = datetime.now()  # Lấy thời gian hiện tại
        c = conn.cursor()
        c.execute("""
            INSERT INTO login_user (id, user_id, name, email, password, setting_login, status, modified_by, modified_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, user_id, name, email, password, setting_login, status, modified_by, modified_at))
        conn.commit()


def login_user(user_name, password):
    with sqlite3.connect("bencodex.db") as conn:
        c = conn.cursor()
        c.execute("""
            select user_id, email, password from login_user where (user_id = ? or email = ?) and password = ?
        """, (
                user_name,
                user_name, 
                password
            )
        )

    data = c.fetchall()

    if data:  # Nếu có dữ liệu trả về
        return {
            "user_id": data[0][0], 
            "email": data[0][1], 
            "password": data[0][2]
        }  # Trả về dictionary
    else:
        return None  # Không có dữ liệu

def view_all_users():
    with sqlite3.connect("bencodex.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM login_user")
        users = c.fetchall()
    return users

def get_user_name(name, email):
    with sqlite3.connect("bencodex.db") as conn:
        c = conn.cursor()
        c.execute("""
            SELECT name FROM login_user WHERE user_id = ? OR email = ?
        """, (
            name,
            email
        ))

    data = c.fetchall()

    if data:  # Nếu có dữ liệu trả về
        return {
            "name": data[0][0]
        }  # Trả về dictionary
    else:
        return None  # Không có dữ liệu

