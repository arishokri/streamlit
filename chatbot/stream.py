import streamlit as st
import random
import time


def response_gen():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.07)

st.title("Chatbot with Streaming")
if "stream" not in st.session_state:
    st.session_state.stream = []

for message in st.session_state.stream:
    st.chat_message(name=message["role"]).markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.stream.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = st.write_stream(response_gen())
    st.session_state.stream.append({"role": "assistant", "content": response})