import os
import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from uuid import uuid4
import math
import time
from langchain_community.docstore.in_memory import InMemoryDocstore


os.environ["COHERE_API_KEY"] = os.environ.get("COHERE_API_KEY")
class DataProcessor:
    def __init__(self, data_dir="data", persist_dir="django_docs"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.embeddings = CohereEmbeddings(user_agent="split",model="embed-english-light-v3.0")
        self.index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))
        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=self.index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        
    def prepare_documents(self):
        documents = []
        for file in os.listdir(self.data_dir):
            loader = PyPDFLoader(f"{self.data_dir}/{file}")
            documents.extend(loader.load())
            print(f"Loaded {file}")
        
        chunks = self.text_splitter.split_documents(documents)[:1800]
        step=math.ceil(len(chunks)/600)
        for i in range(step):
            docs= chunks[i*634:(i+1)*634]
            uuids = [str(uuid4()) for _ in range(len(docs))]
            self.vector_store.add_documents(documents=docs, ids=uuids)
            print(i,end=" , ")
            time.sleep(61)
            print(i,end="")
        self.vector_store.save_local(self.persist_dir)
        
    

dp= DataProcessor()
dp.prepare_documents()