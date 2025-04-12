import os
import streamlit as st
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

# ✅ Set page config
st.set_page_config(
    page_title="💬 Jahanzaib's AI-powered Chatbot",
    page_icon="🧠",
    layout="wide"
)

# 📌 Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔗 Mistral API call function
def call_mistral_api(messages):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']

# 🎨 Chat UI (Centered Title)
st.markdown(""" 
        <div style="text-align: center;">
            <h1 style="font-size: 50px;">💬 Jahanziab's AI-powered Chatbot</h1>
        </div>
        """, unsafe_allow_html=True)

# 📌 Spacer (creates 5 lines gap)
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)


# 📌 Sidebar options
with st.sidebar:
    st.subheader("📝 Options")
    save_history = st.checkbox("Enable Save History")

    if save_history and st.session_state.messages:
        history_text = ""
        for msg in st.session_state.messages:
            sender = "You" if msg["role"] == "user" else "Bot"
            history_text += f"{sender}: {msg['content']}\n\n"
        st.download_button(
            label="📥 Download Chat History",
            data=history_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )

# 🖥️ If no messages yet — show welcome screen
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding-top: 20px;">
        <h1 style="font-size: 50px;">💬 Friendly Chat</h1>
        <p style="font-size: 20px; color: grey;">Start a conversation by typing your message below</p>
    </div>
    """, unsafe_allow_html=True)

# 📜 Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 💬 User input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_mistral_api(st.session_state.messages)
            st.markdown(response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
