import streamlit as st
def welcome_page():
    st.title("Welcome!")
    st.markdown("""
    This app allows you to obtain an initial assessment of conspicuous skin changes and, based on this, decide whether you would like to make an appointment with a doctor.

    **How it works:**
    1. **Complete the questionnaire on the following page** – This allows the interaction with the artificial intelligence assistant to be better tailored to your needs. 
    \n
    2. **Uploaded photo** -  Take a close look at a picture of your noticeable skin area.
    \n
    3. **Chat with the AI assistant** – Interact with the artificial intelligence assistant and decide whether you would like to make a doctor's appointment based on the conversation.
    """)
    if st.button("To the questionnaire"):
        st.session_state["page"] = "survey"
        st.rerun()