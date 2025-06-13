import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

chroma_client = None
collection = None

def get_chroma_collection():
    global chroma_client, collection

    if collection:
        print("collection::::::::::", collection)
        return collection
    
    MODE = os.getenv("CHROMA_MODE", "local")
    print("MODE::::::::::", MODE)

    if MODE == "hosted":
        print("Inside if clause:::::::::::::;", MODE)
        chroma_client = chromadb.HttpClient(
            ssl=True,
            host=os.getenv("CHROMA_HOST"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE"),
            headers={'x-chroma-token': os.getenv("CHROMA_API_KEY")}
        )
    else:
        print("Inside else clause:::::::::::::;", MODE)
        chroma_client = chromadb.PersistentClient(path="/tmp/chroma_data")

    collection = chroma_client.get_or_create_collection(name="my_collection")
    return collection