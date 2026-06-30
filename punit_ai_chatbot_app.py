import os
import streamlit as st
import requests

from bs4 import BeautifulSoup

from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS



# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖",
    layout="centered"
)



# -----------------------------
# API KEY
# -----------------------------

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY



# -----------------------------
# WEBSITE RESOURCES
# -----------------------------

RESOURCES = {

"Excel":
"https://www.punittechhub.com/excel-tutorials",

"Mainframe":
"https://www.punittechhub.com/mainframe-tutorials",

"COBOL":
"https://www.punittechhub.com/cobol-tutorials",

"JCL":
"https://www.punittechhub.com/jcl-tutorials",

"DB2":
"https://www.punittechhub.com/db2-tutorials",

"CICS":
"https://www.punittechhub.com/cics-tutorials",

"VSAM":
"https://www.punittechhub.com/vsam-tutorials",

"AI":
"https://www.punittechhub.com/ai-learning-resources",

"All":
"https://www.punittechhub.com/all-resources"

}



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



# -----------------------------
# CREATE KNOWLEDGE BASE
# -----------------------------


@st.cache_resource(ttl=86400)
def create_database():


    if os.path.exists("punit_vector_db"):


        embeddings = GoogleGenerativeAIEmbeddings(

            model="models/text-embedding-004",

            google_api_key=GOOGLE_API_KEY

        )


        return FAISS.load_local(

            "punit_vector_db",

            embeddings,

            allow_dangerous_deserialization=True

        )



    documents=[]



    for url in URLS:


        try:

            response=requests.get(
                url,
                timeout=15
            )


            soup=BeautifulSoup(

                response.text,

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


        except Exception:


            pass




    splitter = RecursiveCharacterTextSplitter(

        chunk_size=800,

        chunk_overlap=100

    )



    chunks = splitter.split_documents(

        documents

    )




    embeddings = GoogleGenerativeAIEmbeddings(

        model="models/text-embedding-004",

        google_api_key=GOOGLE_API_KEY

    )



    db = FAISS.from_documents(

        chunks,

        embeddings

    )



    db.save_local(

        "punit_vector_db"

    )


    return db





# -----------------------------
# LOAD DATABASE
# -----------------------------

with st.spinner(
"Loading Punit Tech Hub Knowledge..."
):

    database=create_database()





# -----------------------------
# GEMINI MODEL
# -----------------------------


llm = ChatGoogleGenerativeAI(

    model="gemini-2.0-flash",

    google_api_key=GOOGLE_API_KEY,

    temperature=0.3

)





# -----------------------------
# HEADER
# -----------------------------


st.title(
"🤖 Punit AI Learning Assistant"
)


st.write(
"""
Your AI assistant for:

📊 Excel  
🤖 AI & ChatGPT  
📈 Data Analytics  
💻 Mainframe  
📝 COBOL  
⚙️ JCL  
🗄️ DB2  
📂 CICS / VSAM
"""
)





# -----------------------------
# CHAT MEMORY
# -----------------------------


if "messages" not in st.session_state:

    st.session_state.messages=[]



for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )




# -----------------------------
# QUESTION
# -----------------------------


question = st.chat_input(
"Ask your question..."
)



if question:



    st.session_state.messages.append(

        {
        "role":"user",
        "content":question
        }

    )


    with st.chat_message("user"):

        st.write(question)



    # Search knowledge

    docs = database.similarity_search(

        question,

        k=3

    )



    context=""


    sources=[]



    for doc in docs:


        context += doc.page_content


        sources.append(

            doc.metadata.get(
                "source"
            )

        )




    prompt=f"""

You are Punit AI Learning Assistant.

Answer only questions related to:

Excel
AI
ChatGPT
Data Analytics
Mainframe
COBOL
JCL
DB2
CICS
VSAM


Use this information:

{context}


User Question:

{question}


If information is not available,
say:

"I could not find this in Punit Tech Hub resources."

"""



    response=llm.invoke(

        prompt

    )



    answer=response.content



    with st.chat_message("assistant"):


        st.write(answer)



        st.markdown(
        "---"
        )


        st.write(
        "📚 Related Resources:"
        )


        for source in sources:

            st.write(source)



    st.session_state.messages.append(

        {
        "role":"assistant",
        "content":answer
        }

    )
