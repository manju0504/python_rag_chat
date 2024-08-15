import uuid
import chromadb


class VectorStore:
    def __init__(self, path: str):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("documents")

    async def store(self, embedding: dict, metadata: dict, content: str):
        id = str(uuid.uuid4())  # Generate a unique ID
        self.collection.add(
            embeddings=[embedding["embedding"]],
            metadatas=[{**metadata, "asset_id": id}],
            ids=[id],
            documents=[content]
        )
        print(f"Stored document with asset_id: {id}")  # Debug print
        return id

    async def query(self, asset_id: str, query: str, n_results: int = 5):
        print(f"Querying for asset_id: {asset_id}")  # Debug print
        results = self.collection.query(
            query_texts=[query],
            where={"asset_id": asset_id},
            n_results=n_results
        )
        print(f"Query results: {results}")  # Debug print
        return results