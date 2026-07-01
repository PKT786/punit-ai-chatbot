import streamlit as st
import os
import csv
from datetime import datetime
from PIL import Image
import google.generativeai as genai


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Punit AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# GEMINI CONFIG
# -----------------------------

API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=API_KEY)


model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# -----------------------------
# LOGO
# -----------------------------

logo_path = "assets/punit_logo.png"

if os.path.exists(logo_path):

    logo = Image.open(logo_path)

    st.image(
        logo,
        width=180
    )


# -----------------------------
# TITLE
# -----------------------------

st.markdown(
"""
# 🤖 Punit AI Learning Assistant

Your personal guide for:

📊 Excel  
🤖 Artificial Intelligence  
📈 Data Analytics  
💻 Mainframe Technologies  

Powered by **Punit Tech Hub**
"""
)


# -----------------------------
# RESOURCE LINKS
# -----------------------------

RESOURCES = {


"Mainframe":

{
"title":"💻 COBOL Interview Pack",

"description":
"""
✔ COBOL Interview Questions
✔ Real project scenarios
✔ Mainframe preparation
""",

"link":
"https://drive.google.com/drive/u/1/folders/141O87AxooUedcZ5jFHGM5nCB1wxtYYH"

},



"Excel":

{
"title":"📊 Excel Templates & Guides",

"description":
"""
✔ Excel dashboards
✔ Formula guides
✔ Business templates
""",

"link":
"https://drive.google.com/drive/u/1/folders/1CwQI4hcSuZOxnweWI25GqjCAAhOy0gOm"

},



"AI":

{
"title":"🤖 AI Learning Resources",

"description":
"""
✔ AI tools
✔ ChatGPT prompts
✔ Productivity resources
""",

"link":
"https://drive.google.com/drive/u/1/folders/1yFvmGPKl5O22t9XoY2WWGXokyi2Q6OP2"

},



"Templates":

{
"title":"📁 Premium Templates",

"description":
"""
✔ Ready to use files
✔ Business templates
✔ Productivity sheets
""",

"link":
"https://drive.google.com/drive/u/1/folders/1Iww2a-kGPZagXyoBHr-qGkDCuFP5poaA"

}


}



# -----------------------------
# POPULAR QUESTIONS
# -----------------------------


st.subheader("🔥 Popular Questions")


popular = [

"Give me COBOL interview questions",

"Explain Excel VLOOKUP",

"Best AI prompts",

"How to create JCL job?",

"Create resume"

]


cols = st.columns(5)


for i,q in enumerate(popular):

    if cols[i].button(q):

        st.session_state.messages.append(
            {
            "role":"user",
            "content":q
            }
        )

        st.rerun()



# -----------------------------
# SESSION CHAT MEMORY
# -----------------------------


if "messages" not in st.session_state:

    st.session_state.messages=[]



# -----------------------------
# CATEGORY DETECTION
# -----------------------------


def detect_category(question):

    q = question.lower()


    if any(x in q for x in [
        "cobol",
        "jcl",
        "db2",
        "cics",
        "vsam",
        "mainframe"
    ]):

        return "💻 Mainframe",98



    if any(x in q for x in [
        "excel",
        "formula",
        "pivot",
        "dashboard"
    ]):

        return "📊 Excel",97



    if any(x in q for x in [
        "ai",
        "chatgpt",
        "prompt",
        "resume"
    ]):

        return "🤖 AI",96



    return "General",80




# -----------------------------
# ANALYTICS
# -----------------------------


def save_analytics(question,category):


    file="chatbot_analytics.csv"


    exists=os.path.exists(file)


    with open(
        file,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:


        writer=csv.writer(f)


        if not exists:

            writer.writerow(
            [
            "Date",
            "Question",
            "Category"
            ]
            )


        writer.writerow(
        [
        datetime.now(),
        question,
        category
        ]
        )





# -----------------------------
# DISPLAY CHAT
# -----------------------------


for msg in st.session_state.messages:


    if msg["role"]=="user":

        st.chat_message(
            "user"
        ).write(
            msg["content"]
        )


    else:

        st.chat_message(
            "assistant"
        ).write(
            msg["content"]
        )





# -----------------------------
# USER INPUT
# -----------------------------


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


    category,confidence = detect_category(question)



    save_analytics(
        question,
        category
    )


    st.info(
    f"""
Detected Topic:

{category}

Confidence:
{confidence}%
"""
    )



    # -------------------------
    # SPECIAL LINKS
    # -------------------------


    if "resume" in question.lower():

        answer="""

You can use Punit AI Resume Builder:

https://pth-ai-resume-builder.streamlit.app/

"""


    elif "analyze excel" in question.lower():

        answer="""

Try Punit AI Data Analyzer:

https://pth-ai-data-analyzer.streamlit.app/

"""


    else:


        prompt=f"""

You are Punit AI Assistant.

Answer user query related to:

Excel,
AI,
Data Analytics,
Mainframe.

Question:

{question}

Give practical answers.
"""


        try:

            response=model.generate_content(
                prompt
            )

            answer=response.text


        except Exception as e:


            answer=f"""
AI service temporarily unavailable.

{str(e)}
"""





    st.session_state.messages.append(
    {
    "role":"assistant",
    "content":answer
    }
    )



    st.rerun()



# -----------------------------
# RESOURCE CARDS
# -----------------------------


st.divider()


st.subheader(
"📚 Explore Punit Tech Hub Resources"
)



cols=st.columns(4)



for i,(name,data) in enumerate(RESOURCES.items()):


    with cols[i]:

        st.markdown(
        f"""
### {data['title']}


{data['description']}


"""
        )


        st.link_button(
            "Download Resource",
            data["link"]
        )



# -----------------------------
# WEBSITE NAVIGATION
# -----------------------------


st.divider()


st.subheader(
"🌐 Explore Punit Tech Hub"
)


st.markdown(
"""
📊 Excel Tutorials  
🤖 AI Resources  
💻 Mainframe Tutorials  

Visit:

https://www.punittechhub.com/all-resources

"""
)



# -----------------------------
# FEEDBACK
# -----------------------------


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
