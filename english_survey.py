import streamlit as st
from tipi import calculate_scores
import json

def submit_survey():
    st.session_state["survey_completed"] = True
    st.session_state["tipi_scores"] = calculate_scores(st.session_state["survey"])
    st.session_state["page"] = "chat"

def survey():
    if "survey" not in st.session_state:
        st.session_state["survey"] = {}

    file_path = "questionarre/english_questionarre_slider.json"

    st.title("Survey")


    questions = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            questions = json.load(file)  # Read JSON file
    except FileNotFoundError:
        st.error("❌ The file was not found. Please check the file path.")
        return
    except json.JSONDecodeError:
        st.error("❌ Error loading JSON file. Please check the file format.")
        return

    # Store responses
    if "responses" not in st.session_state:
        st.session_state["survey"]["responses"] = {}

    options_final = [
      "Strong disapproval",  "Disapproval", "Neutral",  "Approval", "Strong approval"

             ]

    #st.subheader("Fragebogen", divider='gray')
    
    responses= {}
    # with st.form(key="my_form"):
    #     for idx, q in enumerate(questions):
    #         q_key = f"q{idx + 1}"
    #         selected_option = st.select_slider( q["question"], options = options_final, key= q_key, value = "Neutral")
    #         st.session_state["survey"]["responses"][q_key] = selected_option
    #         st.subheader("",divider='gray')
    #         responses[q_key]=selected_option

    with st.form(key="my_form"):
        st.markdown("Please enter your ID")
        uuid = st.text_input("ID", value=st.session_state["survey"].get("ID", ""))
        #age = st.number_input("Alter", value=st.session_state["survey"].get("age", 18), min_value=0, max_value=100)
       # age = st.number_input("Alter", value=st.session_state["survey"].get("age", 18), min_value=0, max_value=100)

        
        st.subheader("",divider='gray')
        st.markdown("Please read each of these statements carefully and consider whether or not it applies to you personally for the last 6 months.")
        st.markdown("")
        #st.subheader("",divider='gray')

        for idx, q in enumerate(questions):
            q_key = f"q{idx + 1}"
            st.markdown(q["question"])
            selected_option = st.radio( q["question"],  options_final,index=None, label_visibility="collapsed")
            st.session_state["survey"]["responses"][q_key] = selected_option
            st.subheader("",divider='gray')
            responses[q_key]=selected_option

        # Submit button
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        
        if uuid == "":
            st.error("Please enter your ID.")

        
        else:
            st.session_state['uuid']=uuid
            st.session_state["survey"]["uuid"] = uuid
            #st.session_state["survey"]["gender"] = gender
            #st.session_state["survey"]["skin_color"] = skin_color
            st.session_state["survey"].update(responses)
            st.session_state["page"] = "chat"
            st.success("Thank you very much for your answers.!")
            #st.write("### Ihre Auswahl:")
        

       

            for idx, q in enumerate(questions):
                selected_options = st.session_state["survey"]["responses"].get(f"q{idx}", [])
                st.write(f"**Q{idx}:** {', '.join(selected_options) if selected_options else 'No option was selected'}")

            st.session_state["page"] = "chat"
            print('Survey Data: ',st.session_state["survey"] )
            st.rerun()
