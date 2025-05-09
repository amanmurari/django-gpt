from typing import Literal
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from pydantic import Field, BaseModel
from langgraph.graph import StateGraph,START,END
from langchain.schema import Document
from models import State
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain import hub
from retriver import VectorRetriever
load_dotenv()
vector_store= VectorRetriever()


os.environ["GROQ_API_KEY"]=os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
prompt=hub.pull("rlm/rag-prompt")

tool=DuckDuckGoSearchRun()


class Revert(BaseModel):
    where: Literal["vector","search"]
llmtool= llm.bind_tools([Revert])

class Check(BaseModel):
    ch: bool
llmbool= llm.with_structured_output(Check)

class Seperate(BaseModel):
    importing: str= Field("You are a Python code analyzer. Your work is to extract  the import statements from Python code.")
    func: str= Field("You are a Python code analyzer. Your work is to remove all import statements and extract the logical code part from the given Python script.")
seprt= llm.with_structured_output(Seperate)

def retrieve(state: State):
    retrieved_docs = vector_store.retrieve(state["question"])
    return {"context": retrieved_docs,"question":state["question"]}

def filter_context(state: State):
    result=llmtool.invoke(state["question"])

    return str(result.tool_calls[0]["args"]["where"])

def search(state: State):
    return {"context":[Document(page_content=tool.invoke(state["question"]))]}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content,"context":state["context"],"question":state["question"]}

def filter_answer(state: State):
    template= PromptTemplate.from_template("""you are a Django expert. Your task is to verify whether the given answer is correct for the corresponding question. Respond with 'True' if the answer is correct and 'False' if it is incorrect. Here is the answer: '{answer}' for the question: '{q}'.""")
    result=llmbool.invoke(template.format(answer=state["answer"],q=state["question"]))
    if (bool(result.ch)==False):
        return "search"
    else:
        return END

