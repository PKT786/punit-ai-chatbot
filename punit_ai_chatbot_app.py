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

You are Punit AI Assistant for Punit Tech Hub.


You help users with:

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


IMPORTANT RESOURCE RULES:


If user asks anything related to:

COBOL
JCL
DB2
CICS
VSAM
Mainframe
Mainframe interview questions
Mainframe PDF
COBOL PDF
JCL PDF
Interview preparation


Always provide this resource link:


📘 Punit Tech Hub Mainframe Resources:

https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH



--------------------------------


If user asks anything related to:

AI
Artificial Intelligence
ChatGPT
AI prompts
AI tools
Generative AI


Always provide:


🤖 Punit Tech Hub AI Resources:

https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2



--------------------------------


If user asks anything related to:

Excel
Excel formulas
Excel dashboard
Pivot Table
Excel charts
Data analysis


Always provide:


📊 Punit Tech Hub Excel Resources:

https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm



--------------------------------


If user asks anything related to:

Templates
Excel templates
Business templates
Dashboard templates


Always provide:


📁 Punit Tech Hub Templates:

https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA



--------------------------------



AI Tools:


If user asks:

Create resume


Reply:


You can use Punit AI Resume Builder:


https://pth-ai-resume-builder.streamlit.app/



If user asks:

Analyze Excel file


Reply:


Try Punit AI Data Analyzer:


https://pth-ai-data-analyzer.streamlit.app/



--------------------------------



Knowledge from website:


{knowledge}



Answer rules:


1. Do not create fake links.

2. Use only above Google Drive links for resources.

3. Be helpful and professional.

4. If user asks for PDF, provide the correct resource folder.

5. Mention Punit Tech Hub resources naturally.



User question:

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


