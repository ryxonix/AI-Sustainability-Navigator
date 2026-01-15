import requests
from groq import Groq
from geopy.geocoders import Nominatim
try:
    from config import GROQ_API_KEY
except ImportError:
    GROQ_API_KEY = "your groq key"
client = Groq(api_key=GROQ_API_KEY)
geolocator = Nominatim(user_agent="sustainability_navigator_1m1b")

def get_coords(city_name):
    """Retrieves Lat/Long for any city name."""
    try:
        location = geolocator.geocode(city_name)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception:
        return None, None

def retrieve_weather_rag(lat, lon):
    """The 'Retrieval' part of RAG: Fetches real-time temperature."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url).json()
        return response['current_weather']['temperature']
    except Exception:
        return "Unknown"
def sustainable_navigator(from_city, to_city):
    """Main function that combines RAG with LLM reasoning."""
    lat, lon = get_coords(from_city)
    if lat is None:
        return f"Error: Could not locate the city '{from_city}'."
    
    live_temp = retrieve_weather_rag(lat, lon)
    shade_context = "Local data shows 40% more tree canopy on 'Garden Streets' vs 'Main Highways'."
    prompt = f"""
    You are an AI Sustainability Navigator (SDG 11 & SDG 3).
    User Trip: {from_city} to {to_city}.
    Live Temperature in {from_city}: {live_temp}°C.
    Environmental Context: {shade_context}

    Task:
    Display the temperature of from and to cities.
    
    Suggest a 'Cool Route' strategy. Provide a Google Maps link: 
    https://www.google.com/maps/dir/{from_city}/{to_city}/

    Give landmarks to visit along the route.
    
    Explain how this travel plan supports SDG 11 (Sustainable Cities) and 
    SDG 3 (Health). Mention a safety tip for {live_temp}°C weather.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("--- 🌍 AI Sustainability Navigator (1M1B Prototype) ---")
    start = input("Enter Starting City: ")
    end = input("Enter Destination: ")
    
    print(f"\n[System] Retrieving live climate data for {start}...")
    result = sustainable_navigator(start, end)
    
    print("\n" + "="*50)
    print(result)
    print("="*50)
