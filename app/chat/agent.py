from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import PromptTemplate
import asyncio

from ..database.vector_store import VectorStore
from config import settings
from llm.ollama_llm import OllamaLLM


class RAGAgent:
    def __init__(self, chat_id: str, asset_id: str):
        self.chat_id = chat_id
        self.asset_id = asset_id
        self.vector_store = VectorStore(settings.VECTOR_DB_PATH)


        self.llm = OllamaLLM(settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL)

        self.tools = [
            Tool(
                name="Vector Store",
                func=self.vector_store.query,
                description="Useful for querying information from the document"
            )
        ]

        self.prompt = PromptTemplate(
            template=(
                "You are a helpful AI assistant. Use the following context to answer the human question.\n\n"
                "Context:\n{context}\n\n"
                "Human question: {question}\n\n"
                "Answer:"
            ),
            input_variables=["context", "question"]
        )

    async def generate_response(self, message: str):
        context = await self.vector_store.query(self.asset_id, message, n_results=3)
        # Check if we have any documents
        if not context['documents'][0]:
            yield f"No relevant documents found for asset_id: {self.asset_id}. Please check if the document was properly processed and stored."
            return

        # Prepare the context string
        context_str = "\n".join([f"Document {i + 1}: {doc}" for i, doc in enumerate(context['documents'][0])])
        # Generate the response
        if isinstance(self.llm, OllamaLLM):
            print("Using OllamaLLM or LocalLLM")
            prompt_text = self.prompt.format(question=message, context=context_str)
            async for token in self.llm.generate_stream(prompt_text):
                yield token
                await asyncio.sleep(0)  # Allow other tasks to run
