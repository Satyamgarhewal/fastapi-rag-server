import tempfile
from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from src.app.libraries.chroma_client import get_chroma_collection
from src.functions.documents.service import upload_pdf_to_chroma


router = APIRouter(
    prefix = "/document",
    tags=["document"],
    responses={404: {"description": "Not Found"}}
)


class Document(BaseModel):
    id: str
    text: str
    

@router.post("/add_document")
async def add_document(doc: Document):
    try:
        collection = get_chroma_collection()
        collection.add(documents = doc.text, ids = doc.id)
        return {"message": "Document added successfully"}
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        collection = get_chroma_collection()
        print(f"collection fetched {collection}")
        # Read file contents
        contents = await file.read()
        # Pass the file contents and filename to your service
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        await upload_pdf_to_chroma(tmp_path, collection)  # Pass the collection object, not collection.name
        return {"message": "PDF uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

