import streamlit as st
import openai
import os
import json
import datetime
import uuid
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    filename='error_logging.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
)

# Page config
st.set_page_config(
    page_title="Akash Network Chat",
    layout="wide"
)

# Initialize session state for API key
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get('AKASH_API_KEY', '')

def load_chat_history() -> Dict[str, Any]:
    """Load chat history from JSON file or create new if not exists."""
    try:
        if os.path.exists('chat_history.json'):
            with open('chat_history.json', 'r') as f:
                return json.load(f)
        return {"interactions": []}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse chat history: {str(e)}")
        return {"interactions": []}
    except Exception as e:
        logging.error(f"Unexpected error loading chat history: {str(e)}")
        return {"interactions": []}

def save_interaction(user_prompt: str, llm_response: str, model: str, processing_time: float) -> None:
    """Save a chat interaction to JSON file."""
    try:
        history = load_chat_history()
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_prompt": user_prompt,
            "llm_response": llm_response,
            "llm_model": model,
            "processing_time": processing_time,
            "session_id": str(uuid.uuid4())
        }
        history["interactions"].append(interaction)
        
        with open('chat_history.json', 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save interaction: {str(e)}")
        st.error(f"Failed to save chat history: {str(e)}")

def get_llm_response(prompt: str, api_key: str) -> tuple[str, str, float]:
    """Get response from LLM API and measure processing time."""
    start_time = datetime.datetime.now()
    
    try:
        if not api_key:
            raise ValueError("AKASH_API_KEY is not set")

        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://chatapi.akash.network/api/v1"
        )

        model = "Meta-Llama-3-1-8B-Instruct-FP8"
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        processing_time = (datetime.datetime.now() - start_time).total_seconds()
        return response.choices[0].message.content, model, processing_time

    except ValueError as ve:
        logging.error(f"Configuration error: {str(ve)}")
        raise
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in LLM response: {str(e)}")
        raise

# API Key input at the top
if not st.session_state.api_key:
    st.warning("AKASH_API_KEY not found in environment variables")
    api_key_input = st.text_input("Enter your Akash API Key:", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("API Key saved in session!")
else:
    st.success("Using API Key from environment")

# User input always at top
user_input = st.text_input("Enter your question:", key="user_input")

# Process user input
if user_input:
    try:
        response_text, model, proc_time = get_llm_response(user_input, st.session_state.api_key)
        st.write("Response:", response_text)
        save_interaction(user_input, response_text, model, proc_time)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Create tabs
readme_tab, source_tab, errors_tab, json_tab = st.tabs([
    "README", "Source Code", "Errors", "JSON History"
])

# README Tab
with readme_tab:
    try:
        with open("README.md", "r") as f:
            st.markdown(f.read())
    except Exception as e:
        st.error(f"Error loading README: {str(e)}")

# Source Code Tab
with source_tab:
    try:
        with open("main.py", "r") as f:
            st.code(f.read(), language="python")
    except Exception as e:
        st.error(f"Error loading source code: {str(e)}")

# Errors Tab
with errors_tab:
    try:
        with open("error_logging.log", "r") as f:
            st.code(f.read(), language="text")
    except Exception as e:
        st.error(f"Error loading error log: {str(e)}")

# JSON History Tab
with json_tab:
    try:
        history = load_chat_history()
        st.json(history)
    except Exception as e:
        st.error(f"Error loading chat history: {str(e)}")
