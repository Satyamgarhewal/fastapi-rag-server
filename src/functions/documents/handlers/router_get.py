from fastapi import APIRouter, HTTPException
from src.app.libraries.chroma_client import get_chroma_collection


router = APIRouter(
    prefix = "/document",
    tags = ["document"],
    responses = {404: {"description": "Not Found"}}\
)

@router.get("/query")
async def get_document(text:str):
    try:
        collection = get_chroma_collection()
        results = collection.query(query_texts=[text], n_results = 3)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    