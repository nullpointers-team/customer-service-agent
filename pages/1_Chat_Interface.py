import streamlit as st
from router.classifier import classify_query
from agents.agent_db import handle_db_query
from agents.agent_misc import handle_misc_query
from agents.agent_contact import send_support_email

# Page setup
st.set_page_config(page_title="Customer Support Chat", layout="centered")
st.title("🧠 Multi-Agent Customer Service Chat")

# Sidebar: Chat History
with st.sidebar:
    st.header("🕘 Chat History")
    if "chat_history" in st.session_state and st.session_state.chat_history:
        for idx, msg in enumerate(reversed(st.session_state.chat_history)):
            st.markdown(f"**You:** {msg['user']}")
            st.markdown(f"**Agent ({msg['agent_type']}):** {msg['agent']}")
            if idx < len(st.session_state.chat_history) - 1:
                st.markdown("---")
    else:
        st.info("No previous conversations yet.")

# Session state to store conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("Ask something...")

if user_input:
    # Display user message in chat area
    st.chat_message("user").write(user_input)

    # Run classifier
    label = classify_query(user_input)

    # Route to appropriate agent
    if label == "database_search":
        st.info("🗂️ Delegated to Database Agent.")
        with st.spinner("Searching the database..."):
            response = handle_db_query(user_input)
    elif label == "contact_request":
        st.info("📧 Delegated to Contact Agent.")
        with st.spinner("Sending support request..."):
            response = send_support_email(user_input)
    else:
        st.info("🤖 Delegated to Miscellaneous Agent.")
        with st.spinner("Processing your question..."):
            response = handle_misc_query(user_input)

    # Display assistant response
    st.chat_message("assistant").write(response)

    # Store interaction in session
    st.session_state.chat_history.append({
        "user": user_input,
        "agent": response,
        "agent_type": label
    })
