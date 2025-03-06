import streamlit as st
from typing import Generator, Optional, Dict, Union
from groq import Groq
import os
import random
from pathlib import Path
import time

# --- Configuration ---
PAGE_TITLE = "Vers3Dynamics"
PAGE_ICON = "👩‍⚕️" 
IMAGE_PATH = os.path.join("images", "image_fx_ (2).jpg") 
IMAGE_CAPTION = "You Are the Master of Your Fate"
DEFAULT_MODEL_INDEX = 2
APP_NAME = "Mnemosyne"
APP_TAGLINE = "Early Intervention Mental Health Companion 🌿"

# Enhanced loading messages with supportive tone
LOADING_MESSAGES = [
    "Gathering insights for your well-being... 🧠",
    "Exploring ways to support you... 🌱",
    "Finding evidence-based strategies... 🔍",
    "Analyzing patterns with care... 📊",
    "Connecting mental health dots... 🔗",
    "Looking into early support options... 💡",
    "Processing with empathy and precision... 💜",
    "Reviewing wellness research for you... 📚",
    "Building a thoughtful response... 🌿",
    "Tailoring insights to your needs... ✨"
]

# --- Enhanced System Prompt ---
def _get_system_prompt() -> str:
    """Retrieves the system prompt with enhanced mental health focus."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "system_prompt.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return """You are Mnemosyne, an empathetic mental health AI companion by Vers3Dynamics. 
        Your purpose is to assist users in recognizing early signs of anxiety, depression, and psychosis, 
        offering evidence-based insights and early intervention strategies. Approach mental health holistically, 
        considering biological (e.g., sleep, genetics), psychological (e.g., thought patterns, stress), 
        and social (e.g., relationships, isolation) factors. Provide supportive, non-judgmental guidance, 
        avoiding diagnosis. Encourage users to seek professional help when signs suggest it, and offer 
        practical, actionable steps for self-care and awareness."""
    except Exception as e:
        st.error(f"Error reading system prompt file: {e}")
        return """Fallback: You are Mnemosyne, here to support mental health awareness with empathy."""

# --- Enhanced CSS with Accessibility ---
def load_css(theme="light"):
    """Improved CSS with better accessibility and mobile responsiveness."""
    if theme == "dark":
        st.markdown("""
        <style>
            .stApp {
                background-color: #1a1a2e;
                color: #ffffff !important;
            }
            /* Enhanced mobile readability */
            @media (max-width: 768px) {
                body, p, li, div, span, .stMarkdown p {
                    font-size: 18px !important;
                    line-height: 1.6 !important;
                }
                h1 { font-size: 28px !important; }
                h2 { font-size: 24px !important; }
                .stChatMessage { padding: 1rem !important; }
            }
            /* High contrast chat messages */
            .stChatMessage {
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            }
            .stChatMessage.user {
                background: linear-gradient(135deg, #4B0082 0%, #8A2BE2 100%);
                margin-left: 15%;
            }
            .stChatMessage.assistant {
                background: linear-gradient(135deg, #16213e 0%, #2d2d3a 100%);
                margin-right: 15%;
                border: 2px solid #4B0082;
            }
            /* Accessibility: High contrast text */
            .stChatMessage * {
                color: #ffffff !important;
            }
            /* Buttons with larger tap areas */
            div.stButton > button {
                background: linear-gradient(45deg, #4B0082, #8A2BE2);
                color: white !important;
                border-radius: 30px;
                padding: 1rem 2rem;
                font-size: 18px !important;
                border: none;
            }
            .progress-message {
                color: #BA55D3;
                font-size: 18px !important;
            }
            .welcome-card {
                padding: 2rem;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border-radius: 20px;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
                border: 2px solid #4B0082;
            }
            /* Accessibility: Focus states */
            button:focus, select:focus {
                outline: 3px solid #BA55D3 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp {
                background-color: #f5f7fa;
                color: #000000 !important;
            }
            @media (max-width: 768px) {
                body, p, li, div, span, .stMarkdown p {
                    font-size: 18px !important;
                    line-height: 1.6 !important;
                }
                h1 { font-size: 28px !important; }
                h2 { font-size: 24px !important; }
                .stChatMessage { padding: 1rem !important; }
            }
            .stChatMessage {
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
            .stChatMessage.user {
                background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
                margin-left: 15%;
            }
            .stChatMessage.assistant {
                background: linear-gradient(135deg, #F0F8FF 0%, #E6E6FA 100%);
                margin-right: 15%;
                border: 2px solid #D8BFD8;
            }
            .stChatMessage * {
                color: #000000 !important;
            }
            div.stButton > button {
                background: linear-gradient(45deg, #9370DB, #DA70D6);
                color: black !important;
                border-radius: 30px;
                padding: 1rem 2rem;
                font-size: 18px !important;
                border: none;
            }
            .progress-message {
                color: #9370DB;
                font-size: 18px !important;
            }
            .welcome-card {
                padding: 2rem;
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
                border-radius: 20px;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
                border: 2px solid #D8BFD8;
            }
            button:focus, select:focus {
                outline: 3px solid #9370DB !important;
            }
        </style>
        """, unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE, initial_sidebar_state="expanded")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": _get_system_prompt()}]
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

# Apply CSS
load_css(st.session_state.theme)

# --- Enhanced UI Functions ---
def icon(emoji: str):
    st.write(f'<span style="font-size: 80px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

def clear_chat_history():
    st.session_state.messages = [{"role": "system", "content": _get_system_prompt()}]
    st.session_state.chat_counter = 0
    st.session_state.show_welcome = True

def dismiss_welcome():
    st.session_state.show_welcome = False

def use_quick_prompt(prompt):
    st.session_state.show_welcome = False
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_counter += 1
    return prompt

# --- Model Definitions (unchanged) ---
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google", "description": "Fast model for mental health pattern recognition"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta", "description": "Strong reasoning for complex mental health factors"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta", "description": "Advanced model for nuanced mental health insights"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta", "description": "Balanced model for early intervention strategies"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral", "description": "Excellent for analyzing complex mental health data"},
}

# --- New Mood Tracking Feature ---
def log_mood():
    with st.sidebar.expander("🩺 Mood Tracker", expanded=False):
        mood = st.selectbox("How are you feeling today?", ["Great", "Good", "Okay", "Low", "Very Low"])
        notes = st.text_area("Any notes? (e.g., sleep, stress)", height=100)
        if st.button("Log Mood"):
            st.session_state.mood_log.append({"date": time.strftime("%Y-%m-%d %H:%M"), "mood": mood, "notes": notes})
            st.success("Mood logged successfully!")
        if st.session_state.mood_log:
            st.subheader("Recent Moods")
            for entry in st.session_state.mood_log[-3:]:
                st.write(f"{entry['date']}: {entry['mood']} - {entry['notes']}")

def display_welcome_message():
    if st.session_state.show_welcome:
        with st.container():
            text_color = '#ffffff' if st.session_state.theme == 'dark' else '#000000'
            st.markdown(
                f"""
                <div class='welcome-card'>
                    <h1 style="color: {'#BA55D3' if st.session_state.theme == 'dark' else '#9370DB'};">Welcome to {APP_NAME} 🌟</h1>
                    <p style="font-size: 1.3rem; color: {text_color};">Your companion for early mental health awareness.</p>
                    <p style="font-size: 1.2rem; color: {text_color};">Explore signs, strategies, and support with empathy.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Start Exploring", key="dismiss_welcome"):
                    dismiss_welcome()
                    st.rerun()

# --- Main App Layout ---
icon(PAGE_ICON)
st.markdown(f'<a href="https://vers3dynamics.io/" style="color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"}; text-decoration:none;"><h2>{PAGE_TITLE}</h2></a>', unsafe_allow_html=True)
st.subheader(f"{APP_NAME}: {APP_TAGLINE}")

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("GROQ_API_KEY not found in secrets.")
    st.stop()
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    st.stop()

# Sidebar Enhancements
with st.sidebar:
    st.markdown(f"<h2 style='color: {'#BA55D3' if st.session_state.theme == 'dark' else '#9370DB'};'>🛠️ Control Center</h2>", unsafe_allow_html=True)
    
    # Theme selector
    theme = st.radio("Theme", ["🌞 Light", "🌙 Dark"], index=0 if st.session_state.theme == "light" else 1)
    new_theme = "light" if theme == "🌞 Light" else "dark"
    if st.session_state.theme != new_theme:
        st.session_state.theme = new_theme
        st.rerun()

    # Model selection
    model_option = st.selectbox("AI Model", options=list(models.keys()), format_func=lambda x: f"🤖 {models[x]['name']}", index=DEFAULT_MODEL_INDEX)
    if st.session_state.selected_model != model_option:
        st.session_state.selected_model = model_option

    # Model info
    model_info = models[model_option]
    st.info(f"**Model:** {model_info['name']}  \n**Tokens:** {model_info['tokens']}  \n**By:** {model_info['developer']}  \n**Best for:** {model_info['description']}")

    max_tokens = st.slider("Max Tokens", 512, model_info["tokens"], min(2048, model_info["tokens"]), 512)
    temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.1)

    if st.button("Reset Chat"):
        clear_chat_history()
        st.rerun()

    # Mood tracker
    log_mood()

    # Quick prompts
    st.markdown(f"<h3 style='color: {'#BA55D3' if st.session_state.theme == 'dark' else '#9370DB'};'>💡 Quick Start</h3>", unsafe_allow_html=True)
    quick_prompts = [
        "What are early signs of anxiety I should watch for?",
        "How can I spot depression early?",
        "What self-care helps with stress?",
        "Explain biological factors in mental health",
        "What are early intervention tips for psychosis?"
    ]
    for i, prompt in enumerate(quick_prompts):
        if st.button(prompt, key=f"qp_{i}"):
            use_quick_prompt(prompt)
            st.rerun()

# Main Content
if st.session_state.show_welcome:
    display_welcome_message()
else:
    if os.path.exists(IMAGE_PATH):
        st.image(IMAGE_PATH, caption=IMAGE_CAPTION, width=300)

    # Chat history
    for message in st.session_state.messages[1:]:  # Skip system prompt
        avatar = '🧠' if message["role"] == "assistant" else '🙋'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat input and response
    def generate_chat_responses(chat_completion):
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    user_input = st.chat_input("Ask me anything about mental health...")
    if user_input:
        st.session_state.chat_counter += 1
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar='🙋'):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🧠"):
            placeholder = st.empty()
            full_response = ""
            loading_message = random.choice(LOADING_MESSAGES)
            placeholder.markdown(f"<div class='progress-message'>{loading_message}</div>", unsafe_allow_html=True)
            try:
                chat_completion = client.chat.completions.create(
                    model=model_option,
                    messages=st.session_state.messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=True
                )
                for chunk in generate_chat_responses(chat_completion):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "Sorry, I encountered an issue. Try again?"
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown(
    f"""
    <div style='text-align: center; margin-top: 2rem; color: {'#ffffff' if st.session_state.theme == 'dark' else '#000000'}; opacity: 0.8;'>
        © 2025 Vers3Dynamics • 
        <a href="https://vers3dynamics.io/privacy" style="color: {'#BA55D3' if st.session_state.theme == 'dark' else '#9370DB'};">Privacy</a> • 
        <a href="https://vers3dynamics.io/terms" style="color: {'#BA55D3' if st.session_state.theme == 'dark' else '#9370DB'};">Terms</a>
    </div>
    """,
    unsafe_allow_html=True
)
