import sqlite3
import requests

DATABASE = 'data/user_database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                   id INTEGER PRIMARY KEY,
                   first_name TEXT NOT NULL,
                   last_name TEXT,
                   age INTEGER,
                   gender TEXT,
                   email TEXT,
                   phone TEXT, 
                   birth_date TEXT
    )''')

    conn.commit()
    conn.close()

def create_user(first_name, last_name, age, gender, email, phone, birth_date):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO user (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (first_name, last_name, age, gender, email, phone, birth_date)
    )
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    
    conn.close()

    return users


