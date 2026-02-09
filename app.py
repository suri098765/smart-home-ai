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

    /* Dashboard Grid */
    .dashboard-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        padding: 20px;
    }

    /* Room Card - Ultra Glassmorphism */
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
    }

    /* Decorative Scanline Effect */
    .room-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: scan 3s linear infinite;
    }

    @keyframes scan {
        0% { top: 0%; }
        100% { top: 100%; }
    }

    .icon-style { 
        font-size: 90px; 
        margin-bottom: 25px; 
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));
        transition: transform 0.3s ease;
    }

    .room-card:hover .icon-style { transform: scale(1.1) rotate(5deg); }

    /* Room-Specific Neon Glows */
    .hall-active { border-color: #ffcc00; box-shadow: 0 0 30px rgba(255, 204, 0, 0.4), inset 0 0 20px rgba(255, 204, 0, 0.1); }
    .bedroom-active { border-color: #00d4ff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.4), inset 0 0 20px rgba(0, 212, 255, 0.1); }
    .kitchen-active { border-color: #00ff88; box-shadow: 0 0 30px rgba(0, 255, 136, 0.4), inset 0 0 20px rgba(0, 255, 136, 0.1); }
    .dining-active { border-color: #ff4d4d; box-shadow: 0 0 30px rgba(255, 77, 77, 0.4), inset 0 0 20px rgba(255, 77, 77, 0.1); }

    /* Animated Power Button Refined */
    .power-btn {
        width: 65px; height: 65px;
        border-radius: 50%;
        margin: 30px auto 0;
        background: #111;
        border: 4px solid #222;
        display: flex; align-items: center; justify-content: center;
        position: relative;
    }

    .active-btn {
        background: #000;
        border-color: #39FF14;
        box-shadow: 0 0 15px #39FF14, inset 0 0 10px #39FF14;
    }

    .active-btn::after {
        content: "";
        width: 15px; height: 15px;
        background: #39FF14;
        border-radius: 50%;
        box-shadow: 0 0 20px #39FF14;
        animation: glow-pulse 1s infinite alternate;
    }

    @keyframes glow-pulse {
        from { opacity: 0.5; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1.2); }
    }

    /* Voice Trigger Button */
    .stButton > button {
        background: linear-gradient(45deg, #00f2ff, #0062ff);
        color: white; border: none; padding: 15px 30px;
        border-radius: 50px; font-weight: bold;
        box-shadow: 0 10px 20px rgba(0, 98, 255, 0.3);
        transition: 0.3s;
    }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(0, 98, 255, 0.5); }
</style>
""", unsafe_allow_html=True)

# --- Logic & Voice Engine (Keeping Your State Management) ---
if 'active_room' not in st.session_state:
    st.session_state.active_room = "none"

def process_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎤 System Listening...")
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            text = r.recognize_google(audio).lower()
            
            if "hall" in text: st.session_state.active_room = "hall"
            elif "bedroom" in text: st.session_state.active_room = "bedroom"
            elif "kitchen" in text: st.session_state.active_room = "kitchen"
            elif "dining" in text: st.session_state.active_room = "dining"
            elif "off" in text: st.session_state.active_room = "none"
            
        except Exception:
            st.error("Audio not captured.")

# --- UI Structure ---
st.markdown('<h1 class="main-title">AI HOME CONTROL CENTER</h1>', unsafe_allow_html=True)

if st.button("ACTIVATE VOICE INTERFACE", use_container_width=True):
    process_voice()

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
            <h3 style="font-family: 'Inter'; letter-spacing: 2px; font-weight: 300;">{room['name']}</h3>
            <div class="power-btn {'active-btn' if active else ''}"></div>
            <p style="margin-top: 15px; font-size: 0.8rem; color: {'#39FF14' if active else '#555'};">
                {'● POWER ACTIVE' if active else '○ STANDBY'}
            </p>
        </div>
        """, unsafe_allow_html=True)
