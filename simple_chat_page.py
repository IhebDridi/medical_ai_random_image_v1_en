import streamlit as st
from openai import OpenAI
from PIL import Image


def simple_chat_page():
    # --------------------------------------------------
    # Page title / branding
    # --------------------------------------------------
    st.title("XAI Skin Assistant (Test Mode)")

    client = OpenAI(api_key=st.secrets["openai"]["SECRET_KEY"])

    # --------------------------------------------------
    # Image display (read-only, no OpenAI upload)
    # --------------------------------------------------
    image_path = st.session_state.get(
        "saved_image",
        "skin_images/05ec667cfd8a73d9d51b341af2ca9dc1.jpg"
    )

    try:
        image = Image.open(image_path)
        st.image(image, caption="Skin image used for assessment", width=300)
    except Exception:
        st.info("No image available.")

    st.divider()

    # --------------------------------------------------
    # Load system instructions once
    # --------------------------------------------------
    if "system_instruction" not in st.session_state:
        with open("instructions_t.txt", "r", encoding="utf-8") as f:
            st.session_state.system_instruction = f.read()

    # --------------------------------------------------
    # Initialize messages (system message only once)
    # --------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": st.session_state.system_instruction
            }
        ]

    # --------------------------------------------------
    # Display chat history (skip system message)
    # --------------------------------------------------
    st.subheader("Chat", divider="gray")

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # --------------------------------------------------
    # Chat input and model call
    # --------------------------------------------------
    if prompt := st.chat_input("Ask a question about the skin image"):
        # User message
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

    st.divider()

    # --------------------------------------------------
    # Decision UI (appointment choice)
    # --------------------------------------------------
    st.subheader("Next step")

    col1, col2 = st.columns(2)

    if "decision" not in st.session_state:
        st.session_state.decision = None

    with col1:
        if st.button("✅ Make an appointment"):
            st.session_state.decision = "Make appointment"

    with col2:
        if st.button("❌ Do not make an appointment"):
            st.session_state.decision = "Do not make appointment"

    if st.session_state.decision:
        st.success(f"Your decision: {st.session_state.decision}")