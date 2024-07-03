import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests
import time

# Configure the Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Set up the model
model = genai.GenerativeModel('gemini-pro')

def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Custom CSS to make the app ultra beautiful
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 20px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #ffffff;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        animation: fadeIn 0.5s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message.user {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .chat-message.bot {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    .chat-message .avatar {
        width: 15%;
    }
    
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ffffff;
    }
    
    .chat-message .message {
        width: 85%;
        padding: 0 1.5rem;
        color: #ffffff;
        font-size: 16px;
    }
    
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        font-size: 16px;
    }
    
    .footer {
        text-align: center;
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        font-size: 14px;
        color: #ffffff;
        margin-top: 20px;
    }
    
    .copy-btn {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 5px 10px;
        cursor: pointer;
        font-size: 12px;
        position: absolute;
        top: 10px;
        right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Function to add code block and copy button
def format_code_block(code):
    escaped_code = code.replace("`", "\\`")
    return f"""
        <div style="position: relative; background: #2d2d2d; color: #ffffff; padding: 10px; border-radius: 10px; font-family: monospace;">
            <pre>{code}</pre>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(`{escaped_code}`)">Copy Code</button>
        </div>
    """

# Main chat interface
st.title("💬 Chat with Gemini AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    formatted_message = message['content']
    if '```' in formatted_message:
        parts = formatted_message.split('```')
        formatted_message = parts[0] + format_code_block(parts[1]) + parts[2]

    with st.container():
        st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div class="avatar">
                    <img src="https://api.dicebear.com/7.x/bottts/svg?seed={'Gemini' if message['role'] == 'assistant' else 'User'}" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
                </div>
                <div class="message">{formatted_message}</div>
            </div>
        """, unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message in chat message container
    st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar">
                <img src="https://api.dicebear.com/7.x/bottts/svg?seed=User" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
            </div>
            <div class="message">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Gemini is thinking..."):
        response = generate_response(prompt)
        # Simulate typing effect
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(f"""
                <div class="chat-message bot">
                    <div class="avatar">
                        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Gemini" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
                    </div>
                    <div class="message">{full_response}▌</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Format response if it contains code
        if '```' in full_response:
            parts = full_response.split('```')
            full_response = parts[0] + format_code_block(parts[1]) + parts[2]
        
        message_placeholder.markdown(f"""
            <div class="chat-message bot">
                <div class="avatar">
                    <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Gemini" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
                </div>
                <div class="message">{full_response}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a footer
st.markdown("""
    <div class='footer'>
        Created with ❤️ using Streamlit and Gemini AI
    </div>
""", unsafe_allow_html=True)
