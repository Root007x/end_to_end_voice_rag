from docling.document_converter import DocumentConverter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

from src.mysoft_rag.utils.helper import clean_company_profile_markdown, clean_web_text
from src.mysoft_rag.config import config
from src.mysoft_rag.utils.logger import logger


class PreprocessData:
    def __init__(self):
        self.pdf_file_path = config.pdf_file.loc
        self.web_urls = config.web_data.urls

    def load_and_clean_pdf_data(self):

        company_documents = []

        try:
            logger.info("PDF Data Loading and Cleaning")
            converter = DocumentConverter()
            result = converter.convert(self.pdf_file_path)
            markdown_text = result.document.export_to_markdown()

            cleaned_data = clean_company_profile_markdown(markdown_text)
            sections = cleaned_data["sections"]

            for section in sections:
                company_documents.append(
                    Document(
                        page_content=section,
                        metadata={
                            "Topic": "Machine Learning (ML)",
                            "source": "PDF Document",
                            "type": "pdf_section",
                        },
                    )
                )
            logger.info("PDF Documents Created Successfully")
            return company_documents
        except Exception as e:
            logger.error(f"Failed To Load PDF Data: {e}")
            return None

    def load_and_clean_web_data(self):

        web_documents = []

        try:
            logger.info("Web Data loading and Cleaning")
            docs = [WebBaseLoader(url).load() for url in self.web_urls]
            docs_list = [item for sublist in docs for item in sublist]

            for doc in docs_list:
                cleaned_web_text = clean_web_text(doc.page_content)

                web_documents.append(
                    Document(
                        page_content=cleaned_web_text,
                        metadata={
                            "topic": "Machine Learning (ML)",
                            "source": doc.metadata.get("source", "website"),
                            "type": "web_page",
                        },
                    )
                )
            logger.info("Web Documents Created Successfully")
            return web_documents
        except Exception as e:
            logger.error(f"Failed To Load Web Data: {e}")
            return None
