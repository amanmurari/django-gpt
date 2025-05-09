
from langgraph.graph import StateGraph,START,END
from models import State
from langgraph.checkpoint.memory import InMemorySaver
from graph import retrieve, search, generate, filter_answer
import uuid

class MultiAgentSystem:
    def __init__(self):
        




# Compile application and test
        graph_builder = StateGraph(State)
        graph_builder.add_node("retrieve", retrieve)
        graph_builder.add_node("search", search)
        graph_builder.add_node("generate", generate)
        graph_builder.add_edge(START,"retrieve")
        graph_builder.add_edge("retrieve", "generate")
        graph_builder.add_edge("search", "generate")
        graph_builder.add_conditional_edges("generate", filter_answer,{"search": "search",END: END})
        graph_builder.add_edge("generate", END)
        memory= InMemorySaver()
        self.graph = graph_builder.compile(checkpointer=memory)


      

    def route_query(self, query,ids):
        config = {"configurable": {"thread_id": ids}}
        events = self.graph.stream(
            {"question": query},
            config,
            stream_mode="values",
        )
        out=""
        for event in events:
            if "answer" in event:
                out=event['answer']
        
        return out
    




