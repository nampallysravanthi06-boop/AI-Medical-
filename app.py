import streamlit as st
import google.generativeai as genai
import os
from gtts import gTTS

# ----------------------------
# Setup
# ----------------------------
st.set_page_config(page_title="AI Prescription Verifier", layout="wide")

# Load API key securely
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # set in environment or st.secrets
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

# ----------------------------
# Helper functions
# ----------------------------
def analyze_prescription(text):
    prompt = f"""
    You are a medical assistant AI.
    Extract the medicine names from this prescription and verify if they are real.
    For each medicine, give:
    - Generic name
    - Description
    - Common usage
    - Safety notes (if any)

    Prescription text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("💊 AI Medical Prescription Verifier")

uploaded_file = st.file_uploader("Upload a prescription (.txt)", type="txt")
user_text = st.text_area("Or paste your prescription here:", height=200)

if uploaded_file:
    user_text = uploaded_file.read().decode("utf-8")

if st.button("Analyze Prescription"):
    if user_text.strip():
        st.subheader("📝 Prescription Analysis")
        with st.spinner("Analyzing with AI..."):
            result = analyze_prescription(user_text)
        
        st.write(result)

        # Generate audio narration
        audio_file = text_to_speech(result, "medicine_info.mp3")
        st.audio(audio_file, format="audio/mp3")

        with open(audio_file, "rb") as f:
            st.download_button(
                label="📥 Download Audio Explanation",
                data=f,
                file_name="medicine_info.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("Please provide a prescription first!")
