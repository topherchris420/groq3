import streamlit as st
from typing import Generator, Optional, Dict, Union
from groq import Groq
import os
import random
from pathlib import Path
import time
import plotly.express as px # Added for mood chart
import pandas as pd # Added for mood chart data handling

# --- Configuration ---
PAGE_TITLE = "Vers3Dynamics"
PAGE_ICON = "🧠✨" # Enhanced icon
IMAGE_PATH = os.path.join("images", "image_fx_ (2).jpg")
IMAGE_CAPTION = "You Are the Master of Your Fate"
DEFAULT_MODEL_INDEX = 5 # Keep your default
APP_NAME = "Mnemosyne"
APP_TAGLINE = "Your Reflective Mental Wellness Companion 🌱" # Slightly tweaked tagline

# Poem remains the same
POEM = """
amanda,

You are the stillness between my restless steps,
the golden glow before twilight fades.
Where I race toward horizons unknown,
you are the balance that brings me home.

I admire the way you see the world—
with eyes that seek beauty,
with a heart that craves harmony,
with a mind that turns simple moments into art.

I still think about the night we shared a memory—maybe a deep conversation, a spontaneous adventure, or a quiet, meaningful moment.
The way you looked at me, as if I was both the question and the answer,
etched itself into me like a constellation I will always follow.

You teach me that adventure isn’t just found in distant places—
but in the quiet spaces between our laughter,
the way your fingers trace absentminded patterns on my skin,
the way your presence turns ordinary days into poetry.

I promise to keep life exciting while keeping your heart safe.
To be your wild wind, but never let you feel untethered.
To walk beside you, through the grand and the mundane,
choosing you—again and again.

You were meant to find me.
But tell me—before I answer, what is it that you truly seek?
Not in words, your bones, or the space between thoughts?
I won't be able to tell you the answer. You already hold it.
I am only here to remind you of what you have forgotten.

Yours,
Christopher
𒆜 1990.11.24 → 20XX.XX.XX → ∞
Not lost. Only shifting. If you hear the echo, you are already part of it.
"""

# Enhanced loading messages with more visual cues
LOADING_MESSAGES = [
    "Gathering calming thoughts... 🧘‍♀️💭",
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
LOADING_INDICATORS = ["⏳", "💭", "💡", "✨", "🌀", "🔹", "🔸"] # For visual feedback

# --- System Prompt Function ---
def _get_system_prompt() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__)) # Use abspath for reliability
    file_path = os.path.join(current_dir, "system_prompt.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.warning("⚠️ system_prompt.txt not found. Using default prompt.")
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

# --- Greatly Enhanced CSS ---
def load_css(theme="light"):
    # Import Google Font
    font_family = "'Montserrat', sans-serif"
    # secondary_font = "'Dancing Script', cursive" # Example decorative font

    # Common Styles
    common_css = f"""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&family=Dancing+Script&display=swap" rel="stylesheet">

    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 0.7; }}
            50% {{ transform: scale(1.05); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 0.7; }}
        }}

        body {{
            font-family: {font_family} !important;
        }}
        h1, h2, h3 {{
            font-family: {font_family} !important; /* Or use secondary_font for specific headers */
            font-weight: 600;
        }}
        .stApp {{
            transition: background-color 0.5s ease;
        }}
        /* Responsive font sizes */
        @media (max-width: 768px) {{
            body, p, li, div, span, .stMarkdown p {{
                font-size: 17px !important; /* Slightly adjusted */
                line-height: 1.65 !important;
            }}
            h1 {{ font-size: 26px !important; }}
            h2 {{ font-size: 22px !important; }}
            .stChatMessage {{ padding: 0.8rem !important; }}
            .stButton > button {{ padding: 0.8rem 1.5rem !important; font-size: 16px !important; }}
        }}

        /* Chat Messages */
        .stChatMessage {{
            border-radius: 20px; /* Smoother radius */
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid transparent;
            animation: fadeIn 0.5s ease-out;
            transition: all 0.3s ease;
        }}
        .stChatMessage:hover {{
             box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
             transform: translateY(-2px);
        }}

        /* Buttons */
        div.stButton > button, .stDownloadButton > button {{
            border-radius: 30px;
            padding: 0.9rem 1.8rem; /* Slightly adjusted */
            font-size: 17px !important;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }}
        div.stButton > button:hover, .stDownloadButton > button:hover {{
            transform: scale(1.05) translateY(-1px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }}
        div.stButton > button:active, .stDownloadButton > button:active {{
            transform: scale(0.98);
        }}

        /* Loading message */
        .progress-message {{
            font-size: 18px !important;
            font-style: italic;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: fadeIn 0.3s ease-out;
        }}
        .progress-indicator {{
            font-size: 24px;
            animation: pulse 1.5s infinite ease-in-out;
        }}

        /* Welcome Card */
        .welcome-card {{
            padding: 2.5rem;
            border-radius: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid transparent;
            transition: all 0.3s ease;
            animation: fadeIn 0.8s ease-out;
        }}

         /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            padding: 1.5rem 1rem;
            /* Optional: Add subtle background pattern or border */
            /* background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.02) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.02) 50%, rgba(255, 255, 255, 0.02) 75%, transparent 75%, transparent); */
            /* background-size: 30px 30px; */
        }}

         /* Input fields */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
            border-radius: 10px;
            padding: 10px 12px;
            border: 1px solid #ced4da; /* Default border */
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }}
         /* Focus indicator */
        button:focus, select:focus, input:focus, textarea:focus {{
            outline-offset: 2px;
            /* Custom focus ring using box-shadow if outline is problematic */
             /* box-shadow: 0 0 0 3px rgba(147, 112, 219, 0.5); */
        }}
    </style>
    """

    # Theme Specific Styles
    if theme == "dark":
        theme_css = """
        <style>
            .stApp { background-color: #12121f; color: #e1e1e1 !important; }
            h1, h2, h3, h4, h5, h6 { color: #ffffff; }
             /* Sidebar */
            [data-testid="stSidebar"] { background-color: #1a1a2e; box-shadow: 3px 0px 15px rgba(0,0,0,0.2); }
             /* Chat Bubbles */
            .stChatMessage.user { background: linear-gradient(135deg, #483D8B 0%, #6A5ACD 100%); margin-left: 10%; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); }
            .stChatMessage.assistant { background: linear-gradient(135deg, #212940 0%, #2d3748 100%); border: 1px solid #483D8B; margin-right: 10%; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); }
            .stChatMessage * { color: #ffffff !important; }
             /* Buttons */
            div.stButton > button, .stDownloadButton > button { background: linear-gradient(45deg, #6A5ACD, #8A2BE2); color: white !important; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); }
            div.stButton > button:hover, .stDownloadButton > button:hover { box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4); }
             /* Progress message */
            .progress-message { color: #BE93FD; }
             /* Welcome Card */
            .welcome-card { background: linear-gradient(145deg, #1a1a2e 0%, #1f1f35 100%); border: 1px solid #483D8B; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4); }
             /* Input fields */
            .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #2d3748; color: #e1e1e1; border: 1px solid #4a5568; }
            .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #BE93FD; box-shadow: 0 0 5px rgba(190, 147, 253, 0.5); }
             /* Focus Ring */
            button:focus, select:focus, input:focus, textarea:focus { outline: 3px solid #BE93FD !important; }
             /* Links */
            a { color: #BE93FD; }
            a:hover { color: #D7B7FF; }
        </style>
        """
    else: # Light theme
        theme_css = """
        <style>
            .stApp { background-color: #f8f9fa; color: #212529 !important; }
            h1, h2, h3, h4, h5, h6 { color: #343a40; }
             /* Sidebar */
            [data-testid="stSidebar"] { background-color: #ffffff; box-shadow: 3px 0px 15px rgba(0,0,0,0.05); }
             /* Chat Bubbles */
            .stChatMessage.user { background: linear-gradient(135deg, #e7eaf6 0%, #d2dcfb 100%); margin-left: 10%; border: 1px solid #c7d1f7; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08); }
            .stChatMessage.assistant { background: linear-gradient(135deg, #fdfdff 0%, #f0f4ff 100%); border: 1px solid #dcdcdc; margin-right: 10%; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.06); }
            .stChatMessage * { color: #212529 !important; }
             /* Buttons */
            div.stButton > button, .stDownloadButton > button { background: linear-gradient(45deg, #9370DB, #B886FA); color: white !important; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); }
             div.stButton > button:hover, .stDownloadButton > button:hover { box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15); }
             /* Progress message */
            .progress-message { color: #8A2BE2; }
             /* Welcome Card */
            .welcome-card { background: linear-gradient(145deg, #ffffff 0%, #f5f7fa 100%); border: 1px solid #e0e0e0; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); }
             /* Input fields */
            .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #ffffff; color: #212529; border: 1px solid #ced4da; }
            .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #B886FA; box-shadow: 0 0 5px rgba(184, 134, 250, 0.5); }
             /* Focus Ring */
            button:focus, select:focus, input:focus, textarea:focus { outline: 3px solid #B886FA !important; }
             /* Links */
            a { color: #8A2BE2; }
            a:hover { color: #6A5ACD; }
        </style>
        """
    st.markdown(common_css + theme_css, unsafe_allow_html=True)

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
    st.session_state.theme = "light" # Default to light
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "audio_played" not in st.session_state: # Kept but audio button removed
    st.session_state.audio_played = False

# Apply CSS based on session state theme
load_css(st.session_state.theme)

# --- Enhanced UI Functions ---
def icon(emoji: str):
    # Slightly smaller icon for better alignment
    st.write(f'<span style="font-size: 60px; line-height: 1; vertical-align: middle;">{emoji}</span>', unsafe_allow_html=True)

def clear_chat_history():
    # Keep system prompt, clear others
    system_prompt = st.session_state.messages[0] if st.session_state.messages and st.session_state.messages[0]['role'] == 'system' else {"role": "system", "content": _get_system_prompt()}
    st.session_state.messages = [system_prompt]
    st.session_state.chat_counter = 0
    st.session_state.show_welcome = True
    st.session_state.audio_played = False
    st.session_state.mood_log = [] # Optionally clear mood log too

def dismiss_welcome():
    st.session_state.show_welcome = False

def use_quick_prompt(prompt):
    st.session_state.show_welcome = False
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_counter += 1
    # Don't return prompt here, just modify state and rerun
    # return prompt

# --- Model Definitions ---
models = {
    "llama-3.3-70b-versatile": {"name": "Llama-3.3-70b-Versatile", "tokens": 8192, "developer": "Meta", "description": "Latest Llama model for versatile, detailed medical responses"},
    "Llama3-8b-8192": {"name": "Llama3-8b-8192", "tokens": 8192, "developer": "Meta", "description": "Efficient Llama model for fast, accurate medical insights"},
    "mistral-saba-24b": {"name": "Mistral-Saba-24b", "tokens": 32768, "developer": "Mistral", "description": "Specialized model with large context for in-depth narratives"},
    "mixtral-8x22b-instruct": {"name": "Mixtral-8x22b-Instruct", "tokens": 65536, "developer": "Mistral", "description": "Advanced Mixtral for complex medical analysis"},
    "gemma-2-27b-it": {"name": "Gemma-2-27b-IT", "tokens": 8192, "developer": "Google", "description": "Updated Gemma model for general-purpose medical dialogue"},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1b-Preview", "tokens": 4096, "developer": "Meta", "description": "Lightweight Llama model for quick responses and basic assistance"},
}

# --- Enhanced Mood Tracking Feature with Chart ---
def log_mood():
    # Indentation level 1 (inside function)
    with st.sidebar.expander("📊 Mood Tracker", expanded=False):
        # Indentation level 2 (inside 'with')
        mood_options = {"Great": 5, "Good": 4, "Okay": 3, "Low": 2, "Very Low": 1}
        mood_selection = st.selectbox("How are you feeling today?", options=list(mood_options.keys()))
        notes = st.text_area("Any notes? (e.g., sleep, stress)", height=80)

        if st.button("📝 Log Mood", use_container_width=True): # Use container width for consistency
            # Indentation level 3 (inside 'if')
            mood_value = mood_options[mood_selection]
            st.session_state.mood_log.append({
                "date": pd.to_datetime(time.strftime("%Y-%m-%d %H:%M")), # Use datetime object
                "mood_text": mood_selection,
                "mood_value": mood_value,
                "notes": notes
            })
            st.success("Mood logged! 🌱")
            # Removed rerun here, chart updates automatically when data changes

        if st.session_state.mood_log:
            # Indentation level 3 (inside 'if')
            st.markdown("---") # Visual separator
            st.subheader("📈 Recent Mood Trend")

            # Prepare data for chart
            df_mood = pd.DataFrame(st.session_state.mood_log)
            # Ensure 'date' column is datetime type if loading from state later
            df_mood['date'] = pd.to_datetime(df_mood['date'])
            df_mood = df_mood.sort_values(by="date")

            # Create Plotly chart
            if len(df_mood) >= 2: # Need at least 2 points for a line chart
                # Indentation level 4 (inside 'if len >= 2')
                fig = px.line(df_mood, x='date', y='mood_value',
                              markers=True, # Show markers on points
                              labels={'date': 'Date', 'mood_value': 'Mood Level'},
                              )
                fig.update_layout(
                    yaxis=dict(
                        tickvals=list(mood_options.values()),
                        ticktext=list(mood_options.keys()),
                        range=[0.5, 5.5] # Ensure all mood levels are visible
                    ),
                    xaxis_title=None, yaxis_title=None, # Cleaner axes
                    plot_bgcolor='rgba(0,0,0,0)', # Transparent background
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color="#e1e1e1" if st.session_state.theme == 'dark' else "#212529",
                    margin=dict(l=10, r=10, t=10, b=10) # Reduce margins
                )
                line_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'
                fig.update_traces(
                    line=dict(color=line_color, width=3),
                    marker=dict(color=line_color, size=8)
                )
                st.plotly_chart(fig, use_container_width=True)
            elif len(df_mood) == 1:
                # Indentation level 4 (inside 'elif')
                st.info(f"Logged '{df_mood.iloc[0]['mood_text']}' on {df_mood.iloc[0]['date'].strftime('%b %d, %H:%M')}. Need more data for a trend chart.")
            else:
                # Indentation level 4 (inside 'else')
                st.info("Log your mood to see trends here.")

            # Display recent raw logs
            st.markdown("---")
            st.subheader("🗒️ Latest Logs")
            # Indentation level 3 (back inside 'if st.session_state.mood_log')
            # Corrected loop start
            for entry in reversed(st.session_state.mood_log[-3:]): # Show newest first
                # Indentation level 4 (inside 'for' loop) - *** THIS IS THE FIX ***
                st.write(f"**{entry['date'].strftime('%b %d, %H:%M')}:** {entry['mood_text']}{ (' - *' + entry['notes'] + '*') if entry['notes'] else '' }")
# --- End of log_mood function ---

def display_welcome_message():
    # Indentation level 1
    if st.session_state.show_welcome:
        with st.container():
            # Indentation level 2
            primary_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'
            secondary_color = '#ffffff' if st.session_state.theme == 'dark' else '#343a40'
            st.markdown(
                f"""
                <div class='welcome-card'>
                    <span style="font-size: 4rem; display: block; margin-bottom: 1rem;">{PAGE_ICON}</span>
                    <h1 style="color: {primary_color}; margin-bottom: 0.5rem;">Welcome to {APP_NAME}</h1>
                    <p style="font-size: 1.3rem; color: {secondary_color}; margin-bottom: 1.5rem;">{APP_TAGLINE}</p>
                    <p style="font-size: 1.1rem; color: {secondary_color} opacity: 0.9;">
                        I'm here to help you explore early signs, gentle strategies, and supportive insights for mental wellness.
                        Ready to begin your reflective journey?
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Centered Button
            col1, col2, col3 = st.columns([1, 1.5, 1]) # Adjust column ratios for centering
            with col2:
                 # Indentation level 3
                if st.button("✨ Let's Begin Exploring ✨", key="dismiss_welcome", use_container_width=True):
                    # Indentation level 4
                    dismiss_welcome()
                    st.rerun()
# --- End of display_welcome_message function ---

# --- Main App Layout ---
# Header aligned with Icon
col1_header, col2_header = st.columns([0.15, 0.85])
with col1_header:
     icon(PAGE_ICON)
with col2_header:
    primary_color_header = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB' # Renamed variable
    st.markdown(f'<a href="https://vers3dynamics.io/" target="_blank" style="color: {primary_color_header}; text-decoration:none; font-weight: 600;"><h1>{PAGE_TITLE}</h1></a>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="opacity: 0.9;">{APP_NAME}: {APP_TAGLINE}</h3>', unsafe_allow_html=True)

st.divider() # Visual separation

# Initialize Groq client
try:
    # Ensure secrets are loaded correctly, especially in cloud environments
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("🚨 GROQ_API_KEY not found in secrets. Please add it to continue.")
        st.stop()
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {e}")
    st.stop()

# Sidebar Enhancements
with st.sidebar:
    sidebar_header_color = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2'
    st.markdown(f"<h2 style='color: {sidebar_header_color};'><span style='font-size: 1.5rem; vertical-align: middle;'>🛠️</span> Control Center</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Theme selector
    theme_selection = st.radio("🎨 Theme", ["🌞 Light", "🌙 Dark"], index=0 if st.session_state.theme == "light" else 1, horizontal=True, key="theme_selector")
    new_theme = "light" if theme_selection == "🌞 Light" else "dark"
    if st.session_state.theme != new_theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("---")

    # Model selection
    st.markdown(f"<h3 style='color: {sidebar_header_color}; font-size: 1.2rem;'>🧠 AI Model</h3>", unsafe_allow_html=True)
    # Use the actual selected model from session state for the default index if it exists
    current_model_index = list(models.keys()).index(st.session_state.selected_model) if st.session_state.selected_model in models else DEFAULT_MODEL_INDEX
    model_option = st.selectbox("Select Model", options=list(models.keys()), format_func=lambda x: f"{models[x]['name']}", index=current_model_index, label_visibility="collapsed", key="model_selector")
    if st.session_state.selected_model != model_option:
        st.session_state.selected_model = model_option
        # Optionally clear history or notify user on model change if desired
        # clear_chat_history() # Uncomment to clear chat on model change
        # st.rerun()

    # Model info Expander
    model_info = models[st.session_state.selected_model or list(models.keys())[DEFAULT_MODEL_INDEX]] # Use selected or default
    with st.expander("ℹ️ Model Details", expanded=False):
        st.markdown(f"**Tokens:** `{model_info['tokens']}`  \n"
                    f"**Developer:** _{model_info['developer']}_  \n"
                    f"**Use Case:** {model_info['description']}")

    st.markdown(f"<h3 style='color: {sidebar_header_color}; font-size: 1.2rem;'>🔧 Parameters</h3>", unsafe_allow_html=True)
    max_tokens = st.slider("Max Response Length (Tokens)", min_value=128, max_value=model_info["tokens"], value=min(2048, model_info["tokens"]), step=128, key="max_tokens_slider")
    temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="temp_slider")

    st.markdown("---")

    if st.button("🔄 Reset Conversation", use_container_width=True, key="reset_button"):
        clear_chat_history()
        st.rerun()

    # Audio Player - Enhanced Look
    st.markdown(f"<h3 style='color: {sidebar_header_color};'>🔊 Welcome Message</h3>", unsafe_allow_html=True)
    audio_filename = "ElevenLabs_2025-02-16T06_54_38_Amanda_gen_s50_sb75_se0_b_m2.mp3"
    # Robust path finding
    current_dir_audio = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(current_dir_audio, audio_filename)

    if os.path.exists(audio_path):
        try:
            audio_bytes = Path(audio_path).read_bytes()
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.warning(f"Could not load audio file: {e}")
    else:
         st.warning(f"Audio file not found: {audio_filename}")
    # Removed the play button, directly embedding the player is cleaner if file exists

    st.markdown("---")

    # Mood tracker function called here
    log_mood()

    st.markdown("---")

    # Quick prompts
    st.markdown(f"<h3 style='color: {sidebar_header_color};'>💡 Quick Start Prompts</h3>", unsafe_allow_html=True)
    quick_prompts = [
        "Early signs of anxiety?",
        "How to spot depression early?",
        "Self-care tips for stress?",
        "Explain biopsychosocial factors",
        "Early help for psychosis?" # Shortened prompts
    ]
    for i, prompt in enumerate(quick_prompts):
        if st.button(f"💬 {prompt}", key=f"qp_{i}", use_container_width=True):
            use_quick_prompt(prompt)
            st.rerun()

# --- Main Content Area ---
if st.session_state.show_welcome:
    display_welcome_message()
else:
    # Displaying the image centered if it exists
    if os.path.exists(IMAGE_PATH):
        col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
        with col_img2:
             # Check image path again, ensure it's relative to the script or use absolute path
            image_display_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_PATH)
            if os.path.exists(image_display_path):
                st.image(image_display_path, caption=IMAGE_CAPTION, width=300)
            else:
                 st.warning(f"Image not found at: {image_display_path}")

        st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # Chat history display
    # Filter out the system prompt for display
    display_messages = [msg for msg in st.session_state.messages if msg.get("role") != "system"]
    for message in display_messages:
        role = message.get("role", "unknown")
        avatar_icon = '💬' if role == "assistant" else '👤'
        with st.chat_message(role, avatar=avatar_icon):
            st.markdown(message.get("content", ""), unsafe_allow_html=True) # Allow basic HTML

    # --- Chat Input and Response Handling ---
    def generate_chat_responses(chat_completion):
        """Yields response chunks"""
        try:
            for chunk in chat_completion:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            st.error(f"Error during response streaming: {e}")
            yield " An error occurred while generating the response. "


    user_input = st.chat_input("Ask Mnemosyne anything about mental wellness...", key="chat_input")
    if user_input:
        st.session_state.chat_counter += 1
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message immediately
        with st.chat_message("user", avatar='👤'):
            st.markdown(user_input)

        # Generate and display assistant response
        with st.chat_message("assistant", avatar="💬"):
            placeholder = st.empty()
            full_response = ""
            loading_message = random.choice(LOADING_MESSAGES)
            loading_indicator_emoji = random.choice(LOADING_INDICATORS)

            # Show initial loading message with indicator
            placeholder.markdown(f"<div class='progress-message'><span class='progress-indicator'>{loading_indicator_emoji}</span> {loading_message}</div>", unsafe_allow_html=True)

            # Check for Easter egg trigger
            if "amanda" in user_input.lower() or "poem" in user_input.lower():
                # Add a slight delay for effect
                time.sleep(1)
                full_response = f"Ah, a whisper on the wind... perhaps this is what you seek? 💌\n\n---\n\n{POEM}"
                placeholder.markdown(full_response, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                # Normal response generation
                try:
                    # Use the selected model from session state
                    selected_model_key = st.session_state.selected_model or list(models.keys())[DEFAULT_MODEL_INDEX]

                    # Ensure messages being sent are in the correct format
                    messages_to_send = []
                    for msg in st.session_state.messages:
                         if msg.get("role") and msg.get("content"):
                              messages_to_send.append({"role": msg["role"], "content": msg["content"]})
                         else:
                              st.warning(f"Skipping invalid message format: {msg}")

                    if not messages_to_send:
                         st.error("No valid messages to send to the model.")
                         st.stop()


                    chat_completion = client.chat.completions.create(
                        model=selected_model_key,
                        messages=messages_to_send,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        stream=True
                    )

                    # Stream response with visual indicator updates
                    response_stream = generate_chat_responses(chat_completion)
                    for chunk in response_stream:
                        full_response += chunk
                        # Update placeholder with text and a subtle typing indicator
                        placeholder.markdown(full_response + "▌", unsafe_allow_html=True) # Use a block cursor indicator
                        # Optional: Small delay for smoother streaming appearance
                        # time.sleep(0.01)

                    # Final response without indicator
                    placeholder.markdown(full_response, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred while communicating with the AI: {e}")
                    full_response = "I seem to have encountered a hiccup. Could you please try rephrasing or asking again? 🙏"
                    placeholder.markdown(full_response) # Display error in placeholder

                # Add final assistant response to history ONLY IF IT'S NOT THE EASTER EGG
                if not ("amanda" in user_input.lower() or "poem" in user_input.lower()):
                     st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Rerun at the end of processing a user message to update the display cleanly
        st.rerun()


# --- Footer ---
st.divider()
footer_color = '#e1e1e1' if st.session_state.theme == 'dark' else '#495057'
link_color = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2'
st.markdown(
    f"""
    <div style='text-align: center; margin-top: 1rem; color: {footer_color}; opacity: 0.8; font-size: 0.9rem;'>
        © {time.strftime('%Y')} Vers3Dynamics •
        <a href="https://woodyard.dappling.network/" target="_blank" style="color: {link_color};">Privacy Policy</a> •
        <a href="https://vers3dynamics.io/titanic" target="_blank" style="color: {link_color};">Terms of Service</a> <br>
        <span style="font-size: 0.8rem;">Mnemosyne is an AI companion and does not provide medical advice. Please consult a qualified professional for diagnosis or treatment.</span>
    </div>
    """,
    unsafe_allow_html=True
)
