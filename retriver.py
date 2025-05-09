from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
import os
import faiss
import uuid
from dotenv import load_dotenv
from langchain_community.docstore.in_memory import InMemoryDocstore


load_dotenv()
os.environ["COHERE_API_KEY"] = os.environ.get("COHERE_API_KEY")
class VectorRetriever:
    def __init__(self, persist_dir="django_docs"):
        embeddings=CohereEmbeddings(user_agent="split",model="embed-english-light-v3.0")
        index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
        self.vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        self.vector_store.load_local(
            persist_dir, embeddings, allow_dangerous_deserialization=True,
        )


    def retrieve(self, query, k=3):
        return self.vector_store.similarity_search(query, k=k)