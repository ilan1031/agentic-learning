import uuid

def get_session_token():
    return str(uuid.uuid4())[:8]
