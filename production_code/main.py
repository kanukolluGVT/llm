from langchain.llms import GooglePalm
from dotenv import load_dotenv
import os
from langchain.embeddings import GooglePalmEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
llm = GooglePalm(google_api_key=os.environ["api_key"], temperature=0.0)
gpe = GooglePalmEmbeddings(google_api_key=os.environ["api_key"])

vectordb_file_path = "fiass_index"


def create_vector_db():
    loader = CSVLoader(
        file_path="/home/kgvt/llm/experiements/faq.csv", source_column="prompt"
    )
    data = loader.load()
    vectordb = FAISS.from_documents(documents=data, embedding=gpe)
    vectordb.save_local(vectordb_file_path)


def get_qa_chain():
    vectordb = FAISS.load_local(vectordb_file_path, gpe)
    retriver = vectordb.as_retriever(score_threshold=0.7)
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriver,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )
    return chain


if __name__ == "__main__":
    # create_vector_db()
    chain = get_qa_chain()
    print(chain("do u have a java coutrse and emi option"))
