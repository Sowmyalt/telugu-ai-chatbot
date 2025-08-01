import streamlit as st
import google.generativeai as genai
import speech_recognition as sr

# Configure API Key securely
genai.configure(api_key=st.secrets["API_KEY"])

# Page config
st.set_page_config(page_title="Telugu AI Chatbot", page_icon="🤖", layout="wide")

# CSS for blurred background
background_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"  # Change if you want
custom_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("{background_url}") no-repeat center center fixed;
    background-size: cover;
}}

.chat-container {{
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(15px);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    color: black;
    font-size: 16px;
}}
input[type="text"] {{
    background-color: rgba(255,255,255,0.8);
    border-radius: 8px;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center; color:white;'>🎙 Telugu AI Chatbot</h1>", unsafe_allow_html=True)
st.write("<h4 style='text-align:center; color:white;'>Ask in Telugu or English by typing or speaking.</h4>", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Speech Recognition (via Upload for Streamlit Cloud)
uploaded_audio = st.file_uploader("🎵 Upload your audio file (Telugu speech):", type=["wav", "mp3"])

if uploaded_audio is not None:
    st.audio(uploaded_audio)
    recognizer = sr.Recognizer()
    with sr.AudioFile(uploaded_audio) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="te-IN")
        st.success(f"✅ Recognized: {text}")
        st.session_state.user_input = text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError:
        st.error("Speech Recognition API error")

# Input Section
col1, col2 = st.columns([3, 1])
with col1:
    user_text = st.text_input("👉 Type your question here:", value=st.session_state.user_input, key="text_input")
with col2:
    st.markdown("<p style='color:white;'>Upload audio above ☝️</p>", unsafe_allow_html=True)

# Send Button
if st.button("Send"):
    if st.session_state.user_input.strip() or user_text.strip():
        final_input = user_text if user_text.strip() else st.session_state.user_input
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(final_input)
                st.session_state.chat_history.append(("You", final_input))
                st.session_state.chat_history.append(("Bot", response.text))
                st.session_state.user_input = ""
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("⚠️ Please type or upload an audio question.")

# Chat History Display
st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
for sender, msg in st.session_state.chat_history:
    st.markdown(f"<div class='chat-container'><strong>{sender}:</strong> {msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
