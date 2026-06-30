import os
import streamlit as st

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS

from langchain_community.document_loaders import WebBaseLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import ConversationalRetrievalChain

from langchain.memory import ConversationBufferMemory


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🤖 Punit AI Learning Assistant")

st.write(
    """
Ask questions about:

📊 Excel  
🤖 AI / ChatGPT  
💻 Mainframe  
📝 COBOL  
⚙️ JCL  
🗄️ DB2  
📡 CICS  
📂 VSAM  

Answers are generated from Punit Tech Hub resources.
"""
)



# ---------------------------------------------------
# GEMINI KEY
# ---------------------------------------------------

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]



# ---------------------------------------------------
# RESOURCE URLS
# ---------------------------------------------------

RESOURCE_URLS = [

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



# ---------------------------------------------------
# LOAD WEBSITE KNOWLEDGE
# ---------------------------------------------------

@st.cache_resource
def load_database():


    documents = []


    for url in RESOURCE_URLS:

        try:

            loader = WebBaseLoader(url)

            docs = loader.load()

            documents.extend(docs)


        except Exception as e:

            st.warning(
                f"Unable to load {url}"
            )



    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )


    chunks = splitter.split_documents(
        documents
    )



    embeddings = GoogleGenerativeAIEmbeddings(

        model="models/embedding-001",

        google_api_key=GOOGLE_API_KEY

    )



    db = FAISS.from_documents(

        chunks,

        embeddings

    )


    return db





# ---------------------------------------------------
# LOAD CHATBOT
# ---------------------------------------------------

@st.cache_resource
def create_chain():


    db = load_database()



    llm = ChatGoogleGenerativeAI(

        model="gemini-2.0-flash",

        google_api_key=GOOGLE_API_KEY,

        temperature=0.3

    )



    memory = ConversationBufferMemory(

        memory_key="chat_history",

        return_messages=True

    )



    chain = ConversationalRetrievalChain.from_llm(

        llm=llm,

        retriever=db.as_retriever(
            search_kwargs={
                "k":5
            }
        ),

        memory=memory,

        return_source_documents=True

    )


    return chain





# ---------------------------------------------------
# START CHATBOT
# ---------------------------------------------------

if "chain" not in st.session_state:


    with st.spinner(
        "Loading Punit Tech Hub knowledge..."
    ):

        st.session_state.chain = create_chain()





# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages=[]



for msg in st.session_state.messages:


    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )





# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

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



    with st.chat_message("assistant"):


        with st.spinner(
            "Searching Punit Tech Hub resources..."
        ):


            response = (
                st.session_state.chain(
                    {
                        "question":question
                    }
                )
            )


            answer = response["answer"]



            st.write(answer)



            st.subheader(
                "📚 Sources"
            )


            for doc in response["source_documents"]:


                st.write(

                    doc.metadata.get(
                        "source",
                        "Punit Tech Hub"
                    )

                )



    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer
        }

    )
