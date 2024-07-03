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

# Stunning CSS to create a visually captivating app
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top left, #1a237e, #0d47a1, #01579b);
        color: #ffffff;
        padding: 30px;
        min-height: 100vh;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 15px 25px;
        font-size: 18px;
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4fc3f7;
        box-shadow: 0 0 25px rgba(79, 195, 247, 0.5);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #4fc3f7, #00b0ff, #0091ea);
        color: #ffffff;
        border-radius: 30px;
        border: none;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 18px;
        transition: all 0.4s ease;
        cursor: pointer;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, #0091ea, #00b0ff, #4fc3f7);
    }
    
    .chat-message {
        padding: 2rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: flex-start;
        animation: fadeInUp 0.6s ease-out, floating 4s ease-in-out infinite;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .chat-message:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(79, 195, 247, 0.5);
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .chat-message .avatar {
        width: 15%;
        margin-right: 20px;
        position: relative;
    }
    
    .chat-message .avatar img {
        max-width: 80px;
        max-height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #4fc3f7;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
    }
    
    .chat-message:hover .avatar img {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 25px rgba(79, 195, 247, 0.5);
    }
    
    .chat-message .message {
        width: 85%;
        padding: 0 1.5rem;
        color: #ffffff;
        font-size: 18px;
        line-height: 1.7;
        position: relative;
        overflow: hidden;
    }
    
    .chat-message .message::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, rgba(79, 195, 247, 0.2), rgba(0, 176, 255, 0.2));
        border-radius: 15px;
        z-index: -1;
        opacity: 0;
        transition: all 0.4s ease;
    }
    
    .chat-message:hover .message::before {
        opacity: 1;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        font-size: 16px;
        color: #ffffff;
        margin-top: 40px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .footer:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 195, 247, 0.1) 0%, transparent 70%);
        transform: rotate(45deg);
        animation: footerGlow 10s linear infinite;
    }
    
    @keyframes footerGlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .copy-btn {
        background: linear-gradient(45deg, #4fc3f7, #00b0ff);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 8px 15px;
        cursor: pointer;
        font-size: 14px;
        position: absolute;
        top: 15px;
        right: 15px;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .copy-btn:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        background: linear-gradient(45deg, #00b0ff, #4fc3f7);
    }
    
    /* Mesmerizing animated title */
    .title {
        text-align: center;
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 3rem;
        background: linear-gradient(45deg, #4fc3f7, #00b0ff, #0091ea, #4fc3f7);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientFlow 5s ease infinite, glowPulse 3s ease-in-out infinite alternate;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes glowPulse {
        from {
            text-shadow: 0 0 10px #4fc3f7, 0 0 20px #4fc3f7, 0 0 30px #4fc3f7, 0 0 40px #4fc3f7;
        }
        to {
            text-shadow: 0 0 20px #00b0ff, 0 0 30px #00b0ff, 0 0 40px #00b0ff, 0 0 50px #00b0ff, 0 0 60px #00b0ff;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #4fc3f7, #00b0ff);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #00b0ff, #4fc3f7);
    }
    
    /* Code block styling */
    .code-block {
        position: relative;
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 25px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .code-block::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4fc3f7, #00b0ff, #0091ea);
    }
    
    .code-block pre {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# Function to add code block and copy button with syntax highlighting
def format_code_block(code):
    escaped_code = code.replace("`", "\\`")
    return f"""
        <div class="code-block">
            <pre><code class="language-python">{code}</code></pre>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(`{escaped_code}`)">Copy</button>
        </div>
    """

# Main chat interface
st.markdown("<h1 class='title'>💬 Chat with Gemini AI</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    formatted_message = message['content']
    if '```' in formatted_message:
        parts = formatted_message.split('```')
        formatted_message = parts[0] + format_code_block(parts[1]) + ''.join(parts[2:])

    with st.container():
        st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div class="avatar">
                    <img src="https://api.dicebear.com/7.x/bottts/svg?seed={'Gemini' if message['role'] == 'assistant' else 'User'}" style="max-height: 80px; max-width: 80px; border-radius: 50%; object-fit: cover;">
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
                <img src="https://api.dicebear.com/7.x/bottts/svg?seed=User" style="max-height: 80px; max-width: 80px; border-radius: 50%; object-fit: cover;">
            </div>
            <div class="message">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Gemini is crafting a response..."):
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
                        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Gemini" style="max-height: 80px; max-width: 80px; border-radius: 50%; object-fit: cover;">
                    </div>
                    <div class="message">{full_response}▌</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Format response if it contains code
        if '```' in full_response:
            parts = full_response.split('```')
            full_response = parts[0] + format_code_block(parts[1]) + ''.join(parts[2:])
        
        message_placeholder.markdown(f"""
            <div class="chat-message bot">
                <div class="avatar">
                    <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Gemini" style="max-height: 80px; max-width: 80px; border-radius: 50%; object-fit: cover;">
                </div>
                <div class="message">{full_response}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # ... (previous code remains the same)

# Add a pulsating, interactive footer with hover effects
st.markdown("""
    <div class='footer'>
        <div class='footer-content'>
            <p>Created with <span class='heart'>❤️</span> using Streamlit and Gemini AI</p>
            <p><a href="https://www.anthropic.com" class='anthropic-link'>Powered by Anthropic</a></p>
        </div>
        <div class='footer-glow'></div>
    </div>
""", unsafe_allow_html=True)

# Add Prism.js for syntax highlighting
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-python.min.js"></script>
""", unsafe_allow_html=True)

# Add custom JavaScript for interactive elements
st.markdown("""
    <script>
    // Function to add ripple effect to buttons
    function addRippleEffect(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        ripple.classList.add('ripple');
        
        button.appendChild(ripple);
        
        ripple.addEventListener('animationend', () => {
            ripple.remove();
        });
    }

    // Add ripple effect to all buttons
    document.querySelectorAll('.stButton > button').forEach(button => {
        button.addEventListener('click', addRippleEffect);
    });

    // Animate the heart in the footer
    const heart = document.querySelector('.heart');
    setInterval(() => {
        heart.classList.add('pulse');
        setTimeout(() => {
            heart.classList.remove('pulse');
        }, 1000);
    }, 2000);

    // Add hover effect to Anthropic link
    const anthropicLink = document.querySelector('.anthropic-link');
    anthropicLink.addEventListener('mouseover', () => {
        anthropicLink.style.textShadow = '0 0 10px #4fc3f7';
    });
    anthropicLink.addEventListener('mouseout', () => {
        anthropicLink.style.textShadow = 'none';
    });
    </script>
""", unsafe_allow_html=True)

# Add custom CSS for new interactive elements
st.markdown("""
    <style>
    /* ... (previous styles remain the same) ... */

    /* Enhanced footer styles */
    .footer {
        text-align: center;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        font-size: 16px;
        color: #ffffff;
        margin-top: 40px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .footer-content {
        position: relative;
        z-index: 1;
    }

    .footer-glow {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 195, 247, 0.2) 0%, transparent 70%);
        transform: rotate(45deg);
        animation: footerGlow 10s linear infinite;
    }

    @keyframes footerGlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .footer:hover .footer-glow {
        animation-duration: 5s;
    }

    .heart {
        color: #ff4081;
        display: inline-block;
        transition: transform 0.3s ease;
    }

    .heart.pulse {
        animation: heartbeat 1s ease-in-out;
    }

    @keyframes heartbeat {
        0% { transform: scale(1); }
        50% { transform: scale(1.3); }
        100% { transform: scale(1); }
    }

    .anthropic-link {
        color: #4fc3f7;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .anthropic-link:hover {
        color: #ff4081;
    }

    /* Ripple effect for buttons */
    .stButton > button {
        position: relative;
        overflow: hidden;
    }

    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.7);
        transform: scale(0);
        animation: ripple 0.6s linear;
    }

    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    /* Improved code block styling */
    .code-block {
        position: relative;
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 25px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        margin: 15px 0;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .code-block:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        transform: translateY(-5px);
    }

    .code-block::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4fc3f7, #00b0ff, #0091ea);
    }

    .code-block pre {
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    /* Enhanced avatar styling */
    .chat-message .avatar::after {
        content: '';
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        background: linear-gradient(45deg, #4fc3f7, #00b0ff, #0091ea);
        border-radius: 50%;
        z-index: -1;
        opacity: 0;
        transition: all 0.3s ease;
    }

    .chat-message:hover .avatar::after {
        opacity: 1;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
    }
    </style>
""", unsafe_allow_html=True)

# Add a loading animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets5.lottiefiles.com/packages/lf20_bdsthrsn.json"
lottie_json = load_lottie_url(lottie_url)
st_lottie(lottie_json, speed=1, height=200, key="loading")

# Main app logic (chat interface) remains the same
# ...
