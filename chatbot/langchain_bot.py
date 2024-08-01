import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

st.title("🦜🔗 Langchain App")

openai_api_key = st.secrets.openai_api_key


def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    # st.info(model.invoke(input_text).content)
    return model.invoke(input_text).content


# with st.form("my_form"):
#     text = st.text_area(
#         "Enter text:",
#         "What are the three key pieces of advice for learning how to code?",
#     )
#     submitted = st.form_submit_button("Submit")
#     if not openai_api_key.startswith("sk-"):
#         st.warning("Please enter your OpenAI API key!", icon="⚠")
#     if submitted and openai_api_key.startswith("sk-"):
#         generate_response(text)

if "message_history" not in st.session_state:
    st.session_state.message_history = []

for message in st.session_state.message_history:
    st.chat_message(message["role"]).markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.message_history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
    st.session_state.message_history.append({"role": "assistant", "content": response})
