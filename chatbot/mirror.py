import streamlit as st

st.title("Echo Bot")

if "mirror" not in st.session_state:
    st.session_state.mirror = []

for message in st.session_state.mirror:
    with st.chat_message(name=message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type something..."):
    with st.chat_message(name=st.session_state.consultant, avatar="👩‍💼"):
        st.markdown(prompt)
    st.session_state.mirror.append({"role": st.session_state.consultant, "content": prompt, "avatar": "👩‍💼"})

    with st.chat_message(name="Consult Assist", avatar="🕺"):
        st.markdown(prompt)
    st.session_state.mirror.append({"role": "assistant", "content": prompt, "avatar": "🕺"})
