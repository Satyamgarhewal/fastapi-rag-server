from src.app.libraries.redis_client import redis_client
import json

def save_chat_history(user_id, messages):
    redis_client.set(f"chat_history:{user_id}", json.dumps(messages))

def load_chat_history(user_id):
    data = redis_client.get(f"chat_history:{user_id}")
    if data:
        return json.loads(data)
    return []