import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

st.title("Voice RAG Chatbot")

# User and Session Inputs
st.sidebar.header("Session Settings")
user_id = st.sidebar.text_input("User ID", value="default_user")
session_id = st.sidebar.text_input("Session ID", value="default_session")

# Text Chat Section
st.header("Text Chat")
message = st.text_area("Enter your message")
if st.button("Send Text Message"):
    if message.strip():
        payload = {"messages": message, "user_id": user_id, "session_id": session_id}
        try:
            response = requests.post("http://localhost:8000/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success("Response received!")
                st.write("**Bot:**", data["messages"])
                st.write("**Confidence Score:**", data["confidence_score"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect: {str(e)}")
    else:
        st.warning("Please enter a message.")

# Voice Chat Section
st.header("Voice Chat")
st.write("Click the button below to record your voice message.")
audio = mic_recorder(
    start_prompt="🎤 Start Recording", stop_prompt="⏹️ Stop Recording", key="recorder"
)

if audio:
    st.audio(audio["bytes"], format="audio/webm")
    if st.button("Send Voice Message"):
        files = {"audio": ("audio.webm", audio["bytes"], "audio/webm")}
        data = {"session_id": session_id, "user_id": user_id}
        try:
            response = requests.post(
                "http://localhost:8000/voice_chat", files=files, data=data
            )
            if response.status_code == 200:
                data = response.json()
                st.success("Voice processed!")
                st.write("**Bot:**", data["messages"])
                st.write("**Confidence Score:**", data["confidence_score"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect: {str(e)}")

# Chat History Section
st.header("Chat History")
if st.button("Fetch History"):
    payload = {"user_id": user_id, "session_id": session_id}
    try:
        response = requests.post("http://localhost:8000/chat_history", json=payload)
        if response.status_code == 200:
            history = response.json()
            st.write("**Chat History:**")
            for msg in history:
                if hasattr(msg, "type"):
                    st.write(f"**{msg.type}:** {msg.content}")
                else:
                    st.write(msg)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Failed to connect: {str(e)}")
