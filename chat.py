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
            st.session_state["button_clicked"] = "Yes"
            print("Button Clicked")
            st.write(f"You decided for: {st.session_state['button_clicked']}")
            st.session_state["page"] = "thanks"
            st.rerun()
        
        if st.button("No"):
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
            "This application requires a **valid, paid OpenAI API key** "
            "with permission to use the Assistants API and read messages.\n\n"
            "Without such an API key, the chatbot cannot function.\n\n"
            f"**Technical details:** {str(e)}"
        )


def chat_page():
    st.subheader("Chat", divider="gray")
    st.markdown(
        "Please read each of these statements carefully and consider whether or not it applies to you personally for the last 6 months."
    )

    # ✅ Initialize messages ONCE
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ✅ Render ALL previous messages EVERY run
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ Static greeting (UI-only, stays fixed)
    with st.chat_message("assistant"):
        st.markdown("Hello! How may I help you?")

    # ✅ User input
    if prompt := st.chat_input("Ask a question"):
        # Store user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Immediately render user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.spinner("One moment, please"):
            assistant_response = get_assistant_response(prompt)

        # Store assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_response
        })

        # Render assistant message
        with st.chat_message("assistant"):
            st.markdown(assistant_response)