import streamlit as st

def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "user" and password == "123":
            st.session_state["authenticated"] = True
            st.success("Login successful. Redirecting...")
            st.rerun()
        else:
            st.error("Invalid credentials.")
