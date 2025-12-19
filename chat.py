import streamlit as st
import time
from images import show_images, show_upload_images
from styling import decision_page_styling
from icecream import ic


#@st.dialog("Sind Sie sicher?")
def appointment_dialog():
    with st.popover("End chat"):
        st.markdown("Are you sure?")
        if st.button("Yes"):
            # ✅ DO NOT clear messages here
            st.session_state.conversation_started = False

            # added value to the clicked button
            st.session_state["button_clicked"] = "Yes"

            # ✅ Let the normal page transition trigger saving
            st.session_state["page"] = "thanks"
            st.rerun()

        if st.button("No"):

            # added value to the clicked button
            st.session_state["button_clicked"] = "No"
            st.rerun()


def create_appointment_bttns(): 
    with st.popover('Would you like to make an appointment with a doctor?', use_container_width=True):
        st.button(
            "Yes",
            key="btn1",
            on_click=lambda: st.session_state.update(button_clicked="Make an appointment"),
            use_container_width=True
        )
        st.button(
            "No",
            key="btn2",
            on_click=lambda: st.session_state.update(button_clicked="Do not make appointment"),
            use_container_width=True
        )


def get_assistant_response(prompt: str):
    try:
        return st.session_state.assistant.chat(prompt)
    except Exception as e:
        return (
            "❌ **AI service is currently unavailable**\n\n"
            "This application requires a valid, paid OpenAI API key.\n\n"
            f"**Technical details:** {str(e)}"
        )


def chat_page(): 
    # ---------------------------------
    # Conversation lifecycle flag
    # ---------------------------------
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

    # ---------------------------------
    # Initialize message history once
    # ---------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.subheader("Chat", divider="gray")
    st.markdown(
        "Please read each of the following statements carefully and consider to what degree it has applied to you personally during the past six months."
    )

    # ---------------------------------
    # Initial assistant greeting (ONCE)
    # ---------------------------------
    if not st.session_state.conversation_started:
        with st.chat_message("assistant"):
            st.markdown("Hello! How may I help you?")

    # ---------------------------------
    # Render full chat history
    # ---------------------------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------------------------
    # Chat input
    # ---------------------------------
    if prompt := st.chat_input("Ask a question"):
        st.session_state.conversation_started = True

        # Store and render user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.spinner("One moment, please"):
            assistant_response = get_assistant_response(prompt)

        # Store and render assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    # ---------------------------------
    # End-chat dropdown (popover)
    # ---------------------------------
    if st.session_state.messages or st.session_state.conversation_started:
        appointment_dialog()