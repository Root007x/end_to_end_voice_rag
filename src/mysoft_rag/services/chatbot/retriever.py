from langchain_community.vectorstores import FAISS

from src.mysoft_rag.services.chatbot.groq_llm import GroqLLM
from src.mysoft_rag.config import config
from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.utils.helper import check_data_exist


class Retriever:
    def __init__(self):
        self.embed = GroqLLM().get_embedding()
        self.vector_database_loc = config.vector_database.loc

    def get_retriever(self):

        try:
            if check_data_exist(self.vector_database_loc):
                logger.info("Loading Vector Database")

                load_vector_store = FAISS.load_local(
                    folder_path=self.vector_database_loc,
                    embeddings=self.embed,
                    allow_dangerous_deserialization=True,
                )

                retriever = load_vector_store.as_retriever(
                    search_type="similarity", search_kwargs={"k": 5}
                )
                # retriever = load_vector_store.as_retriever(
                #     search_type="mmr",
                #     search_kwargs={
                #         "k": 4,  # final docs returned
                #         "fetch_k": 20,  # initial candidates to consider
                #         "lambda_mult": 0.5,  # diversity factor
                #     },
                # )
                logger.info("Retriever Created Successfully")

                return retriever
            else:
                logger.warning("Vector Database Does't Exist")
                return None

        except Exception as e:
            logger.error(f"Failed To Create Retriever: {e}")
            return None

    def get_vectore_store(self):
        try:
            if check_data_exist(self.vector_database_loc):
                logger.info("Loading Vector Database")

                load_vector_store = FAISS.load_local(
                    folder_path=self.vector_database_loc,
                    embeddings=self.embed,
                    allow_dangerous_deserialization=True,
                )

                return load_vector_store
            else:
                return None

        except Exception as e:
            raise e
