import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
async def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

async def chunk_text(text, chunk_size = 500, overlap = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

async def upload_pdf_to_chroma(file_path, collection):
    print(f"Reading PDF: {file_path}")
    text = await extract_text_from_pdf(file_path)
    if not text.strip():
        print("❌ No text found in PDF.")
        return
    
    print("📚 Splitting into chunks...")
    chunks = await chunk_text(text)

    print("🧠 Generating embeddings...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(chunks).tolist()

    ids = [f"{os.path.basename (file_path)}_chunk_{i}" for i in range(len(chunks))]
    
    print(f"📦 Uploading {len(chunks)} chunks to ChromaDB...")

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": os.path.basename(file_path)}] * len(chunks)
    )

    print("✅ Upload complete.")