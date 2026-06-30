import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq



# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(

    page_title="Punit AI Assistant",

    page_icon="🤖",

    layout="wide"

)



# ==========================
# BRANDING
# ==========================


col1, col2 = st.columns([1,5])


with col1:

    st.image(
        "assets/punit_logo.png",
        width=120
    )


with col2:

    st.title(
        "🤖 Punit AI Assistant"
    )

    st.caption(
        "AI Learning Assistant by Punit Tech Hub"
    )




st.markdown("---")



# ==========================
# WELCOME
# ==========================


st.success(
"""
Welcome to Punit AI Assistant 🤖


I can help you with:


📊 Excel  
🤖 Artificial Intelligence  
📈 Data Analytics  
💻 Mainframe Technologies  


Ask me anything!
"""
)



# ==========================
# QUICK BUTTONS
# ==========================


st.subheader(
"Explore Resources"
)


c1,c2,c3,c4 = st.columns(4)



if c1.button("📊 Excel Tutorials"):

    st.markdown(

    "https://www.punittechhub.com/excel-tutorials"

    )



if c2.button("🤖 AI Resources"):

    st.markdown(

    "https://www.punittechhub.com/ai-learning-resources"

    )



if c3.button("💻 Mainframe Guides"):

    st.markdown(

    "https://www.punittechhub.com/mainframe-tutorials"

    )



if c4.button("⭐ Premium Resources"):

    st.markdown(

    "https://www.punittechhub.com/services"

    )



st.markdown("---")





# ==========================
# GROQ API
# ==========================


GROQ_KEY = st.secrets["GROQ_API_KEY"]



llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    groq_api_key=GROQ_KEY,

    temperature=0.2

)




# ==========================
# WEBSITE KNOWLEDGE
# ==========================


URLS=[


"https://www.punittechhub.com/all-resources",

"https://www.punittechhub.com/excel-tutorials",

"https://www.punittechhub.com/mainframe-tutorials",

"https://www.punittechhub.com/cobol-tutorials",

"https://www.punittechhub.com/jcl-tutorials",

"https://www.punittechhub.com/db2-tutorials",

"https://www.punittechhub.com/ai-learning-resources"


]




@st.cache_data(ttl=86400)

def load_content():


    data=""


    for url in URLS:


        try:


            r=requests.get(url,timeout=10)


            soup=BeautifulSoup(

                r.text,

                "html.parser"

            )


            data += soup.get_text()



        except:


            pass



    return data[:10000]



knowledge=load_content()




# ==========================
# CHAT MEMORY
# ==========================


if "messages" not in st.session_state:

    st.session_state.messages=[]




for msg in st.session_state.messages:


    with st.chat_message(msg["role"]):

        st.write(msg["content"])




# ==========================
# USER INPUT
# ==========================


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

You are Punit AI Assistant.


You help users with:


Excel

AI

ChatGPT

Data Analytics

Mainframe

COBOL

JCL

DB2


Use this knowledge:


{knowledge}



Special rules:


If user asks:

"create resume"

reply:


You can use Punit AI Resume Builder:

https://pth-ai-resume-builder.streamlit.app/


If user asks:

"analyze excel"

reply:


Try Punit AI Data Analyzer:

https://pth-ai-data-analyzer.streamlit.app/


Answer professionally.

Question:

{question}


"""



    with st.chat_message("assistant"):


        response=llm.invoke(prompt)


        answer=response.content


        st.write(answer)



    st.session_state.messages.append(

        {

        "role":"assistant",

        "content":answer

        }

    )




# ==========================
# ANALYTICS
# ==========================


if "questions" not in st.session_state:

    st.session_state.questions=[]



st.session_state.questions.append(question)



with st.sidebar:


    st.subheader(
    "📊 Usage Analytics"
    )


    st.write(

    "Questions asked:",

    len(st.session_state.questions)

    )


    st.write(

    "Popular topics will appear here later"

    )


