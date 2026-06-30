import streamlit as st
import requests
from bs4 import BeautifulSoup

from langchain_google_genai import ChatGoogleGenerativeAI



# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖"
)



# -------------------------
# GEMINI KEY
# -------------------------

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]



# -------------------------
# GEMINI MODEL
# -------------------------

llm = ChatGoogleGenerativeAI(

    model="gemini-2.0-flash",

    google_api_key=GOOGLE_API_KEY,

    temperature=0.3
)



# -------------------------
# YOUR WEBSITE RESOURCES
# -------------------------

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



# -------------------------
# LOAD WEBSITE CONTENT
# -------------------------

@st.cache_data(ttl=86400)

def load_content():


    content=""


    for url in URLS:


        try:


            response=requests.get(

                url,

                timeout=10

            )


            soup=BeautifulSoup(

                response.text,

                "html.parser"

            )


            text=soup.get_text(

                separator=" "

            )


            content += "\n\n" + text



        except:

            pass



    return content[:50000]



knowledge = load_content()



# -------------------------
# HEADER
# -------------------------


st.title(
"🤖 Punit AI Learning Assistant"
)


st.write(

"""
Your AI assistant for:

📊 Excel  
🤖 AI / ChatGPT  
📈 Data Analytics  
💻 Mainframe  
📝 COBOL  
⚙️ JCL  
🗄️ DB2  
📂 CICS / VSAM

"""

)



# -------------------------
# CHAT
# -------------------------

if "messages" not in st.session_state:

    st.session_state.messages=[]



for msg in st.session_state.messages:


    with st.chat_message(msg["role"]):

        st.write(msg["content"])





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




    prompt=f"""

You are Punit AI Learning Assistant.

You help users with:

Excel
AI
ChatGPT
Data Analysis
Mainframe
COBOL
JCL
DB2
CICS
VSAM


Use this Punit Tech Hub knowledge:

{knowledge}


User Question:

{question}


Rules:

- Give simple practical answers
- If related resource exists mention it
- Do not answer unrelated topics


"""



    response=llm.invoke(prompt)



    answer=response.content




    with st.chat_message("assistant"):


        st.write(answer)



        st.markdown(
        """

        📚 More Resources:

        https://www.punittechhub.com/all-resources

        """
        )



    st.session_state.messages.append(

        {

        "role":"assistant",

        "content":answer

        }

    )
