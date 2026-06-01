import streamlit as st

# fetches the username and password from secrets.toml
# users become {'admin': {'password': "password", 'role': "admin"}}
USERS = {
    st.secrets["users"]["admin_username"]: {"password": st.secrets["users"]["admin_password"], "role": "admin"},
    st.secrets["users"]["staff_username"]: {"password": st.secrets["users"]["staff_password"], "role": "staff"},
}


def login():
    """
    if the user is already logged in, it returns True, else False
    if not, then it shows a log in form 
    if the user entered password and the password in secrets matches, 
    then it log in and save it to session state
    """
    if "role" in st.session_state:
        return True
    st.title("🔧 MotoParts Manager")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            user = USERS.get(username)
            if user and user["password"] == password:
                st.session_state["role"] = user["role"]
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid credentials")
    return False

def is_admin():
    """checks if the user is an admin """
    return st.session_state.get("role") == "admin"

def logout():
    """shows a log out button and clears the data when clicked"""
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
