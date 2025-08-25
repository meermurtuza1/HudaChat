import streamlit as st
import json
import requests

# Set page config
st.set_page_config(page_title="💖 Whispers for Huda", page_icon="💖", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .big-title {
        font-size: 40px !important;
        color: #e75480;
        text-align: center;
        font-weight: bold;
    }
    .stTextArea textarea {
        background: linear-gradient(135deg, #ffe6f0, #e6ccff);
        border: 2px solid #e75480;
        border-radius: 14px;
        font-size: 16px;
        color: #4b0082;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #e75480;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #c71585;
        transform: scale(1.05);
    }
    .analysis-box {
        background-color: #ffe6f0;
        padding: 18px;
        border-radius: 12px;
        font-size: 18px;
        font-style: italic;
        color: #800080;
        box-shadow: 0 0 12px rgba(231, 84, 128, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="big-title">💖 Whispers for Huda 💖</div>', unsafe_allow_html=True)
st.markdown("#### ✍️ Enter any word, and I’ll turn it into a sweet poetic whisper for Huda!")

# Gemini API configuration
GOOGLE_API_KEY = "AIzaSyB2gXFyadYNXEaUQHE2vRfzEuIoxgtjl9c"  # replace with your valid Gemini key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Load template.json
def load_template():
    try:
        with open("template.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("template", "")
    except Exception as e:
        st.error(f"⚠️ Error loading template.json: {e}")
        return ""

# Text input
user_word = st.text_area("✨ Type a word for magical whispers ✨", height=120)

# Button
if st.button("💌 Whisper a Rhyme"):
    if not GOOGLE_API_KEY:
        st.error("❌ Google API Key is not set. Please update the script with your valid API key.")
    elif not user_word.strip():
        st.warning("⚠️ Please enter a word first.")
    else:
        with st.spinner("🎶 Creating a poetic whisper for Huda..."):
            # Load and format template
            template_text = load_template()
            final_prompt_text = template_text.replace("{word}", user_word)

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": final_prompt_text}]
                    }
                ]
            }

            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(
                    f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()

                if result.get("candidates") and \
                   result["candidates"][0].get("content") and \
                   result["candidates"][0]["content"].get("parts"):
                    rhyme = result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    rhyme = "❗ Could not generate a whisper. Please try again."

                st.markdown("### 💕 Your Whisper for Huda")
                st.markdown(f"<div class='analysis-box'>{rhyme}</div>", unsafe_allow_html=True)

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API call error: {e}")
            except Exception as e:
                st.error(f"🚨 Unexpected error: {e}")
