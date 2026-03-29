from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from uuid import uuid4

from src.mysoft_rag.services.chatbot.voice import VoiceService
from src.mysoft_rag.services.chatbot.vector_store_data import VectorStore
from src.mysoft_rag.services.chatbot.chat import InitChat
from src.mysoft_rag.schemas.schema import ChatRequest
from src.mysoft_rag.utils.logger import logger


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


@router.post("/chat")
async def chat(request: ChatRequest, init_chat: InitChat = Depends(get_chat_instance)):
    try:
        logger.info(f"Received chat request: {request}")
        session_id = request.session_id or uuid4()
        user_id = request.user_id
        full_id = f"{user_id}_{session_id}"

        respond, confidence = init_chat.chat(request.messages, full_id)

        return JSONResponse(
            status_code=200,
            content={
                "messages": respond,
                "confidence_score": confidence,
                "session_id": session_id,
            },
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
        print(f"Transcribed text: {transcript}")
        respond, confidence = init_chat.chat(transcript, full_id)

        return JSONResponse(
            status_code=200,
            content={
                "messages": respond,
                "confidence_score": confidence,
                "session_id": session_id,
            },
        )

    except Exception as e:
        logger.error(f"Error in voice chat endpoint: {e}")
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
