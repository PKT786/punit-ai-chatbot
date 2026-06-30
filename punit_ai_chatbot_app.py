import streamlit as st
import os

from openai import OpenAI

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings



# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# OPENAI CONNECTION
# -----------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)



# -----------------------------
# RESOURCE LINKS
# -----------------------------

resources = {

"Excel":
"https://www.punittechhub.com/excel-tutorials",

"AI":
"https://www.punittechhub.com/ai-learning-resources",

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

"Interview":
"https://www.punittechhub.com/mainframe-interview-questions",

"Formula":
"https://www.punittechhub.com/excel-formulas-guide",

"Data Analysis":
"https://www.punittechhub.com/data-analysis-tutorials",

"Charts":
"https://www.punittechhub.com/excel-charts-tutorials",

"Advanced Excel":
"https://www.punittechhub.com/advanced-excel-tutorials",

"All Resources":
"https://www.punittechhub.com/all-resources"

}



# -----------------------------
# LOAD KNOWLEDGE BASE
# -----------------------------


@st.cache_resource
def load_database():


    if os.path.exists("punit_vector_db"):

        embeddings = OpenAIEmbeddings()

        return FAISS.load_local(
            "punit_vector_db",
            embeddings,
            allow_dangerous_deserialization=True
        )



    documents=[]


    folder="knowledge_base"


    if not os.path.exists(folder):

        os.makedirs(folder)


    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(
                f"{folder}/{file}"
            )

            documents.extend(
                loader.load()
            )


    if len(documents)==0:

        return None



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




db = load_database()



# -----------------------------
# HEADER
# -----------------------------


st.title(
"🤖 Punit AI Learning Assistant"
)


st.write(
"Ask questions about Excel, AI, ChatGPT, Data Analysis and Mainframe technologies."
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
# USER INPUT
# -----------------------------


question = st.chat_input(
"Ask your question..."
)



if question:



    st.session_state.messages.append({

        "role":"user",

        "content":question

    })


    with st.chat_message("user"):

        st.write(question)




    # -----------------------------
    # TOPIC DETECTION
    # -----------------------------


    topic="All Resources"


    q=question.lower()



    if "excel" in q or "formula" in q or "pivot" in q:

        topic="Excel"



    elif "cobol" in q:

        topic="COBOL"



    elif "jcl" in q:

        topic="JCL"



    elif "db2" in q:

        topic="DB2"



    elif "cics" in q:

        topic="CICS"



    elif "vsam" in q:

        topic="VSAM"



    elif "mainframe" in q:

        topic="Mainframe"



    elif "ai" in q or "chatgpt" in q:

        topic="AI"



    elif "dashboard" in q or "analysis" in q:

        topic="Data Analysis"





    # -----------------------------
    # SEARCH KNOWLEDGE
    # -----------------------------


    context=""



    if db:


        docs=db.similarity_search(

            question,

            k=3

        )


        for doc in docs:

            context += doc.page_content




    else:


        context = """
        No PDF uploaded yet.
        Answer using general knowledge.
        """





    # -----------------------------
    # AI RESPONSE
    # -----------------------------


    response = client.chat.completions.create(


        model="gpt-4.1-mini",


        messages=[


        {


        "role":"system",


        "content":f"""

You are Punit AI Learning Assistant.

You answer only Excel,
AI, ChatGPT, Data Analytics,
and Mainframe questions.

Use this Punit Tech Hub knowledge:

{context}


If the answer is not available,
say:
'I could not find this in Punit Tech Hub resources.'

"""


        },


        {


        "role":"user",

        "content":question

        }


        ]

    )



    answer = response.choices[0].message.content




    with st.chat_message("assistant"):


        st.write(answer)



        st.markdown(
        f"""
        ---
        📚 Related Learning Resource:

        👉 [{topic}]
        ({resources.get(topic,resources["All Resources"])})
        """
        )



    st.session_state.messages.append({

        "role":"assistant",

        "content":answer

    })
