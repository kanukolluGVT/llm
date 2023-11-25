import streamlit as st
from main import create_vector_db, get_qa_chain

st.title("QA 🤔")
st.title("are u system administrator🖥️")
system_admin = st.button("🖥")
system_admin_no = st.button("🚫")
if system_admin:
    btn = st.button("create knowledgeBase")
    if btn:
        create_vector_db()
st.title("choose ur gender ")
male = st.button("🙋‍♂")
female = st.button("🙋‍♀️")


if male:
    question = st.text_input("Question: 🙋‍♂️")
else:
    question = st.text_input("Question: 🙋‍♀️")

if question:
    chain = get_qa_chain()
    response = chain(question)
    print(response)
    st.header("Answer: ")
    st.write(response["result"])

st.title("source doucments ")
src_doc = st.button("📄")
if src_doc:
    st.write(response["source_documents"])
