# Python RAG Project with Local Ollama

This project demonstrates how to use Ollama locally with a Python application.

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed locally

## Setup

1. Clone this repository:
git clone https://github.com/manju0504/python_rag_chat.git


2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required packages using the requirements.txt file:
```
pip install -r requirements.txt
```

5. Ensure Ollama is running locally:
ollama run llama3.1

## Usage

Start the server by running the below command:
```
python run.py
```

Submit your custom document to the server by running the below command:
```
curl --location 'http://localhost:8000/api/documents/process' \
--form 'file=@"custom_doc.docx"'
```

Use the assetId that you got from previous step to create a chat_id.

```
curl --location --request POST 'localhost:8000/api/chat/start?asset_id=ASSET_ID' 
```

Use the chat_id that you got from previous step in the chat_client.py file to chat with the RAG model.

For chatting with the RAG model, open a new terminal and run the below command:
This chat client uses websockets to receive streaming data from the server. It will prompt you to enter a message, and then display the live streaming response from the LLM model.
```
python chat_client.py
```

## Configuration

Modify `config.py` to adjust settings such as the Ollama model or API endpoint.

## Troubleshooting

If you encounter issues, check that:
- Ollama is installed and running
- Your firewall isn't blocking the connection
- The Ollama API endpoint in `config.py` matches your local setup
- All required libraries are installed correctly (check the output of `pip list`)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
