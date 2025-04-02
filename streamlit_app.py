import streamlit as st
from typing import Generator, Optional, Dict, Union
from groq import Groq
import os
import random
from pathlib import Path
import time
import base64 # Added from visual script
import pandas as pd # Needed for mood chart
import plotly.express as px # Needed for mood chart

# --- Configuration ---
PAGE_TITLE = "Vers3Dynamics"
PAGE_ICON = "🧠" # Using a simpler icon that might animate better
IMAGE_PATH = os.path.join("images", "image_fx_ (2).jpg") # Make sure this path is correct relative to script
IMAGE_CAPTION = "You Are the Master of Your Fate"
DEFAULT_MODEL_INDEX = 5 # Choose the index of your preferred default model
APP_NAME = "Mnemosyne"
APP_TAGLINE = "Your Reflective Mental Wellness Companion 🌿" # Updated tagline

# Poem for Amanda (Easter egg) - Keep as is
POEM = """
amanda,
... (Poem content remains unchanged) ...
"""

# Enhanced loading messages with supportive tone - Keep as is
LOADING_MESSAGES = [
    "Gathering insights for your well-being... 🧘‍♀️💭", # Using updated messages
    "Weaving threads of insight... 🧶✨",
    "Consulting the echoes of memory... 🌌👂",
    "Brewing a supportive perspective... ☕️🌿",
    "Tuning into wellness frequencies... 🎶💖",
    "Planting seeds of understanding... 🌱💡",
    "Polishing gems of wisdom... 💎🧠",
    "Navigating the mindscape with care... 🗺️❤️",
    "Unfolding layers of awareness... 📜🦋",
    "Crafting a mindful response...✍️🧘‍♂️"
]
LOADING_INDICATORS = ["⏳", "💭", "💡", "✨", "🌀", "🔹", "🔸"] # Added from visually enhanced script


# --- Visual Elements & Animations (from Visual Script) ---
def get_base64_encoded_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"Image file not found for base64 encoding: {image_path}")
        return None

# Brain visualization SVG
BRAIN_SVG = """
<svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M50 10 C30 10, 15 30, 15 50 C15 70, 30 90, 50 90 C70 90, 85 70, 85 50 C85 30, 70 10, 50 10" fill="none" stroke="#9370DB" stroke-width="2">
    <animate attributeName="stroke-dasharray" from="0,250" to="250,0" dur="3s" repeatCount="indefinite" />
  </path>
  <path d="M30 30 C40 20, 60 20, 70 30" fill="none" stroke="#BA55D3" stroke-width="2">
    <animate attributeName="stroke-dasharray" from="0,100" to="100,0" dur="2s" repeatCount="indefinite" />
  </path>
  <path d="M30 70 C40 80, 60 80, 70 70" fill="none" stroke="#BA55D3" stroke-width="2">
    <animate attributeName="stroke-dasharray" from="0,100" to="100,0" dur="2s" repeatCount="indefinite" />
  </path>
  <path d="M50 10 C50 30, 30 50, 50 70 C70 50, 50 30, 50 10" fill="none" stroke="#9370DB" stroke-width="2">
    <animate attributeName="stroke-dasharray" from="0,200" to="200,0" dur="4s" repeatCount="indefinite" />
  </path>
</svg>
"""

# Pulse animation CSS definitions string
PULSE_ANIMATION = """
@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 0.8; }
}
.pulse { animation: pulse 3s ease-in-out infinite; display: inline-block; } /* Added display inline-block */

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); } /* Reduced float height */
  100% { transform: translateY(0px); }
}
.float { animation: float 6s ease-in-out infinite; display: inline-block; } /* Added display inline-block */

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); } /* Adjusted transform */
  to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.8s ease-out forwards; }

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes shimmer { /* Keep shimmer if used */
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.shimmer { /* Example usage */
  /* background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0) 100%); */
  /* background-size: 200% 100%; */
  /* animation: shimmer 3s infinite; */
}

@keyframes bubbleAppear {
  0% { transform: scale(0.5) translateY(10px); opacity: 0; } /* Added Y transform */
  100% { transform: scale(1) translateY(0px); opacity: 1; }
}
.chat-bubble-appear { animation: bubbleAppear 0.4s ease-out forwards; } /* Apply this class to chat messages */

/* Typewriter not used in current integration, but kept definition */
@keyframes typing { from { width: 0 } to { width: 100% } }
@keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #BA55D3 } }
.typewriter { /* Example usage */
  /* overflow: hidden; */
  /* border-right: .15em solid #BA55D3; */
  /* white-space: nowrap; */
  /* animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite; */
}
"""

# --- Get System Prompt (Keep original function) ---
def _get_system_prompt() -> str:
    # Use abspath for better path reliability
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "system_prompt.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.warning("system_prompt.txt not found, using default.")
        # Provide the default prompt directly
        return """You are Mnemosyne, an empathetic mental health AI companion by Vers3Dynamics... (rest of prompt)"""
    except Exception as e:
        st.error(f"Error reading system prompt file: {e}")
        return """Fallback: You are Mnemosyne, here to support mental health awareness."""

# --- REPLACED load_css function with the Enhanced Version ---
def load_css(theme="light"):
    # Inject keyframe animations first
    st.markdown(f'<style>{PULSE_ANIMATION}</style>', unsafe_allow_html=True)

    # Base font import (optional, if not using Streamlit's default)
    # st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">""", unsafe_allow_html=True)
    # font_family = "'Montserrat', sans-serif" # If using custom font

    # Common CSS base (can be minimal if relying on theme specifics)
    common_base = """
        <style>
             /* General link styling */
             a { text-decoration: none; transition: color 0.3s ease; }
             a:hover { text-decoration: underline; }

             /* Input styling base */
            .stTextInput > div > div > input, .stTextArea > div > div > textarea {
                border-radius: 15px !important; /* Rounded inputs */
                border: 1px solid transparent !important;
                transition: all 0.3s ease !important;
                padding: 10px 15px !important;
            }
            .stTextInput > label, .stTextArea > label, .stSelectbox > label, .stSlider > label {
                font-weight: 600; /* Make labels slightly bolder */
                padding-bottom: 5px;
            }
        </style>
    """
    st.markdown(common_base, unsafe_allow_html=True)

    if theme == "dark":
        st.markdown("""
        <style>
            /* --- Dark Theme Specifics --- */
            .stApp {
                /* Animated Gradient Background */
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                color: #e1e1e1 !important; /* Light text color */
            }
            /* Headers */
            h1, h2, h3 { color: #ffffff; }
            .header-gradient { /* Class for special headers */
                background: linear-gradient(90deg, #CDB4DB, #A28089); /* Adjusted gradient */
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent !important;
                font-weight: 700;
            }
            /* Sidebar */
            [data-testid="stSidebar"] > div:first-child {
                background: rgba(26, 26, 46, 0.8); /* Semi-transparent dark */
                backdrop-filter: blur(8px);
                border-right: 1px solid rgba(138, 43, 226, 0.2);
                padding: 1.5rem 1rem;
            }
             /* Responsive */
            @media (max-width: 768px) { /* Keep responsive rules */
                body, p, li, div, span, .stMarkdown p { font-size: 17px !important; line-height: 1.6 !important; }
                h1 { font-size: 26px !important; } h2 { font-size: 22px !important; }
                .stChatMessage { padding: 1rem !important; }
                div.stButton > button, .pill-button { padding: 0.8rem 1.5rem !important; font-size: 16px !important; }
            }
            /* Chat Messages */
            .stChatMessage {
                border-radius: 18px; padding: 1.2rem 1.5rem; margin: 1rem 0;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
                transition: all 0.3s ease;
                position: relative; /* Needed for pseudo-elements */
                border: 1px solid transparent;
                animation: bubbleAppear 0.4s ease-out forwards; /* Add animation */
            }
            .stChatMessage:hover { transform: translateY(-4px); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5); }
            .stChatMessage.user {
                background: linear-gradient(135deg, #4B0082 0%, #8A2BE2 100%);
                margin-left: 10%; /* Adjust margin */
            }
            /* Optional: Triangle pointers (subtle) */
            /* .stChatMessage.user::after { content:''; position:absolute; bottom:15px; right:-8px; width:0; height:0; border-top: 8px solid transparent; border-bottom: 8px solid transparent; border-left: 8px solid #6A5ACD; } */
            .stChatMessage.assistant {
                background: linear-gradient(135deg, #1e2a4a 0%, #2d375a 100%); /* Slightly different dark shade */
                margin-right: 10%;
                border: 1px solid #4B0082;
            }
             /* .stChatMessage.assistant::before { content:''; position:absolute; bottom:15px; left:-8px; width:0; height:0; border-top: 8px solid transparent; border-bottom: 8px solid transparent; border-right: 8px solid #2d375a; } */
            .stChatMessage * { color: #ffffff !important; }
            /* Buttons (Standard Streamlit Button) */
            div.stButton > button {
                background: linear-gradient(45deg, #6A5ACD, #8A2BE2); /* Darker gradient */
                color: white !important; border-radius: 30px;
                padding: 0.9rem 1.8rem; font-size: 17px !important; border: none;
                transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(75, 0, 130, 0.4);
            }
            div.stButton > button:hover { transform: translateY(-3px) scale(1.03); box-shadow: 0 7px 20px rgba(75, 0, 130, 0.6); }
            /* Pill Buttons (Used for Quick Prompts) */
            .pill-button {
                background: linear-gradient(45deg, #4B0082, #6A5ACD); /* Adjusted gradient */
                color: white !important; border-radius: 30px; padding: 0.7rem 1.5rem;
                margin: 0.3rem 0; display: block; /* Make block for full width */
                transition: all 0.3s ease; border: none;
                box-shadow: 0 4px 15px rgba(75, 0, 130, 0.3); cursor: pointer;
                font-weight: 500; text-align: center; width: 100%;
            }
            .pill-button:hover { transform: translateY(-3px); box-shadow: 0 7px 20px rgba(75, 0, 130, 0.5); background: linear-gradient(45deg, #6A5ACD, #4B0082); }
            /* Progress/Loading */
            .progress-message { color: #D8BFD8; font-size: 17px !important; font-style: italic; }
            /* Welcome Card */
            .welcome-card { /* Apply glass effect */
                padding: 2.5rem;
                background: rgba(26, 26, 46, 0.75); /* Glass background */
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(138, 43, 226, 0.3); /* Subtle border */
                transition: all 0.5s ease; margin-bottom: 2rem; text-align: center;
                animation: fadeIn 0.8s ease-out forwards;
            }
            .welcome-card:hover { box-shadow: 0 15px 40px rgba(75, 0, 130, 0.4); transform: translateY(-5px); }
            /* Focus Outline */
            button:focus, select:focus, input:focus, textarea:focus { outline: 3px solid #BA55D3 !important; outline-offset: 2px; }
            /* Input Box Specific Class */
            .input-box .stTextInput > div > div > input { /* Target input within the class */
                border-radius: 30px !important;
                border: 1px solid #4B0082 !important;
                background: rgba(26, 26, 46, 0.8) !important; /* Darker glass */
                color: #e1e1e1 !important;
                box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.3);
            }
            .input-box .stTextInput > div > div > input:focus { border-color: #8A2BE2 !important; box-shadow: 0 0 8px rgba(138, 43, 226, 0.5); }
             /* Slider styling */
            .stSlider > div[data-baseweb="slider"] > div { background: #4B0082 !important; /* Track */ }
            .stSlider > div[data-baseweb="slider"] > div > div { background: #8A2BE2 !important; /* Filled part */ box-shadow: 0 0 5px #8A2BE2; } /* Thumb */
            /* Links */
             a { color: #CDB4DB; } a:hover { color: #E6E6FA; }
        </style>
        """, unsafe_allow_html=True)
    else: # Light Theme
        st.markdown("""
        <style>
            /* --- Light Theme Specifics --- */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 50%, #c3cfe2 100%);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                color: #212529 !important; /* Dark text */
            }
            h1, h2, h3 { color: #343a40; }
            .header-gradient {
                 background: linear-gradient(90deg, #9370DB, #DA70D6);
                 -webkit-background-clip: text; background-clip: text;
                 color: transparent !important; font-weight: 700;
            }
            /* Sidebar */
             [data-testid="stSidebar"] > div:first-child {
                background: rgba(255, 255, 255, 0.85); /* Semi-transparent light */
                backdrop-filter: blur(8px);
                border-right: 1px solid rgba(216, 191, 216, 0.4);
                 padding: 1.5rem 1rem;
            }
             /* Responsive */
             @media (max-width: 768px) { /* Keep responsive rules */
                body, p, li, div, span, .stMarkdown p { font-size: 17px !important; line-height: 1.6 !important; }
                h1 { font-size: 26px !important; } h2 { font-size: 22px !important; }
                .stChatMessage { padding: 1rem !important; }
                div.stButton > button, .pill-button { padding: 0.8rem 1.5rem !important; font-size: 16px !important; }
            }
            /* Chat Messages */
            .stChatMessage {
                border-radius: 18px; padding: 1.2rem 1.5rem; margin: 1rem 0;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease; position: relative; border: 1px solid #e9ecef; /* Light border */
                animation: bubbleAppear 0.4s ease-out forwards;
            }
            .stChatMessage:hover { transform: translateY(-4px); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12); }
            .stChatMessage.user {
                background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
                margin-left: 10%; border-color: #D8BFD8;
            }
            /* .stChatMessage.user::after { border-left-color: #D8BFD8; } */
            .stChatMessage.assistant {
                background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%); /* Lighter assistant bg */
                margin-right: 10%; border-color: #dee2e6;
            }
            /* .stChatMessage.assistant::before { border-right-color: #E9ECEF; } */
            .stChatMessage * { color: #212529 !important; } /* Ensure text color inside */
            /* Buttons (Standard Streamlit Button) */
            div.stButton > button {
                background: linear-gradient(45deg, #A084CA, #B886FA); /* Lighter gradient */
                color: white !important; border-radius: 30px;
                padding: 0.9rem 1.8rem; font-size: 17px !important; border: none;
                transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(147, 112, 219, 0.3);
            }
            div.stButton > button:hover { transform: translateY(-3px) scale(1.03); box-shadow: 0 7px 20px rgba(147, 112, 219, 0.4); }
            /* Pill Buttons */
            .pill-button {
                background: linear-gradient(45deg, #9370DB, #B886FA); /* Main gradient */
                color: white !important; border-radius: 30px; padding: 0.7rem 1.5rem;
                margin: 0.3rem 0; display: block; transition: all 0.3s ease; border: none;
                box-shadow: 0 4px 15px rgba(147, 112, 219, 0.3); cursor: pointer;
                font-weight: 500; text-align: center; width: 100%;
            }
            .pill-button:hover { transform: translateY(-3px); box-shadow: 0 7px 20px rgba(147, 112, 219, 0.4); background: linear-gradient(45deg, #B886FA, #9370DB); }
            /* Progress/Loading */
            .progress-message { color: #8A2BE2; font-size: 17px !important; font-style: italic; }
            /* Welcome Card */
            .welcome-card {
                padding: 2.5rem;
                background: rgba(255, 255, 255, 0.85); /* Light Glass effect */
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(216, 191, 216, 0.4);
                transition: all 0.5s ease; margin-bottom: 2rem; text-align: center;
                animation: fadeIn 0.8s ease-out forwards;
            }
             .welcome-card:hover { box-shadow: 0 15px 40px rgba(147, 112, 219, 0.15); transform: translateY(-5px); }
            /* Focus Outline */
            button:focus, select:focus, input:focus, textarea:focus { outline: 3px solid #B886FA !important; outline-offset: 2px; }
            /* Input Box Specific Class */
            .input-box .stTextInput > div > div > input {
                 border-radius: 30px !important;
                 border: 1px solid #D8BFD8 !important;
                 background: rgba(255, 255, 255, 0.9) !important;
                 color: #212529 !important;
                 box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
            }
            .input-box .stTextInput > div > div > input:focus { border-color: #9370DB !important; box-shadow: 0 0 8px rgba(147, 112, 219, 0.4); }
             /* Slider styling */
             .stSlider > div[data-baseweb="slider"] > div { background: #D8BFD8 !important; /* Track */ }
             .stSlider > div[data-baseweb="slider"] > div > div { background: #9370DB !important; /* Filled part */ box-shadow: 0 0 5px #9370DB;} /* Thumb */
             /* Links */
             a { color: #8A2BE2; } a:hover { color: #6A5ACD; }
        </style>
        """, unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE, initial_sidebar_state="expanded")

# --- Session State Initialization ---
# Usesetdefault for cleaner initialization
st.session_state.setdefault("messages", [{"role": "system", "content": _get_system_prompt()}])
st.session_state.setdefault("selected_model", list(models.keys())[DEFAULT_MODEL_INDEX] if DEFAULT_MODEL_INDEX < len(models) else list(models.keys())[0]) # Ensure default is valid
st.session_state.setdefault("chat_counter", 0)
st.session_state.setdefault("show_welcome", True)
st.session_state.setdefault("theme", "light") # Default theme
st.session_state.setdefault("mood_log", [])
st.session_state.setdefault("audio_played", False)
st.session_state.setdefault("wellness_score", 75) # Example starting score
st.session_state.setdefault("animation_enabled", True) # Control animations

# Apply CSS based on current theme
load_css(st.session_state.theme)

# Apply conditional glow effect
# if st.session_state.animation_enabled:
#    add_glow_effect(intensity=1) # Optional: Add glow effect

# --- Enhanced UI Functions ---
def icon(emoji: str):
    # Apply float animation if enabled
    animation_class = "float" if st.session_state.get("animation_enabled", True) else ""
    st.write(f'<div class="{animation_class}" style="text-align: center;"><span style="font-size: 60px; line-height: 1;">{emoji}</span></div>', unsafe_allow_html=True)

def brain_animation():
    # Apply pulse animation if enabled
    animation_class = "pulse" if st.session_state.get("animation_enabled", True) else ""
    st.markdown(f'<div class="{animation_class}" style="text-align: center;">{BRAIN_SVG}</div>', unsafe_allow_html=True)

def clear_chat_history():
    # Preserve system prompt, clear others
    system_prompt = st.session_state.messages[0] if st.session_state.messages and st.session_state.messages[0]['role'] == 'system' else {"role": "system", "content": _get_system_prompt()}
    st.session_state.messages = [system_prompt]
    st.session_state.chat_counter = 0
    st.session_state.show_welcome = True
    st.session_state.audio_played = False
    st.session_state.mood_log = [] # Also clear mood log on reset

def dismiss_welcome():
    st.session_state.show_welcome = False

def use_quick_prompt(prompt_text): # Renamed parameter
    st.session_state.show_welcome = False
    # Check if the last message is already this prompt to avoid duplicates on quick clicks
    if not st.session_state.messages or st.session_state.messages[-1].get("content") != prompt_text:
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        st.session_state.chat_counter += 1
    # No return needed, state change triggers rerun

# --- Animated Wellness Gauge (Keep original function) ---
def wellness_gauge(score):
    # Use theme colors
    if st.session_state.theme == 'dark':
        color = "#4CAF50" if score > 70 else "#FFC107" if score > 40 else "#F44336" # Keep colors consistent
        track_color = "#444"
        text_color = "#e1e1e1"
    else:
        color = "#66BB6A" if score > 70 else "#FFA726" if score > 40 else "#EF5350"
        track_color = "#e0e0e0"
        text_color = "#333"

    # Simplified SVG for better compatibility
    gauge_html = f"""
    <div style="width: 100%; text-align: center; padding: 10px 0;">
        <svg width="120" height="65" viewBox="0 0 120 65">
            <path d="M10 60 A50 50 0 0 1 110 60" stroke="{track_color}" stroke-width="12" fill="none" stroke-linecap="round"/>
            <path d="M10 60 A50 50 0 0 1 110 60" stroke="{color}" stroke-width="12" fill="none" stroke-linecap="round"
                stroke-dasharray="157" stroke-dashoffset="{157 - (score/100) * 157}">
                {'<animate attributeName="stroke-dashoffset" from="157" to="{}" dur="1s" fill="freeze" />'.format(157 - (score/100) * 157) if st.session_state.get("animation_enabled", True) else ""}
            </path>
            <text x="60" y="55" text-anchor="middle" font-size="18" font-weight="bold" fill="{text_color}">
                {score}%
            </text>
        </svg>
        <div style="font-size: 14px; margin-top: -5px; color: {text_color}; opacity: 0.9;">Wellness</div>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)


# --- Model Definitions (Keep original) ---
models = {
    "llama-3.3-70b-versatile": {"name": "Llama-3.3-70b-Versatile", "tokens": 8192, "developer": "Meta", "description": "Latest Llama model for versatile, detailed medical responses"},
    "Llama3-8b-8192": {"name": "Llama3-8b-8192", "tokens": 8192, "developer": "Meta", "description": "Efficient Llama model for fast, accurate medical insights"},
    "mistral-saba-24b": {"name": "Mistral-Saba-24b", "tokens": 32768, "developer": "Mistral", "description": "Specialized model with large context for in-depth narratives"},
    "mixtral-8x22b-instruct": {"name": "Mixtral-8x22b-Instruct", "tokens": 65536, "developer": "Mistral", "description": "Advanced Mixtral for complex medical analysis"},
    "gemma-2-27b-it": {"name": "Gemma-2-27b-IT", "tokens": 8192, "developer": "Google", "description": "Updated Gemma model for general-purpose medical dialogue"},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1b-Preview", "tokens": 4096, "developer": "Meta", "description": "Lightweight Llama model for quick responses and basic assistance"},
}

# --- Mood Tracking with Plotly Chart (Use the corrected version) ---
def log_mood():
    with st.sidebar.expander("📊 Mood Tracker", expanded=False):
        mood_options = {"Great": 5, "Good": 4, "Okay": 3, "Low": 2, "Very Low": 1}
        mood_selection = st.selectbox("How are you feeling today?", options=list(mood_options.keys()), key="mood_select")
        notes = st.text_area("Any notes? (e.g., sleep, stress)", height=80, key="mood_notes")

        if st.button("📝 Log Mood", use_container_width=True, key="log_mood_button"):
            mood_value = mood_options[mood_selection]
            st.session_state.mood_log.append({
                "date": pd.to_datetime(time.strftime("%Y-%m-%d %H:%M")),
                "mood_text": mood_selection,
                "mood_value": mood_value,
                "notes": notes
            })
            st.success("Mood logged! 🌱")
            # No rerun needed, chart updates via Plotly

        if st.session_state.mood_log:
            st.markdown("---")
            st.subheader("📈 Recent Mood Trend")
            df_mood = pd.DataFrame(st.session_state.mood_log)
            df_mood['date'] = pd.to_datetime(df_mood['date'])
            df_mood = df_mood.sort_values(by="date")

            if len(df_mood) >= 2:
                fig = px.line(df_mood, x='date', y='mood_value', markers=True, labels={'date': 'Date', 'mood_value': 'Mood Level'})
                fig.update_layout(
                    yaxis=dict(tickvals=list(mood_options.values()), ticktext=list(mood_options.keys()), range=[0.5, 5.5]),
                    xaxis_title=None, yaxis_title=None,
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color="#e1e1e1" if st.session_state.theme == 'dark' else "#212529",
                    margin=dict(l=5, r=5, t=5, b=5) # Further reduced margins
                )
                line_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'
                fig.update_traces(line=dict(color=line_color, width=2), marker=dict(color=line_color, size=6))
                st.plotly_chart(fig, use_container_width=True)
            elif len(df_mood) == 1:
                st.info(f"Logged '{df_mood.iloc[0]['mood_text']}'. Need more data for a trend chart.")
            else:
                st.info("Log your mood to see trends here.")

            st.markdown("---")
            st.subheader("🗒️ Latest Logs")
            for entry in reversed(st.session_state.mood_log[-3:]):
                 # Using the corrected f-string logic and applying mood-card class
                 note_str = f" - *{entry['notes']}*" if entry['notes'] else ""
                 mood_color_class = "mood-card" # Using the general class defined in CSS
                 st.markdown(f"<div class='{mood_color_class}'>**{entry['date'].strftime('%b %d, %H:%M')}:** {entry['mood_text']}{note_str}</div>", unsafe_allow_html=True)


# --- Display Welcome Message Function ---
def display_welcome_message():
    if st.session_state.show_welcome:
        with st.container():
            primary_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'
            secondary_color = '#ffffff' if st.session_state.theme == 'dark' else '#343a40'
            st.markdown( # Welcome card class applied here
                f"""
                <div class='welcome-card fade-in'>
                    <div class="float" style="margin-bottom: 1rem;">
                        <span style="font-size: 4rem; display: block;">{PAGE_ICON}</span>
                    </div>
                    <h1 class="header-gradient" style="margin-bottom: 0.5rem;">Welcome to {APP_NAME}</h1>
                    <p style="font-size: 1.3rem; color: {secondary_color}; margin-bottom: 1.5rem;">{APP_TAGLINE}</p>
                    <p style="font-size: 1.1rem; color: {secondary_color}; opacity: 0.9;">
                        Your space for reflection and early awareness in mental wellness.
                        Ready to explore?
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2: # Centered button
                # Use standard Streamlit button, styled by CSS
                if st.button("✨ Let's Begin Exploring ✨", key="dismiss_welcome_btn", use_container_width=True):
                    dismiss_welcome()
                    st.rerun()

# --- Main App Layout ---

# Header Section
col_icon, col_title = st.columns([0.1, 0.9])
with col_icon:
     icon(PAGE_ICON) # Floating icon
with col_title:
    primary_color_header = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2' # Header specific color
    st.markdown(f'<a href="https://vers3dynamics.io/" target="_blank" style="color: {primary_color_header}; text-decoration:none; font-weight: 600;"><h1 class="header-gradient">{PAGE_TITLE}</h1></a>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="opacity: 0.9;">{APP_NAME}: {APP_TAGLINE}</h3>', unsafe_allow_html=True)

st.markdown("---", unsafe_allow_html=True) # Use markdown divider for potential styling later

# Initialize Groq Client (Keep original robust check)
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("🚨 GROQ_API_KEY not found in secrets. Please add it.")
        st.stop()
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {e}")
    st.stop()

# Sidebar Enhancements
with st.sidebar:
    # Wrap content in a styled div if desired (e.g., glass-card from CSS)
    # st.markdown('<div class="glass-card">', unsafe_allow_html=True) # Optional glass effect

    sidebar_header_color = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2'
    st.markdown(f"<h2 style='color: {sidebar_header_color}; text-align: center;'>Controls & Insights</h2>", unsafe_allow_html=True)

    # Brain Animation
    brain_animation()

    # Wellness Gauge
    wellness_gauge(st.session_state.wellness_score)

    st.markdown("---")

    # Theme Selector
    theme_selection = st.radio("🎨 Theme", ["🌞 Light", "🌙 Dark"], index=0 if st.session_state.theme == "light" else 1, horizontal=True, key="theme_selector")
    new_theme = "light" if theme_selection == "🌞 Light" else "dark"
    if st.session_state.theme != new_theme:
        st.session_state.theme = new_theme
        st.rerun()

    # Animation Toggle (Optional)
    # st.session_state.animation_enabled = st.toggle("✨ Enable Animations", value=st.session_state.get("animation_enabled", True), key="anim_toggle")


    st.markdown("---")
    st.markdown(f"<h3 style='color: {sidebar_header_color};'>🧠 AI Configuration</h3>", unsafe_allow_html=True)

    # Model selection
    current_model_index = list(models.keys()).index(st.session_state.selected_model) if st.session_state.selected_model in models else DEFAULT_MODEL_INDEX
    model_option = st.selectbox("Model", options=list(models.keys()), format_func=lambda x: f"{models[x]['name']}", index=current_model_index, label_visibility="collapsed", key="model_selector")
    if st.session_state.selected_model != model_option:
        st.session_state.selected_model = model_option

    model_info = models[st.session_state.selected_model]
    with st.expander("ℹ️ Model Details", expanded=False):
        st.markdown(f"**Tokens:** `{model_info['tokens']}` | **Dev:** _{model_info['developer']}_")
        st.caption(f"Use Case: {model_info['description']}")


    # Parameters
    max_tokens = st.slider("Max Response Length", min_value=128, max_value=model_info["tokens"], value=min(2048, model_info["tokens"]), step=128, key="max_tokens_slider")
    temperature = st.slider("Creativity Level", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="temp_slider")

    st.markdown("---")

    # Reset Button
    if st.button("🔄 Reset Conversation", use_container_width=True, key="reset_button"):
        clear_chat_history()
        st.rerun()

    st.markdown("---")

    # Mood Tracker (Function Call)
    log_mood() # This now includes the chart and log display within the expander

    st.markdown("---")

       # Quick Prompts Section
    st.markdown(f"<h3 style='color: {sidebar_header_color};'>💡 Quick Prompts</h3>", unsafe_allow_html=True)
    quick_prompts = [
        "Early signs of anxiety?", "Spotting depression early?",
        "Self-care for stress?", "Explain biopsychosocial factors",
        "Early help for psychosis?"
    ]
    for i, prompt in enumerate(quick_prompts):
        # Ensure 'if' is indented correctly under 'for'
        if st.button(f"💬 {prompt}", key=f"qp_{i}", use_container_width=True):
            # Ensure these lines are indented correctly under 'if' (e.g., 4 spaces more)
            use_quick_prompt(prompt)
            st.rerun()
    # st.markdown('</div>', unsafe_allow_html=True) # Close optional glass-card div


# --- Main Chat Area ---
if st.session_state.show_welcome:
    display_welcome_message()
else:
    # Displaying the image centered if it exists
    # Ensure IMAGE_PATH is correctly resolved relative to the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_image_path = os.path.join(script_dir, IMAGE_PATH)
    if os.path.exists(full_image_path):
        col_img1, col_img2, col_img3 = st.columns([1, 1, 1]) # Centering column
        with col_img2:
            # Add fade-in animation class to the image container if desired
            st.image(full_image_path, caption=IMAGE_CAPTION, width=300, use_column_width='auto') # Adjusted width
        st.markdown("<br>", unsafe_allow_html=True) # Spacer


    # Chat history display
    message_container = st.container() # Use a container for messages
    with message_container:
        display_messages = [msg for msg in st.session_state.messages if msg.get("role") != "system"]
        for message in display_messages:
            role = message.get("role", "unknown")
            avatar_icon = '💬' if role == "assistant" else '👤'
            with st.chat_message(role, avatar=avatar_icon):
                 # Apply chat-bubble-appear class here if desired, requires more complex handling or component
                st.markdown(message.get("content", ""), unsafe_allow_html=True)

    # --- Chat Input and Response Handling ---
    def generate_chat_responses(chat_completion):
        """Yields response chunks"""
        try:
            for chunk in chat_completion:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            st.error(f"Stream Error: {e}", icon="⚠️")
            yield " An error occurred during response generation. "

    # Wrap chat input in a div to apply the input-box class
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    user_input = st.chat_input("Ask Mnemosyne about mental wellness...", key="chat_input")
    st.markdown('</div>', unsafe_allow_html=True)

    if user_input:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with message_container: # Add to the same container
             with st.chat_message("user", avatar='👤'):
                 st.markdown(user_input)

        # Generate and display assistant response
        with message_container: # Add to the same container
            with st.chat_message("assistant", avatar="💬"):
                placeholder = st.empty()
                full_response = ""
                loading_message = random.choice(LOADING_MESSAGES)
                loading_indicator_emoji = random.choice(LOADING_INDICATORS)
                placeholder.markdown(f"<div class='progress-message'><span class='pulse'>{loading_indicator_emoji}</span>  {loading_message}</div>", unsafe_allow_html=True)

                # Easter Egg Check
                if "amanda" in user_input.lower() or "poem" in user_input.lower():
                    time.sleep(1)
                    full_response = f"Ah, a whisper for Amanda... 💌\n\n---\n\n{POEM}"
                    placeholder.markdown(full_response, unsafe_allow_html=True)
                    # Add Easter egg response to history differently if needed, or just display
                    # st.session_state.messages.append({"role": "assistant", "content": "Displayed the poem for Amanda."}) # Log differently
                else:
                    # Normal Response Generation
                    try:
                        selected_model_key = st.session_state.selected_model
                        messages_to_send = [
                            {"role": msg["role"], "content": msg["content"]}
                            for msg in st.session_state.messages
                            if msg.get("role") and msg.get("content")
                        ]

                        if not messages_to_send:
                            raise ValueError("No valid messages to send.")

                        chat_completion = client.chat.completions.create(
                            model=selected_model_key, messages=messages_to_send,
                            max_tokens=max_tokens, temperature=temperature, stream=True
                        )

                        response_stream = generate_chat_responses(chat_completion)
                        for chunk in response_stream:
                            full_response += chunk
                            placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

                        placeholder.markdown(full_response, unsafe_allow_html=True) # Final display
                        # Add actual response to history
                        st.session_state.messages.append({"role": "assistant", "content": full_response})

                    except Exception as e:
                        st.error(f"AI Error: {e}", icon="🤖")
                        full_response = "I encountered an issue connecting. Please try again shortly. 🙏"
                        placeholder.markdown(full_response)
                        # Optionally add error message to chat history
                        # st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Rerun to clear input and potentially update other elements
        st.rerun()


# --- Footer ---
st.markdown("---") # Divider before footer
footer_color = '#d1d1e1' if st.session_state.theme == 'dark' else '#555' # Adjusted footer colors
link_color = '#CDB4DB' if st.session_state.theme == 'dark' else '#8A2BE2'
st.markdown(
    f"""
    <div style='text-align: center; margin-top: 1.5rem; padding-bottom: 1.5rem; color: {footer_color}; opacity: 0.85; font-size: 0.9rem;'>
        © {time.strftime('%Y')} Vers3Dynamics •
        <a href="https://woodyard.dappling.network/" target="_blank" style="color: {link_color};">Privacy Policy</a> •
        <a href="https://vers3dynamics.io/titanic" target="_blank" style="color: {link_color};">Terms of Service</a> <br>
        <span style="font-size: 0.8rem; display: block; margin-top: 0.5rem;">Disclaimer: Mnemosyne is an AI assistant for informational purposes only and does not substitute professional medical advice.</span>
    </div>
    """,
    unsafe_allow_html=True
)
