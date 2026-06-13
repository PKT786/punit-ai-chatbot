import streamlit as st
st.set_page_config(
    page_title="Punit AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.set_page_config(page_title="Punit AI Assistant", page_icon="🤖")

st.title("🤖 Punit AI Learning Assistant")
st.write("Ask questions about Excel, AI, ChatGPT and Mainframe.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask your question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    text = question.lower()

    if "excel" in text:
        reply = "I can help with Excel formulas, dashboards, Pivot Tables and automation."
    elif "ai" in text or "chatgpt" in text:
        reply = "I can explain AI concepts, ChatGPT, prompts and AI projects."
    elif "mainframe" in text:
        reply = "I can help with COBOL, JCL, DB2 and Mainframe interview preparation."
    else:
        reply = "Please ask me about Excel, AI, ChatGPT or Mainframe learning."

    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
