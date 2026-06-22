import streamlit as st

from query import ask_question

st.set_page_config(
    page_title="Document Q&A Bot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Document Q&A Bot")

st.write("Ask questions from your documents")

question = st.text_input("Enter your question")

if st.button("Ask"):

    if question:

        with st.spinner("Searching documents..."):

            answer = ask_question(question)

        st.success("Answer Generated")

        st.write(answer)