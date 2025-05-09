import streamlit as st
from agent import MultiAgentSystem
import os
from dotenv import load_dotenv
import uuid
load_dotenv()

os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_API_KEY']=os.environ["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"]="django-gpt"

st.set_page_config(page_title="Django GPT",page_icon="🧠", layout="wide")
st.title("🧠 Django BOt ")

@st.cache_resource
def get_agent():
    return MultiAgentSystem()

agent = get_agent()

query = st.text_input("Ask a question:", placeholder="you ask about the django python code and question")
if 'key' not in st.session_state:
    st.session_state['key'] = uuid.uuid4()
if query:
    with st.spinner("Processing..."):
        key=st.session_state['key']
        result = agent.route_query(query,ids=key)
        st.subheader(F"Question====>         {query}")
        st.subheader("Answer")
        st.write(result)
  