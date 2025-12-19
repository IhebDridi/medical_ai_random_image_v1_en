from openai import OpenAI
import streamlit as st


class XAIAssistant:
    """
    Simple LLM wrapper using OpenAI chat completions.
    This replaces the broken Assistants-based implementation.
    """

    def __init__(self, assistant_id=None, image_path=None, survey_data=None):
        # ✅ Initialize OpenAI client using Streamlit secrets
        self.client = OpenAI(
            api_key=st.secrets["openai"]["SECRET_KEY"]
        )

        # ✅ Load system instructions once
        with open("instructions_t.txt", "r", encoding="utf-8") as f:
            self.system_instruction = f.read()

        # ✅ Initialize conversation history with system message
        self.messages = [
            {
                "role": "system",
                "content": self.system_instruction
            }
        ]

        # ✅ Store survey data if provided (not yet injected, but preserved)
        self.survey_data = survey_data if survey_data else {}

        # ✅ Image path kept for compatibility (not uploaded)
        self.image_path = image_path

    def chat(self, msg: str) -> str:
        """
        Send one user message to the LLM and return the assistant reply.
        """

        # ✅ Append user message
        self.messages.append(
            {"role": "user", "content": msg}
        )

        # ✅ Call OpenAI chat completions (this is the proven working logic)
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )

        assistant_text = response.choices[0].message.content

        # ✅ Append assistant response
        self.messages.append(
            {"role": "assistant", "content": assistant_text}
        )

        return assistant_text