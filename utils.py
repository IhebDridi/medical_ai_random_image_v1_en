import re
import json
import streamlit as st
import datetime
import os


def clean_latex_formatting(text: str) -> str:
    # Entfernt alle LaTeX-Mathematik-Umgebungen
    cleaned_text = re.sub(r"\\$", "", text)
    cleaned_text = re.sub(r"\\$", "", cleaned_text)
    return cleaned_text


def save_state_json():
    """
    Saves selected Streamlit session state to a JSON file.
    System prompts and internal configuration are explicitly excluded.
    """
    uuid = st.session_state.get("uuid")
    if not uuid:
        # No UUID → do not save anything
        return

    session_state_dict = {}

    for key, value in st.session_state.items():
        # ❌ NEVER persist assistant objects or system instructions
        if key in ["assistant", "system_instruction"]:
            continue

        # ✅ Filter chat messages: exclude system role content
        if key == "messages" and isinstance(value, list):
            session_state_dict["messages"] = [
                msg for msg in value
                if isinstance(msg, dict) and msg.get("role") != "system"
            ]
            continue

        # ✅ Everything else is stored as string (original behavior)
        try:
            session_state_dict[key] = str(value)
        except Exception:
            # Fallback if something is unserializable
            session_state_dict[key] = "[UNSERIALIZABLE]"

    # ✅ Timestamp for provenance
    session_state_dict["last_updated"] = datetime.datetime.now().isoformat()

    # ✅ Ensure local directory exists
    if not os.path.exists("state_data"):
        os.makedirs("state_data")

    # ✅ Write JSON file
    with open(f"state_data/{uuid}.json", "w", encoding="utf-8") as f:
        json.dump(session_state_dict, f, ensure_ascii=False, indent=2)