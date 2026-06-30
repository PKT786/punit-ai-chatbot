import streamlit as st
import pandas as pd
import os
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Punit AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================
# API KEY
# ==========================

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


# ==========================
# BRANDING
# ==========================

st.image(
    "punit_logo.png",
    width=180
)


st.title("🤖 Punit AI Learning Assistant")

st.markdown(
"""
### Welcome to Punit AI Assistant 🚀


I can help you with:


📊 Excel formulas & dashboards

🤖 AI tools & prompts

📈 Data Analytics

💻 COBOL, JCL, DB2, CICS, VSAM

📄 Interview preparation PDFs


Ask me anything!
"""
)


# ==========================
# QUICK BUTTONS
# ==========================


st.subheader("Quick Actions")


col1,col2,col3,col4,col5 = st.columns(5)


quick_question=""


with col1:
    if st.button("📊 Excel Help"):
        quick_question="Give me Excel help"


with col2:
    if st.button("🤖 AI Tools"):
        quick_question="Show me AI resources"


with col3:
    if st.button("💻 Mainframe"):
        quick_question="Give me Mainframe learning resources"


with col4:
    if st.button("📄 Interview Questions"):
        quick_question="Give me interview questions"


with col5:
    if st.button("📁 Download Resources"):
        quick_question="Give me resource links"



# ==========================
# RESOURCE ROUTER
# ==========================


def resource_logic(question):

    q = question.lower()


    if any(x in q for x in [
        "cobol",
        "jcl",
        "db2",
        "cics",
        "vsam",
        "mainframe",
        "interview"
    ]):


        return """

📘 Punit Tech Hub Mainframe Resources


You can find COBOL, JCL, DB2,
CICS, VSAM and interview PDFs here:


https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH


"""


    if any(x in q for x in [
        "excel",
        "formula",
        "dashboard",
        "pivot",
        "chart"
    ]):


        return """

📊 Punit Tech Hub Excel Resources


Download Excel templates and guides:


https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm


"""


    if any(x in q for x in [
        "ai",
        "chatgpt",
        "prompt"
    ]):


        return """

🤖 Punit Tech Hub AI Resources


Explore AI resources:


https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2


"""


    if "template" in q:


        return """

📁 Punit Tech Hub Templates


Download templates:


https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA


"""


    if "resume" in q:


        return """

Create your resume using:


https://pth-ai-resume-builder.streamlit.app/


"""


    if "analyze" in q:


        return """

Analyze your Excel file using:


https://pth-ai-data-analyzer.streamlit.app/


"""


    return None



# ==========================
# ANALYTICS
# ==========================


def save_analytics(question,category,feedback=""):


    file="chatbot_analytics.csv"


    data={
        "Date":[datetime.now()],
        "Question":[question],
        "Category":[category],
        "Feedback":[feedback]
    }


    df=pd.DataFrame(data)


    if os.path.exists(file):

        old=pd.read_csv(file)

        df=pd.concat(
            [old,df],
            ignore_index=True
        )


    df.to_csv(file,index=False)



# ==========================
# GEMINI
# ==========================


llm=ChatGoogleGenerativeAI(

    model="gemini-2.0-flash",

    google_api_key=GOOGLE_API_KEY

)



# ==========================
# CHAT INPUT
# ==========================


question=st.chat_input(
"Ask your question..."
)


if quick_question:

    question=quick_question



if question:


    st.chat_message("user").write(question)



    resource=resource_logic(question)



    if resource:


        answer=resource


    else:


        prompt=f"""


You are Punit AI Assistant.


Answer only related to:

Excel
AI
Data Analytics
Mainframe


User question:

{question}


Give practical answer.

"""


        answer=llm.invoke(prompt).content



    st.chat_message("assistant").write(answer)



    save_analytics(
        question,
        "Auto"
    )



    st.divider()


    st.write("Was this helpful?")


    c1,c2=st.columns(2)


    with c1:

        if st.button("👍 Yes"):

            save_analytics(
                question,
                "Feedback",
                "Yes"
            )


    with c2:

        if st.button("👎 No"):

            save_analytics(
                question,
                "Feedback",
                "No"
            )



# ==========================
# FOOTER
# ==========================


st.markdown(
"""
---

🚀 Powered by **Punit Tech Hub AI**

Excel • AI • Data Analytics • Mainframe

Learn • Implement • Grow

"""
)
