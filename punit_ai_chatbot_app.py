import streamlit as st
from groq import Groq
import pandas as pd
from datetime import datetime
import os


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# API KEY
# -----------------------------

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(
    api_key=GROQ_API_KEY
)



# -----------------------------
# LOGO
# -----------------------------

if os.path.exists("assets/punit_logo.png"):

    st.image(
        "assets/punit_logo.png",
        width=180
    )



# -----------------------------
# TITLE
# -----------------------------

st.title(
    "🤖 Punit AI Learning Assistant"
)


st.markdown(
"""
## Welcome to Punit AI Assistant 🚀

I can help you with:

📊 Excel formulas & dashboards  
🤖 AI tools & prompts  
📈 Data Analytics  
💻 COBOL, JCL, DB2, CICS, VSAM  
📄 Interview preparation PDFs  

Ask me anything!
"""
)


# -----------------------------
# SESSION CHAT HISTORY
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []



# -----------------------------
# ANALYTICS
# -----------------------------

if "analytics" not in st.session_state:

    st.session_state.analytics = []



# -----------------------------
# QUICK BUTTONS
# -----------------------------


st.subheader("🔥 Popular Questions")


col1,col2,col3,col4 = st.columns(4)


questions = [

"Top COBOL interview questions",

"Excel dashboard ideas",

"Best AI prompts",

"Create resume"

]


buttons = [

col1,
col2,
col3,
col4

]


for btn,q in zip(buttons,questions):

    if btn.button(q):

        st.session_state.messages.append(
            {
            "role":"user",
            "content":q
            }
        )



# -----------------------------
# RESOURCE LINKS
# -----------------------------


RESOURCES = {

"mainframe":
"https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH",

"ai":
"https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2",

"excel":
"https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm",

"template":
"https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA"

}



# -----------------------------
# CATEGORY DETECTION
# -----------------------------


def detect_category(text):

    text=text.lower()


    if any(x in text for x in [
        "cobol",
        "jcl",
        "db2",
        "cics",
        "vsam",
        "mainframe"
    ]):

        return "💻 Mainframe",98



    if any(x in text for x in [
        "excel",
        "formula",
        "pivot",
        "dashboard"
    ]):

        return "📊 Excel",97



    if any(x in text for x in [
        "ai",
        "chatgpt",
        "prompt",
        "resume"
    ]):

        return "🤖 AI",96


    return "General",80




# -----------------------------
# SPECIAL REPLIES
# -----------------------------


def special_reply(question):

    q=question.lower()


    if "resume" in q:

        return """

You can use Punit AI Resume Builder 🚀


https://pth-ai-resume-builder.streamlit.app/


"""


    if "analyze excel" in q or "data analyzer" in q:

        return """

Try Punit AI Data Analyzer 📊


https://pth-ai-data-analyzer.streamlit.app/


"""


    if (
        "cobol" in q
        or
        "mainframe" in q
        or
        "jcl" in q
    ):

        return f"""

I recommend these Mainframe resources:

💻 COBOL Interview Questions  
💻 JCL Guides  
💻 Mainframe Learning PDFs


Download:

{RESOURCES["mainframe"]}

"""


    if "excel" in q:

        return f"""

Excel learning resources:

📊 Formulas
📊 Dashboards
📊 Templates


Download:

{RESOURCES["excel"]}

"""


    return None




# -----------------------------
# DISPLAY HISTORY
# -----------------------------


for msg in st.session_state.messages:


    with st.chat_message(msg["role"]):

        st.write(
            msg["content"]
        )




# -----------------------------
# CHAT INPUT
# -----------------------------


prompt = st.chat_input(
    "Ask your question..."
)



if prompt:


    st.session_state.messages.append(
        {
        "role":"user",
        "content":prompt
        }
    )


    category,confidence = detect_category(prompt)



    st.info(
        f"""
Detected Topic:

{category}

Confidence: {confidence}%
"""
    )



    reply = special_reply(prompt)



    if not reply:


        try:


            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[

                {
                "role":"system",

                "content":
                """
You are Punit AI Assistant.
Answer only about:
Excel,
AI,
Data Analytics,
Mainframe technologies.

Promote Punit Tech Hub resources when relevant.
"""
                },

                *st.session_state.messages

                ],

                temperature=0.4

            )


            reply=response.choices[0].message.content



        except Exception as e:


            reply=f"""
AI service error:

{e}
"""



    st.session_state.messages.append(

        {
        "role":"assistant",
        "content":reply
        }

    )


    # analytics

    st.session_state.analytics.append(

        {

        "Date":
        datetime.now(),

        "Question":
        prompt,

        "Category":
        category

        }

    )



    with st.chat_message("assistant"):

        st.write(reply)



# -----------------------------
# RESOURCE NAVIGATION
# -----------------------------


st.divider()


st.subheader(
"Explore Punit Tech Hub"
)



c1,c2,c3 = st.columns(3)


c1.link_button(
"📊 Excel Tutorials",
"https://www.punittechhub.com/excel-tutorials"
)


c2.link_button(
"🤖 AI Resources",
"https://www.punittechhub.com/ai-learning-resources"
)


c3.link_button(
"💻 Mainframe Tutorials",
"https://www.punittechhub.com/mainframe-tutorials"
)



# -----------------------------
# DOWNLOAD ANALYTICS
# -----------------------------


if st.checkbox(
"Show Analytics"
):


    df=pd.DataFrame(
        st.session_state.analytics
    )


    st.dataframe(df)
