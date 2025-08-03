import streamlit as st

st.title("🔍 App Startup Trace")

try:
    st.info("Importing login module...")
    from auth.login import login_page
    st.success("✅ login_page loaded")
except Exception as e:
    st.error(f"Login import failed: {e}")

try:
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    st.success("✅ Session state ready")
except Exception as e:
    st.error(f"Session setup failed: {e}")

try:
    if not st.session_state["authenticated"]:
        st.info("Rendering login...")
        login_page()
    else:
        st.info("Switching to Chat Interface...")
        st.switch_page("pages/1_Chat_Interface.py")
except Exception as e:
    st.error(f"Main control flow failed: {e}")
