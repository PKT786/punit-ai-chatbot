import streamlit as st
import requests
from bs4 import BeautifulSoup

from langchain_groq import ChatGroq



# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(

    page_title="Punit AI Learning Assistant",

    page_icon="🤖",

    layout="wide"

)



# =====================================
# GEMINI API KEY
# =====================================


try:

    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except:


    st.error(
        "Gemini API Key not found. Add GROQ_API_KEY in Streamlit Secrets."
    )

    st.stop()



# =====================================
# GEMINI MODEL
# =====================================


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    groq_api_key=GROQ_API_KEY,

    temperature=0.2

)




# =====================================
# PUNIT TECH HUB RESOURCES
# =====================================


RESOURCE_LINKS = [

"https://www.punittechhub.com/all-resources",

"https://www.punittechhub.com/excel-tutorials",

"https://www.punittechhub.com/mainframe-tutorials",

"https://www.punittechhub.com/cobol-tutorials",

"https://www.punittechhub.com/jcl-tutorials",

"https://www.punittechhub.com/db2-tutorials",

"https://www.punittechhub.com/cics-tutorials",

"https://www.punittechhub.com/vsam-tutorials",

"https://www.punittechhub.com/mainframe-interview-questions",

"https://www.punittechhub.com/excel-formulas-guide",

"https://www.punittechhub.com/data-analysis-tutorials",

"https://www.punittechhub.com/excel-charts-tutorials",

"https://www.punittechhub.com/advanced-excel-tutorials"

]





# =====================================
# LOAD WEBSITE CONTENT
# =====================================


@st.cache_data(ttl=86400)


def get_website_content():


    all_content = ""


    for url in RESOURCE_LINKS:


        try:


            response = requests.get(

                url,

                timeout=10

            )


            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )


            text = soup.get_text(

                separator=" "

            )


            all_content += "\n\n" + text



        except Exception:


            continue



    # Gemini free limit safe

    return all_content[:6000]





knowledge = get_website_content()





# =====================================
# HEADER
# =====================================


st.title(
"🤖 Punit AI Learning Assistant"
)


st.write(

"""
Ask anything about:

📊 Excel  
🤖 AI / ChatGPT  
📈 Data Analysis  
💻 Mainframe  
📝 COBOL  
⚙️ JCL  
🗄️ DB2  
📂 CICS  
📁 VSAM  

Powered by Punit Tech Hub resources.
"""

)





# =====================================
# CHAT MEMORY
# =====================================


if "messages" not in st.session_state:

    st.session_state.messages=[]




for message in st.session_state.messages:


    with st.chat_message(

        message["role"]

    ):

        st.write(

            message["content"]

        )





# =====================================
# USER QUESTION
# =====================================


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



    prompt = f"""

You are Punit AI Learning Assistant.

Your job is to answer users related to:

- Excel
- Microsoft Excel formulas
- Data Analysis
- AI
- ChatGPT
- Generative AI
- Mainframe
- COBOL
- JCL
- DB2
- CICS
- VSAM


Use this Punit Tech Hub knowledge:


{knowledge}



User Question:

{question}



Instructions:

1. Give simple beginner friendly explanation.

2. Add examples where useful.

3. If related resource exists mention:

https://www.punittechhub.com/all-resources


4. If information is not available say:

"I could not find this topic in Punit Tech Hub resources."

"""


    with st.chat_message("assistant"):


        with st.spinner(

            "Thinking..."

        ):


            try:


                response = llm.invoke(

                    prompt

                )


                answer = response.content



                st.write(answer)



                st.markdown(

                """

                ---

                📚 Explore more:

                https://www.punittechhub.com/all-resources

                """

                )



            except Exception as e:


                answer = (

                    "Sorry, AI service is temporarily unavailable."

                )


                st.error(

                    str(e)

                )


                st.write(answer)




    st.session_state.messages.append(

        {

            "role":"assistant",

            "content":answer

        }

    )
