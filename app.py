from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import uvicorn

from src.mysoft_rag.api.endpoints import chat_endpoints
from src.mysoft_rag.services.chatbot.redis_client import init_redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    app.state.redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
    )
    await init_redis(app)


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis_client.close()


app.include_router(chat_endpoints.router)


@app.get("/")
async def read_root():
    return {"message": "Voice Chatbot API"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
