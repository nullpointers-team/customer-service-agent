from agents.agent_db import handle_db_query
from agents.agent_contact import handle_contact_request
from agents.agent_misc import handle_misc

def delegate_task(label: str, query: str) -> str:
    if label == "database_search":
        return handle_db_query(query)
    elif label == "contact_request":
        return handle_contact_request(query)
    else:
        return handle_misc(query)
