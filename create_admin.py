from modules.utils import connect_db, hash_password

def create_admin(username, email, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                   (username, email, hashed, "admin"))
    conn.commit()
    conn.close()
    print(f"Admin '{username}' created successfully!")

if __name__ == "__main__":
    username = input("Admin username: ")
    email = input("Admin email: ")
    password = input("Admin password: ")
    create_admin(username, email, password)
