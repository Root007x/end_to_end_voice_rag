from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.mysoft_rag.api.endpoints import chat_endpoints

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_endpoints.router)


@app.get("/")
async def read_root():
    return {"message": "Voice Chatbot API"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
