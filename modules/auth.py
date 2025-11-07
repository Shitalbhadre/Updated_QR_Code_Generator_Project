from modules.utils import connect_db, hash_password, verify_password

def signup(username, email, password, role='user'):
    conn = connect_db()
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username,email,password,role) VALUES (?,?,?,?)",
                       (username,email,hashed,role))
        conn.commit()
        return True, "Signup successful!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id,password,role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_id, hashed, role = user
        if verify_password(password, hashed):
            return True, user_id, role
    return False, None, None
