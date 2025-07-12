from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.app.libraries.chroma_client import get_chroma_collection
from src.app.services.openai_services import qa_rag
from src.app.services.langchain_services import langchain_rag
from langchain_core.messages import HumanMessage
from src.app.libraries.redis_client import redis_client

router = APIRouter(
    prefix = "/document",
    tags = ["document"],
    responses = {404: {"description": "Not Found"}}\
)
class QueryRequest(BaseModel):
    user_id: str
    text: str
    top_k: int = 3

@router.get("/query")
async def get_document(request: QueryRequest):
    try:
        print('top results:::::', request.top_k)
        collection = get_chroma_collection()
        # results = collection.query(query_texts=[text], n_results = top_k)
        retrieved_docs = collection.query(query_texts=[request.text], n_results = request.top_k)
        context = "\n\n".join(retrieved_docs)
        # rag_response = await qa_rag(text, context)
        state = {"messages": [HumanMessage(content=request.text)]}
        result = langchain_rag(state, retrieved_docs)
        print('result fetched:::', result)
        return {
            "query": request.text,
            "answer": result,
            "source_docs": retrieved_docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))