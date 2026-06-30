from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings

from openai import OpenAI



def ask_punit_ai(question):


    embeddings = OpenAIEmbeddings()


    db = FAISS.load_local(
        "punit_vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )


    docs = db.similarity_search(
        question,
        k=3
    )


    context=""


    for d in docs:

        context += d.page_content



    client=OpenAI()


    response=client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

        {

        "role":"system",

        "content":
        f"""
        You are Punit AI Learning Assistant.

        Answer only from this knowledge:

        {context}

        If information is missing,
        say it is not available.
        """

        },

        {

        "role":"user",

        "content":question

        }

        ]

    )


    return response.choices[0].message.content