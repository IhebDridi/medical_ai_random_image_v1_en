import json
from xai_assistant_cls import XAIAssistant
from icecream import ic
import streamlit as st
import os
import datetime
import uuid
from utils import clean_latex_formatting, save_state_json
from welcome import welcome_page
#from survey import survey
from english_survey import survey
from chat import chat_page
from images import get_images
from decision_popover import decision
from thanks import thank_you_page
from config import ASSISTANT_ID
from images import save_upload_images
from sciebo_uploader import Sciebo
from simple_chat_page import simple_chat_page

import llm_test
llm_test.test_llm()


def initialize(image_path):
    if "user_uuid" not in st.session_state:
        user_uuid = str(uuid.uuid4())
        start_time = datetime.datetime.now().isoformat()

        # ✅ FIX: only create assistant once
        if "assistant" not in st.session_state:
            if os.environ.get("SMOKE_TEST"):
                st.session_state["assistant"] = None
            else:
                survey_data = st.session_state.get("survey", {})

                st.session_state["assistant"] = XAIAssistant(
                    assistant_id=ASSISTANT_ID,
                    image_path=image_path,
                    survey_data=survey_data
                )

        assistant = st.session_state["assistant"]
        print(f'Selected Image path during AI intialization: {image_path}')
        if assistant:
            print(f'Assistant object created successfully')

        # Store session metadata
        st.session_state["user_uuid"] = user_uuid
        st.session_state["start_time"] = start_time
        st.session_state["saved_image"] = image_path

        save_state_json()



def main():
    simple_chat_page()
      
      


if __name__ == "__main__":
    main()
