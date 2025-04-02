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
APP_TAGLINE = "Your Reflective Mental Wellness Companion 🌱" 

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

# --- System Prompt Function (No changes needed here) ---
def _get_system_prompt() -> str:
    # ... (keep your existing function) ...
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "system_prompt.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        # Using a shorter fallback here for brevity in the example
        return """You are Mnemosyne, an empathetic AI by Vers3Dynamics for mental wellness support."""
    except Exception as e:
        st.error(f"Error reading system prompt file: {e}")
        return """Fallback: You are Mnemosyne, here to support mental health awareness."""

# --- Greatly Enhanced CSS ---
def load_css(theme="light"):
    # Import Google Font
    font_family = "'Montserrat', sans-serif"
    secondary_font = "'Dancing Script', cursive" # Example decorative font

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
            border-radius: 15px; /* Apply consistent border-radius */
            box-shadow: 3px 0px 15px rgba(0,0,0,0.05); /* Subtle shadow */
        }}

         /* Input fields */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
            border-radius: 10px;
            padding: 10px 12px;
        }}
         /* Focus indicator */
        button:focus, select:focus, input:focus, textarea:focus {{
            outline-offset: 2px;
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
            [data-testid="stSidebar"] { background-color: #1a1a2e; }
             /* Chat Bubbles */
            .stChatMessage.user { background: linear-gradient(135deg, #483D8B 0%, #6A5ACD 100%); margin-left: 10%; }
            .stChatMessage.assistant { background: linear-gradient(135deg, #212940 0%, #2d3748 100%); border: 1px solid #483D8B; margin-right: 10%; }
            .stChatMessage * { color: #ffffff !important; }
             /* Buttons */
            div.stButton > button, .stDownloadButton > button { background: linear-gradient(45deg, #6A5ACD, #8A2BE2); color: white !important; }
             /* Progress message */
            .progress-message { color: #BE93FD; }
             /* Welcome Card */
            .welcome-card { background: linear-gradient(145deg, #1a1a2e 0%, #1f1f35 100%); border: 1px solid #483D8B; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); }
             /* Input fields */
            .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #2d3748; color: #e1e1e1; border: 1px solid #4a5568; }
             /* Focus */
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
            [data-testid="stSidebar"] { background-color: #ffffff; }
             /* Chat Bubbles */
            .stChatMessage.user { background: linear-gradient(135deg, #e7eaf6 0%, #d2dcfb 100%); margin-left: 10%; border: 1px solid #c7d1f7; }
            .stChatMessage.assistant { background: linear-gradient(135deg, #fdfdff 0%, #f0f4ff 100%); border: 1px solid #dcdcdc; margin-right: 10%; }
            .stChatMessage * { color: #212529 !important; }
             /* Buttons */
            div.stButton > button, .stDownloadButton > button { background: linear-gradient(45deg, #9370DB, #B886FA); color: white !important; }
             /* Progress message */
            .progress-message { color: #8A2BE2; }
             /* Welcome Card */
            .welcome-card { background: linear-gradient(145deg, #ffffff 0%, #f5f7fa 100%); border: 1px solid #e0e0e0; }
             /* Input fields */
            .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #ffffff; color: #212529; border: 1px solid #ced4da; }
             /* Focus */
            button:focus, select:focus, input:focus, textarea:focus { outline: 3px solid #B886FA !important; }
             /* Links */
            a { color: #8A2BE2; }
            a:hover { color: #6A5ACD; }
        </style>
        """
    st.markdown(common_css + theme_css, unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE, initial_sidebar_state="expanded")

# --- Session State Initialization (Added mood_chart_data) ---
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
if "audio_played" not in st.session_state:
    st.session_state.audio_played = False

# Apply CSS based on session state theme
load_css(st.session_state.theme)

# --- Enhanced UI Functions ---
def icon(emoji: str):
    # Slightly smaller icon for better alignment
    st.write(f'<span style="font-size: 60px; line-height: 1; vertical-align: middle;">{emoji}</span>', unsafe_allow_html=True)

def clear_chat_history():
    st.session_state.messages = [{"role": "system", "content": _get_system_prompt()}]
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
    return prompt

# --- Model Definitions (No changes needed) ---
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
    with st.sidebar.expander("📊 Mood Tracker", expanded=False): # Added chart icon
        mood_options = {"Great": 5, "Good": 4, "Okay": 3, "Low": 2, "Very Low": 1}
        mood_selection = st.selectbox("How are you feeling today?", options=list(mood_options.keys()))
        notes = st.text_area("Any notes? (e.g., sleep, stress)", height=80) # Slightly smaller

        if st.button("📝 Log Mood"): # Added icon
            mood_value = mood_options[mood_selection]
            st.session_state.mood_log.append({
                "date": pd.to_datetime(time.strftime("%Y-%m-%d %H:%M")), # Use datetime object
                "mood_text": mood_selection,
                "mood_value": mood_value,
                "notes": notes
            })
            st.success("Mood logged! 🌱")
            st.rerun() # Rerun to update chart immediately

        if st.session_state.mood_log:
            st.markdown("---") # Visual separator
            st.subheader("📈 Recent Mood Trend")

            # Prepare data for chart
            df_mood = pd.DataFrame(st.session_state.mood_log)
            df_mood = df_mood.sort_values(by="date")

            # Create Plotly chart
            if len(df_mood) >= 2: # Need at least 2 points for a line chart
                 fig = px.line(df_mood, x='date', y='mood_value',
                              markers=True, # Show markers on points
                              labels={'date': 'Date', 'mood_value': 'Mood Level'},
                              # title="Mood Over Time" # Title removed, using subheader
                              )
                 fig.update_layout(yaxis=dict(tickvals=list(mood_options.values()), ticktext=list(mood_options.keys())), # Custom Y-axis labels
                                   xaxis_title=None, yaxis_title=None, # Cleaner axes
                                   plot_bgcolor='rgba(0,0,0,0)', # Transparent background
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   font_color="#e1e1e1" if st.session_state.theme == 'dark' else "#212529",
                                   margin=dict(l=10, r=10, t=10, b=10)) # Reduce margins
                 fig.update_traces(line=dict(color='#BE93FD' if st.session_state.theme == 'dark' else '#9370DB', width=3),
                                   marker=dict(color='#BE93FD' if st.session_state.theme == 'dark' else '#9370DB', size=8))
                 st.plotly_chart(fig, use_container_width=True)
            elif len(df_mood) == 1:
                st.write(f"Logged '{df_mood.iloc[0]['mood_text']}' on {df_mood.iloc[0]['date'].strftime('%b %d, %H:%M')}. Need more data for a trend chart.")
            else:
                st.write("Log your mood to see trends here.")

            # Display recent raw logs
            st.markdown("---")
            st.subheader("🗒️ Latest Logs")
            for entry in reversed(st.session_state.mood_log[-3:]): # Show newest first
                 st.write(f"**{entry['date'].strftime('%b %d, %H:%M')}:** {entry['mood_text']} {f'- *{entry["notes"]}*' if entry['notes'] else ''}")


def display_welcome_message():
    if st.session_state.show_welcome:
        with st.container():
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
                if st.button("✨ Let's Begin Exploring ✨", key="dismiss_welcome", use_container_width=True):
                    dismiss_welcome()
                    st.rerun()


# --- Main App Layout ---
# Header aligned with Icon
col1_header, col2_header = st.columns([0.15, 0.85])
with col1_header:
     icon(PAGE_ICON)
with col2_header:
    primary_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'
    st.markdown(f'<a href="https://vers3dynamics.io/" style="color: {primary_color}; text-decoration:none; font-weight: 600;"><h1>{PAGE_TITLE}</h1></a>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="opacity: 0.9;">{APP_NAME}: {APP_TAGLINE}</h3>', unsafe_allow_html=True)

st.divider() # Visual separation

# Initialize Groq client (No changes needed)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("🚨 GROQ_API_KEY not found in secrets. Please add it to continue.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {e}")
    st.stop()

# Sidebar Enhancements
with st.sidebar:
    sidebar_header_color = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2'
    st.markdown(f"<h2 style='color: {sidebar_header_color};'><span style='font-size: 1.5rem; vertical-align: middle;'>🛠️</span> Control Center</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Theme selector
    theme = st.radio("🎨 Theme", ["🌞 Light", "🌙 Dark"], index=0 if st.session_state.theme == "light" else 1, horizontal=True)
    new_theme = "light" if theme == "🌞 Light" else "dark"
    if st.session_state.theme != new_theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("---")

    # Model selection
    st.markdown(f"<h3 style='color: {sidebar_header_color}; font-size: 1.2rem;'>🧠 AI Model</h3>", unsafe_allow_html=True)
    model_option = st.selectbox("Select Model", options=list(models.keys()), format_func=lambda x: f"{models[x]['name']}", index=DEFAULT_MODEL_INDEX, label_visibility="collapsed")
    if st.session_state.selected_model != model_option:
        st.session_state.selected_model = model_option
        # Optionally clear history or notify user on model change if desired

    # Model info Expander
    model_info = models[model_option]
    with st.expander("ℹ️ Model Details", expanded=False):
        st.markdown(f"**Tokens:** `{model_info['tokens']}`  \n"
                    f"**Developer:** _{model_info['developer']}_  \n"
                    f"**Use Case:** {model_info['description']}")

    st.markdown(f"<h3 style='color: {sidebar_header_color}; font-size: 1.2rem;'>🔧 Parameters</h3>", unsafe_allow_html=True)
    max_tokens = st.slider("Max Response Length (Tokens)", 512, model_info["tokens"], min(2048, model_info["tokens"]), 512)
    temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.7, 0.1)

    st.markdown("---")

    if st.button("🔄 Reset Conversation", use_container_width=True): # Added icon
        clear_chat_history()
        st.rerun()

    # Audio Player - Enhanced Look
    st.markdown(f"<h3 style='color: {sidebar_header_color};'>🔊 Welcome Message</h3>", unsafe_allow_html=True)
    audio_filename = "ElevenLabs_2025-02-16T06_54_38_Amanda_gen_s50_sb75_se0_b_m2.mp3"
    audio_path = os.path.join(os.path.dirname(__file__), audio_filename)

    if os.path.exists(audio_path):
        audio_bytes = Path(audio_path).read_bytes()
        st.audio(audio_bytes, format="audio/mp3")
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
        if st.button(f"💬 {prompt}", key=f"qp_{i}", use_container_width=True): # Added icon
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
            st.image(IMAGE_PATH, caption=IMAGE_CAPTION, width=300)
        st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # Chat history display
    for message in st.session_state.messages[1:]:  # Skip system prompt
        avatar_icon = '💬' if message["role"] == "assistant" else '👤' # Different avatars
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"], unsafe_allow_html=True) # Allow basic HTML in responses if needed

    # --- Chat Input and Response Handling ---
    def generate_chat_responses(chat_completion):
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    user_input = st.chat_input("Ask Mnemosyne anything about mental wellness...") # More descriptive placeholder
    if user_input:
        st.session_state.chat_counter += 1
        st.session_state.messages.append({"role": "user", "content": user_input})
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
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                # Normal response generation
                try:
                    # Filter messages to prevent sending system prompt if not desired by API, or keep it
                    messages_to_send = st.session_state.messages

                    chat_completion = client.chat.completions.create(
                        model=model_option,
                        messages=messages_to_send,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        stream=True
                    )

                    # Stream response with visual indicator updates
                    indicator_counter = 0
                    for chunk in generate_chat_responses(chat_completion):
                        full_response += chunk
                        indicator_counter += 1
                        # Update placeholder with text and a subtle typing indicator
                        current_indicator = "..." if indicator_counter % 3 == 0 else (".." if indicator_counter % 3 == 1 else ".")
                        placeholder.markdown(full_response + current_indicator, unsafe_allow_html=True)
                         # Optional: Small delay for smoother streaming appearance
                        time.sleep(0.01)

                    # Final response without indicator
                    placeholder.markdown(full_response, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    full_response = "I seem to have encountered a hiccup. Could you please try rephrasing or asking again? 🙏"
                    placeholder.markdown(full_response)

                # Add final response to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

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
