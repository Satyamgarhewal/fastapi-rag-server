from fastapi import APIRouter
from src.functions.users import routes as user_routes
from src.functions.documents.routes import routers as document_routes

router = APIRouter()
router.include_router(user_routes.router)
for r in document_routes:
    router.include_router(r)