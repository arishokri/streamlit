import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = st.session_state.llm

# vectorstore = Chroma(
#     collection_name=st.session_state.client,
#     persist_directory="dbs/",
#     embedding_function=OpenAIEmbeddings(),
# )
retriever = st.session_state.vector_db_collection.as_retriever()

### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)
### Answer question ###
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
def get_session_history() -> BaseChatMessageHistory:
    if "chat_memory" not in st.session_state:
        st.session_state.chat_memory = ChatMessageHistory()
    return st.session_state.chat_memory


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


def generate_response(prompt):
    return conversational_rag_chain.pick("answer").stream({"input": prompt})


### Conversation UI elements goes here.
if "chat_memory" in st.session_state:
    for message in st.session_state.chat_memory.messages:
        st.chat_message(
            message.type,
            avatar=(
                "👩‍💼"
                if message.type == "human"
                else "🤖" if message.type == "ai" else None
            ),
        ).markdown(message.content)

if prompt := st.chat_input("What's up?"):
    st.chat_message("human", avatar="👩‍💼").markdown(prompt)
    st.chat_message("ai", avatar="🤖").write_stream(generate_response(prompt))
