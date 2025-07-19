"""
Google Maps API services for ScenicSync
"""
import streamlit as st
import requests
import math
import folium
from config import *

class GoogleMapsServices:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_available = api_key and api_key != "YOUR_GOOGLE_MAPS_API_KEY_HERE"
    
    def geocode_location(self, place_name):
        """Convert place name to coordinates using Google Geocoding API"""
        if not self.api_available:
            return self.geocode_location_fallback(place_name)
        
        try:
            params = {
                'address': place_name,
                'key': self.api_key,
                'region': 'us'
            }
            
            response = requests.get(GOOGLE_GEOCODING_URL, params=params, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    location = data['results'][0]['geometry']['location']
                    return [location['lat'], location['lng']]
                else:
                    st.warning(f"No results found for '{place_name}'")
            elif response.status_code == 403:
                st.error("Google Maps API key issue. Using fallback.")
                return self.geocode_location_fallback(place_name)
            else:
                st.warning(f"API error: {response.status_code}")
                
        except Exception as e:
            st.warning(f"Geocoding error: {str(e)}")
        
        return self.geocode_location_fallback(place_name)
    
    def geocode_location_fallback(self, place_name):
        """Fallback geocoding using built-in database"""
        place_lower = place_name.lower().strip()
        known_locations = self.get_known_locations()
        
        if place_lower in known_locations:
            return known_locations[place_lower]
        
        return None
    
    def get_known_locations(self):
        """Database of common locations"""
        return {
            "new york, ny": [40.7128, -74.0060],
            "new york city": [40.7128, -74.0060],
            "nyc": [40.7128, -74.0060],
            "boston, ma": [42.3601, -71.0589],
            "boston": [42.3601, -71.0589],
            "los angeles, ca": [34.0522, -118.2437],
            "chicago, il": [41.8781, -87.6298],
            "houston, tx": [29.7604, -95.3698],
            "philadelphia, pa": [39.9526, -75.1652],
            "san diego, ca": [32.7157, -117.1611],
            "san francisco, ca": [37.7749, -122.4194],
            "seattle, wa": [47.6062, -122.3321],
            "denver, co": [39.7392, -104.9903],
            "washington, dc": [38.9072, -77.0369],
            "miami, fl": [25.7617, -80.1918],
            "las vegas, nv": [36.1699, -115.1398],
            "atlanta, ga": [33.7490, -84.3880],
            "portland, or": [45.5152, -122.6784],
            "nashville, tn": [36.1627, -86.7816],
            "austin, tx": [30.2672, -97.7431],
            "bar harbor, me": [44.3876, -68.2039],
            "portsmouth, nh": [43.0717, -70.7625],
            "kennebunkport, me": [43.3615, -70.4767],
            "camden, me": [44.2098, -69.0648]
        }
    
    def get_directions(self, start_coords, end_coords, waypoints=None, avoid_highways=True):
        """Get directions using Google Directions API"""
        if not self.api_available:
            return self.create_simple_route(start_coords, end_coords, waypoints)
        
        try:
            params = {
                'origin': f"{start_coords[0]},{start_coords[1]}",
                'destination': f"{end_coords[0]},{end_coords[1]}",
                'key': self.api_key,
                'units': 'imperial'
            }
            
            if waypoints:
                waypoint_str = "|".join([f"{wp[0]},{wp[1]}" for wp in waypoints])
                params['waypoints'] = waypoint_str
            
            if avoid_highways:
                params['avoid'] = 'highways'
            
            response = requests.get(GOOGLE_DIRECTIONS_URL, params=params, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data['routes']:
                    return self.convert_google_route(data['routes'][0])
                else:
                    st.warning("No routes found")
            else:
                st.warning(f"Directions API error: {response.status_code}")
                
        except Exception as e:
            st.warning(f"Directions error: {str(e)}")
        
        return self.create_simple_route(start_coords, end_coords, waypoints)
    
    def find_places_along_route(self, start_coords, end_coords, place_types, radius_km=50):
        """Find places along a route using multiple search points"""
        if not self.api_available:
            return []
        
        places = []
        search_points = self.generate_route_search_points(start_coords, end_coords)
        
        for point in search_points:
            for place_type in place_types:
                try:
                    radius_meters = radius_km * 1000
                    nearby_places = self.search_places_near_point(point, place_type, radius_meters)
                    places.extend(nearby_places)
                except Exception as e:
                    st.warning(f"Error searching for {place_type}: {str(e)}")
        
        # Remove duplicates and limit results
        unique_places = []
        seen_place_ids = set()
        
        for place in places:
            place_id = place.get('place_id')
            if place_id and place_id not in seen_place_ids:
                unique_places.append(place)
                seen_place_ids.add(place_id)
        
        return unique_places[:MAX_PLACES_PER_SEARCH]
    
    def generate_route_search_points(self, start_coords, end_coords, num_points=5):
        """Generate search points along a route"""
        points = []
        for i in range(num_points):
            lat = start_coords[0] + (end_coords[0] - start_coords[0]) * i / (num_points - 1)
            lng = start_coords[1] + (end_coords[1] - start_coords[1]) * i / (num_points - 1)
            points.append([lat, lng])
        return points
    
    def search_places_near_point(self, coords, place_type, radius_meters):
        """Search for places near a specific point"""
        try:
            params = {
                'location': f"{coords[0]},{coords[1]}",
                'radius': radius_meters,
                'type': place_type,
                'key': self.api_key
            }
            
            response = requests.get(GOOGLE_PLACES_URL, params=params, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                places = []
                
                for place in data.get('results', []):
                    place_info = {
                        'place_id': place.get('place_id'),
                        'name': place.get('name'),
                        'rating': place.get('rating', 'N/A'),
                        'address': place.get('vicinity', 'Address not available'),
                        'coords': [
                            place['geometry']['location']['lat'],
                            place['geometry']['location']['lng']
                        ],
                        'place_type': place_type
                    }
                    places.append(place_info)
                
                return places
            else:
                st.warning(f"Places API error: {response.status_code}")
                
        except Exception as e:
            st.warning(f"Places search error: {str(e)}")
        
        return []
    
    def get_place_details(self, place_id):
        """Get detailed information about a specific place"""
        if not self.api_available:
            return None
        
        try:
            params = {
                'place_id': place_id,
                'key': self.api_key,
                'fields': 'name,formatted_address,formatted_phone_number,website,opening_hours,rating,reviews'
            }
            
            response = requests.get(GOOGLE_PLACE_DETAILS_URL, params=params, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('result', {})
            else:
                st.warning(f"Place details API error: {response.status_code}")
                
        except Exception as e:
            st.warning(f"Place details error: {str(e)}")
        
        return None
    
    def convert_google_route(self, google_route):
        """Convert Google Directions API response to our route format"""
        try:
            legs = google_route['legs']
            total_distance = sum(float(leg['distance']['text'].split()[0]) for leg in legs)
            total_duration = sum(float(leg['duration']['text'].split()[0]) for leg in legs)
            
            # Extract polyline points
            polyline_points = []
            for leg in legs:
                for step in leg['steps']:
                    if 'polyline' in step:
                        points = self.decode_polyline(step['polyline']['points'])
                        polyline_points.extend(points)
            
            return {
                'distance': total_distance,
                'duration': total_duration,
                'polyline_points': polyline_points
            }
        except Exception as e:
            st.warning(f"Route conversion error: {str(e)}")
            return None
    
    def decode_polyline(self, polyline_str):
        """Decode Google polyline string to coordinates"""
        try:
            points = []
            index = 0
            lat = 0
            lng = 0
            
            while index < len(polyline_str):
                # Decode latitude
                shift = 0
                result = 0
                while True:
                    byte = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (byte & 0x1F) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break
                lat += (~(result >> 1) if (result & 1) else (result >> 1))
                
                # Decode longitude
                shift = 0
                result = 0
                while True:
                    byte = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (byte & 0x1F) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break
                lng += (~(result >> 1) if (result & 1) else (result >> 1))
                
                points.append([lat * 1e-5, lng * 1e-5])
            
            return points
        except Exception as e:
            st.warning(f"Polyline decode error: {str(e)}")
            return []
    
    def create_simple_route(self, start_coords, end_coords, waypoints=None):
        """Create a simple straight-line route when API is not available"""
        try:
            # Calculate distance using Haversine formula
            lat1, lng1 = start_coords
            lat2, lng2 = end_coords
            
            R = 3959  # Earth's radius in miles
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lng = math.radians(lng2 - lng1)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
            
            # Estimate duration (assuming 60 mph average)
            duration = distance / 60
            
            # Create simple polyline
            polyline_points = [start_coords, end_coords]
            
            return {
                'distance': round(distance, 1),
                'duration': round(duration, 1),
                'polyline_points': polyline_points
            }
        except Exception as e:
            st.warning(f"Simple route creation error: {str(e)}")
            return None
    
    def get_route_stats(self, route):
        """Get distance and duration from route"""
        if route:
            return route.get('distance', 0), route.get('duration', 0)
        return 0, 0
    
    def create_route_map(self, route, start_coords, end_coords, waypoints=None, places=None):
        """Create an interactive map with the route and places"""
        try:
            # Calculate map center
            all_coords = [start_coords, end_coords]
            if waypoints:
                all_coords.extend([wp['coords'] for wp in waypoints])
            
            center_lat = sum(coord[0] for coord in all_coords) / len(all_coords)
            center_lng = sum(coord[1] for coord in all_coords) / len(all_coords)
            
            # Create map
            route_map = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=DEFAULT_ZOOM,
                tiles='OpenStreetMap'
            )
            
            # Add route polyline
            if route and route.get('polyline_points'):
                folium.PolyLine(
                    locations=route['polyline_points'],
                    color='#4CAF50',
                    weight=4,
                    opacity=0.8,
                    popup='Your Scenic Route'
                ).add_to(route_map)
            
            # Add start marker
            folium.Marker(
                location=start_coords,
                popup=f"Start: {start_coords}",
                icon=folium.Icon(color='green', icon='play')
            ).add_to(route_map)
            
            # Add end marker
            folium.Marker(
                location=end_coords,
                popup=f"End: {end_coords}",
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(route_map)
            
            # Add waypoints
            if waypoints:
                for i, waypoint in enumerate(waypoints):
                    folium.Marker(
                        location=waypoint['coords'],
                        popup=f"Stop {i+1}: {waypoint['name']}",
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(route_map)
            
            # Add discovered places
            if places:
                for place in places:
                    folium.Marker(
                        location=place['coords'],
                        popup=f"{place['name']}<br>Rating: {place['rating']}<br>{place['address']}",
                        icon=folium.Icon(color='orange', icon='star')
                    ).add_to(route_map)
            
            return route_map
            
        except Exception as e:
            st.error(f"Map creation error: {str(e)}")
            # Return a simple map as fallback
            return folium.Map(location=[40, -100], zoom_start=4) 