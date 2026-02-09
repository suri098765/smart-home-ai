import streamlit as st
import speech_recognition as sr

# --- Page Setup ---
st.set_page_config(page_title="Next-Gen Smart Home AI", layout="wide")

# --- Enhanced Realistic CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #1a1a2e 0%, #050505 100%); 
    }
    
    .main-title {
        font-family: 'Syncopate', sans-serif;
        color: #ffffff;
        text-align: center;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 40px;
        background: linear-gradient(to right, #00f2ff, #0062ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .room-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 50px 20px;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }

    .icon-style { font-size: 70px; margin-bottom: 20px; }

    /* Neon Glows */
    .hall-active { border-color: #ffcc00; box-shadow: 0 0 30px rgba(255, 204, 0, 0.4); }
    .bedroom-active { border-color: #00d4ff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.4); }
    .kitchen-active { border-color: #00ff88; box-shadow: 0 0 30px rgba(0, 255, 136, 0.4); }
    .dining-active { border-color: #ff4d4d; box-shadow: 0 0 30px rgba(255, 77, 77, 0.4); }

    .power-btn {
        width: 40px; height: 40px;
        border-radius: 50%;
        margin: 20px auto 0;
        background: #111;
        border: 3px solid #222;
    }

    .active-btn {
        background: #39FF14;
        box-shadow: 0 0 15px #39FF14;
        border-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'active_room' not in st.session_state:
    st.session_state.active_room = "none"

# --- UI Structure ---
st.markdown('<h1 class="main-title">AI HOME CONTROL CENTER</h1>', unsafe_allow_html=True)

# --- MOBILE VOICE INTERFACE ---
# This widget is the key to fixing the error on your phone
# --- Replace your old 'Activate' button logic with this ---

# This creates the browser-compatible mic that avoids the OSError
audio_data = st.audio_input("Activate Voice Interface")

if audio_data:
    st.info("Processing your command...")
    
    # Use the SpeechRecognition library to read the captured file
    r = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = r.record(source)
        try:
            # Convert speech to text
            text = r.recognize_google(audio)
            st.success(f"Command Received: {text}")
            
            # Add your logic here, for example:
            if "lounge" in text.lower():
                st.write("Adjusting Main Lounge settings...")
                
        except Exception as e:
            st.error("Could not understand the audio. Please try again.")

# --- Dashboard Display ---
rooms = [
    {"id": "hall", "name": "MAIN LOUNGE", "icon": "🛋️", "class": "hall-active"},
    {"id": "bedroom", "name": "SLEEP SUITE", "icon": "🛏️", "class": "bedroom-active"},
    {"id": "kitchen", "name": "CULINARY HUB", "icon": "🍳", "class": "kitchen-active"},
    {"id": "dining", "name": "DINING SPACE", "icon": "🍽️", "class": "dining-active"},
]

col1, col2 = st.columns(2)
for i, room in enumerate(rooms):
    active = st.session_state.active_room == room["id"]
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"""
        <div class="room-card {room['class'] if active else ''}">
            <div class="icon-style">{room['icon']}</div>
            <h3 style="font-family: 'Inter'; color: white;">{room['name']}</h3>
            <div class="power-btn {'active-btn' if active else ''}"></div>
            <p style="color: {'#39FF14' if active else '#555'}; font-size: 0.8rem;">
                {'● ACTIVE' if active else '○ STANDBY'}
            </p>
        </div>
        """, unsafe_allow_html=True)


