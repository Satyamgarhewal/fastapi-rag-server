from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from src.functions.users import routes as user_routes
from src.app.libraries.chroma_client import get_chroma_collection

app = FastAPI()

app.include_router(user_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!!"}


class Document(BaseModel):
    id: str
    text: str


@app.post("/add_document")
async def add_document(doc: Document):
    try:
        collection = get_chroma_collection()
        collection.add(documents=doc.text, ids=doc.id)
        return {"message": "Document added successfully"}
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    
@app.get("/query")
def query_document(text: str):
    try:
        collection = get_chroma_collection()
        print('collection fetched =====>', collection)
        results = collection.query(query_texts=[text], n_results=3)
        print("results fetched::::::",results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q:str = None):
#     return {"item_id": item_id, "q": q}

handler = Mangum(app)