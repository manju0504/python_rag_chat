import asyncio

from sentence_transformers import SentenceTransformer

from config import settings

model = SentenceTransformer(settings.EMBEDDING_MODEL)

async def create_embedding(text: str, filename: str):
    embedding = await asyncio.to_thread(model.encode, text)
    return {"embedding": embedding.tolist(), "metadata": {"filename": filename}}