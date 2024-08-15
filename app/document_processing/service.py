import os

import docx
import fitz
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from config import settings
from .embedding import create_embedding
from ..database.vector_store import VectorStore

router = APIRouter()
vector_store = VectorStore(settings.VECTOR_DB_PATH)


def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif ext == '.pdf':
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif ext == '.docx':
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")

@router.post("/api/documents/process")
async def process_document(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Read the file content
        text = read_file(temp_file_path)

        # Create embeddings
        embedding = await create_embedding(text, file.filename)

        # Store embeddings in ChromaDB
        metadata = {"file_path": temp_file_path}
        asset_id = await vector_store.store(embedding, metadata, text)

        print(asset_id)
        # Clean up the temporary file
        os.remove(temp_file_path)

        return JSONResponse(content={"asset_id": asset_id}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
