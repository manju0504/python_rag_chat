from fastapi import FastAPI
from app.document_processing.service import router as document_router
from app.chat.service import router as chat_router

app = FastAPI(title="RAG Chatbot System")

app.include_router(document_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot System"}

print("FastAPI app initialized")