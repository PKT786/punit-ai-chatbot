import streamlit as st
from groq import Groq
import os
import pandas as pd
from datetime import datetime


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Punit AI Assistant",
    page_icon="🤖",
    layout="wide"
)



# =========================
# GROQ
# =========================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)



# =========================
# SESSION
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []



if "analytics" not in st.session_state:

    st.session_state.analytics = []



# =========================
# HEADER
# =========================


if os.path.exists("assets/punit_logo.png"):

    st.image(
        "assets/punit_logo.png",
        width=160
    )


st.title(
    "🤖 Punit AI Learning Assistant"
)


st.markdown(
"""
### Welcome to Punit AI Assistant 🚀


I can help you with:

📊 Excel formulas & dashboards

🤖 AI tools & ChatGPT

📈 Data Analytics

💻 COBOL, JCL, DB2, CICS, VSAM

📄 Interview preparation PDFs

"""
)



# =========================
# RESOURCE LINKS
# =========================


mainframe_link = (
"https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH"
)


excel_link = (
"https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm"
)


ai_link = (
"https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2"
)


template_link = (
"https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA"
)



# =========================
# CATEGORY
# =========================


def category_detect(text):

    t=text.lower()


    if any(x in t for x in [
        "cobol",
        "jcl",
        "db2",
        "cics",
        "vsam",
        "mainframe"
    ]):

        return "💻 Mainframe",98


    if any(x in t for x in [
        "excel",
        "formula",
        "dashboard"
    ]):

        return "📊 Excel",97


    if any(x in t for x in [
        "ai",
        "chatgpt",
        "prompt",
        "resume"
    ]):

        return "🤖 AI",96


    return "General",80




# =========================
# SPECIAL RESPONSES
# =========================


def resource_response(q):

    q=q.lower()


    if "resume" in q:

        return """

Use Punit AI Resume Builder:

https://pth-ai-resume-builder.streamlit.app/

"""


    if "data analyzer" in q:

        return """

Use Punit AI Data Analyzer:

https://pth-ai-data-analyzer.streamlit.app/

"""


    if "cobol" in q or "mainframe" in q or "jcl" in q:

        return f"""

💻 COBOL / Mainframe Resources


Includes:

✔ Interview Questions

✔ JCL Guides

✔ Mainframe PDFs


Download:

{mainframe_link}

"""



    if "excel" in q:

        return f"""

📊 Excel Resources


Includes:

✔ Templates

✔ Dashboards

✔ Formula Guides


Download:

{excel_link}

"""


    return None





# =========================
# POPULAR QUESTIONS
# =========================


st.subheader(
"🔥 Popular Questions"
)



buttons = [

"Top COBOL interview questions",

"Excel dashboard ideas",

"Best AI prompts",

"Create resume"

]


cols = st.columns(4)


clicked_question=None


for c,q in zip(cols,buttons):

    if c.button(q):

        clicked_question=q




# =========================
# USER INPUT
# =========================


if clicked_question:

    user_input=clicked_question


else:

    user_input=st.chat_input(
        "Ask me anything..."
    )




# =========================
# PROCESS QUESTION
# =========================


if user_input:


    st.session_state.messages.append(

        {
        "role":"user",
        "content":user_input
        }

    )


    topic,score = category_detect(user_input)


    st.info(
f"""
Detected Topic:

{topic}

Confidence:

{score}%

"""
)



    answer = resource_response(user_input)



    if not answer:


        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

            {
            "role":"system",

            "content":
            """
You are Punit AI Assistant.

Help users with:

Excel

AI

Data Analytics

Mainframe

Give practical answers.
"""
            },

            *st.session_state.messages

            ]

        )


        answer=response.choices[0].message.content




    st.session_state.messages.append(

        {
        "role":"assistant",
        "content":answer
        }

    )



    st.session_state.analytics.append(

        {

        "time":datetime.now(),

        "question":user_input,

        "topic":topic

        }

    )



# =========================
# CHAT DISPLAY
# =========================


for m in st.session_state.messages:


    with st.chat_message(
        m["role"]
    ):

        st.write(
            m["content"]
        )



# =========================
# RESOURCES
# =========================


st.divider()


st.subheader(
"🌐 Explore Punit Tech Hub"
)


c1,c2,c3=st.columns(3)



c1.link_button(

"📊 Excel",

"https://www.punittechhub.com/excel-tutorials"

)



c2.link_button(

"🤖 AI",

"https://www.punittechhub.com/ai-learning-resources"

)



c3.link_button(

"💻 Mainframe",

"https://www.punittechhub.com/mainframe-tutorials"

)



# =========================
# ANALYTICS
# =========================


if st.checkbox(
"Show Analytics"
):

    st.dataframe(

        pd.DataFrame(
            st.session_state.analytics
        )

    )
