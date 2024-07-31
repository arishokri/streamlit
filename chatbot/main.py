import streamlit as st

st.sidebar.text_input("Consultant Name", key="consultant")
st.sidebar.text_input("Client Name", key="client")
st.sidebar.write(st.session_state.consultant)
pg = st.navigation([st.Page("mirror.py"), st.Page("stream.py")])
pg.run()
# How to export and handle session state between pages.