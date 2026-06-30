import streamlit as st
import pandas as pd
import os
from datetime import datetime

from langchain_groq import ChatGroq


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Punit AI Assistant",
    page_icon="🤖",
    layout="wide"
)



# =========================
# BRAND HEADER
# =========================

col1, col2 = st.columns([1,5])


with col1:

    logo_path = "assets/punit_logo.png"

    if os.path.exists(logo_path):

        st.image(
            logo_path,
            width=120
        )



with col2:

    st.markdown(
    """
    <h1 style="
    margin-top:25px;
    color:#1F2937;">
    Punit AI Learning Assistant 🤖
    </h1>

    <p style="
    font-size:18px;
    color:#555;">
    Powered by <b>Punit Tech Hub</b>
    </p>

    """,
    unsafe_allow_html=True
    )



st.divider()



# =========================
# WELCOME SECTION
# =========================


st.markdown(
"""
## Welcome to Punit AI Assistant 🚀


I can help you with:


📊 **Excel formulas & dashboards**

🤖 **AI tools & ChatGPT**

📈 **Data Analytics**

💻 **COBOL, JCL, DB2, CICS, VSAM**

📄 **Interview preparation PDFs**


Ask me anything!
"""
)



st.divider()



# =========================
# QUICK ACTIONS
# =========================


st.subheader("Quick Actions")


c1,c2,c3,c4,c5 = st.columns(5)


question=""


with c1:

    if st.button("📊 Excel Help"):

        question="Give me Excel resources"



with c2:

    if st.button("🤖 AI Tools"):

        question="Give me AI resources"



with c3:

    if st.button("💻 Mainframe"):

        question="Give me Mainframe resources"



with c4:

    if st.button("📄 Interview PDFs"):

        question="Give me COBOL interview questions PDF"



with c5:

    if st.button("📁 Templates"):

        question="Give me templates"




# =========================
# GROQ AI
# =========================


if "GROQ_API_KEY" not in st.secrets:

    st.error(
        "Please add GROQ_API_KEY in Streamlit secrets"
    )

    st.stop()



llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    groq_api_key=st.secrets["GROQ_API_KEY"],

    temperature=0.2

)




# =========================
# RESOURCE ENGINE
# =========================


def resource_answer(q):


    q=q.lower()



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

## 💻 Punit Tech Hub Mainframe Resources


COBOL, JCL, DB2, CICS, VSAM PDFs:


📂 Download:

https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH

"""



    elif any(x in q for x in [

        "excel",
        "formula",
        "dashboard",
        "pivot"

    ]):


        return """

## 📊 Punit Tech Hub Excel Resources


Excel formulas, dashboards and templates:


📂 Download:

https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm

"""



    elif any(x in q for x in [

        "ai",
        "chatgpt",
        "prompt"

    ]):


        return """

## 🤖 Punit Tech Hub AI Resources


AI learning resources:


📂 Download:

https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2

"""



    elif "template" in q:


        return """

## 📁 Templates


Download business templates:


📂 Download:

https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA

"""



    elif "resume" in q:


        return """

## 📄 AI Resume Builder


Create your professional resume:


https://pth-ai-resume-builder.streamlit.app/

"""



    elif "analyze" in q:


        return """

## 📈 AI Data Analyzer


Analyze Excel/CSV using AI:


https://pth-ai-data-analyzer.streamlit.app/

"""



    return None




# =========================
# ANALYTICS
# =========================


def save_log(q,feedback=""):


    file="chatbot_analytics.csv"


    data=pd.DataFrame({

        "Date":[datetime.now()],

        "Question":[q],

        "Feedback":[feedback]

    })



    if os.path.exists(file):

        old=pd.read_csv(file)

        data=pd.concat(

            [old,data],

            ignore_index=True

        )



    data.to_csv(

        file,

        index=False

    )





# =========================
# CHAT
# =========================


user_question = st.chat_input(
"Ask your question..."
)



if question:

    user_question=question



if user_question:


    st.chat_message(
        "user"
    ).write(user_question)



    answer = resource_answer(user_question)



    if answer is None:


        response = llm.invoke(

        f"""

You are Punit AI Assistant.

Answer about:

Excel

AI

ChatGPT

Data Analytics

Mainframe


Question:

{user_question}

"""

        )


        answer=response.content



    st.chat_message(
        "assistant"
    ).write(answer)



    save_log(user_question)



    st.divider()


    st.write(
    "Was this helpful?"
    )


    a,b=st.columns(2)


    with a:

        if st.button("👍 Yes"):

            save_log(
                user_question,
                "Yes"
            )



    with b:

        if st.button("👎 No"):

            save_log(
                user_question,
                "No"
            )



# =========================
# FOOTER
# =========================


st.divider()


st.caption(
"🚀 Punit Tech Hub AI | Learn • Implement • Grow"
)
