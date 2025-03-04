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
    body {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    .main {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        max-width: 800px;
        margin: auto;
        min-height: 100vh;
        overflow: hidden;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Chat message animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Message bubbles styling */
    .stChatMessage {
        animation: fadeIn 0.3s ease-in;
        margin: 1rem 0;
        transition: transform 0.2s;
    }

    [data-testid="stChatMessageUser"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 20px 20px 0 20px !important;
        margin-left: auto !important;
        max-width: 75%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    [data-testid="stChatMessageAssistant"] {
        background-color: #f8f9ff !important;
        border-radius: 20px 20px 20px 0 !important;
        max-width: 75%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb !important;
    }

    /* Input field styling */
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

    .stChatInput:hover {
        border-color: #4F46E5 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
    }

    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
        background: linear-gradient(45deg, #4F46E5, #10B981);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    /* Time display styling */
    .time-display {
        text-align: center;
        color: #666;
        font-size: 0.9em;
        margin-bottom: 2rem;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
        display: inline-block;
        margin: 0 auto 2rem;
    }

    /* Loading spinner styling */
    .stSpinner > div {
        border-color: #4F46E5 !important;
        border-right-color: transparent !important;
    }

    /* Scrollable chat container */
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 8rem;
        border-radius: 20px;
        overflow: hidden;
    }
            
     /* Fixed footer styling */
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
