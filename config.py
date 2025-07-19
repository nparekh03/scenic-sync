"""
Configuration settings for ScenicSync
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Maps API Configuration
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

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