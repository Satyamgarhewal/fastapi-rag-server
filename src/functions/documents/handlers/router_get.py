from fastapi import APIRouter, HTTPException
from src.app.libraries.chroma_client import get_chroma_collection
from src.app.services.openai_services import qa_rag

router = APIRouter(
    prefix = "/document",
    tags = ["document"],
    responses = {404: {"description": "Not Found"}}\
)

@router.get("/query")
async def get_document(text:str, top_k:int = 3):
    try:
        print('top results:::::', top_k)
        collection = get_chroma_collection()
        # results = collection.query(query_texts=[text], n_results = top_k)
        retrieved_docs = collection.query(query_texts=[text], n_results = top_k)
        context = "\n\n".join(retrieved_docs)
        rag_response = await qa_rag(text, context)
        print(rag_response.choices[0].message.content)
        return {
            "query": text,
            "answer": rag_response.choices[0].message.content,
            "source_docs": retrieved_docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))