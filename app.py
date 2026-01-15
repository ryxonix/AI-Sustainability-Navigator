import streamlit as st
import requests
from groq import Groq
from geopy.geocoders import Nominatim

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sustainability Navigator", page_icon="🌍")

# --- INITIALIZATION ---
# It's better to use Streamlit secrets or a text input for the key

# 1. Try to get the key from Streamlit Secrets (for Web/Cloud)
# 2. Fallback to st.sidebar input if Secrets are missing
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = st.sidebar.text_input("Paste your Groq API Key here:", type="password")

# Only initialize if the key actually exists to avoid the TypeError
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    st.error("Please add your GROQ_API_KEY to Streamlit Secrets or the sidebar.")
    st.stop() # Prevents the rest of the app from running and crashing

client = Groq(api_key=GROQ_API_KEY)
geolocator = Nominatim(user_agent="sustainability_navigator_1m1b")

# --- YOUR ORIGINAL FUNCTIONS ---
def get_coords(city_name):
    try:
        location = geolocator.geocode(city_name)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception:
        return None, None

def retrieve_weather_rag(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url).json()
        return response['current_weather']['temperature']
    except Exception:
        return "Unknown"

# --- WEB INTERFACE ---
st.title("🌍 AI Sustainability Navigator")
st.markdown("### SDG 11 (Sustainable Cities) & SDG 3 (Health & Well-being)")

# Layout for inputs
col1, col2 = st.columns(2)
with col1:
    start_city = st.text_input("Starting City", placeholder="e.g. Mumbai")
with col2:
    end_city = st.text_input("Destination", placeholder="e.g. Bangalore")

if st.button("Generate Sustainable Route"):
    if not GROQ_API_KEY:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif start_city and end_city:
        with st.spinner(f"Analyzing climate data for {start_city}..."):
            # Logic execution
            lat, lon = get_coords(start_city)
            
            if lat is None:
                st.error(f"Could not locate the city: {start_city}")
            else:
                live_temp = retrieve_weather_rag(lat, lon)
                shade_context = "Local data shows 40% more tree canopy on 'Garden Streets' vs 'Main Highways'."
                
                prompt = f"""
                You are an AI Sustainability Navigator (SDG 11 & SDG 3).
                User Trip: {start_city} to {end_city}.
                Live Temperature in {start_city}: {live_temp}°C.
                Environmental Context: {shade_context}

                Task:
                Display the temperature of from and to cities.
                Suggest a 'Cool Route' strategy. Provide a Google Maps link.
                Give landmarks to visit along the route.
                Explain how this supports SDG 11 and SDG 3. 
                Mention a safety tip for {live_temp}°C weather.
                """

                try:
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    # Display Result
                    st.divider()
                    st.markdown(chat_completion.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter both cities.")
