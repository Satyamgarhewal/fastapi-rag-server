from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def qa_rag(query:str, db_result: str):
    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are an assistant answering based on retrieved documents."},
            {"role": "user", "content": f"Context:\n{db_result}\n\nQuestion: {query}"}
            ],
            temperature=0.3
        )
        # print(response)
        return response
    except Exception as e:
        raise HTTPException(status_code= 400,detail= str(e))