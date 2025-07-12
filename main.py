import uuid
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from src.app.libraries.chroma_client import get_chroma_collection
from routes import router as app_router

unique_id = str(uuid.uuid4())
print(unique_id)
def generate_uuid():
    unique_id = str(uuid.uuid4())
    return unique_id

class user_access(BaseModel):
    user_id: str

app = FastAPI()
app.include_router(app_router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!!"}

handler = Mangum(app)