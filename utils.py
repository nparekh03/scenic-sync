"""
Utility functions for ScenicSync
"""
import streamlit as st
from urllib.parse import quote

def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #4CAF50;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .route-stats {
        display: flex;
        justify-content: space-around;
        background: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .place-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .place-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .place-rating {
        color: #ff9800;
        margin-left: 0.5rem;
    }
    .place-details {
        font-size: 0.9rem;
        color: #666;
        margin: 0.25rem 0;
    }
    .maps-button {
        background: #4CAF50;
        color: white;
        padding: 12px 24px;
        text-decoration: none;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 10px 5px;
        text-align: center;
        border: none;
    }
    .maps-button:hover {
        background: #45a049;
        text-decoration: none;
        color: white;
    }
    .attraction-type {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_place_type_options():
    """Get available place type options for discovery"""
    return {
        "Food & Dining": {
            "restaurant": "🍽️ Restaurants",
            "cafe": "☕ Cafes & Coffee Shops",
            "bakery": "🥐 Bakeries",
            "bar": "🍺 Bars & Pubs",
            "food": "🍕 Food Courts"
        },
        "Attractions": {
            "tourist_attraction": "🎯 Tourist Attractions",
            "museum": "🏛️ Museums",
            "park": "🌳 Parks & Gardens",
            "amusement_park": "🎢 Amusement Parks",
            "aquarium": "🐠 Aquariums",
            "zoo": "🦁 Zoos"
        },
        "Accommodation": {
            "lodging": "🏨 Hotels & Lodging",
            "campground": "⛺ Campgrounds",
            "rv_park": "🚐 RV Parks"
        },
        "Utilities": {
            "gas_station": "⛽ Gas Stations",
            "atm": "🏧 ATMs",
            "hospital": "🏥 Hospitals",
            "pharmacy": "💊 Pharmacies",
            "police": "👮 Police Stations"
        },
        "Shopping": {
            "shopping_mall": "🛍️ Shopping Malls",
            "grocery_or_supermarket": "🛒 Grocery Stores",
            "convenience_store": "🏪 Convenience Stores"
        }
    }

def format_place_card(place):
    """Format a place as an HTML card"""
    name = place.get('name', 'Unknown Place')
    rating = place.get('rating', 'N/A')
    address = place.get('address', 'Address not available')
    place_type = place.get('place_type', 'other')
    
    # Get display name for place type
    type_display_names = {}
    for cat_name, types in get_place_type_options().items():
        for type_key, type_display in types.items():
            type_display_names[type_key] = type_display
    
    display_type = type_display_names.get(place_type, place_type.replace('_', ' ').title())
    
    return f"""
    <div class="place-card">
        <div class="place-header">
            <strong>{name}</strong>
            <span class="place-rating">⭐ {rating}</span>
        </div>
        <div class="place-details">
            <span class="attraction-type">{display_type}</span>
        </div>
        <div class="place-details">
            📍 {address}
        </div>
    </div>
    """

def get_scenic_routes():
    """Get predefined scenic routes"""
    return {
        "New England Coastal": {
            "description": "Historic seaports, lighthouses, and fresh lobster",
            "waypoints": [
                {"name": "Boston, MA", "coords": [42.3601, -71.0589], "description": "Historic city with rich maritime heritage"},
                {"name": "Portsmouth, NH", "coords": [43.0717, -70.7625], "description": "Charming seaport with colonial architecture"},
                {"name": "Kennebunkport, ME", "coords": [43.3615, -70.4767], "description": "Picturesque coastal town with lobster shacks"},
                {"name": "Camden, ME", "coords": [44.2098, -69.0648], "description": "Beautiful harbor with sailing opportunities"},
                {"name": "Bar Harbor, ME", "coords": [44.3876, -68.2039], "description": "Gateway to Acadia National Park"}
            ]
        },
        "Pacific Coast Highway": {
            "description": "Dramatic coastlines, redwood forests, and artistic communities",
            "waypoints": [
                {"name": "San Francisco, CA", "coords": [37.7749, -122.4194], "description": "Iconic city with Golden Gate Bridge"},
                {"name": "Monterey, CA", "coords": [36.6002, -121.8947], "description": "Historic fishing village and aquarium"},
                {"name": "Big Sur, CA", "coords": [36.2704, -121.8081], "description": "Spectacular coastal cliffs and redwoods"},
                {"name": "Santa Barbara, CA", "coords": [34.4208, -119.6982], "description": "Spanish colonial architecture and beaches"},
                {"name": "Los Angeles, CA", "coords": [34.0522, -118.2437], "description": "Entertainment capital with diverse culture"}
            ]
        }
    } 