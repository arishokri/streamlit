import streamlit as st
from pydantic import HttpUrl, ValidationError
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

if "links" not in st.session_state:
    st.session_state.links = []


def validate_link(url):
    try:
        HttpUrl(url)
        return True, None
    except ValidationError as e:
        return False, str(e)


def create_links_list():
    links_list = []
    errors_list = []
    for link in st.session_state.links_text.split(","):
        is_valid, error = validate_link(link.strip())
        if is_valid:
            links_list.append(link.strip())
        else:
            errors_list.append(
                f"The entered URL {link} is not a valid URL. Error details: {error}"
            )
    st.session_state.links.extend(links_list)
    for error in errors_list:
        st.error(error)


with st.form(key="links_form", clear_on_submit=True):
    st.text_area(
        label="Context URLs",
        placeholder="Insert web URLs you want to import here. Separate URLs by comma.",
        key="links_text",
    )
    st.form_submit_button(label="Submit", on_click=create_links_list)


files = st.file_uploader(
    label="Context Files",
    accept_multiple_files=True,
    help="Hi I'm here to help.",
    key="files",
)

### Vector Storage


def store_links():
    if st.session_state.links:
        web_loader = WebBaseLoader(web_paths=st.session_state.links)
        docs = web_loader.load()
        for doc in reversed(docs):
            if st.session_state.vector_db_collection.get(
                where={"source": doc.metadata["source"]}
            )["documents"]:
                st.error(
                    body=f"The following document already exists in database:\n{doc.metadata['source']}"
                )
                docs.remove(doc)

        if docs:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)
            # Find a way to use a persisting db instance instead of rewriting the state object everytime.
            st.session_state.vector_db_collection.from_documents(
                documents=splits,
                embedding=st.session_state.embedding,
                collection_name=st.session_state.client,
                persist_directory="dbs/",
            )
        del st.session_state.links
    else:
        st.error(body="No new links were provided.")


def push_to_db():
    # Chroma.from_documents(
    #     collection_name=st.session_state.client,
    #     persist_directory="dbs/",
    #     embedding=OpenAIEmbeddings(),
    #     documents=docs,
    # )
    return None


st.button(
    label="Commit new content to knowledge base.",
    key="commit_to_kb",
    on_click=store_links,
)

## I need to make push_to_db work for file uploads as well
