import streamlit as st
from groq import Groq
import pandas as pd
from datetime import datetime
import os


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Punit AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================
# GROQ SETUP
# ==========================

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


client = Groq(
    api_key=GROQ_API_KEY
)



# ==========================
# RESOURCES
# ==========================


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



# ==========================
# LOGO
# ==========================


if os.path.exists(
    "assets/punit_logo.png"
):

    st.image(
        "assets/punit_logo.png",
        width=220
    )



# ==========================
# HEADER
# ==========================


st.title(
    "🤖 Punit AI Learning Assistant"
)


st.markdown(
"""
## Welcome to Punit AI Assistant 🚀


I can help you with:


📊 Excel formulas & dashboards  


🤖 AI tools & ChatGPT prompts  


📈 Data Analytics  


💻 COBOL, JCL, DB2, CICS, VSAM  


📄 Interview preparation PDFs  


Ask me anything!
"""
)


st.divider()



# ==========================
# SESSION MEMORY
# ==========================


if "messages" not in st.session_state:

    st.session_state.messages=[]



if "analytics" not in st.session_state:

    st.session_state.analytics=[]




# ==========================
# CATEGORY DETECTION
# ==========================


def detect_category(question):

    q=question.lower()


    if any(
        x in q for x in
        [
        "cobol",
        "jcl",
        "db2",
        "cics",
        "vsam",
        "mainframe"
        ]
    ):

        return "💻 Mainframe",98



    elif any(
        x in q for x in
        [
        "excel",
        "formula",
        "pivot",
        "dashboard"
        ]
    ):

        return "📊 Excel",97



    elif any(
        x in q for x in
        [
        "ai",
        "chatgpt",
        "prompt",
        "resume"
        ]
    ):

        return "🤖 AI",96



    return "General",85





# ==========================
# RESOURCE CARDS
# ==========================


def resource_card(
    title,
    desc,
    link
):


    st.info(

f"""

### {title}


{desc}


[📥 Download Resource]({link})

"""

)





# ==========================
# SPECIAL LOGIC
# ==========================


def special_answer(question):

    q=question.lower()



    if "resume" in q:


        return """

You can create your professional resume using:


🚀 Punit AI Resume Builder


https://pth-ai-resume-builder.streamlit.app/


"""



    if (
        "analyze excel" in q
        or
        "data analyzer" in q
    ):


        return """

Try Punit AI Data Analyzer:


📊 Upload Excel/CSV

Get:
✔ Insights
✔ Charts
✔ Summary


https://pth-ai-data-analyzer.streamlit.app/


"""



    if (
        "cobol" in q
        or
        "mainframe" in q
        or
        "jcl" in q
    ):


        return "MAINFRAME_RESOURCE"



    if "excel" in q:


        return "EXCEL_RESOURCE"



    return None





# ==========================
# POPULAR QUESTIONS
# ==========================


st.subheader(
"🔥 Popular Questions"
)



cols = st.columns(5)


popular=[

"Top COBOL interview questions",

"Excel dashboard ideas",

"Best AI prompts",

"Create resume",

"JCL examples"

]


for col,q in zip(cols,popular):


    if col.button(q):

        st.session_state.selected_question=q

        st.rerun()






# ==========================
# DISPLAY CHAT HISTORY
# ==========================


for msg in st.session_state.messages:


    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )





# ==========================
# HANDLE BUTTON QUESTIONS
# ==========================


if "selected_question" in st.session_state:


    prompt = st.session_state.selected_question


    del st.session_state.selected_question



else:


    prompt = st.chat_input(
        "Ask your question..."
    )





# ==========================
# MAIN CHAT ENGINE
# ==========================


if prompt:


    st.session_state.messages.append(

        {
        "role":"user",
        "content":prompt
        }

    )



    category,confidence = detect_category(prompt)



    st.success(

f"""

Detected Topic:

{category}


Confidence:

{confidence}%

"""

)



    answer = special_answer(prompt)



    if answer=="MAINFRAME_RESOURCE":


        resource_card(

        "💻 COBOL / Mainframe Interview Pack",

        """

Includes:

✔ COBOL Questions

✔ JCL Guides

✔ Mainframe Interview Preparation


""",

        RESOURCES["mainframe"]

        )


        answer=""



    elif answer=="EXCEL_RESOURCE":


        resource_card(

        "📊 Excel Learning Resources",

        """

Includes:

✔ Excel Templates

✔ Dashboards

✔ Formulas


""",

        RESOURCES["excel"]

        )


        answer=""



    elif answer is None:


        try:


            result = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[


                {

                "role":"system",

                "content":

                """

You are Punit AI Assistant.

Only answer questions related to:

Excel

AI

Data Analytics

Mainframe


Recommend Punit Tech Hub resources when useful.

"""

                },


                *st.session_state.messages


                ],


                temperature=0.4


            )


            answer=result.choices[0].message.content



        except Exception as e:


            answer=f"""

AI service unavailable.


Error:

{e}

"""



    if answer:


        st.session_state.messages.append(

            {

            "role":"assistant",

            "content":answer

            }

        )



        with st.chat_message(
            "assistant"
        ):

            st.write(answer)




# ==========================
# FEEDBACK
# ==========================


st.divider()


st.write(
"Was this helpful?"
)


c1,c2=st.columns(2)


c1.button(
"👍 Yes"
)


c2.button(
"👎 No"
)





# ==========================
# WEBSITE LINKS
# ==========================


st.divider()


st.subheader(
"🌐 Explore Punit Tech Hub"
)



a,b,c=st.columns(3)



a.link_button(

"📊 Excel Tutorials",

"https://www.punittechhub.com/excel-tutorials"

)



b.link_button(

"🤖 AI Resources",

"https://www.punittechhub.com/all-resources"

)



c.link_button(

"💻 Mainframe Tutorials",

"https://www.punittechhub.com/mainframe-tutorials"

)




# ==========================
# ANALYTICS
# ==========================


st.divider()


if st.checkbox(
"Admin Analytics"
):


    df=pd.DataFrame(

        st.session_state.analytics

    )


    st.dataframe(df)
