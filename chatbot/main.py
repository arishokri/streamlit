import streamlit as st

st.sidebar.text_input("Consultant Name", key="consultant")
st.sidebar.text_input("Client Name", key="client")
st.sidebar.write(st.session_state.consultant)
pg = st.navigation(
    [
        st.Page("mirror.py", title="Mirror Bot", icon=":material/self_care:"),
        st.Page("stream.py", title="Stream Bot", icon=":material/cast:"),
        st.Page("langchain_bot.py", title="Langchain", icon=":material/link:"),
    ]
)
pg.run()
# How to export and handle session state between pages.
