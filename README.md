# 🤖 Customer Service Agent (Multi-Agent System)

A modular **multi-agent customer support system** that classifies incoming user queries and routes them to the most relevant agent, with an **LLM-based fallback dispatcher** for handling ambiguous or unseen requests.

##  System Overview
The system follows a **router → agent → response** pipeline:
1. User submits a query
2. A classifier/router identifies the intent
3. The query is forwarded to a specialized agent
4. If no clear intent is found, an LLM fallback handles the request

This design allows scalable, maintainable, and intelligent customer support automation.

##  Agent Architecture
Each agent is responsible for a specific category of queries:

###  `agent_contact.py`
- Handles contact-related queries  
- Examples: support email, phone number, office hours  

###  `agent_db.py`
- Handles database or data-backed queries  
- Fetches customer-related information from stored data  

###  `agent_misc.py`
- Handles uncategorized or general queries  
- Acts as a soft fallback before LLM escalation  

Agents are **loosely coupled**, making it easy to add or replace functionality.

## 🔀 Router & Dispatcher
- Classifies user intent based on keywords / logic  
- Routes queries to the appropriate agent  
- Uses **LLM fallback** when intent confidence is low  

## 🛠 Tech Stack
- Python  
- Multi-Agent Architecture  
- LLM (fallback reasoning)  
- Streamlit (UI)  

## How to Run It?
```bash
pip install -r requirements.txt
python app.py
