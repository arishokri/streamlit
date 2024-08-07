import streamlit as st
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

# from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(page_title="AI Alchemy", page_icon="⚛️")


def set_llm():  # Sets llm models as session_state to be used across the app.
    if "llm" not in st.session_state:
        st.session_state.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


def set_embedding():
    if "embedding" not in st.session_state:
        st.session_state.embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
        # st.session_state.embedding = OpenAIEmbeddings(model='text-embedding-3-small')


def set_vector_store():
    if "vector_db_collection" not in st.session_state:
        st.session_state.vector_db_collection = Chroma(
            collection_name=st.session_state.client,
            persist_directory="dbs/",
            embedding_function=st.session_state.embedding,
        )


def set_text_splitter(chunk_size=1000, chunk_overlap=200):
    if "text_splitter" not in st.session_state:
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )


def reset_client():
    set_embedding()
    st.session_state.vector_db_collection = Chroma(
        collection_name=st.session_state.client,
        persist_directory="dbs/",
        embedding_function=st.session_state.embedding,
    )


def check_project_params():
    passed = True
    if consultant := st.session_state.consultant:
        st.sidebar.markdown(f"Consultant Name: {consultant}")
    else:
        st.error(body="Please enter a consultant name.", icon="🚨")
        passed = False
    if client := st.session_state.client:
        st.sidebar.markdown(f"Client Name: {client}")
    else:
        st.error(body="Please enter a client name.", icon="🚨")
        passed = False
    return passed


st.sidebar.text_input("Consultant Name", placeholder="Joe Smith", key="consultant")
st.sidebar.text_input(
    "Client Name",
    placeholder="Microsoft",
    key="client",
    on_change=reset_client,
)
# st.session_state.temperature = (
#     st.session_state.temperature if "temperature" in st.session_state else 0.1
# )

pg = st.navigation(
    [
        st.Page(
            "user_config.py",
            title="Configurations",
            icon=":material/settings_input_component:",
        ),
        st.Page(
            "rag_with_history.py",
            title="Assistant",
            icon=":material/headset_mic:",
        ),
    ]
)

if check_project_params():
    set_llm()
    set_embedding()
    set_vector_store()
    set_text_splitter(chunk_size=1000, chunk_overlap=200)
    pg.run()

st.sidebar.write("© 2024 AI Alchemy")