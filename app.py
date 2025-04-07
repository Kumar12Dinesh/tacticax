import streamlit as st
import google.generativeai as genai
import geopy.distance
import time

# Gemini API Key (recommended: use secrets in Streamlit Cloud)
genai.configure(api_key=st.secrets["gemini_api_key"])

ALLOWED_COORDINATES = (37.7749, -122.4194)

def is_within_geofence(user_coordinates):
    distance = geopy.distance.geodesic(ALLOWED_COORDINATES, user_coordinates).km
    return distance < 5

def generate_ai_strategy_gemini(mission_details):
    prompt = f"Develop a tactical military strategy based on the following mission details: {mission_details}. " \
             "Include troop movement, risk assessment, and strategic execution."
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else "No strategy available."

def morse_code_translate(text, to_morse=True):
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

def main():
    st.set_page_config(page_title="TacticaX", layout="wide", page_icon="⚔️")

    if "welcome_shown" not in st.session_state:
        st.session_state.welcome_shown = True
        with st.spinner("Initializing TacticaX..."):
            time.sleep(2)
        st.success("⚔️ Welcome to the TacticaX!")
        st.toast("Empowering Tactical Decisions with AI! 🚀", icon="🤖")

    st.sidebar.title("⚔️ TacticaX")
    choice = st.sidebar.radio("Navigation", ["🏠 Home", "📜 Mission Planning", "💡 Morse Code Communication", "📍 Geo-Fencing Messages"])

    if choice == "🏠 Home":
        st.title("⚡TacticaX⚡ ")
        st.subheader("A Cutting-Edge AI System for Tactical Warfare")
        st.write("""
        Welcome to the **TacticaX** – an advanced AI-driven system designed to 
        support **real-time tactical analysis, mission planning, encrypted communication, and intelligent decision-making**.
        
        🛡️ **Core Features**:  
        - 📜 **Mission Planning**: AI-generated battlefield strategies  
        - 💡 **Morse Code Communication**: Secure text encoding & decoding  
        - 📍 **Geo-Fencing**: Self-destruct messages for secure operations  
        """)

    elif choice == "📜 Mission Planning":
        st.title("📜 AI-Driven Mission Planning")
        mission_details = st.text_area("Enter Mission Details")
        if st.button("Generate Strategy"):
            ai_strategy = generate_ai_strategy_gemini(mission_details)
            st.write(f"**🛡️ Strategy for Mission:** {ai_strategy}")

    elif choice == "💡 Morse Code Communication":
        st.title("💡 Morse Code Communication")
        text_input = st.text_input("Enter Text to Convert")
        if st.button("Convert to Morse Code"):
            morse_code = morse_code_translate(text_input)
            st.write(f"**Morse Code:** {morse_code}")

    elif choice == "📍 Geo-Fencing Messages":
        st.title("📍 Geo-Fencing Self-Destruct Messages")
        user_lat = st.number_input("Enter Your Latitude")
        user_lon = st.number_input("Enter Your Longitude")
        message = st.text_area("Enter Secure Message")
        if st.button("Send Secure Message"):
            if is_within_geofence((user_lat, user_lon)):
                st.success("✅ Secure Message Sent Successfully!")
            else:
                st.error("❌ Access Denied: Message Self-Destructed Outside Geo-Fence!")

if __name__ == "__main__":
    main()
