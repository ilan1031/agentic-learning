import json
import os

SESSION_DIR = "sessions"

os.makedirs(SESSION_DIR, exist_ok=True)

def save_session(name, history):
    path = os.path.join(SESSION_DIR, f"{name}.json")
    with open(path, 'w') as f:
        json.dump(history, f)

def load_sessions():
    return [f for f in os.listdir(SESSION_DIR) if f.endswith('.json')]

def load_session(name):
    path = os.path.join(SESSION_DIR, f"{name}.json")
    with open(path, 'r') as f:
        return json.load(f)
