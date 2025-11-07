from modules.utils import users_collection, hash_password, verify_password
from datetime import datetime
from bson.objectid import ObjectId
from modules.utils import users_collection, qrcodes_collection, hash_password, verify_password, add_qrcode, get_user_qrcodes


# Signup function for Streamlit
def signup(username: str, email: str, password: str):
    if users_collection.find_one({"username": username}):
        return False, "Username already exists"
    if users_collection.find_one({"email": email}):
        return False, "Email already exists"

    hashed = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed,
        "role": "user",
        "created_at": datetime.utcnow()
    })
    return True, "Signup successful"

# Login function
def login(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True, str(user["_id"]), user["role"]
    return False, None, None
