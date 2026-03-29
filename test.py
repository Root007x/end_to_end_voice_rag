from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
import base64
import uvicorn
from src.mysoft_rag.services.chatbot.voice import VoiceService


app = FastAPI()


@app.post("/voice-query")
async def voice_query(audio: UploadFile = File(...), return_audio: bool = False):
    audio_bytes = await audio.read()
    voice_service = VoiceService()
    transcript = await voice_service.transcribe_audio(audio_bytes)  # STT
    # result = await run_rag(transcript)  # RAG

    # if return_audio:
    #     audio_response = await text_to_speech(result["answer"])
    #     return StreamingResponse(audio_response, media_type="audio/mpeg")
    text_to_audio = await voice_service.text_to_speech(transcript)  # TTS
    audio_base64 = base64.b64encode(text_to_audio).decode("utf-8")
    return {
        "transcript": transcript,
        "audio_base64": audio_base64,  # client can decode and play
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
