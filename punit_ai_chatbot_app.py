import streamlit as st
import os
import requests
from bs4 import BeautifulSoup

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------
# Gemini API
# -------------------------------

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY



# -------------------------------
# Website Knowledge Base
# -------------------------------

URLS = [

"https://www.punittechhub.com/all-resources",

"https://www.punittechhub.com/excel-tutorials",

"https://www.punittechhub.com/mainframe-tutorials",

"https://www.punittechhub.com/cobol-tutorials",

"https://www.punittechhub.com/jcl-tutorials",

"https://www.punittechhub.com/db2-tutorials",

"https://www.punittechhub.com/cics-tutorials",

"https://www.punittechhub.com/vsam-tutorials",

"https://www.punittechhub.com/mainframe-interview-questions",

"https://www.punittechhub.com/excel-formulas-guide",

"https://www.punittechhub.com/data-analysis-tutorials",

"https://www.punittechhub.com/excel-charts-tutorials",

"https://www.punittechhub.com/advanced-excel-tutorials"

]



# -------------------------------
# Load Website Data
# -------------------------------


@st.cache_resource
def load_database():


    documents=[]


    for url in URLS:

        try:

            r=requests.get(url,timeout=10)

            soup=BeautifulSoup(
                r.text,
                "html.parser"
            )


            text=soup.get_text(
                separator=" "
            )


            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source":url
                    }
                )
            )


        except Exception as e:

            pass



    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )


    docs = splitter.split_documents(
        documents
    )


    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )


    db = FAISS.from_documents(
        docs,
        embeddings
    )


    return db



# -------------------------------
# Load AI
# -------------------------------

db = load_database()



llm = ChatGoogleGenerativeAI(

    model="gemini-1.5-flash",

    temperature=0.3

)



# -------------------------------
# UI
# -------------------------------


st.title(
"🤖 Punit AI Learning Assistant"
)


st.write(
"Ask questions about Excel, AI, ChatGPT, Data Analysis and Mainframe."
)



question = st.chat_input(
"Ask your question..."
)



if question:


    with st.chat_message("user"):

        st.write(question)



    docs = db.similarity_search(
        question,
        k=3
    )


    context=""

    for d in docs:

        context += d.page_content



    prompt=f"""

You are Punit AI Learning Assistant.

Answer only related to:
- Excel
- AI
- ChatGPT
- Data Analysis
- Mainframe
- COBOL
- JCL
- DB2
- CICS
- VSAM


Use this knowledge:

{context}


Question:

{question}


If answer is not available say:

"I don't have this information in Punit Tech Hub resources."

"""


    response = llm.invoke(prompt)



    with st.chat_message("assistant"):

        st.write(
            response.content
        )
