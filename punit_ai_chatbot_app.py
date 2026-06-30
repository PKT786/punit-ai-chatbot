import streamlit as st
import openai
import re

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="Punit AI Learning Assistant",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------
# CUSTOM CSS
# ---------------------------

st.markdown("""
<style>

.main {
    background-color:#ffffff;
}


.title {
    font-size:42px;
    font-weight:700;
    color:#25283D;
}


.subtitle {
    font-size:18px;
    color:#34495E;
}


.card {

background:#f5f7fb;
padding:20px;
border-radius:15px;
margin-bottom:15px;

}


.topic {

background:#e8f0ff;
padding:6px 12px;
border-radius:20px;
font-size:14px;
font-weight:bold;

}


.chat-user {

background:#eef2f7;
padding:15px;
border-radius:15px;

}


.chat-bot {

background:#fff7e6;
padding:15px;
border-radius:15px;

}

</style>
""", unsafe_allow_html=True)



# ---------------------------
# HEADER
# ---------------------------

st.markdown(
"""
<div class="title">
🤖 Punit AI Learning Assistant
</div>

<div class="subtitle">
Your AI mentor for Excel, Artificial Intelligence, ChatGPT, Data Analytics and Mainframe technologies.
</div>

<br>

""",
unsafe_allow_html=True
)



# ---------------------------
# CAPABILITY CARDS
# ---------------------------


with st.container():

    st.markdown(
    """
    <div class="card">

    <b>I can help you with:</b>

    <br><br>

    📊 <b>Excel</b><br>
    Formulas • Dashboards • Pivot Tables • Automation

    <br><br>

    🤖 <b>AI & ChatGPT</b><br>
    Prompts • AI Tools • Automation

    <br><br>

    🖥 <b>Mainframe</b><br>
    COBOL • JCL • DB2 • CICS

    <br><br>

    📈 <b>Data Analytics</b><br>
    Power BI • Reporting • Visualization

    </div>

    """,
    unsafe_allow_html=True
    )




# ---------------------------
# TOPIC DETECTOR
# ---------------------------


def detect_topic(question):

    q = question.lower()


    if any(word in q for word in
           [
            "excel",
            "formula",
            "pivot",
            "vlookup",
            "dashboard",
            "spreadsheet"
           ]):

        return "📊 Excel"


    elif any(word in q for word in
             [
              "ai",
              "artificial intelligence",
              "chatgpt",
              "prompt",
              "machine learning"
             ]):

        return "🤖 AI / ChatGPT"



    elif any(word in q for word in
             [
              "cobol",
              "jcl",
              "mainframe",
              "db2",
              "cics",
              "vsam"
             ]):

        return "🖥 Mainframe"



    elif any(word in q for word in
             [
              "power bi",
              "analytics",
              "data",
              "visualization"
             ]):

        return "📈 Data Analytics"



    else:

        return "❓ General"



# ---------------------------
# QUICK QUESTIONS
# ---------------------------


st.write("### Try asking:")


col1,col2,col3,col4 = st.columns(4)


if col1.button("Excel Dashboard"):
    question="How to create an Excel dashboard?"


elif col2.button("AI Prompt"):
    question="Create a ChatGPT prompt for resume"


elif col3.button("COBOL"):
    question="Explain COBOL interview questions"


elif col4.button("JCL"):
    question="Explain JCL JOB statement"


else:
    question=None




# ---------------------------
# CHAT HISTORY
# ---------------------------


if "messages" not in st.session_state:

    st.session_state.messages=[]



for msg in st.session_state.messages:

    if msg["role"]=="user":

        st.markdown(
        f"""
        <div class="chat-user">
        👤 {msg['content']}
        </div>
        """,
        unsafe_allow_html=True
        )


    else:

        st.markdown(
        f"""
        <div class="chat-bot">
        🤖 {msg['content']}
        </div>
        """,
        unsafe_allow_html=True
        )



# ---------------------------
# INPUT BOX
# ---------------------------


user_input = st.chat_input(
"Ask your question..."
)



if question:

    user_input=question



if user_input:


    topic = detect_topic(user_input)


    st.session_state.messages.append(
        {
        "role":"user",
        "content":user_input
        }
    )



    # Out of scope

    if topic=="❓ General":


        answer="""

I specialize in:

📊 Excel  
🤖 AI & ChatGPT  
📈 Data Analytics  
🖥 Mainframe


Please ask me something related to these technologies.

"""


    else:


        answer=f"""

<span class="topic">
{topic}
</span>


I detected your question as a **{topic}** topic.


Here is your learning answer:

---

Your question:

**{user_input}**


This topic can be explained with practical examples, tutorials and resources available on Punit Tech Hub.

---

You can also explore related learning resources on:

🌐 https://www.punittechhub.com/all-resources

"""


    st.session_state.messages.append(
        {
        "role":"assistant",
        "content":answer
        }
    )


    st.rerun()
