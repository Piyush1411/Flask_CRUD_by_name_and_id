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

def search_users_by_name(first_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE first_name LIKE ?", (f"{first_name}%",))
    matching_users = cursor.fetchall()

    columns = [column[0] for column in cursor.description]  # Fetch column names

    formatted_users = [{column: user[i] for i, column in enumerate(columns)} for user in matching_users]

    conn.close()

    return formatted_users

def fetch_users_from_dummy_api(first_name):
    dummy_api_url = f"https://dummyjson.com/users/search?q={first_name}"
    response = requests.get(dummy_api_url)
    new_users_data = response.json()

    new_users = new_users_data.get('users', [])
    return new_users

def save_users_to_database(users):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    valid_users = [
        user for user in users if user.get('first_name') is not None
    ]
    
    cursor.executemany(
        "INSERT INTO user (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [(user.get('first_name'), user.get('last_name'), user.get('age'), user.get('gender'), user.get('email'), user.get('phone'), user.get('birth_date')) for user in valid_users]
    )
    conn.commit()
    conn.close()


def search_users(first_name):
    matching_users = search_users_by_name(first_name)

    if matching_users:
        return matching_users
    else:
        new_users = fetch_users_from_dummy_api(first_name)
        if new_users:
            save_users_to_database(new_users)
            return new_users
        else:
            return []