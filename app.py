import streamlit as st

st.title("🧪 Step-by-step import test")

try:
    from auth.login import login_page
    st.success("auth.login imported successfully")
except Exception as e:
    st.error(f"auth.login import failed: {e}")

try:
    from agents.agent_db import handle_db_query
    st.success("agent_db imported successfully")
except Exception as e:
    st.error(f"agent_db import failed: {e}")

try:
    st.switch_page("pages/1_Chat_Interface.py")
except Exception as e:
    st.error(f"Page switch failed: {e}")
