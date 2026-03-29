from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.utils.helper import delete_file_from_folder
from src.mysoft_rag.config import config
from src.mysoft_rag.services.chatbot.groq_llm import GroqLLM
from src.mysoft_rag.services.chatbot.preprocess_data import PreprocessData


class VectorStore:
    def __init__(self):
        self.vector_database_loc = config.vector_database.loc
        self.embed = GroqLLM().get_embedding()
        self.pdf_doc = PreprocessData().load_and_clean_pdf_data()
        self.web_doc = PreprocessData().load_and_clean_web_data()

    def vectorize_data_and_save(self):

        try:
            logger.info("Vectorize Data")
            combine_docs = self.pdf_doc + self.web_doc

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=150
            )

            docs_splits = text_splitter.split_documents(combine_docs)

            ## Vector
            vector_store = FAISS.from_documents(
                documents=docs_splits, embedding=self.embed
            )

            # Save vector store
            delete_file_from_folder(self.vector_database_loc)
            vector_store.save_local(self.vector_database_loc)

            logger.info("Vectorize Data Saved Successfully")
            return None

        except Exception as e:
            logger.error(f"Failed To Vectorize Data: {e}")
            return None
