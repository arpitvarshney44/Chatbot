import streamlit as st
from groq import Groq

# Set up the page configuration
st.set_page_config(
    page_title="ArvaGPT",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stChatInput {position: fixed; bottom: 5rem; width: 60%;}
    .stChatMessage {width: 80%; margin: 0 auto;}
    .header {text-align: center; padding: 4rem 0;}
    .sidebar .sidebar-content {background-color: #f0f2f6;}
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = "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"
    model = st.selectbox(
        "🧠 Model",
        options=["llama-3.3-70b-versatile"],
        index=0
    )
    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.5
    )
    with st.expander("❓ Temperature Guide"):
        st.markdown("""
        **Temperature Settings Guide:**
        
        | Value Range | Effect                     | Best For                 |
        |---------|--------------------------------|-------------------------------|
        | **0.0** | Strict, deterministic answers  | Factual Q&A, technical topics |
        | **0.5** | Balanced responses             | General conversation         |
        | **1.0** | Highly creative/random         | Poetry, brainstorming        |
        
        **Examples:**
        - 🔵 Low (0.2): "The capital of France is Paris."
        - 🟢 Medium (0.5): "Paris is the beautiful capital known for the Eiffel Tower."
        - 🔴 High (0.8): "Ah, Paris! City of lights and croissants by the Seine..."
        """)

    st.markdown("---")
    st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io/) and [Groq](https://groq.com/)")

# Main header
st.header("🤖 ArvaGPT")
st.markdown("AI powered Chatbot")

# Initialize Groq client

client = Groq(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

     # Get response from Groq API
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="llama-3.3-70b-versatile",
    )
    
    msg = response.choices[0].message.content
    
    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)    
