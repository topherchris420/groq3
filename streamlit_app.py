import streamlit as st
from typing import Generator, Optional, Dict, Union
from groq import Groq
import os
import random
from pathlib import Path

# --- Configuration ---
PAGE_TITLE = "Vers3Dynamics"
PAGE_ICON = "👩‍⚕️"  # Changed to brain emoji for mental health focus
IMAGE_PATH = os.path.join("images", "image_fx_ (2).jpg") 
IMAGE_CAPTION = "You Are the Master of Your Fate"
DEFAULT_MODEL_INDEX = 2
APP_NAME = "Mnemosyne"
APP_TAGLINE = "Early Intervention Mental Health Companion 🌿"  # Updated tagline

# Add animated loading messages focused on mental health
LOADING_MESSAGES = [
    "Analyzing mental health patterns... 🧠",
    "Processing longitudinal data insights... 📊",
    "Identifying early intervention options... 🔍",
    "Reviewing research on anxiety indicators... 📋",
    "Correlating psychological and social factors... 🔄",
    "Examining depression early warning signs... 📉",
    "Analyzing mental wellness trajectories... 📈",
    "Integrating biological, psychological, and social factors... 🧬",
    "Computing evidence-based intervention insights... 💭",
    "Reviewing early psychosis research findings... 🔎"
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
        # Provide a fallback system prompt with mental health focus
        return """You are Mnemosyne, a mental health AI assistant developed by Vers3Dynamics. 
        Your primary goal is to help identify early signs of anxiety, depression, and psychosis, 
        and to suggest evidence-based early interventions. You understand that mental health conditions 
        are complex with many interconnecting biological, psychological, and social factors. 
        Provide supportive, empathetic guidance while emphasizing early intervention strategies. 
        Never diagnose but help users understand potential warning signs that merit professional attention."""
    except Exception as e:
        st.error(f"Error reading system prompt file: {e}")
        return """You are Mnemosyne, a mental health AI assistant developed by Vers3Dynamics. 
        Your primary goal is to help identify early signs of anxiety, depression, and psychosis, 
        and to suggest evidence-based early interventions. You understand that mental health conditions 
        are complex with many interconnecting biological, psychological, and social factors. 
        Provide supportive, empathetic guidance while emphasizing early intervention strategies. 
        Never diagnose but help users understand potential warning signs that merit professional attention."""

# --- Mobile-optimized CSS ---
def load_css(theme="light"):
    if theme == "dark":
        st.markdown("""
        <style>
            /* Dark Theme with improved mobile visibility */
            .stApp {
                background-color: #1a1a2e;
                color: #ffffff !important;
            }
            
            /* Increased font size for all text on mobile */
            @media (max-width: 768px) {
                body, p, li, div, span {
                    font-size: 16px !important;
                    line-height: 1.5 !important;
                }
                h1 { font-size: 24px !important; }
                h2 { font-size: 22px !important; }
                h3 { font-size: 20px !important; }
                .stMarkdown p { 
                    font-size: 16px !important;
                    color: #ffffff !important;
                }
            }
            
            /* Improve Chat Messages contrast for mobile */
            .stChatMessage {
                border-radius: 20px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            
            .stChatMessage.user {
                background: linear-gradient(135deg, #4B0082 0%, #8A2BE2 100%);
                margin-left: 10%;  /* Reduced margin for mobile */
                color: white !important;
            }
            
            .stChatMessage.assistant {
                background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
                margin-right: 10%;  /* Reduced margin for mobile */
                color: #ffffff !important;
                border: 1px solid #4B0082;
            }
            
            /* Force white text for all chat messages in dark mode */
            .stChatMessage .stMarkdown, 
            .stChatMessage .stMarkdown p,
            .stChatMessage .stMarkdown li,
            .stChatMessage .stMarkdown a {
                color: #ffffff !important;
            }
            
            /* Ensure code blocks have proper contrast */
            .stChatMessage code {
                background-color: #2d2d3a !important;
                color: #f8f8f2 !important;
                padding: 0.2em 0.4em !important;
                border-radius: 3px !important;
                font-size: 85% !important;
            }
            
            /* Buttons */
            div.stButton > button:first-child {
                background: linear-gradient(45deg, #4B0082, #8A2BE2);
                color: white !important;
                border-radius: 25px;
                padding: 0.75rem 1.25rem;  /* Larger tap targets for mobile */
                border: none;
                font-size: 16px !important;  /* Larger text for mobile */
            }
            
            /* Loading animation */
            .progress-message {
                color: #BA55D3;
                font-weight: bold;
                font-size: 16px !important;
            }
            
            /* Welcome Card mobile optimization */
            .welcome-card {
                text-align: center; 
                padding: 1.5rem;  /* Adjusted padding for mobile */
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border-radius: 20px; 
                margin: 1.5rem 0; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                border: 1px solid #4B0082;
            }
            
            /* Info Box */
            .stInfo {
                background: #16213e;
                color: #ffffff !important;
                border: 1px solid #4B0082;
                border-radius: 10px;
            }
            
            .stInfo * {
                color: #ffffff !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:  # Light theme
        st.markdown("""
        <style>
            /* Light Theme with improved mobile visibility */
            .stApp {
                background-color: #f5f7fa;
                color: #000000 !important;
            }
            
            /* Increased font size for all text on mobile */
            @media (max-width: 768px) {
                body, p, li, div, span {
                    font-size: 16px !important;
                    line-height: 1.5 !important;
                }
                h1 { font-size: 24px !important; }
                h2 { font-size: 22px !important; }
                h3 { font-size: 20px !important; }
                .stMarkdown p { 
                    font-size: 16px !important;
                    color: #000000 !important;
                }
            }
            
            /* Improve Chat Messages contrast for mobile */
            .stChatMessage {
                border-radius: 20px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .stChatMessage.user {
                background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
                margin-left: 10%;  /* Reduced margin for mobile */
                color: #000000 !important;
            }
            
            .stChatMessage.assistant {
                background: linear-gradient(135deg, #F0F8FF 0%, #E6E6FA 100%);
                margin-right: 10%;  /* Reduced margin for mobile */
                border: 1px solid #D8BFD8;
                color: #000000 !important;
            }
            
            /* Force black text for all chat messages in light mode */
            .stChatMessage .stMarkdown, 
            .stChatMessage .stMarkdown p,
            .stChatMessage .stMarkdown li,
            .stChatMessage .stMarkdown a {
                color: #000000 !important;
            }
            
            /* Ensure code blocks have proper contrast */
            .stChatMessage code {
                background-color: #f0f0f0 !important;
                color: #000000 !important;
                padding: 0.2em 0.4em !important;
                border-radius: 3px !important;
                font-size: 85% !important;
            }
            
            /* Buttons */
            div.stButton > button:first-child {
                background: linear-gradient(45deg, #9370DB, #DA70D6);
                color: black !important;
                border-radius: 25px;
                padding: 0.75rem 1.25rem;  /* Larger tap targets for mobile */
                border: none;
                font-size: 16px !important;  /* Larger text for mobile */
            }
            
            /* Loading animation */
            .progress-message {
                color: #9370DB;
                font-weight: bold;
                font-size: 16px !important;
            }
            
            /* Welcome Card mobile optimization */
            .welcome-card {
                text-align: center; 
                padding: 1.5rem;  /* Adjusted padding for mobile */
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
                border-radius: 20px; 
                margin: 1.5rem 0; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border: 1px solid #D8BFD8;
                color: #000000;
            }
            
            /* Make sure text is black in the info box */
            .stInfo, .stInfo * {
                color: #000000 !important;
            }
            
            /* Ensure any links are visible but distinguished */
            a, a:visited {
                color: #9370DB !important;
                font-weight: bold !important;
            }
        </style>
        """, unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(page_icon=PAGE_ICON, layout="wide", page_title=PAGE_TITLE)

# --- Initialize Session State ---
if "messages" not in st.session_state:
    system_prompt = _get_system_prompt()
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Apply CSS based on theme
load_css(st.session_state.theme)

# --- UI Functions ---
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

def clear_chat_history():
    """Clears chat history and resets to the initial system message."""
    system_prompt = _get_system_prompt()
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.chat_counter = 0
    st.session_state.show_welcome = True

def dismiss_welcome():
    """Dismiss the welcome message."""
    st.session_state.show_welcome = False

def use_quick_prompt(prompt):
    """Handle a quick prompt selection."""
    st.session_state.show_welcome = False
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_counter += 1
    return prompt

# --- Model Definitions ---
models = {
    "gemma-7b-it": {
        "name": "Gemma-7b-it", 
        "tokens": 8192, 
        "developer": "Google",
        "description": "Fast model for mental health pattern recognition"
    },
    "llama2-70b-4096": {
        "name": "LLaMA2-70b-chat", 
        "tokens": 4096, 
        "developer": "Meta",
        "description": "Strong reasoning for complex mental health factors"
    },
    "llama3-70b-8192": {
        "name": "LLaMA3-70b-8192", 
        "tokens": 8192, 
        "developer": "Meta",
        "description": "Advanced model for nuanced mental health insights"
    },
    "llama3-8b-8192": {
        "name": "LLaMA3-8b-8192", 
        "tokens": 8192, 
        "developer": "Meta",
        "description": "Balanced model for early intervention strategies"
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral-8x7b-Instruct-v0.1", 
        "tokens": 32768, 
        "developer": "Mistral",
        "description": "Excellent for analyzing complex mental health data"
    },
}

def display_welcome_message():
    if st.session_state.show_welcome:
        welcome_card = st.container()
        with welcome_card:
            text_color = '#ffffff' if st.session_state.theme == 'dark' else '#000000'
            st.markdown(
                f"""
                <div class='welcome-card'>
                    <h1 style="color: {'#BA55D3' if st.session_state.theme == 'dark' else '#9370DB'};">Early Signs Matter🫂</h1>
                    <p style="font-size: 1.2rem; color: {text_color};">{APP_NAME} helps identify early signs of anxiety, depression, and psychosis.</p>
                    <p style="font-size: 1.2rem; color: {text_color};">Using insights from longitudinal research data to support early intervention.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Continue to Chat", key="dismiss_welcome"):
                    dismiss_welcome()
                    st.rerun()

def display_chat_tips():
    if st.session_state.chat_counter == 0 and not st.session_state.show_welcome:
        st.info("""
        💡 **Mental Health Early Signs Tips:**
        - Ask about early warning signs for anxiety or depression
        - Discuss biological, psychological, and social factors
        - Learn about effective early intervention strategies
        - Explore longitudinal research on mental health conditions
        - Discover how to recognize early psychosis indicators
        """)

# --- Main App Layout ---
icon(PAGE_ICON)
st.markdown(f'<a href="https://vers3dynamics.io/" style="color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"}; text-decoration:none;"><h2>{PAGE_TITLE}</h2></a>', unsafe_allow_html=True)
st.subheader(f"{APP_NAME}: {APP_TAGLINE}")

# Show welcome message or chat interface
if st.session_state.show_welcome:
    display_welcome_message()
else:
    # Image and Caption with Error Handling
    try:
        if os.path.exists(IMAGE_PATH):
            st.image(IMAGE_PATH, caption=IMAGE_CAPTION, width=300)
        else:
            # Don't show warning if image is missing
            pass
    except Exception as e:
        # Silently handle image error
        pass

    # Initialize Groq client
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except KeyError:
        st.error("GROQ_API_KEY not found in secrets. Please ensure it is set.")
        st.stop()
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        st.stop()

    # Sidebar with Enhanced UI
    with st.sidebar:
        text_color = '#ffffff' if st.session_state.theme == 'dark' else '#000000'
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h2 style='color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"};'>🔍 Mental Health Insights</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Theme selector
        theme_options = ["light", "dark"]
        theme_labels = ["🌞 Light Theme", "🌙 Dark Theme"]
        theme_index = 0 if st.session_state.theme == "light" else 1
        
        new_theme_index = st.selectbox(
            "Choose Theme:",
            options=range(len(theme_options)),
            format_func=lambda i: theme_labels[i],
            index=theme_index,
            key="theme_selector",
            help="Select the visual theme for the application."
        )
        
        new_theme = theme_options[new_theme_index]
        if st.session_state.theme != new_theme:
            st.session_state.theme = new_theme
            st.rerun()
        
        # Model Selection with Visual Feedback
        model_option = st.selectbox(
            "Choose your AI Model:",
            options=list(models.keys()),
            format_func=lambda x: f"🤖 {models[x]['name']}",
            index=DEFAULT_MODEL_INDEX,
            help="Select the language model to use for the chat."
        )

        if st.session_state.selected_model != model_option:
            st.session_state.selected_model = model_option
            # Don't clear chat history on model change to improve user experience

        # Model Information Card
        model_info = models[model_option]
        st.markdown(f"""
            <div style='background: {"#16213e" if st.session_state.theme == "dark" else "white"}; 
                      padding: 1rem; 
                      border-radius: 15px; 
                      box-shadow: 0 4px 6px rgba(0, 0, 0, {"0.3" if st.session_state.theme == "dark" else "0.1"});
                      border: 1px solid {"#4B0082" if st.session_state.theme == "dark" else "#E6E6FA"};
                      margin-top: 1rem;'>
                <h3 style='color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"}; margin-bottom: 0.5rem;'>Model Details</h3>
                <p style='color: {text_color};'><strong>🔮 Model:</strong> {model_info['name']}</p>
                <p style='color: {text_color};'><strong>🏢 Developer:</strong> {model_info['developer']}</p>
                <p style='color: {text_color};'><strong>📊 Max Tokens:</strong> {model_info['tokens']}</p>
                <p style='color: {text_color};'><strong>📝 Description:</strong> {model_info['description']}</p>
            </div>
        """, unsafe_allow_html=True)

        max_tokens = st.slider(
            "Max Response Tokens:",
            min_value=512,
            max_value=model_info["tokens"],
            value=min(2048, model_info["tokens"]),
            step=512,
            help=f"Control the length of the AI's response. Maximum for {model_info['name']}: {model_info['tokens']} tokens."
        )

        # Temperature slider for response creativity
        temperature = st.slider(
            "Response Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower values make responses more deterministic, higher values more creative."
        )

        if st.button("Clear Chat History", help="Reset the conversation history."):
            clear_chat_history()
            st.rerun()

        # Enhanced Audio Player in Sidebar
       
    audio_filename = "ElevenLabs_2025-02-16T06_54_38_Amanda_gen_s50_sb75_se0_b_m2.mp3"
    audio_path = os.path.join(os.path.dirname(__file__), audio_filename)
    
    # Explicitly use a button to control audio
    st.markdown("🔊 Welcome Audio Message")
    
    # Add a play button that only triggers when clicked
    if st.button("▶️ Play Welcome Audio"):
        try:
            # Verify file exists before attempting to play
            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/mp3")
            else:
                st.warning(f"Audio file not found: {audio_path}")
        except Exception as e:
            st.error(f"Error playing audio: {e}")
            
        # Quick prompt suggestions with mental health focus
        st.markdown(f"""
            <div style='background: {"#16213e" if st.session_state.theme == "dark" else "white"}; 
                      padding: 1rem; 
                      border-radius: 15px; 
                      box-shadow: 0 4px 6px rgba(0, 0, 0, {"0.3" if st.session_state.theme == "dark" else "0.1"});
                      border: 1px solid {"#4B0082" if st.session_state.theme == "dark" else "#E6E6FA"};
                      margin-top: 1rem;'>
                <h3 style='color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"}; margin-bottom: 0.5rem;'>💡 Mental Health Ideas</h3>
            </div>
        """, unsafe_allow_html=True)
        
        quick_prompts = [
            "What are early warning signs of anxiety?",
            "How can I recognize depression in its early stages?",
            "What biological factors contribute to mental health conditions?",
            "Tell me about effective early interventions for psychosis",
            "How do longitudinal studies help understand mental health?"
        ]
        
        for i, prompt in enumerate(quick_prompts):
            if st.button(prompt, key=f"quick_prompt_{i}"):
                if use_quick_prompt(prompt):
                    st.rerun()

    # Chat Display
    display_chat_tips()
    
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = '🧠' if message["role"] == "assistant" else '✨'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Generate chat responses
    def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
        """Generates chat response content from Groq API streaming."""
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # Chat Input and Response Generation
    user_input = st.chat_input(f"Hi, I'm {APP_NAME}💜.", key="user_input")
    if user_input:
        st.session_state.chat_counter += 1
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user", avatar='✨'):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🧠"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Display random loading message
                loading_message = random.choice(LOADING_MESSAGES)
                message_placeholder.markdown(
                    f"<div class='progress-message'>{loading_message}</div>", 
                    unsafe_allow_html=True
                )

                chat_completion = client.chat.completions.create(
                    model=model_option,
                    messages=st.session_state.messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=True
                )

                # Apply stronger styling to ensure text visibility on mobile
                text_color_style = "color: #000000 !important; font-size: 16px !important;" if st.session_state.theme == "light" else "color: #ffffff !important; font-size: 16px !important;"
                
                response_generator = generate_chat_responses(chat_completion)
                for response_chunk in response_generator:
                    full_response += response_chunk
                    message_placeholder.markdown(
                        f"<div style='{text_color_style}'>{full_response}▌</div>", 
                        unsafe_allow_html=True
                    )
                
                # Final response with proper styling
                message_placeholder.markdown(
                    f"<div style='{text_color_style}'>{full_response}</div>", 
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Oops! An error occurred: {e}. Please try again or select a different model.", icon="🚨")
                full_response = f"I apologize, but I encountered an error while generating a response. Please try again or select a different model."

            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer with conditional styling
text_color = '#ffffff' if st.session_state.theme == 'dark' else '#000000'
st.markdown(f"""
    <div style='text-align: center; margin-top: 2rem; opacity: 0.7; color: {text_color};'>
        <p>© 2025 Vers3Dynamics • 
        <a href="https://vers3dynamics.io/privacy" style="text-decoration:none; color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"};">Privacy Policy</a> • 
        <a href="https://vers3dynamics.io/terms" style="text-decoration:none; color: {"#BA55D3" if st.session_state.theme == "dark" else "#9370DB"};">Terms of Service</a></p>
    </div>
""", unsafe_allow_html=True)
