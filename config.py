"""
Configuration settings for ScenicSync
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Maps API Configuration
# Try to get API key from environment variables or Streamlit secrets
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# If running in Streamlit, try to get from secrets
try:
    import streamlit as st
    if hasattr(st, 'secrets') and st.secrets.get("GOOGLE_MAPS_API_KEY"):
        GOOGLE_MAPS_API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]
        print(f"✅ API Key loaded from Streamlit secrets: {GOOGLE_MAPS_API_KEY[:10]}...")
    else:
        print(f"⚠️ No API key found in Streamlit secrets. Current key: {GOOGLE_MAPS_API_KEY[:10] if GOOGLE_MAPS_API_KEY else 'None'}...")
except ImportError:
    print("⚠️ Streamlit not available, using environment variables only")
except Exception as e:
    print(f"⚠️ Error loading secrets: {e}")

# Google Maps API endpoints
GOOGLE_GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
GOOGLE_PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# App Settings
APP_TITLE = "ScenicSync"
APP_SUBTITLE = "Take the long way. On purpose."
MAP_HEIGHT = int(os.getenv("MAP_HEIGHT", "500"))
DEFAULT_ZOOM = int(os.getenv("DEFAULT_ZOOM", "8"))

# API Settings
REQUEST_TIMEOUT = 15
MAX_PLACES_PER_SEARCH = 20 