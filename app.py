import streamlit as st
from auth.login import login_page

def main():
    st.set_page_config(page_title="Multiagent Support System", layout="wide")
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
    else:
        st.switch_page("pages/1_Chat_Interface.py")

if _name_ == "_main_":
    main()
