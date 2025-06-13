from fastapi import APIRouter, HTTPException, status
from typing import List, Dict

fake_users_db = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob", "email": "bob@example.com"}
}

router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    responses = {404: {"description": "Not found"}}
)

@router.get("/")
async def get_all_users():
    return list(fake_users_db.values())

@router.get("/{user_id}")
async def get_user(user_id: int):
    print(user_id)
    user = fake_users_db.get(str(user_id))
    print('user', user)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user
