from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Stores conversation history or messages passed between nodes
    messages: Annotated[List, add_messages]
    originalQuery: str
    transformedQuery: List[str]
    retrievedDocs: List[dict]
    decision:str
    loop:int
    finalOutput: str