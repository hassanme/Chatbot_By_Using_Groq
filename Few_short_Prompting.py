import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")  # Load model from .env


# Set page config
st.set_page_config(page_title="Hassan Chatbot", page_icon="🤖", layout="wide")

# Apply custom styles for a more attractive look
st.markdown(
    """
    <style>
        body {background-color: #f5f7fa;}
        .stApp {background-color: #ffffff;}
        .sidebar .sidebar-content {background-color: #1E1E1E; color: white;}
        .stChatMessage {border-radius: 10px; padding: 15px; margin: 10px 0; font-size: 18px;}
        .user-message {background-color: #DCF8C6; text-align: right; padding: 15px; border-radius: 10px;}
        .assistant-message {background-color: #EAEAEA; padding: 15px; border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Creates Groq client
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

# Page Header
st.title("🤖 Hassan AI Chatbot")
st.write("A smart and interactive chatbot powered by **Groq AI**.")
st.divider()

# Sidebar for chat history
st.sidebar.title("📌 Chat History")
st.sidebar.markdown("*Keep track of your previous chats here!*")

# Session State for model and messages
if "Groq_model" not in st.session_state:
    st.session_state["Groq_model"] = model_name
    
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Prompting techniques
few_shot_examples = [
    {"role": "user", "content": "Translate 'Hello' to French."},
    {"role": "assistant", "content": "Bonjour."},
    {"role": "user", "content": "Translate 'Goodbye' to Spanish."},
    {"role": "assistant", "content": "Adiós."}
]

# Display messages
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(f'<div class="{role_class}" style="font-size:18px;">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="user-message" style="font-size:18px;">{prompt}</div>', unsafe_allow_html=True)
    
    # AI Response
    with st.chat_message("assistant", avatar="🤖"):
        response_text = st.empty()
        
        # Constructing messages with prompting techniques
        messages_to_send = few_shot_examples + st.session_state.messages
        messages_to_send.append({"role": "user", "content": "Think step by step: " + prompt})  # Chain-of-thought prompting
        
        # Call Groq API
        completion = client.chat.completions.create(
            model=st.session_state.Groq_model,
            messages=messages_to_send,
            stream=True
        )
        
        full_response = ""
        for chunk in completion:
            full_response += chunk.choices[0].delta.content or ""
            response_text.markdown(f'<div class="assistant-message" style="font-size:18px;">{full_response}</div>', unsafe_allow_html=True)
        
        # Store AI response
        st.session_state.messages.append({"role": "assistant", "content": full_response})
