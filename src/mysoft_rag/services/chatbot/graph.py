from langgraph.graph import StateGraph, START, END


from src.mysoft_rag.services.chatbot.state import State
from src.mysoft_rag.services.chatbot.node import ChatBotNode
from src.mysoft_rag.utils.logger import logger


class GraphBuilder:
    def __init__(self, model, checkpointer):
        self.llm = model
        self.checkpointer = checkpointer

    def chatbot_graph(self):

        try:
            logger.info("Building ChatBot Graph")

            chatbot_nodes = ChatBotNode(self.llm)

            builder = StateGraph(State)

            # add node
            builder.add_node("chatbot", chatbot_nodes.rag_llm)

            # add edges
            builder.add_edge(START, "chatbot")
            builder.add_edge("chatbot", END)

            logger.info("Graph Built Successfully")

            return builder.compile(checkpointer=self.checkpointer)
        except Exception as e:
            logger.error(f"Failed To Build Graph: {e}")
            return None
