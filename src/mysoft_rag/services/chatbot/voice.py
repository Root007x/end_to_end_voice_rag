from faster_whisper import WhisperModel
import tempfile, os
import edge_tts

from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.config import config


class VoiceService:
    def __init__(self):
        self.whisper_model_name = config.whisper_model.name
        self.whisper_device = config.whisper_model.device

    def init_whisper_model(self):
        try:
            logger.info("Initializing Whisper Model....")
            model = WhisperModel(
                self.whisper_model_name, device=self.whisper_device, compute_type="int8"
            )
            return model
        except Exception as e:
            logger.error(f"Error Initializing Whisper Model: {e}")
            return None

    async def transcribe_audio(self, audio_bytes: bytes) -> str:
        try:
            model = self.init_whisper_model()

            if model is None:
                raise Exception("Whisper model initialization failed")

            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as file:
                file.write(audio_bytes)
                temp_path = file.name

            try:
                segments, info = model.transcribe(temp_path, beam_size=5)
                text = " ".join([seg.text for seg in segments])
                return text.strip()
            finally:
                os.unlink(temp_path)
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None

    async def text_to_speech(self, text: str) -> bytes:
        try:
            logger.info("Converting text to speech...")
            tts = edge_tts.Communicate(text, "en-US-JennyNeural")
            audio_chunks = []
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
            return b"".join(audio_chunks)
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return None
