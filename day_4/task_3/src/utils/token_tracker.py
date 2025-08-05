import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
coll = db[os.getenv("MONGO_COLLECTION")]

def log_token_count(session_id, token_count):
    coll.insert_one({"session": session_id, "tokens": token_count})
