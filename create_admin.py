from modules.utils import users_collection, hash_password
from datetime import datetime

def create_admin(username, email, password):
    if users_collection.find_one({"username": username}):
        print(f"Admin '{username}' already exists")
        return
    hashed = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed,
        "role": "admin",
        "created_at": datetime.utcnow()
    })
    print(f"Admin '{username}' created successfully!")

if __name__ == "__main__":
    create_admin("SujataBhadre", "sujatabhadre@gmail.com", "admin123")
