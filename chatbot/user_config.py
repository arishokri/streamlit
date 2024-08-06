import streamlit as st
from pydantic import HttpUrl, ValidationError
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.parsers import PyMuPDFParser, PyPDFParser
from langchain_community.document_loaders.blob_loaders import Blob

if "links" not in st.session_state:
    st.session_state.links = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  # The state for uploader cannot be set directly. This is a workaround to reset this state value.

st.write(f"links are: {st.session_state.links}")
st.write(f"uploader key is: {st.session_state.uploader_key}")
### Functions for validating links and files to state.

# st.slider(
#     label="Temperature value:",
#     value=0.1,
#     min_value=0.0,
#     max_value=1.0,
#     key="temperature",
#     help="This value controls the creativity of our model. The lower values result in more consistant responses while higher values encourage variety and creativity.",
# )


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

def split_and_store(
    docs,
    text_splitter=st.session_state.text_splitter,
    db_collection=st.session_state.vector_db_collection,
    embedding=st.session_state.embedding,
    collection_name=st.session_state.client,
):
    splits = text_splitter.split_documents(docs)
    db_collection.from_documents(
        documents=splits,
        embedding=embedding,
        collection_name=collection_name,
        persist_directory="dbs/",
    )
    st.info(body="Documents have been successfully stored in the knowledge base.")


def store_links():
    db_collection = st.session_state.vector_db_collection
    # text_splitter = st.session_state.text_splitter
    if st.session_state.links:
        web_loader = WebBaseLoader(web_paths=st.session_state.links)
        docs = web_loader.load()
        for doc in reversed(docs):
            if db_collection.get(where={"source": doc.metadata["source"]})[
                "documents"
            ]:
                st.error(
                    body=f"The following document already exists in database:\n{doc.metadata['source']}"
                )
                docs.remove(doc)
        if docs:
            # splits = text_splitter.split_documents(docs)
            # db_collection.from_documents(
            #     documents=splits,
            #     embedding=st.session_state.embedding,
            #     collection_name=st.session_state.client,
            #     persist_directory="dbs/",
            # )
            split_and_store(docs)
        del st.session_state.links
    else:
        st.error(body="No new links were provided.")


with st.form(key="links_form", clear_on_submit=True):
    st.text_area(
        label="Insert URLs to import into knowledge base:",
        placeholder="Insert web URLs you want to import here. Separate URLs by comma.",
        key="links_text",
    )
    st.form_submit_button(label="Submit", on_click=create_links_list)


uploaded_files = st.file_uploader(
    label="Choose files to import into knowledge base:",
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}",  # Workaround to refreshing the state value after execution.
)



st.radio(
    label="Select document parsing method:",
    options=["default", "tables"],
    key="pdf_mode",
    horizontal=False,
    help="For most use-cases you would want to leave this as default which results in much faster file processing. Only use other options if your document has a significant number of unstructured elements that otherwise are not being picked up by AI. The default parser can process majority of tables and images with great results.",
)


def store_pdfs():
    mode = st.session_state.pdf_mode
    db_collection = st.session_state.vector_db_collection
    text_splitter = st.session_state.text_splitter
    parser = None
    if mode == "default":
        parser = PyMuPDFParser()
    elif mode == "tables":
        parser = PyPDFParser()
    else:
        st.error(body="No valid parsing mode provided.")
        return None
    if files := uploaded_files:
        st.session_state.uploader_key += 1  # Increments the uploader key to remove the uploaded documents from the state.
        for file in reversed(files):
            if db_collection.get(where={"source": file.name})["documents"]:
                st.error(
                    body=f"The following document already exists in database:\n{file.name}"
                )
                files.remove(file)
        for file in files:
            st.write(file.name)
            blob = Blob(data=file.getvalue(), metadata={"source": file.name})
            docs = parser.parse(blob=blob)
            splits = text_splitter.split_documents(docs)
            for split in splits:
                st.write(split)
    else:
        st.error(body="No new files were provided.")


st.button(
    label="Import Files to Knowledge Base",
    key="import_to_kb",
    on_click=store_pdfs,
    help="Click this button once you're finished with inputing all the links and uploading all of your files. You may commit your documents to knowledge base separately and in a number of batches.",
)
