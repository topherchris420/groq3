# -*- coding: utf-8 -*-
import streamlit as st
from typing import Generator, Optional, Dict, Union
from groq import Groq
import os
import random
from pathlib import Path
import time
import base64
import pandas as pd
import plotly.express as px

# --- Configuration ---
PAGE_TITLE = "Vers3Dynamics"
PAGE_ICON = "🧠"
script_dir_config = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join("images", "image_fx_ (2).jpg")
FULL_IMAGE_PATH = os.path.join(script_dir_config, IMAGE_PATH)
IMAGE_CAPTION = "You Are the Master of Your Fate"
DEFAULT_MODEL_INDEX = 5 # Index in the models list below
APP_NAME = "Mnemosyne"
APP_TAGLINE = "Your Reflective Mental Wellness Companion 🌿"

# Poem for Amanda (Easter egg)
POEM = """
amanda,
... (Poem content remains unchanged) ...
"""

# Enhanced loading messages
LOADING_MESSAGES = [
    "Gathering calming thoughts... 🧘‍♀️💭", "Weaving threads of insight... 🧶✨",
    "Consulting the echoes of memory... 🌌👂", "Brewing a supportive perspective... ☕️🌿",
    "Tuning into wellness frequencies... 🎶💖", "Planting seeds of understanding... 🌱💡",
    "Polishing gems of wisdom... 💎🧠", "Navigating the mindscape with care... 🗺️❤️",
    "Unfolding layers of awareness... 📜🦋", "Crafting a mindful response...✍️🧘‍♂️"
]
LOADING_INDICATORS = ["⏳", "💭", "💡", "✨", "🌀", "🔹", "🔸"]

# --- Visual Elements & Animations ---
def get_base64_encoded_image(image_path):
    # (Keep function as defined previously)
    try:
        with open(image_path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError: st.warning(f"Image file not found: {image_path}"); return None

BRAIN_SVG = """<svg width="80" height="80" ... (SVG content) ... </svg>""" # Keep SVG definition
PULSE_ANIMATION = """ @keyframes pulse { ... } ... """ # Keep CSS animation definitions

# --- Get System Prompt ---
def _get_system_prompt() -> str:
    # (Keep function as defined previously)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "system_prompt.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file: return file.read()
    except FileNotFoundError: st.warning("system_prompt.txt not found."); return """Default prompt..."""
    except Exception as e: st.error(f"Error reading prompt: {e}"); return """Fallback prompt."""

# --- Enhanced CSS loader ---
def load_css(theme="light"):
    # (Keep function as defined previously, including PULSE_ANIMATION injection)
    st.markdown(f'<style>{PULSE_ANIMATION}</style>', unsafe_allow_html=True)
    common_base = """ <style> ... </style> """ # Common CSS
    st.markdown(common_base, unsafe_allow_html=True)
    if theme == "dark": st.markdown(""" <style> /* Dark theme */ ... </style> """, unsafe_allow_html=True)
    else: st.markdown(""" <style> /* Light theme */ ... </style> """, unsafe_allow_html=True)

# --- *** MOVED MODEL DEFINITIONS HERE *** ---
models = {
    # Define your models dictionary here, before Session State Init
    "llama-3.3-70b-versatile": {"name": "Llama-3.3-70b-Versatile", "tokens": 8192, "developer": "Meta", "description": "Latest Llama model for versatile, detailed medical responses"},
    "Llama3-8b-8192": {"name": "Llama3-8b-8192", "tokens": 8192, "developer": "Meta", "description": "Efficient Llama model for fast, accurate medical insights"},
    "mistral-saba-24b": {"name": "Mistral-Saba-24b", "tokens": 32768, "developer": "Mistral", "description": "Specialized model with large context for in-depth narratives"},
    "mixtral-8x22b-instruct": {"name": "Mixtral-8x22b-Instruct", "tokens": 65536, "developer": "Mistral", "description": "Advanced Mixtral for complex medical analysis"},
    "gemma-2-27b-it": {"name": "Gemma-2-27b-IT", "tokens": 8192, "developer": "Google", "description": "Updated Gemma model for general-purpose medical dialogue"},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1b-Preview", "tokens": 4096, "developer": "Meta", "description": "Lightweight Llama model for quick responses and basic assistance"},
}
# --- *** END OF MOVED MODEL DEFINITIONS *** ---


# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE, initial_sidebar_state="expanded")

# --- Session State Initialization ---
# Now this section comes *after* 'models' is defined
st.session_state.setdefault("messages", [{"role": "system", "content": _get_system_prompt()}])
# Ensure default model index is valid using the now-defined 'models'
available_models = list(models.keys())
if DEFAULT_MODEL_INDEX >= len(available_models):
    actual_default_index = 0
    st.warning(f"Default model index {DEFAULT_MODEL_INDEX} out of bounds. Using index 0.")
else:
    actual_default_index = DEFAULT_MODEL_INDEX
# Set the default selected model using the key from the available_models list
st.session_state.setdefault("selected_model", available_models[actual_default_index])
st.session_state.setdefault("chat_counter", 0)
st.session_state.setdefault("show_welcome", True)
st.session_state.setdefault("theme", "light")
st.session_state.setdefault("mood_log", [])
st.session_state.setdefault("audio_played", False)
st.session_state.setdefault("wellness_score", 75)
st.session_state.setdefault("animation_enabled", True)
# --- End of Session State Initialization ---

# Apply CSS
load_css(st.session_state.theme)

# --- UI Functions ---
# (Keep icon, brain_animation, clear_chat_history, dismiss_welcome, use_quick_prompt,
#  wellness_gauge, log_mood, display_welcome_message functions as defined previously)
def icon(emoji: str):
    animation_class = "float" if st.session_state.get("animation_enabled", True) else ""
    st.write(f'<div class="{animation_class}" style="text-align: center;"><span style="font-size: 60px; line-height: 1;">{emoji}</span></div>', unsafe_allow_html=True)

def brain_animation():
    animation_class = "pulse" if st.session_state.get("animation_enabled", True) else ""
    st.markdown(f'<div class="{animation_class}" style="text-align: center;">{BRAIN_SVG}</div>', unsafe_allow_html=True)

def clear_chat_history():
    system_prompt = st.session_state.messages[0] if st.session_state.messages and st.session_state.messages[0]['role'] == 'system' else {"role": "system", "content": _get_system_prompt()}
    st.session_state.messages = [system_prompt]
    st.session_state.chat_counter = 0; st.session_state.show_welcome = True
    st.session_state.audio_played = False; st.session_state.mood_log = []

def dismiss_welcome(): st.session_state.show_welcome = False

def use_quick_prompt(prompt_text):
    st.session_state.show_welcome = False
    if not st.session_state.messages or st.session_state.messages[-1].get("content") != prompt_text:
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        st.session_state.chat_counter += 1

def wellness_gauge(score):
    if st.session_state.theme == 'dark': color = "#4CAF50" if score > 70 else "#FFC107" if score > 40 else "#F44336"; track_color="#444"; text_color="#e1e1e1"
    else: color = "#66BB6A" if score > 70 else "#FFA726" if score > 40 else "#EF5350"; track_color="#e0e0e0"; text_color="#333"
    animate_tag = '<animate attributeName="stroke-dashoffset" from="157" to="{}" dur="1s" fill="freeze" />'.format(157 - (score/100) * 157) if st.session_state.get("animation_enabled", True) else ""
    gauge_html = f"""<div style="width:100%;text-align:center;padding:10px 0;"><svg width="120" height="65" viewBox="0 0 120 65"><path d="M10 60 A50 50 0 0 1 110 60" stroke="{track_color}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M10 60 A50 50 0 0 1 110 60" stroke="{color}" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="157" stroke-dashoffset="{157 - (score/100) * 157}">{animate_tag}</path><text x="60" y="55" text-anchor="middle" font-size="18" font-weight="bold" fill="{text_color}">{score}%</text></svg><div style="font-size:14px;margin-top:-5px;color:{text_color};opacity:0.9;">Wellness</div></div>"""
    st.markdown(gauge_html, unsafe_allow_html=True)

def log_mood():
    with st.sidebar.expander("📊 Mood Tracker", expanded=False):
        mood_options = {"Great": 5, "Good": 4, "Okay": 3, "Low": 2, "Very Low": 1}
        mood_selection = st.selectbox("Feeling today?", options=list(mood_options.keys()), key="mood_select")
        notes = st.text_area("Notes?", height=80, key="mood_notes")
        if st.button("📝 Log Mood", use_container_width=True, key="log_mood_button"):
            mood_value = mood_options[mood_selection]
            st.session_state.mood_log.append({"date":pd.to_datetime(time.strftime("%Y-%m-%d %H:%M")), "mood_text":mood_selection, "mood_value":mood_value, "notes":notes})
            st.success("Mood logged! 🌱")
        if st.session_state.mood_log:
            st.markdown("---"); st.subheader("📈 Mood Trend")
            df_mood = pd.DataFrame(st.session_state.mood_log); df_mood['date']=pd.to_datetime(df_mood['date']); df_mood=df_mood.sort_values(by="date")
            if len(df_mood) >= 2:
                fig = px.line(df_mood, x='date', y='mood_value', markers=True, labels={'date':'Date','mood_value':'Mood Level'})
                fig.update_layout(yaxis=dict(tickvals=list(mood_options.values()),ticktext=list(mood_options.keys()),range=[0.5,5.5]),xaxis_title=None,yaxis_title=None,plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',font_color="#e1e1e1" if st.session_state.theme == 'dark' else "#212529",margin=dict(l=5,r=5,t=5,b=5))
                line_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'; fig.update_traces(line=dict(color=line_color,width=2),marker=dict(color=line_color,size=6))
                st.plotly_chart(fig, use_container_width=True)
            elif len(df_mood)==1: st.info(f"Logged '{df_mood.iloc[0]['mood_text']}'. Need more data.")
            else: st.info("Log mood to see trends.")
            st.markdown("---"); st.subheader("🗒️ Latest Logs")
            for entry in reversed(st.session_state.mood_log[-3:]):
                note_str = f" - *{entry['notes']}*" if entry['notes'] else ""
                mood_card_class = "mood-card"
                st.markdown(f"<div class='{mood_card_class}'>**{entry['date'].strftime('%b %d, %H:%M')}:** {entry['mood_text']}{note_str}</div>", unsafe_allow_html=True)

def display_welcome_message():
    if st.session_state.show_welcome:
        with st.container():
            primary_color = '#BE93FD' if st.session_state.theme == 'dark' else '#9370DB'; secondary_color = '#ffffff' if st.session_state.theme == 'dark' else '#343a40'
            st.markdown(f"""<div class='welcome-card fade-in'><div class="float" style="margin-bottom:1rem;"><span style="font-size:4rem;display:block;">{PAGE_ICON}</span></div><h1 class="header-gradient" style="margin-bottom:0.5rem;">Welcome to {APP_NAME}</h1><p style="font-size:1.3rem;color:{secondary_color};margin-bottom:1.5rem;">{APP_TAGLINE}</p><p style="font-size:1.1rem;color:{secondary_color};opacity:0.9;">Your space for reflection and early awareness in mental wellness. Ready to explore?</p></div>""", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                if st.button("✨ Let's Begin Exploring ✨", key="dismiss_welcome_btn", use_container_width=True): dismiss_welcome(); st.rerun()

# --- Main App Layout ---
# (Keep Header section as previously defined)
col_icon, col_title = st.columns([0.1, 0.9])
with col_icon: icon(PAGE_ICON)
with col_title:
    primary_color_header = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2'
    st.markdown(f'<a href="https://vers3dynamics.io/" target="_blank" style="color:{primary_color_header};text-decoration:none;font-weight:600;"><h1 class="header-gradient">{PAGE_TITLE}</h1></a>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="opacity:0.9;">{APP_NAME}: {APP_TAGLINE}</h3>', unsafe_allow_html=True)
st.divider()

# Initialize Groq Client
# (Keep Groq client initialization as previously defined)
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY")
    if not groq_api_key: raise ValueError("GROQ_API_KEY missing.")
    client = Groq(api_key=groq_api_key)
except Exception as e: st.error(f"🚨 Groq Init Error: {e}"); st.stop()

# --- Sidebar ---
# (Keep Sidebar layout and elements as previously defined, including the corrected quick prompts loop)
with st.sidebar:
    sidebar_header_color = '#BE93FD' if st.session_state.theme == 'dark' else '#8A2BE2'
    st.markdown(f"<h2 style='color:{sidebar_header_color};text-align:center;'>Controls & Insights</h2>", unsafe_allow_html=True)
    brain_animation(); wellness_gauge(st.session_state.wellness_score); st.markdown("---")

    theme_selection = st.radio("🎨 Theme",["🌞 Light","🌙 Dark"],index=0 if st.session_state.theme=="light" else 1,horizontal=True,key="theme_selector")
    new_theme="light" if theme_selection=="🌞 Light" else "dark"
    if st.session_state.theme != new_theme: st.session_state.theme = new_theme; st.rerun()
    st.markdown("---")

    st.markdown(f"<h3 style='color:{sidebar_header_color};'>🧠 AI Configuration</h3>", unsafe_allow_html=True)
    current_model_idx = available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else actual_default_index
    model_option = st.selectbox("Model", options=available_models, format_func=lambda x:f"{models[x]['name']}", index=current_model_idx, label_visibility="collapsed", key="model_selector")
    if st.session_state.selected_model != model_option: st.session_state.selected_model = model_option

    model_info = models[st.session_state.selected_model]
    with st.expander("ℹ️ Model Details"): st.markdown(f"**Tokens:** `{model_info['tokens']}` | **Dev:** _{model_info['developer']}_"); st.caption(f"Use Case: {model_info['description']}")

    max_tokens = st.slider("Max Response Length", 128, model_info["tokens"], min(2048,model_info["tokens"]), 128, key="max_tokens_slider")
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1, key="temp_slider")
    st.markdown("---")

    if st.button("🔄 Reset Conversation", use_container_width=True, key="reset_button"): clear_chat_history(); st.rerun()
    st.markdown("---")

    # Audio Player
    st.markdown(f"<h3 style='color:{sidebar_header_color};'>🔊 Welcome Message</h3>", unsafe_allow_html=True)
    audio_filename = "ElevenLabs_2025-02-16T06_54_38_Amanda_gen_s50_sb75_se0_b_m2.mp3"
    full_audio_path = os.path.join(script_dir_config, audio_filename)
    if os.path.exists(full_audio_path):
        try: st.audio(Path(full_audio_path).read_bytes(), format="audio/mp3")
        except Exception as e: st.warning(f"Audio load error: {e}")
    else: st.warning(f"Audio file missing: {audio_filename}")
    st.markdown("---")

    log_mood() # Mood tracker function call
    st.markdown("---")

    # Quick Prompts Loop (Corrected indentation already applied in previous step)
    st.markdown(f"<h3 style='color:{sidebar_header_color};'>💡 Quick Prompts</h3>", unsafe_allow_html=True)
    quick_prompts = ["Early signs of anxiety?","Spotting depression early?","Self-care for stress?","Explain biopsychosocial factors","Early help for psychosis?"]
    for i, prompt in enumerate(quick_prompts):
        if st.button(f"💬 {prompt}", key=f"qp_{i}", use_container_width=True):
            use_quick_prompt(prompt)
            st.rerun() # Rerun needed to process quick prompt

# --- Main Chat Area ---
# (Keep Main Chat Area layout and logic as previously defined)
if st.session_state.show_welcome:
    display_welcome_message()
else:
    if os.path.exists(FULL_IMAGE_PATH):
        col_img1, col_img2, col_img3 = st.columns([1,1,1])
        with col_img2: st.image(FULL_IMAGE_PATH, caption=IMAGE_CAPTION, width=300)
        st.markdown("<br>", unsafe_allow_html=True)

    message_container = st.container()
    with message_container:
        display_messages = [msg for msg in st.session_state.messages if msg.get("role") != "system"]
        for message in display_messages:
            role = message.get("role", "unknown"); avatar = '💬' if role == "assistant" else '👤'
            with st.chat_message(role, avatar=avatar): st.markdown(message.get("content", ""), unsafe_allow_html=True)

    # Chat Input
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    user_input = st.chat_input("Ask Mnemosyne about mental wellness...", key="chat_input")
    st.markdown('</div>', unsafe_allow_html=True)

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun() # Rerun to display user message and trigger response generation

# --- Assistant Response Generation (After Rerun) ---
if (not st.session_state.show_welcome and st.session_state.messages and st.session_state.messages[-1].get("role") == "user"):
    last_user_message = st.session_state.messages[-1].get("content", "")
    with message_container: # Display in the same container
        with st.chat_message("assistant", avatar="💬"):
            placeholder = st.empty(); full_response = ""
            loading_message = random.choice(LOADING_MESSAGES); loading_indicator = random.choice(LOADING_INDICATORS)
            placeholder.markdown(f"<div class='progress-message'><span class='pulse'>{loading_indicator}</span>  {loading_message}</div>", unsafe_allow_html=True)

            if "amanda" in last_user_message.lower() or "poem" in last_user_message.lower():
                time.sleep(1); full_response = f"Ah, for Amanda... 💌\n\n---\n\n{POEM}"
                placeholder.markdown(full_response, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": "Displayed poem."}) # Log simplified response
            else:
                try:
                    selected_model_key = st.session_state.selected_model
                    messages_to_send=[{"role":m["role"],"content":m["content"]} for m in st.session_state.messages if m.get("role") and m.get("content")]
                    if not messages_to_send: raise ValueError("No valid messages.")

                    chat_completion = client.chat.completions.create(model=selected_model_key,messages=messages_to_send,max_tokens=max_tokens,temperature=temperature,stream=True)
                    response_stream = generate_chat_responses(chat_completion)
                    for chunk in response_stream:
                        full_response += chunk; placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                    placeholder.markdown(full_response, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"AI Error: {e}", icon="🤖")
                    full_response = "Connection issue. Please try again. 🙏"
                    placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Footer ---
# (Keep Footer as previously defined)
st.markdown("---")
footer_color = '#d1d1e1' if st.session_state.theme == 'dark' else '#555'
link_color = '#CDB4DB' if st.session_state.theme == 'dark' else '#8A2BE2'
st.markdown(f"""<div style='text-align:center;margin-top:1.5rem;padding-bottom:1.5rem;color:{footer_color};opacity:0.85;font-size:0.9rem;'>© {time.strftime('%Y')} Vers3Dynamics • <a href="https://woodyard.dappling.network/" target="_blank" style="color:{link_color};">Privacy</a> • <a href="https://vers3dynamics.io/titanic" target="_blank" style="color:{link_color};">Terms</a> <br><span style="font-size:0.8rem;display:block;margin-top:0.5rem;">Disclaimer: AI assistant for informational purposes only. Not medical advice.</span></div>""", unsafe_allow_html=True)
