import streamlit as st
from groq import Groq
from datetime import datetime

# Set up the page configuration
st.set_page_config(
    page_title="ArvaGPT",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Global Styles */
    * {
        box-sizing: border-box !important;
    }

    body {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        margin: 0;
        padding: 0;
    }

    /* Main Container */
    .main {
        background: rgba(255,255,255,0.9) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        max-width: 800px !important;
        margin: auto !important;
        min-height: 100vh !important;
        overflow: hidden !important;
        position: relative !important;
        box-shadow: 0 0 20px rgba(0,0,0,0.1) !important;
    }

    /* Header */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
        background: linear-gradient(45deg, #4F46E5, #10B981);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    /* Chat Container */
    .chat-container {
        max-height: 70vh !important;
        overflow-y: auto !important;
        padding: 0 12px 8rem !important;
        margin: 0 -12px !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        isolation: isolate !important;
    }

    /* Message Bubbles */
    [data-testid="stChatMessage"] {
        margin: 8px 12px !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        animation: fadeIn 0.3s ease-in;
        max-width: calc(100% - 24px) !important;
    }

    [data-testid="stChatMessageUser"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 20px 20px 0 20px !important;
        margin-left: auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    [data-testid="stChatMessageAssistant"] {
        background-color: #f8f9ff !important;
        border-radius: 20px 20px 20px 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb !important;
    }

    /* Input Field */
    .stChatInput {
        position: fixed !important;
        bottom: 5rem;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 80% !important;
        max-width: 800px !important;
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        z-index: 999;
    }

    /* Animations */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main {
            margin: 10px !important;
            width: calc(100% - 20px) !important;
            min-height: 95vh !important;
            border-radius: 18px !important;
            padding: 1rem !important;
        }
        
        .chat-container {
            max-height: 60vh !important;
            border-radius: 18px !important;
            padding: 0 8px 6rem !important;
            margin: 0 -8px !important;
        }
        
        [data-testid="stChatMessage"] {
            margin: 8px !important;
            max-width: calc(100% - 16px) !important;
            border-radius: 18px !important;
        }
        
        .stChatInput {
            width: 90% !important;
            bottom: 4rem;
        }
    }

    /* Footer */
    .fixed-footer {
        position: fixed !important;
        bottom: 1.5rem;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        max-width: 800px;
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        padding: 0.5rem;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(5px);
        border-radius: 8px;
        z-index: 998;
    }

    /* Loading Spinner */
    .stSpinner > div {
        border-color: #4F46E5 !important;
        border-right-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="header-container">
    <h1 class="title">ArvaGPT</h1>
    <div class="subtitle">AI-Powered Chatbot with Real-Time </div>
    <div class="time-display">{}</div>
</div>
""".format(datetime.now().strftime("%A, %d %B %Y | %I:%M %p")), unsafe_allow_html=True)

# Initialize Groq client
api_key = "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"
client = Groq(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Message ArvaGPT..."):
    # Update time display
    current_time = datetime.now().strftime("%A, %d %B %Y | %I:%M %p")
    st.markdown(f'<div class="time-display">{current_time}</div>', unsafe_allow_html=True)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Get response from Groq API
    with st.spinner("ArvaGPT is typing..."):
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5
        )
    
    msg = response.choices[0].message.content
    
    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(msg)

# Footer
st.markdown("""
<div class="fixed-footer">
    ArvaGPT v1.0 | Safe & Ethical AI Conversations
</div>
""", unsafe_allow_html=True)
