import streamlit as st
from openai import OpenAI

def simple_chat_page():
    st.title("✅ LLM Test Chat (Baseline)")

    client = OpenAI(api_key=st.secrets["openai"]["SECRET_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Say something"):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )

        assistant_text = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_text}
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_text)