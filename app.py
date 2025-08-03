import streamlit as st
from auth.login import login_page
from streamlit_extras.switch_page_button import switch_page

def main():
    st.set_page_config(page_title="Multiagent Support System", layout="wide")

    # Safely initialize session variable
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
    else:
        switch_page("Chat_Interface")

if __name__ == "__main__":
    main()
