import streamlit as st
from urllib.parse import quote

# Your Google Maps Embed API key
GMAPS_API_KEY = ""

# Define scenic route options
ROUTES = {
    "Boston → Bar Harbor": ["Boston, MA", "Portsmouth, NH", "Camden, ME", "Bar Harbor, ME"],
    "NYC → Lake Placid": ["New York, NY", "Cold Spring, NY", "Saranac Lake, NY", "Lake Placid, NY"],
    "Philadelphia → Shenandoah": ["Philadelphia, PA", "Lancaster, PA", "Harpers Ferry, WV", "Shenandoah National Park, VA"],
    "Chicago → Upper Peninsula": ["Chicago, IL", "Milwaukee, WI", "Green Bay, WI", "Pictured Rocks National Lakeshore, MI"],
    "Seattle → Olympic Peninsula": ["Seattle, WA", "Port Townsend, WA", "Forks, WA", "Hoh Rainforest, WA"],
    "San Francisco → Big Sur": ["San Francisco, CA", "Santa Cruz, CA", "Monterey, CA", "Big Sur, CA"],
    "Orlando → Blue Ridge Parkway": ["Orlando, FL", "Savannah, GA", "Asheville, NC", "Blue Ridge Parkway, NC"]
}

# Streamlit UI
st.set_page_config(page_title="ScenicSync", layout="centered")
st.title("🌄 ScenicSync (Google Maps Version)")
st.markdown("**Take the long way. On purpose.**")

selected_route = st.selectbox("Choose a Scenic Route", list(ROUTES.keys()))

if selected_route:
    places = ROUTES[selected_route]
    encoded_places = [quote(p) for p in places]
    maps_url = f"https://www.google.com/maps/embed/v1/directions?key={GMAPS_API_KEY}&origin={encoded_places[0]}&destination={encoded_places[-1]}&waypoints={'|'.join(encoded_places[1:-1])}"

    st.markdown("### 📍 Route Preview")
    st.components.v1.iframe(maps_url, height=600)

    gmaps_link = f"https://www.google.com/maps/dir/" + "/".join(encoded_places)
    st.markdown(f"👉 [Open Fullscreen in Google Maps]({gmaps_link})", unsafe_allow_html=True)
