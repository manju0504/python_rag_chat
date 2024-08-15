import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting the server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)