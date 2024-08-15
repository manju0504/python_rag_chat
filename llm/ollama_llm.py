import aiohttp
from typing import AsyncGenerator


class OllamaLLM:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model


    async def generate(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt}
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ollama API error: {response.status}")
                data = await response.json()
                return data['response']

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": True},
                headers={"Accept": "application/x-ndjson"}
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ollama API error: {response.status}")
                async for line in response.content:
                    data = line.decode('utf-8').strip()
                    if data:
                        yield data