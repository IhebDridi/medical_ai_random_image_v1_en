from openai import OpenAI
import streamlit as st


OPENAI_API_KEY = st.secrets["openai"]["SECRET_KEY"]

# Use exactly the same way you load your key elsewhere
# If you use st.secrets, temporarily paste the key directly for this test
client = OpenAI(api_key=OPENAI_API_KEY)

def test_llm():
    print("SENDING REQUEST TO OPENAI...")

    response = client.responses.create(
        model="gpt-4o",
        input="Say hello and explain in one sentence what you can do."
    )

    print("RAW RESPONSE OBJECT:")
    print(response)

    print("\nEXTRACTED TEXT:")
    print(response.output_text)

if __name__ == "__main__":
    test_llm()