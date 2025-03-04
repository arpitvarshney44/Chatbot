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

# Custom CSS for responsive design
st.markdown("""
<style>
    /* Base styles */
    body {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        margin: 0;
        padding: 0;
    }
    
    .main {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem !important;
        width: 100% !important;
        max-width: 100% !important;
        min-height: 100vh;
    }

    /* Mobile-first adjustments */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem !important;
            border-radius: 0;
        }
        
        .title {
            font-size: 1.8rem !important;
            margin-bottom: 0.3rem !important;
        }
        
        .subtitle {
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .time-display {
            font-size: 0.8em !important;
            padding: 0.3rem !important;
            margin-bottom: 1rem !important;
        }
        
        [data-testid="stChatMessageUser"], 
        [data-testid="stChatMessageAssistant"] {
            max-width: 90% !important;
            margin: 0.5rem 0 !important;
            font-size: 0.9rem;
        }
        
        .stChatInput {
            width: 95% !important;
            bottom: 1rem !important;
            padding: 0.5rem !important;
            font-size: 0.9rem;
        }
        
        .chat-container {
            max-height: 65vh;
            padding-bottom: 6rem;
        }
        
        .fixed-footer {
            width: 95% !important;
            bottom: 0.5rem !important;
            font-size: 0.7rem !important;
            padding: 0.3rem !important;
        }
        
        .stChatMessage {
            margin: 0.5rem 0 !important;
        }
    }

    /* Desktop styles */
    @media (min-width: 769px) {
        .main {
            max-width: 800px !important;
            margin: auto;
        }
    }

    /* Universal styles */
    [data-testid="stChatMessageUser"], 
    [data-testid="stChatMessageAssistant"] {
        max-width: 85%;
        word-wrap: break-word;
        margin: 1rem 0;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .stChatInput {
        position: fixed !important;
        bottom: 5rem;
        width: 90% !important;
        max-width: 100% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
        font-size: 1rem;
        z-index: 999;
    }

    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 8rem;
        -webkit-overflow-scrolling: touch;
    }

    .fixed-footer {
        position: fixed !important;
        bottom: 1rem;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        text-align: center;
        color: #666;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(5px);
        border-radius: 8px;
        z-index: 998;
        padding: 0.5rem;
    }

    .header-container {
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }

    .title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #4F46E5, #10B981);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .time-display {
        text-align: center;
        color: #666;
        font-size: 0.9em;
        margin: 1rem auto;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
        display: inline-block;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stChatMessage {
        animation: fadeIn 0.3s ease-in;
        transition: transform 0.2s;
    }

    .stSpinner > div {
        border-color: #4F46E5 !important;
        border-right-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Header section
current_time = datetime.now().strftime("%A, %d %B %Y | %I:%M %p")
st.markdown(f"""
<div class="header-container">
    <h1 class="title">ArvaGPT</h1>
    <div class="subtitle">AI-Powered Chatbot with Real-Time</div>
    <div class="time-display">{current_time}</div>
</div>
""", unsafe_allow_html=True)

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
            model="llama3-70b-8192",
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
