import sqlite3
from datetime import datetime

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect("bencodex.db")
c = conn.cursor()

def create_user_table():
    with sqlite3.connect("bencodex.db") as conn:
        c.execute("""
            CREATE TABLE IF NOT EXISTS login_user (
                id,
                user_id,
                name TEXT,
                email TEXT,
                password TEXT,
                setting_login INTEGER,
                status INTEGER,
                modified_by TEXT,
                modified_at DATETIME
            )
        """)
        conn.commit()  # Lưu thay đổi

def add_user(id, user_id, name, email, password, setting_login, status, modified_by):
    modified_at = datetime.now()  # Lấy thời gian hiện tại
    c.execute("""
        INSERT INTO login_user (
            id
            user_id
            name, 
            email, 
            password, 
            setting_login, 
            status, 
            modified_by, 
            modified_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
            id,
            user_id,
            name, 
            email, 
            password, 
            setting_login, 
            status, 
            modified_by, 
            modified_at
        )
    )
    conn.commit()  # Lưu thay đổi

def login_user(user_id, password):
    c.execute("""
        select * from login_user where user_id =? and password =?
    """, (
            user_id, 
            password
        )
    )

    data = c.fetchall()
    return data

def view_all_users():
    c.execute("""
        select * from login_user
    """)

    data = c.fetchall()
    return data







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
        c = conn.cursor()
        c.execute("""
            INSERT INTO login_user (id, user_id, name, email, password, setting_login, status, modified_by, modified_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, user_id, name, email, password, setting_login, status, modified_by, modified_at))
        conn.commit()


def login_user(user_id, password):
    with sqlite3.connect("bencodex.db") as conn:
        c = conn.cursor()
        c.execute("""
            select * from login_user where user_id =? and password =?
        """, (
                user_id, 
                password
            )
        )

    data = c.fetchall()
    return data

def view_all_users():
    with sqlite3.connect("bencodex.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM login_user")
        users = c.fetchall()
    return users
