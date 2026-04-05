from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from fastapi.params import Depends
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import JSONResponse
from uuid import uuid4
import base64
import hashlib

from src.mysoft_rag.services.chatbot.voice import VoiceService
from src.mysoft_rag.services.chatbot.vector_store_data import VectorStore
from src.mysoft_rag.services.chatbot.chat import InitChat
from src.mysoft_rag.schemas.schema import ChatRequest, HistoryModel
from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.services.chatbot.redis_client import set_cache, get_cache


router = APIRouter()


chat_instance = None
voice_instance = None


async def get_chat_instance():
    global chat_instance
    if chat_instance is None:
        chat_instance = InitChat()
        chat_instance.initialize_chat()
    return chat_instance


async def get_voice_instance():
    global voice_instance
    if voice_instance is None:
        voice_instance = VoiceService()
    return voice_instance


async def get_user_identifier(request: Request):
    return request.headers.get("X-User-ID") or request.client.host


@router.post("/chat")
async def chat(
    chat_req: ChatRequest,
    init_chat: InitChat = Depends(get_chat_instance),
    rate_limit: None = Depends(
        RateLimiter(times=5, seconds=60, identifier=get_user_identifier)
    ),
):
    try:
        logger.info(f"Received chat request: {chat_req}")
        session_id = chat_req.session_id or uuid4()
        user_id = chat_req.user_id
        full_id = f"{user_id}_{session_id}"

        # cache setup
        query_str = str(chat_req.messages)
        cache_key = f"chat:{full_id}:{hashlib.md5(query_str.encode()).hexdigest()}"

        # check cache
        cached_response = await get_cache(cache_key)
        if cached_response:
            print("### Using cached response...")
            return JSONResponse(status_code=200, content=cached_response)

        # llm response
        respond, confidence = init_chat.chat(chat_req.messages, full_id)

        respond_data = {
            "messages": respond,
            "confidence_score": confidence,
            "session_id": session_id,
        }

        # set cache
        await set_cache(
            key=cache_key, value=respond_data, expire=1800
        )  # cache for 30 mins

        return JSONResponse(
            status_code=200,
            content=respond_data,
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice_chat")
async def voice_chat(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
    user_id: str = Form(...),
    voice_service: VoiceService = Depends(get_voice_instance),
    init_chat: InitChat = Depends(get_chat_instance),
):
    try:
        logger.info(f"Received voice chat request: {audio.filename}")
        session_id = session_id or uuid4()
        user_id = user_id
        full_id = f"{user_id}_{session_id}"

        audio_bytes = await audio.read()
        transcript = await voice_service.transcribe_audio(audio_bytes)  # STT
        respond, confidence = init_chat.chat(transcript, full_id)  # get text response

        generated_audio_bytes = await voice_service.text_to_speech(respond)
        audio_base64 = (
            base64.b64encode(generated_audio_bytes).decode("utf-8")
            if generated_audio_bytes
            else None
        )

        return JSONResponse(
            status_code=200,
            content={
                "transcript": transcript,
                "messages": respond,
                "confidence_score": confidence,
                "session_id": session_id,
                "audio_base64": audio_base64,
            },
        )

    except Exception as e:
        logger.error(f"Error in voice chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat_history")
async def chat_history(
    request: HistoryModel, init_chat: InitChat = Depends(get_chat_instance)
):
    try:
        logger.info(f"Received chat history request: {request}")
        full_id = f"{request.user_id}_{request.session_id}"

        respond = await init_chat.get_chat_history(full_id)

        return JSONResponse(status_code=200, content=respond)
    except Exception as e:
        logger.error(f"Error in chat history endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/init_vector")
async def vector():
    try:
        VectorStore().vectorize_data_and_save()
        return JSONResponse(
            status_code=200, content={"Response": "Data Vectorize Successful"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
