"""
ScenicSync - Take the long way. On purpose.
Complete scenic route planning with attractions, dining, and utilities
"""

import streamlit as st
from streamlit_folium import st_folium
from urllib.parse import quote

# Import our modules
from config import *
from services import GoogleMapsServices
from utils import apply_custom_css, get_place_type_options, format_place_card, get_scenic_routes

def main():
    # Page setup
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🌄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply styling
    apply_custom_css()
    
    # Get API key from Streamlit secrets (this ensures it's loaded after Streamlit starts)
    api_key = ""
    
    try:
        # Check if st.secrets exists and get API key
        if hasattr(st, 'secrets') and "GOOGLE_MAPS_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
        else:
            # Fallback to environment variable
            import os
            api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
                
    except Exception as e:
        # Silent fallback to environment variable
        import os
        api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Initialize services
    maps_service = GoogleMapsServices(api_key)
    scenic_routes = get_scenic_routes()
    place_types = get_place_type_options()
    
    # App Header
    st.markdown(f'<h1 class="main-title">🌄 {APP_TITLE}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{APP_SUBTITLE}</p>', unsafe_allow_html=True)
    
    # API Status
    if maps_service.api_available:
        st.markdown('<div class="success-message">✅ Google Maps API is active - Full functionality enabled</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-message">⚠️ Using fallback mode - add your Google Maps API key for full functionality</div>', unsafe_allow_html=True)
    
    # Session state
    if 'route_data' not in st.session_state:
        st.session_state.route_data = None
    if 'discovered_places' not in st.session_state:
        st.session_state.discovered_places = []
    
    # Sidebar for route planning
    with st.sidebar:
        st.header("🗺️ Plan Your Route")
        
        # Route type selection
        route_type = st.selectbox(
            "Choose Route Type",
            ["Custom Route", "Predefined Scenic Routes"]
        )
        
        if route_type == "Custom Route":
            st.subheader("📍 Your Journey")
            
            # Location inputs
            start_location = st.text_input(
                "Start Location",
                placeholder="e.g., Boston, MA"
            )
            
            end_location = st.text_input(
                "End Location", 
                placeholder="e.g., Bar Harbor, ME"
            )
            
            # Quick location buttons
            st.write("**Quick Locations:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📍 NYC"):
                    st.session_state.start_location = "New York, NY"
                if st.button("📍 Boston"):
                    st.session_state.start_location = "Boston, MA"
            with col2:
                if st.button("📍 SF"):
                    st.session_state.end_location = "San Francisco, CA"
                if st.button("📍 LA"):
                    st.session_state.end_location = "Los Angeles, CA"
            
            # Route options
            st.subheader("⚙️ Route Options")
            avoid_highways = st.checkbox("Avoid major highways", value=True)
            
            # Place discovery options
            st.subheader("🔍 Discover Places")
            discover_places = st.checkbox("Find attractions & amenities", value=True)
            
            if discover_places:
                st.write("**Select what to find along your route:**")
                
                selected_place_types = []
                
                for category, types in place_types.items():
                    with st.expander(category):
                        for type_key, type_name in types.items():
                            if st.checkbox(type_name, key=f"place_{type_key}"):
                                selected_place_types.append(type_key)
                
                search_radius = st.slider("Search radius (km)", 10, 100, 50)
        
        else:
            st.subheader("🗺️ Curated Routes")
            selected_route = st.selectbox(
                "Choose a Scenic Route",
                list(scenic_routes.keys())
            )
            
            if selected_route:
                route_info = scenic_routes[selected_route]
                st.write(f"**{route_info['description']}**")
                
                st.write("**Stops:**")
                for waypoint in route_info['waypoints']:
                    st.write(f"• {waypoint['name']}")
            
            # Place discovery for predefined routes
            st.subheader("🔍 Discover Places")
            discover_places = st.checkbox("Find attractions & amenities", value=True, key="predefined_discover")
            
            if discover_places:
                selected_place_types = ['restaurant', 'tourist_attraction', 'gas_station', 'lodging']
                search_radius = 30
        
        # Generate route button
        if st.button("🚀 Generate Route", type="primary", use_container_width=True):
            with st.spinner("Creating your scenic route..."):
                if route_type == "Custom Route" and start_location and end_location:
                    # Custom route logic
                    start_coords = maps_service.geocode_location(start_location)
                    
                    if start_coords:
                        st.success(f"✅ Found {start_location}")
                        end_coords = maps_service.geocode_location(end_location)
                        
                        if end_coords:
                            st.success(f"✅ Found {end_location}")
                            
                            # Get route
                            route = maps_service.get_directions(
                                start_coords, 
                                end_coords, 
                                avoid_highways=avoid_highways
                            )
                            
                            if route:
                                st.session_state.route_data = {
                                    'route': route,
                                    'start_coords': start_coords,
                                    'end_coords': end_coords,
                                    'start_name': start_location,
                                    'end_name': end_location,
                                    'waypoints': [],
                                    'route_name': f"{start_location} to {end_location}"
                                }
                                
                                # Discover places along route
                                if discover_places and selected_place_types:
                                    with st.spinner("🔍 Discovering attractions and amenities..."):
                                        places = maps_service.find_places_along_route(
                                            start_coords, 
                                            end_coords, 
                                            selected_place_types,
                                            search_radius
                                        )
                                        st.session_state.discovered_places = places
                                        st.success(f"🎉 Found {len(places)} places along your route!")
                                else:
                                    st.session_state.discovered_places = []
                                
                                st.success("🎉 Route generated!")
                                st.rerun()  # Force refresh to show the route
                            else:
                                st.error("Failed to generate route")
                        else:
                            st.error(f"Could not find: {end_location}")
                    else:
                        st.error(f"Could not find: {start_location}")
                
                elif route_type == "Predefined Scenic Routes":
                    # Predefined route logic
                    route_info = scenic_routes[selected_route]
                    waypoints = route_info['waypoints']
                    
                    if len(waypoints) >= 2:
                        start_coords = waypoints[0]['coords']
                        end_coords = waypoints[-1]['coords']
                        
                        route = maps_service.get_directions(start_coords, end_coords)
                        
                        if route:
                            st.session_state.route_data = {
                                'route': route,
                                'start_coords': start_coords,
                                'end_coords': end_coords,
                                'start_name': waypoints[0]['name'],
                                'end_name': waypoints[-1]['name'],
                                'waypoints': waypoints,
                                'route_name': selected_route
                            }
                            
                            # Discover places for predefined routes
                            if discover_places:
                                with st.spinner("🔍 Discovering attractions and amenities..."):
                                    places = maps_service.find_places_along_route(
                                        start_coords, 
                                        end_coords, 
                                        selected_place_types,
                                        search_radius
                                    )
                                    st.session_state.discovered_places = places
                                    st.success(f"🎉 Found {len(places)} places along your route!")
                            
                            st.success("🎉 Route loaded!")
                            st.rerun()  # Force refresh to show the route
                
                else:
                    st.error("Please fill in all fields")
    
    # MAIN CONTENT AREA - Always show, regardless of route status
    
    # Show current route if exists
    if st.session_state.route_data:
        route_data = st.session_state.route_data
        route = route_data['route']
        places = st.session_state.discovered_places
        
        # Route header - ALWAYS VISIBLE
        st.header(f"🛣️ {route_data['route_name']}")
        
        # Route statistics in columns
        col1, col2, col3, col4 = st.columns(4)
        distance, duration = maps_service.get_route_stats(route)
        
        with col1:
            st.metric("Distance", f"{distance} miles")
        with col2:
            st.metric("Duration", f"{duration} hours")
        with col3:
            st.metric("Route Stops", len(route_data['waypoints']) + 2)
        with col4:
            st.metric("Places Found", len(places))
        
        # Google Maps link - RIGHT AFTER STATS, BEFORE MAP
        st.markdown("---")
        maps_link = f"https://www.google.com/maps/dir/{quote(route_data['start_name'])}/{quote(route_data['end_name'])}"
        
        # Create columns for buttons
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            st.markdown(f"""
            <div style="text-align: center; margin: 10px 0;">
                <a href="{maps_link}" target="_blank" class="maps-button">
                    📱 Open Full Route in Google Maps
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        # Create and display map - AFTER GOOGLE MAPS BUTTON
        st.subheader("🗺️ Interactive Route Map")
        
        route_map = maps_service.create_route_map(
            route,
            route_data['start_coords'],
            route_data['end_coords'],
            route_data['waypoints'],
            places
        )
        
        # Display map with proper sizing
        map_data = st_folium(route_map, height=MAP_HEIGHT, use_container_width=True)
        
        # Places discovery results
        if places:
            st.markdown("---")
            st.subheader(f"🔍 Discovered Places Along Your Route ({len(places)} found)")
            
            # Filter and categorize places
            place_categories = {}
            for place in places:
                place_type = place.get('place_type', 'other')
                if place_type not in place_categories:
                    place_categories[place_type] = []
                place_categories[place_type].append(place)
            
            # Create tabs for different place categories
            if place_categories:
                # Get category display names
                category_names = []
                category_keys = []
                
                type_display_names = {}
                for cat_name, types in get_place_type_options().items():
                    for type_key, type_display in types.items():
                        type_display_names[type_key] = type_display
                
                for place_type in place_categories.keys():
                    display_name = type_display_names.get(place_type, place_type.replace('_', ' ').title())
                    category_names.append(f"{display_name} ({len(place_categories[place_type])})")
                    category_keys.append(place_type)
                
                if category_names:
                    tabs = st.tabs(category_names)
                    
                    for i, (tab, place_type) in enumerate(zip(tabs, category_keys)):
                        with tab:
                            places_in_category = place_categories[place_type]
                            
                            # Sort by rating (highest first)
                            places_in_category.sort(key=lambda x: x.get('rating', 0), reverse=True)
                            
                            # Display places in a grid
                            for j in range(0, len(places_in_category), 2):
                                cols = st.columns(2)
                                
                                for k, col in enumerate(cols):
                                    if j + k < len(places_in_category):
                                        place = places_in_category[j + k]
                                        
                                        with col:
                                            # Create place card
                                            st.markdown(format_place_card(place), unsafe_allow_html=True)
                                            
                                            # Add action buttons
                                            place_coords = f"{place['coords'][0]},{place['coords'][1]}"
                                            place_maps_link = f"https://www.google.com/maps/place/?q={place_coords}"
                                            
                                            btn_col_1, btn_col_2 = st.columns(2)
                                            with btn_col_1:
                                                st.markdown(f"""
                                                <a href="{place_maps_link}" target="_blank" class="maps-button" style="font-size: 12px; padding: 8px 16px;">
                                                    📍 View in Maps
                                                </a>
                                                """, unsafe_allow_html=True)
                                            
                                            with btn_col_2:
                                                if st.button(f"ℹ️ Details", key=f"details_{place.get('place_id', j+k)}"):
                                                    # Get additional details
                                                    if place.get('place_id'):
                                                        details = maps_service.get_place_details(place['place_id'])
                                                        if details:
                                                            st.json(details)  # Display detailed info
        
        # Show waypoints if any
        if route_data['waypoints']:
            st.markdown("---")
            st.subheader("⭐ Scenic Stops Along Your Route")
            for i, waypoint in enumerate(route_data['waypoints']):
                with st.expander(f"Stop {i+1}: {waypoint['name']}"):
                    st.write(waypoint['description'])
                    
                    # Add Google Maps link for each waypoint
                    waypoint_coords = f"{waypoint['coords'][0]},{waypoint['coords'][1]}"
                    waypoint_maps_link = f"https://www.google.com/maps/place/?q={waypoint_coords}"
                    st.markdown(f"[📍 View {waypoint['name']} in Google Maps]({waypoint_maps_link})")
    
    else:
        # Welcome screen - ALWAYS VISIBLE when no route
        st.header("🌄 ScenicSync")
        st.subheader("Take the long way. On purpose.")
        
        st.markdown("### 🌟 Ready for an Adventure?")
        st.write("Use the sidebar to plan your scenic route and discover amazing places along the way!")
        
        # Show features in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✨ Route Features")
            st.write("🗺️ **Google Maps Integration** - Accurate routes and locations")
            st.write("📍 **Scenic Route Planning** - Avoid highways, find beautiful roads")
            st.write("⭐ **Curated Routes** - Pre-planned scenic drives")
            st.write("📱 **Mobile Export** - Open routes in Google Maps app")
        
        with col2:
            st.markdown("### 🔍 Place Discovery")
            st.write("🍽️ **Restaurants & Cafes** - Find great dining along your route")
            st.write("🎯 **Tourist Attractions** - Discover museums, parks, and landmarks")
            st.write("🏨 **Accommodations** - Hotels, campgrounds, and RV parks")
            st.write("⛽ **Utilities** - Gas stations, ATMs, hospitals, and pharmacies")
            st.write("🛍️ **Shopping** - Malls, grocery stores, and local shops")
        
        # Show example routes
        st.markdown("### 🛣️ Popular Scenic Routes")
        
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            st.info("""
            **🌊 New England Coastal**
            Boston, MA → Bar Harbor, ME
            • Historic seaports
            • Lighthouse views
            • Fresh lobster stops
            """)
        
        with example_col2:
            st.info("""
            **🏔️ Pacific Coast Highway**
            San Francisco, CA → Los Angeles, CA
            • Dramatic coastlines
            • Redwood forests
            • Artistic communities
            """)
        
        # Quick start guide
        st.markdown("### 🚀 Quick Start Guide")
        st.write("""
        1. **Choose Route Type**: Custom route or predefined scenic drive
        2. **Enter Locations**: Start and end destinations
        3. **Select Preferences**: What places to discover along the way
        4. **Generate Route**: Click the button and explore your journey!
        5. **Explore Results**: View map, places, and export to Google Maps
        """)

if __name__ == "__main__":
    main() 