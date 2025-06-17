from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from src.app.libraries.chroma_client import get_chroma_collection
from src.functions.users import routes as user_routes
from src.functions.documents.routes import routers as document_routes

app = FastAPI()

app.include_router(user_routes.router)
for router in document_routes:
    print('router in document_routes', router)
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!!"}

handler = Mangum(app)