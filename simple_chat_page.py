import streamlit as st
from openai import OpenAI

def simple_chat_page():
    st.title("✅ LLM Test Chat (With Instructions)")

    client = OpenAI(api_key=st.secrets["openai"]["SECRET_KEY"])

    # ✅ Load instructions once
    if "system_instruction" not in st.session_state:
        with open("instructions_t.txt", "r", encoding="utf-8") as f:
            st.session_state.system_instruction = f.read()

    # ✅ Initialize message history with system message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": st.session_state.system_instruction
            }
        ]

    # ✅ Render chat history (skip system message in UI)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Say something"):
        # User message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Call LLM
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )

        assistant_text = response.choices[0].message.content

        # Assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_text}
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_text)