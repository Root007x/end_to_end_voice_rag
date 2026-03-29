from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.services.chatbot.retriever import Retriever
from src.mysoft_rag.services.chatbot.state import State
from src.mysoft_rag.utils.prompt import SYSTEM_PROMPT


class ChatBotNode:
    def __init__(self, model):
        self.llm = model
        self.retriever = Retriever().get_retriever()
        self.load_vectore_store = Retriever().get_vectore_store()

    def rag_llm(self, state: State):
        """
        Invoke the LLM with the current chat state.

        Args:
            state: ChatState containing messages and context

        Returns:
            dict: Updated state with LLM response

        Raises:
            Exception: Re-raises LLM errors after logging
        """
        try:
            if not state or "messages" not in state:
                raise ValueError("Invalid state")

            prompt = ChatPromptTemplate(
                [
                    ("system", SYSTEM_PROMPT),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{input}"),
                ]
            )

            query = state["messages"]
            chat_history = query[:-1]
            last_message = query[-1]

            current_input = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

            qa_chain = create_stuff_documents_chain(llm=self.llm, prompt=prompt)
            rag_chain = create_retrieval_chain(self.retriever, qa_chain)

            # docs_and_scores = self.load_vectore_store.similarity_search_with_score(
            #     current_input
            # )
            # _, top_score = docs_and_scores[0]
            # print(top_score)

            # CONF_THRESHOLD = 1.0  # similarity threshold

            # if CONF_THRESHOLD < top_score:
            #     return {
            #         "messages": [
            #             {
            #                 "role": "assistant",
            #                 "content": "I’m not confident about that. Could you clarify or ask another question?",
            #             }
            #         ]
            #     }

            response = rag_chain.invoke(
                {"chat_history": chat_history, "input": current_input}
            )

            return {"messages": [response["answer"]]}

        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise e
