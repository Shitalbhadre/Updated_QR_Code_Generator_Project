import sqlite3
import bcrypt
import os

from pymongo import MongoClient
from datetime import datetime

# Function to connect to local MongoDB
def connect_mongo():
    """
    Connects to local MongoDB (localhost:27017) and returns the database object.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["qr_app"]  # Database name
    return db


DB_PATH = os.path.join("db", "database.db")

def connect_db():
    if not os.path.exists("db"):
        os.makedirs("db")
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qrcodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        content TEXT,
        file_path TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)

def get_user_qrcodes(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, content, file_path, created_at
        FROM qrcodes WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows
