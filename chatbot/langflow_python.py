# import streamlit as st
from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

TWEAKS = {
    "OpenAIModel-M0qvB": {
        "api_key": "OpenAI_API_Key",
        "input_value": "",
        "json_mode": False,
        "max_tokens": None,
        "model_kwargs": {},
        "model_name": "gpt-4o-mini",
        "openai_api_base": "",
        "output_schema": {},
        "seed": 1,
        "stream": True,
        "system_message": "",
        "temperature": 0.2,
    },
    "TextInput-4Kujw": {"input_value": "Test"},
    "TextInput-8Sw6t": {"input_value": "Ari"},
    "CombineText-u58t2": {"delimiter": "-", "text1": "", "text2": ""},
}

# message = "Print out the knowledge base you are provided."

# result = run_flow_from_json(
#     flow="chat_retrieval.json", input_value=message, fallback_to_env_vars=True
# )

# returned = result[0].outputs[0].results["message"]["text"]
# print(type(returned))
# print("\n\n", returned)

st.title("⛓️ Langflow App")


def generate_response(user_input):
    flow_response = run_flow_from_json(
        flow="chat_retrieval.json",
        input_value=user_input,
        fallback_to_env_vars=True,
        tweaks=TWEAKS,
    )
    # return flow_response[0].outputs[0].results["message"].text
    return flow_response[0].outputs[0].results["message"].text


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
        st.write_stream(response)
    st.session_state.message_history.append({"role": "assistant", "content": response})
