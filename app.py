import streamlit as st
from groq import Groq

# Set up the page configuration
st.set_page_config(
    page_title="ArvaGPT",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Remove sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Main container padding */
    .main {
        background-color: #ffffff;
        padding-top: 6rem !important;
        padding-bottom: 10rem !important;
    }
    
    /* Chat messages container */
    .stChatMessage {
        max-width: 800px;
        margin: 0.5rem auto;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1000;
    }
            
    /* Message styling */
    .stChatMessage {
        margin: 1rem 0;
        border-radius: 10px;
        padding: 2rem;
        max-width: 100%;
    }
    
    /* User message styling */
    div[data-testid="stChatMessage"][aria-label="user"] {
        background-color: #f0f4ff;
        margin-left: auto;
        border: 1px solid #d0d7de;
    }
    
    /* Assistant message styling */
    div[data-testid="stChatMessage"][aria-label="assistant"] {
        background-color: #f9f9f9;
        margin-right: auto;
        border: 1px solid #e5e7eb;
    }
    
    /* Input box positioning */
    .stChatInput {
        position: fixed !important;
        bottom: 4rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        background: white;
        border-radius: 8px;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        padding: 1rem;
        z-index: 100;
    }
    
     /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4rem;
        background-color: #000000;
        color: white;
        z-index: 1001;
    }

    .footer-content {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-size: 0.8rem;
    }

    /* Separator line above footer */
    .footer-separator {
        position: fixed;
        bottom: 4rem;
        left: 0;
        right: 0;
        height: 1px;
        background-color: #e5e7eb;
        z-index: 1001;
    }
    
    /* Centered header */
    .centered-header {
        text-align: center;
        color: #202123;
        font-size: 2rem;
        margin: 2rem 0 1rem 0;
        font-weight: bold;
    }
    
    /* Centered caption */
    .centered-caption {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Footer section with separator line
st.markdown("""
<div class="footer-separator"></div>
<div class="footer">
    <div class="footer-content">
        ArvaGPT v1.0 • © 2025 • Powered by Groq & Llama 3
    </div>
</div>
""", unsafe_allow_html=True)


# Centered header and caption
st.markdown('<div class="centered-header">ArvaGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="centered-caption">Powered by Groq & Llama 3</div>', unsafe_allow_html=True)

# Initialize Groq client
client = Groq(api_key="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")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# Chat container
chat_container = st.container()

# Display messages in chat container
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)


# Accept user input
if prompt := st.chat_input("Message ArvaGPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="llama-3.3-70b-versatile",
        temperature=0.5
    )
    
    msg = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    with st.chat_message("assistant"):
        st.markdown(msg)
