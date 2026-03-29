from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage


from src.mysoft_rag.utils.logger import logger
from src.mysoft_rag.services.chatbot.groq_llm import GroqLLM
from src.mysoft_rag.services.chatbot.graph import GraphBuilder


class InitChat:
    def __init__(self):
        self.checkpointer = None
        self.llm = None
        self.graph = None

    def initialize_chat(self):
        try:
            logger.info("Initializing Chat")
            self.checkpointer = MemorySaver()
            self.llm = GroqLLM().get_llm()
            self.graph = GraphBuilder(
                model=self.llm, checkpointer=self.checkpointer
            ).chatbot_graph()
            logger.info("Chat Initialized Successfully")
        except Exception as e:
            logger.error(f"Error init Chat: {e}")
            return None

    def chat(self, prompt: str, thread_id: str):
        try:
            logger.info("Start Chat")
            config = {"configurable": {"thread_id": thread_id}}
            input_data = {"messages": [HumanMessage(content=prompt)]}

            result = self.graph.invoke(input_data, config)
            final_result = result["messages"][-1].content

            return final_result
        except Exception as e:
            logger.error(f"Chat functionality not working: {e}")
            return None
