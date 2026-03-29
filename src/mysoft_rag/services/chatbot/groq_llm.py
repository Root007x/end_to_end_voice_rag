from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.config import setting, config


class GroqLLM:
    def __init__(self):
        self.groq_api_key = setting.GROQ_API_KEY
        self.model_name = config.groqai.model
        self.embedding_model = config.groqai.embedding_model

    def get_llm(self):
        try:
            logger.info("Initializing Groq LLM....")

            llm = ChatGroq(api_key=self.groq_api_key, model=self.model_name)

            return llm
        except Exception as e:
            logger.error(f"Error Initializing Groq LLM: {e}")
            return None

    def get_embedding(self):
        try:
            logger.info("Initializing Huggingface Embedding....")

            embed = HuggingFaceEmbeddings(model=self.embedding_model)
            return embed

        except Exception as e:
            logger.error(f"Error initializing Huggingface Embeddings: {e}")
            return None
