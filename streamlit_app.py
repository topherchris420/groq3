import streamlit as st
from typing import Generator
from groq import Groq
import os
from typing import Optional, Dict, Union

# --- Configuration ---
PAGE_TITLE = "Vers3Dynamics DigiDopps™"
PAGE_ICON = "🫂"
IMAGE_PATH = "images/downloadedImage (6).png"
IMAGE_CAPTION = "Groqality is here"
DEFAULT_MODEL_INDEX = 2

# --- Function to get system prompt ---
def _get_system_prompt() -> str:
    """Retrieves the system prompt from 'system_prompt.txt'."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "system_prompt.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"System prompt file not found at: {file_path}")
        st.stop()
    except Exception as e:
        st.error(f"Error reading system prompt file: {e}")
        st.stop()

# --- Initialize Session State ---
if "messages" not in st.session_state:
    system_prompt = _get_system_prompt()
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE)

# --- UI Functions ---
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

def clear_chat_history():
    """Clears chat history and resets to the initial system message."""
    system_prompt = _get_system_prompt()
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.full_response = ""

# --- Model Definitions ---
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# --- Custom CSS ---
st.markdown(
    """
<style>
    /* General app styling */
    body {
        background-color: #f4f4f4; /* Light grey background */
        color: #333; /* Dark grey text */
        font-family: 'Arial', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #007BFF; /* Primary color for headers */
    }

    /* Header link styling */
    h2 a {
        color: #ADD8E6 !important; /* Light blue header link color */
        text-decoration: none;
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .stChatMessage.user {
        background-color: #DCF8C6; /* Light green for user messages */
        color: #333;
        text-align: right; /* Align user messages to the right */
        margin-left: 20%; /* Push user messages to the right */
    }

    .stChatMessage.assistant {
        background-color: #E6E6FA; /* Light lavender for assistant messages */
        color: #333;
        text-align: left; /* Align assistant messages to the left */
        margin-right: 20%; /* Push assistant messages to the left */
    }

    /* Chat input styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #007BFF;
        padding: 15px;
        background-color: #f9f9f9;
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: #f0f2f6; /* Light grey sidebar background */
        padding: 20px;
        border-radius: 10px;
    }
    .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p, .stSidebar label {
        color: #007BFF; /* Sidebar text color */
    }

    /* Button styling */
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3; /* Darker shade on hover */
        color: white;
    }

    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 15px;
        border: 1px solid #007BFF;
    }

    /* Slider styling */
    .stSlider > div > div > div > div[data-baseweb="slider-thumb"] {
        background-color: #007BFF;
    }
    .stSlider > div > div > div > div[data-baseweb="slider-track"] {
        background-color: #ADD8E6; /* Light blue track color */
    }
    .stSlider > div > div > div > div[data-baseweb="slider-thumb"]:hover {
        background-color: #0056b3;
    }

</style>
""",
    unsafe_allow_html=True,
)


# --- Main App Layout ---
icon(PAGE_ICON)
st.markdown(f'<a href="https://vers3dynamics.io/" style="text-decoration:none;"><h2>{PAGE_TITLE}</h2></a>', unsafe_allow_html=True)
st.subheader("Meet Your Wellness Health Companion, Powered by Groq 🌿")
st.sidebar.audio("ElevenLabs_2025-02-16T06_54_38_Amanda_gen_s50_sb75_se0_b_m2.mp3", format="audio/mp3", start_time=0)    
   

# Image and Caption
st.image(IMAGE_PATH, caption=IMAGE_CAPTION, width=200)

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("GROQ_API_KEY not found in secrets. Please ensure it is set.")
    st.stop()
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    st.stop()

# --- Sidebar for Model and Settings ---
with st.sidebar:
    st.header("Model Settings")
    model_option = st.selectbox(
        "Choose your AI Model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=DEFAULT_MODEL_INDEX,
        help="Select the language model to use for the chat."
    )

    if st.session_state.selected_model != model_option:
        clear_chat_history()
        st.session_state.selected_model = model_option

    model_info = models[model_option]
    st.markdown(f"**Model:** {model_info['name']}")
    st.markdown(f"**Developer:** {model_info['developer']}")
    st.markdown(f"**Max Tokens:** {model_info['tokens']}")

    max_tokens_range = model_info["tokens"]
    max_tokens = st.slider(
        "Max Response Tokens:",
        min_value=512,
        max_value=max_tokens_range,
        value=min(2048, max_tokens_range),
        step=512,
        help=f"Control the length of the AI's response. Maximum for {model_info['name']}: {max_tokens_range} tokens."
    )

    if st.button("Clear Chat History", on_click=clear_chat_history, help="Reset the conversation history."):
        st.rerun()

# --- Chat Display Area ---
for message in st.session_state.messages:
    avatar = '👩🏽‍⚕️' if message["role"] == "assistant" else '🧑🏾‍💻'
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"],  unsafe_allow_html=True) # Important for formatted content


# --- Chat Input and Response Generation ---
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Generates chat response content from Groq API streaming."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Hi, I'm Taylor💜 How may I support you today?", key="user_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='🧑🏾‍💻'):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👩🏽‍⚕️"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            chat_completion = client.chat.completions.create(
                model=model_option,
                messages=st.session_state.messages,
                max_tokens=max_tokens,
                stream=True
            )

            response_generator = generate_chat_responses(chat_completion)
            for response_chunk in response_generator:
                full_response += response_chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Oops! An error occurred: {e}. Please try again or select a different model.", icon="🐢🚨")
            full_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})
