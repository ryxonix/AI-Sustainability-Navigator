import requests
from groq import Groq
from geopy.geocoders import Nominatim
try:
    from config import GROQ_API_KEY
except ImportError:
    GROQ_API_KEY = "your groq key"
