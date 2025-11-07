import bcrypt
from pymongo import MongoClient
from datetime import datetime
import streamlit as st
from urllib.parse import quote_plus
from bson.objectid import ObjectId

# ----------------------------
# MongoDB Atlas Connection
# ----------------------------
def connect_mongo():
    username = quote_plus(st.secrets["MONGO"]["username"])
    password = quote_plus(st.secrets["MONGO"]["password"])
    cluster = st.secrets["MONGO"]["cluster"]
    database = st.secrets["MONGO"]["database"]

    MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI)
    return client[database]

# Database & Collections
db = connect_mongo()
users_collection = db["users"]
qrcodes_collection = db["qrcodes"]

# ----------------------------
# Password Functions
# ----------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)

# ----------------------------
# User Functions
# ----------------------------
def get_all_users():
    users = list(users_collection.find({}, {"username":1, "email":1, "role":1}))
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    return users

def get_user_qrcodes(user_id: str):
    qrcodes = list(qrcodes_collection.find({"user_id": ObjectId(user_id)}))
    for qr in qrcodes:
        qr["id"] = str(qr["_id"])
        del qr["_id"]
    return qrcodes

def add_qrcode(user_id: str, qr_type: str, content: str, file_path: str):
    qrcodes_collection.insert_one({
        "user_id": ObjectId(user_id),
        "qr_type": qr_type,
        "content": content,
        "file_path": file_path,
        "created_at": datetime.utcnow()
    })

# ----------------------------
# Database Initialization
# ----------------------------
def init_db():
    users_collection.create_index("username", unique=True)
    qrcodes_collection.create_index("user_id")
