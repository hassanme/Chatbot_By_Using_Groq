import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get API key and model name from environment variables
api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")  # Load model from .env

# Create Groq client
client = Groq(api_key=api_key)

# Page Header
st.title("Hassan Chatbot")
st.write("Chatbot powered by Groq.")
st.divider()

# Sidebar
st.sidebar.title("Chats")

# Session State
if "Groq_model" not in st.session_state:
    st.session_state["Groq_model"] = model_name  # Use model from .env
    
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Debug: Print session state (optional)
print(st.session_state)

# Display the messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input for user message
if prompt := st.chat_input():
    # Append message to message collection
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the new message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display the assistant response from the model
    with st.chat_message("assistant"):
        response_text = st.empty()  # Placeholder for response text
        
        # Call the Groq API with model from .env
        completion = client.chat.completions.create(
            model=st.session_state.Groq_model,
            messages=[
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ],
            stream=True
        )
        
        full_response = ""
        
        for chunk in completion:
            full_response += chunk.choices[0].delta.content or ""
            response_text.markdown(full_response)
        
        # Add full response to the messages
        st.session_state.messages.append({"role": "assistant", "content": full_response})
