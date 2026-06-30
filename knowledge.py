import os

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings



def create_database():


    documents=[]


    folder="knowledge_base"


    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            loader=PyPDFLoader(
                f"{folder}/{file}"
            )

            documents.extend(
                loader.load()
            )


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )


    chunks = splitter.split_documents(
        documents
    )


    embeddings = OpenAIEmbeddings()


    db = FAISS.from_documents(
        chunks,
        embeddings
    )


    db.save_local(
        "punit_vector_db"
    )


    return db