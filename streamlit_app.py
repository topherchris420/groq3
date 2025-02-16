import streamlit as st
from typing import Generator
from groq import Groq
import os
from typing import Optional, Dict, Union
import random

# --- Configuration ---
PAGE_TITLE = "Speak with Mnemosyne"
PAGE_ICON = "🫂"
IMAGE_PATH = "images/downloadedImage (6).png"
IMAGE_CAPTION = "Developed by Vers3Dynamics"
DEFAULT_MODEL_INDEX = 2

# Add animated loading messages
LOADING_MESSAGES = [
    "Thinking deeply about your question... 🤔",
    "Processing with care... 💭",
    "Analyzing your request... 📊",
    "Crafting a thoughtful response... ✨",
    "Computing with compassion... 💝"
]

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
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0

# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE)

# --- Custom CSS with Enhanced Styling ---
st.markdown(
    """
<style>
    /* Modern App Styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
        padding: 2rem;
    }
    
    /* Animated Header */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .stApp > header {
        background: linear-gradient(-45deg, #007BFF, #00A3FF, #00C6FF, #00E1FF);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 1rem;
        border-radius: 0 0 20px 20px;
    }
    
    /* Enhanced Chat Messages */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
    }
    
    .stChatMessage.user {
        background: linear-gradient(135deg, #DCF8C6 0%, #B4E6A1 100%);
        margin-left: 25%;
    }
    
    .stChatMessage.assistant {
        background: linear-gradient(135deg, #E6E6FA 0%, #C5C5F5 100%);
        margin-right: 25%;
    }
    
    /* Animated Input Box */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(45deg, #007BFF, #00E1FF) border-box;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.3);
        transform: scale(1.01);
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f0f2f6 0%, #e6e9ef 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Glowing Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #007BFF, #00A3FF);
        color: white;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
    }
    
    /* Enhanced Slider */
    .stSlider {
        padding: 1rem 0;
    }
    
    .stSlider > div > div > div > div[data-baseweb="slider-thumb"] {
        background: linear-gradient(45deg, #007BFF, #00A3FF);
        box-shadow: 0 2px 10px rgba(0, 123, 255, 0.3);
    }
    
    /* Progress Animation */
    @keyframes pulse {
        0% {opacity: 0.6;}
        50% {opacity: 1;}
        100% {opacity: 0.6;}
    }
    
    .progress-message {
        animation: pulse 2s infinite ease-in-out;
        color: #007BFF;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- UI Functions with Animations ---
def display_welcome_message():
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%); 
                    border-radius: 20px; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h1 style='color: #007BFF; margin-bottom: 1rem;'>Welcome to DigiDopps™ 🌟</h1>
            <p style='font-size: 1.2rem; color: #555;'>Your AI-powered wellness companion is here to support your journey to better health.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_chat_tips():
    if st.session_state.chat_counter == 0:
        st.info("""
        💡 **Quick Tips:**
        - Be specific with your health-related questions
        - Share relevant context for better assistance
        - Ask follow-up questions for clarity
        """)

# --- Main App Layout ---
st.markdown(f'<a href="https://vers3dynamics.io/" style="text-decoration:none;"><h2>{PAGE_TITLE}</h2></a>', unsafe_allow_html=True)
display_welcome_message()

# Sidebar with Enhanced UI
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='color: #007BFF;'>🎯 Customize Your Experience</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Model Selection with Visual Feedback
    model_option = st.selectbox(
        "Choose your AI Model:",
        options=list(models.keys()),
        format_func=lambda x: f"🤖 {models[x]['name']}",
        index=DEFAULT_MODEL_INDEX,
        help="Select the language model to use for the chat."
    )

    if st.session_state.selected_model != model_option:
        clear_chat_history()
        st.session_state.selected_model = model_option

    # Model Information Card
    model_info = models[model_option]
    st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #007BFF; margin-bottom: 0.5rem;'>Model Details</h3>
            <p><strong>🔮 Model:</strong> {model_info['name']}</p>
            <p><strong>🏢 Developer:</strong> {model_info['developer']}</p>
            <p><strong>📊 Max Tokens:</strong> {model_info['tokens']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Enhanced Audio Player
    st.markdown("""
        <div style='background: white; padding: 1rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-top: 1rem;'>
            <h3 style='color: #007BFF; margin-bottom: 0.5rem;'>🎵 Welcome Message</h3>
    """, unsafe_allow_html=True)
    st.audio("ElevenLabs_2025-02-16T06_54_38_Amanda_gen_s50_sb75_se0_b_m2.mp3", format="audio/mp3", start_time=0)

# Chat Interface
display_chat_tips()

for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = '👩🏽‍⚕️' if message["role"] == "assistant" else '🧑🏾‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"], unsafe_allow_html=True)

# Enhanced Chat Input and Response Generation
if prompt := st.chat_input("Hello, I'm  Mnemosyne💜 How may I support you today?", key="user_input"):
    st.session_state.chat_counter += 1
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='🧑🏾‍💻'):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👩🏽‍⚕️"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Display random loading message
            loading_message = random.choice(LOADING_MESSAGES)
            message_placeholder.markdown(f"<div class='progress-message'>{loading_message}</div>", unsafe_allow_html=True)

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
  );
};

export default WellnessChat;
