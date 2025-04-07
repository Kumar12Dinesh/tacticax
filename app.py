import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3  # AI voice output
import geopy.distance  # Geo-Fencing
import cv2  # Camera for Morse Code
import numpy as np
import time

# Set Gemini API Key
genai.configure(api_key="AIzaSyDdHha253xfNqeIqqwE0TqZpB0BkPKhVOU")

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Geo-Fencing Coordinates (Allowed region)
ALLOWED_COORDINATES = (37.7749, -122.4194)  # Example: San Francisco


def is_within_geofence(user_coordinates):
    """Check if the user is within the defined geofencing area."""
    distance = geopy.distance.geodesic(ALLOWED_COORDINATES, user_coordinates).km
    return distance < 5  # Allow within 5 km radius


def generate_ai_strategy_gemini(mission_details):
    """Generate a battlefield strategy using Google's Gemini AI."""
    prompt = f"Develop a tactical military strategy based on the following mission details: {mission_details}. " \
             "Include troop movement, risk assessment, and strategic execution."
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else "No strategy available."


def morse_code_translate(text, to_morse=True):
    """Convert text to Morse code and vice versa."""
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '0': '-----', ' ': '/'
    }
    if to_morse:
        return ' '.join(morse_dict[char] for char in text.upper() if char in morse_dict)
    else:
        reverse_dict = {v: k for k, v in morse_dict.items()}
        return ''.join(reverse_dict[char] for char in text.split(' ') if char in reverse_dict)


def detect_morse_camera():
    """Detect Morse code signals from a flashing light using a camera."""
    cap = cv2.VideoCapture(0)
    prev_intensity = None
    morse_sequence = ""
    start_time = time.time()

    st.info("📹 Detecting Morse Code via Camera...")
    while time.time() - start_time < 10:  # Detect for 10 seconds
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        intensity = np.mean(gray)

        if prev_intensity is not None:
            if intensity - prev_intensity > 50:  # Flash detected
                morse_sequence += '.' if (time.time() - start_time) < 0.5 else '-'
                start_time = time.time()
        prev_intensity = intensity
    cap.release()

    decoded_message = morse_code_translate(morse_sequence, to_morse=False)
    return decoded_message if decoded_message else "No Morse code detected."


def speech_to_text():
    """Convert voice command to text."""
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError:
            return "Speech recognition service unavailable"
        except Exception as e:
            return f"Error: {str(e)}"
        
def speak_message(message):
    """Function to play a voice message."""
    engine.say(message)
    engine.runAndWait()

def main():
    st.set_page_config(page_title="TacticaX", layout="wide", page_icon="⚔️")
     # Voice Welcome Message (Only Once Per Session)
    if "welcome_shown" not in st.session_state:
        st.session_state.welcome_shown = True
        with st.spinner("Initializing TacticaX..."):
            time.sleep(2)  # Simulate loading time
        welcome_text = "Welcome to the TacticaX! Empowering Tactical Decisions with Artificial Intelligence."
        st.success("⚔️ Welcome to the TacticaX!")
        st.toast("Empowering Tactical Decisions with AI! 🚀", icon="🤖")
        speak_message(welcome_text)  # Play Voice Message

    st.sidebar.title("⚔️ TacticaX")
    choice = st.sidebar.radio("Navigation", ["🏠 Home", "📜 Mission Planning", "💡 Morse Code Communication", "📍 Geo-Fencing Messages"])

    if choice == "🏠 Home":
        st.title("⚡TacticaX⚡ ")
        st.write("Welcome to the TacticaX This system provides real-time battle strategies, mission planning, and tactical AI support using advanced AI models.")
        st.subheader("A Cutting-Edge AI System for Tactical Warfare")
        st.write("""
        Welcome to the **TacticaX** – an advanced AI-driven system designed to 
        support **real-time tactical analysis, mission planning, encrypted communication, and intelligent decision-making**.
        
        🛡️ **Core Features**:  
        - 📜 **Mission Planning**: AI-generated battlefield strategies  
        - 💡 **Morse Code Communication**: Secure text encoding & decoding  
        - 📍 **Geo-Fencing**: Self-destruct messages for secure operations  
        - 🎤 **Voice Command Support**: Control the system hands-free  
        """)
    elif choice == "📜 Mission Planning":
        st.title("📜 AI-Driven Mission Planning")
        mission_details = st.text_area("Enter Mission Details")

        if st.button("🎤 Speak Mission"):
            mission_details = speech_to_text()
            st.text_area("Detected Speech", mission_details)

        if st.button("Generate Strategy"):
            ai_strategy = generate_ai_strategy_gemini(mission_details)
            st.write(f"**🛡️ Strategy for Mission:** {ai_strategy}")
            engine.say(f"Strategy for mission: {mission_details}. {ai_strategy}")
            engine.runAndWait()

    elif choice == "💡 Morse Code Communication":
        st.title("💡 Morse Code Communication")
        text_input = st.text_input("Enter Text to Convert")

        if st.button("Convert to Morse Code"):
            morse_code = morse_code_translate(text_input)
            st.write(f"**Morse Code:** {morse_code}")

        if st.button("🎤 Speak Morse Code"):
            spoken_text = speech_to_text()
            morse_code = morse_code_translate(spoken_text)
            st.write(f"**Morse Code:** {morse_code}")

    elif choice == "📍 Geo-Fencing Messages":
        st.title("📍 Geo-Fencing Self-Destruct Messages")
        user_lat = st.number_input("Enter Your Latitude")
        user_lon = st.number_input("Enter Your Longitude")
        message = st.text_area("Enter Secure Message")

        if st.button("🎤 Speak Secure Message"):
            message = speech_to_text()
            st.text_area("Detected Speech", message)

        if st.button("Send Secure Message"):
            if is_within_geofence((user_lat, user_lon)):
                st.success("✅ Secure Message Sent Successfully!")
            else:
                st.error("❌ Access Denied: Message Self-Destructed Outside Geo-Fence!")

if __name__ == "__main__":
    main()
