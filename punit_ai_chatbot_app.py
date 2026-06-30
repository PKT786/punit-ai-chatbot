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
# LOGO
# =========================

try:
    st.image(
        "punit_logo.png",
        width=160
    )
except:
    pass


# =========================
# TITLE
# =========================

st.title(
    "🤖 Punit AI Learning Assistant"
)


st.markdown(
"""
## Welcome to Punit AI Assistant 🚀


I can help you with:


📊 Excel formulas & dashboards

🤖 AI tools & ChatGPT

📈 Data Analytics

💻 COBOL, JCL, DB2, CICS, VSAM

📄 Interview preparation PDFs


Ask me anything!
"""
)


st.divider()



# =========================
# QUICK BUTTONS
# =========================

st.subheader(
"Quick Actions"
)


c1,c2,c3,c4,c5 = st.columns(5)


selected_question = ""


with c1:
    if st.button("📊 Excel Help"):
        selected_question = "Give me Excel resources"


with c2:
    if st.button("🤖 AI Tools"):
        selected_question = "Give me AI resources"


with c3:
    if st.button("💻 Mainframe"):
        selected_question = "Give me Mainframe resources"


with c4:
    if st.button("📄 Interview Questions"):
        selected_question = "Give me interview questions PDF"


with c5:
    if st.button("📁 Templates"):
        selected_question = "Give me templates"




# =========================
# GROQ CONFIG
# =========================


try:

    GROQ_KEY = st.secrets["GROQ_API_KEY"]


except:


    st.error(
        "GROQ_API_KEY missing in Streamlit Secrets"
    )

    st.stop()



llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    groq_api_key=GROQ_KEY,

    temperature=0.2

)



# =========================
# RESOURCE LOGIC
# =========================


def get_resource(question):


    q = question.lower()



    # Mainframe

    if any(word in q for word in [

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


COBOL, JCL, DB2, CICS, VSAM
Interview Questions PDF:


https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH

"""



    # Excel


    if any(word in q for word in [

        "excel",
        "formula",
        "pivot",
        "dashboard",
        "chart"

    ]):


        return """

📊 Punit Tech Hub Excel Resources


Excel guides, formulas and learning material:


https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm

"""



    # AI


    if any(word in q for word in [

        "ai",
        "chatgpt",
        "prompt",
        "artificial intelligence"

    ]):


        return """

🤖 Punit Tech Hub AI Resources


AI learning resources:


https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2

"""



    # Templates


    if "template" in q:


        return """

📁 Punit Tech Hub Templates


Download templates:


https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA

"""



    # Resume


    if "resume" in q:


        return """

Create your resume using Punit AI Resume Builder:


https://pth-ai-resume-builder.streamlit.app/

"""



    # Analyzer


    if "analyze" in q:


        return """

Analyze your Excel files:


https://pth-ai-data-analyzer.streamlit.app/

"""



    return None




# =========================
# ANALYTICS
# =========================


def save_log(question, feedback=""):


    file = "chatbot_analytics.csv"


    new_data = pd.DataFrame(

        {

        "Date":[datetime.now()],

        "Question":[question],

        "Feedback":[feedback]

        }

    )


    if os.path.exists(file):


        old = pd.read_csv(file)


        new_data = pd.concat(

            [old,new_data],

            ignore_index=True

        )



    new_data.to_csv(

        file,

        index=False

    )





# =========================
# CHAT
# =========================


question = st.chat_input(

    "Ask your question..."

)



if selected_question:

    question = selected_question




if question:


    st.chat_message(

        "user"

    ).write(question)



    resource = get_resource(question)



    if resource:


        answer = resource



    else:


        prompt = f"""

You are Punit AI Assistant.


Help users with:


Excel

AI

ChatGPT

Data Analytics

Mainframe Technologies


Give simple beginner friendly answers.


User:

{question}

"""


        response = llm.invoke(prompt)


        answer = response.content



    st.chat_message(

        "assistant"

    ).write(answer)



    save_log(question)



    st.divider()


    st.write(

        "Was this helpful?"

    )


    a,b = st.columns(2)



    with a:


        if st.button("👍 Yes"):

            save_log(

                question,

                "Yes"

            )



    with b:


        if st.button("👎 No"):

            save_log(

                question,

                "No"

            )





# =========================
# FOOTER
# =========================


st.divider()


st.caption(

"🚀 Powered by Punit Tech Hub AI | Learn • Implement • Grow"

)
