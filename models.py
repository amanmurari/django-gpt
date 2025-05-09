from typing_extensions import TypedDict
from typing import List
from langchain.schema import Document
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
