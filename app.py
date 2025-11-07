import streamlit as st
import os
from modules import auth, qr_generator, utils
from modules.utils import users_collection, qrcodes_collection, hash_password, verify_password, add_qrcode, get_user_qrcodes
from datetime import datetime
from streamlit.runtime.scriptrunner import RerunException, get_script_run_ctx

st.set_page_config(page_title="QR Code Generator", layout="wide")

# ------------------------------
# Session State Initialization
# ------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.role = None

# ------------------------------
# Function to safely rerun Streamlit
# ------------------------------
def rerun():
    raise RerunException(get_script_run_ctx())

# ------------------------------
# Login / Signup
# ------------------------------
if not st.session_state.logged_in:
    st.title("Login / Signup")
    tab = st.tabs(["Login", "Signup"])

    # ----- LOGIN -----
    with tab[0]:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            success, user_id, role = auth.login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.role = role
                rerun()
            else:
                st.error("Invalid credentials")

    # ----- SIGNUP -----
    with tab[1]:
        new_username = st.text_input("New Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Signup", key="signup_btn"):
            success, msg = auth.register(new_username, email, new_password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# ------------------------------
# Main App (after login)
# ------------------------------
else:
    st.sidebar.title("Navigation")
    menu = ["Home", "Generate QR", "History"]
    if st.session_state.role == "admin":
        menu.append("Manage Users")
    menu.append("Logout")
    choice = st.sidebar.selectbox("Menu", menu)

    # ----- HOME -----
    if choice == "Home":
        st.title("Welcome to QR Code Generator!")

    # ----- GENERATE QR -----
    elif choice == "Generate QR":
        st.title("Generate QR Code")
        qr_type = st.selectbox("QR Type", ["Text", "URL", "Email", "WiFi", "Contact"])
        content = st.text_area("Enter Content")
        color = st.color_picker("QR Color", "#000000")
        bgcolor = st.color_picker("Background Color", "#FFFFFF")
        logo = st.file_uploader("Upload Logo (optional)", type=["png", "jpg", "jpeg"])
        logo_path = None
        if logo:
            if not os.path.exists("assets/logos"):
                os.makedirs("assets/logos")
            logo_path = os.path.join("assets/logos", logo.name)
            with open(logo_path, "wb") as f:
                f.write(logo.getbuffer())

        if st.button("Generate QR"):
            file_path = qr_generator.generate_qr(
                st.session_state.user_id, content, qr_type, color, bgcolor, logo_path
            )
            st.success("QR Code generated!")
            st.image(file_path, width=250)
            st.download_button(
                "Download QR", file_path, file_name=os.path.basename(file_path)
            )

    # ----- HISTORY -----
    elif choice == "History":
        st.title("Your QR Codes")
        qrcodes = get_user_qrcodes(st.session_state.user_id)

        if qrcodes:
            for qr in qrcodes:
                # Skip QR codes without a valid file path
                if not qr.get("file_path") or not os.path.exists(qr["file_path"]):
                    continue

                st.image(qr["file_path"], width=150)
                st.write(f"Type: {qr['type']} | Created: {qr['created_at']}")
                st.download_button(
                    "Download",
                    qr["file_path"],
                    file_name=os.path.basename(qr["file_path"]),
                    key=f"download_{qr['id']}"
                )
        else:
            st.info("No QR codes found. Generate one!")

    # ----- ADMIN: MANAGE USERS -----
    elif choice == "Manage Users" and st.session_state.role == "admin":
        st.title("Manage Users")
        users = utils.get_all_users()
        for user in users:
            st.write(f"Username: {user['username']} | Email: {user['email']} | Role: {user['role']}")
            if st.button(f"Delete {user['username']}", key=f"del_{user['id']}"):
                users_collection.delete_one({"_id": utils.ObjectId(user["id"])})
                qrcodes_collection.delete_many({"user_id": utils.ObjectId(user["id"])})
                st.success(f"Deleted {user['username']}")
                rerun()

    # ----- LOGOUT -----
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.role = None
        rerun()
