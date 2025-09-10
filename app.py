import streamlit as st
import pandas as pd
import time
import random
import requests

# Page config
st.set_page_config(
    page_title="FloatChat - ARGO Data Explorer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for chat messages and layout
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
    }
    .user-message {
        background-color: #e6f7ff;
        border-left: 4px solid #1890ff;
        color: #000000;
    }
    .assistant-message {
        background-color: #f6ffed;
        border-left: 4px solid #52c41a;
        color: #000000;
    }
    .stButton button {
        width: 100%;
        background-color: #1890ff;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "voice" not in st.session_state:
    st.session_state.voice = "Google US English"
if "pitch" not in st.session_state:
    st.session_state.pitch = 1.0
if "rate" not in st.session_state:
    st.session_state.rate = 1.0

# API keys (Replace these with your actual keys or better use st.secrets for security)
OPENWEATHER_API_KEY = "3f8b16a724162f295bbff82b403997eb"
NEWSAPI_API_KEY = "a371a01adbbf44f6a30de37fa20a5d0f"

# Function to fetch live weather from OpenWeatherMap API
def get_weather_by_coords(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        return f"Current weather: {weather_desc.capitalize()}, Temperature: {temp}°C, Wind Speed: {wind_speed} m/s."
    except Exception as e:
        return "Sorry, I couldn't fetch weather data right now."

# Function to fetch latest ocean-related news from NewsAPI
def get_latest_news(api_key, query="ocean OR climate", page_size=3):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize={page_size}&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        if not articles:
            return "No recent news found."
        news_list = "\n".join([f"- {a['title']} ({a['source']['name']})" for a in articles])
        return f"Here are some recent news headlines:\n{news_list}"
    except Exception as e:
        return "Sorry, I couldn't fetch news right now."

# Function to generate AI-like responses based on user query
def get_ai_response(user_query):
    time.sleep(1)  # simulate thinking delay

    intro_phrases = [
        "Sure thing! 🌊",
        "You've got it! Here's what I found 👇",
        "Ahoy! Here's the info you asked for:",
        "Diving into the data... 🐠",
        "Let's explore together 🌐"
    ]
    outro_phrases = [
        "Let me know if you’d like to dive deeper! 🐬",
        "Need more ocean insights? Just ask! 🌊",
        "Wave if you want to keep exploring! 👋",
        "Always happy to chart the waters with you! ⚓"
    ]
    intro = random.choice(intro_phrases)
    outro = random.choice(outro_phrases)

    query = user_query.lower()

    # Handle weather queries
    if "weather" in query or "storm" in query or "rain" in query:
        # Example coords roughly center Indian Ocean (can be customized or enhanced later)
        lat, lon = -10.0, 80.0
        weather_info = get_weather_by_coords(lat, lon, OPENWEATHER_API_KEY)
        return f"{intro} {weather_info} {outro}"

    # Handle news queries
    elif "news" in query or "update" in query or "latest" in query:
        news_info = get_latest_news(NEWSAPI_API_KEY)
        return f"{intro} {news_info} {outro}"

    # Existing responses
    elif "temperature" in query or "temp" in query:
        return f"{intro} The average temperature in the Indian Ocean is around 28.5°C 📈. {outro}"
    elif "salinity" in query or "salt" in query:
        return f"{intro} Salinity levels are averaging around 34.8 PSU 🧂. {outro}"
    elif "map" in query or "location" in query or "where" in query:
        return f"{intro} Currently tracking 3 active floats in the Indian Ocean 🛰️. {outro}"
    elif "compare" in query or "difference" in query:
        return f"{intro} Here's a comparison of temperature and salinity across floats 📊. {outro}"
    elif "current" in query or "currents" in query:
        return f"{intro} Major currents include the Agulhas Current and the Somali Current 🌊, influencing marine life and climate. {outro}"
    elif "depth" in query or "deep" in query:
        return f"{intro} The Indian Ocean reaches depths over 7,000 meters in the Java Trench 🌐. {outro}"
    elif "marine life" in query or "animals" in query or "species" in query:
        return f"{intro} It hosts whales, dolphins, sea turtles, coral reefs, and many other species 🐋🐢🐠. {outro}"
    elif "climate change" in query or "warming" in query or "impact" in query:
        return f"{intro} Climate change affects ocean temperatures, sea level rise, and acidification, threatening marine ecosystems 🌍. {outro}"
    else:
        return f"{intro} I can help with temperature, salinity, ocean currents, marine life, weather, news, float maps, and more. What would you like to explore today? 🤿"

# Voice speaking function using browser's SpeechSynthesis API
def speak_text(text, voice_name, pitch, rate):
    safe_text = text.replace('"', '\\"').replace('\n', ' ')
    js_code = f"""
    <script>
    var voices = window.speechSynthesis.getVoices();
    var msg = new SpeechSynthesisUtterance("{safe_text}");
    msg.voice = voices.find(v => v.name === "{voice_name}") || null;
    msg.pitch = {pitch};
    msg.rate = {rate};
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

def main():
    st.markdown('<h1 class="main-header">🌊 FloatChat</h1>', unsafe_allow_html=True)
    st.markdown('### AI-Powered Conversational Interface for ARGO Ocean Data Discovery')

    # Sidebar with example queries and voice controls
    with st.sidebar:
        st.header("💡 Example Queries")
        examples = [
            "Show me temperature profiles near India",
            "Compare salinity at 100m depth in 2023",
            "Plot the trajectory of float 2902754",
            "Show me ARGO float locations in Arabian Sea",
            "Compare temperature between different floats",
            "What's the current weather in the Indian Ocean?",
            "Give me the latest news about the ocean"
        ]
        for example in examples:
            if st.button(example):
                st.session_state.messages.append({"role": "user", "content": example})
                response = get_ai_response(example)
                st.session_state.messages.append({"role": "assistant", "content": response})
                speak_text(response, st.session_state.voice, st.session_state.pitch, st.session_state.rate)

        st.markdown("---")
        st.header("🎤 Voice Personality Settings")

        voices_list = [
            "Google US English",
            "Google UK English Male",
            "Google UK English Female",
            "Microsoft Zira Desktop - English (United States)",
            "Microsoft David Desktop - English (United States)"
        ]
        voice = st.selectbox(
            "Select voice",
            voices_list,
            index=voices_list.index(st.session_state.voice) if st.session_state.voice in voices_list else 0
        )
        st.session_state.voice = voice

        pitch = st.slider("Pitch", 0.5, 2.0, st.session_state.pitch, 0.1)
        st.session_state.pitch = pitch

        rate = st.slider("Rate (speed)", 0.5, 2.0, st.session_state.rate, 0.1)
        st.session_state.rate = rate

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

    # User input box and send button
    user_input = st.text_input("Ask me about ocean data...", value=st.session_state.user_input, key="input")
    submit = st.button("Send")

    if submit and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = get_ai_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

        speak_text(response, st.session_state.voice, st.session_state.pitch, st.session_state.rate)
        st.session_state.user_input = ""

if __name__ == "__main__":
    main()
