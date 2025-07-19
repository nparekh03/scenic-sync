# 🌄 ScenicSync - Take the long way. On purpose.

A complete scenic route planning application powered by Google Maps APIs. Discover meaningful detours, small-town stops, and beautiful roads across America.

![ScenicSync Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=ScenicSync+Demo)

## ✨ Features

- 🗺️ **Google Maps Integration** - Accurate geocoding, directions, and route optimization
- 📍 **Smart Point Discovery** - Google Places API finds attractions, restaurants, and scenic spots
- 🛣️ **Scenic Route Optimization** - Avoid highways and take the beautiful backroads
- 📱 **Seamless Navigation** - Export directly to Google Maps mobile app
- 🎯 **Preference-Based Planning** - Customize routes based on your interests
- ⭐ **Curated Scenic Routes** - Pre-built routes for famous scenic drives

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd scenicsync
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env file with your API key
# GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

### 5. Run the Application
```bash
streamlit run scenicsync.py
```

The app will open in your browser at `http://localhost:8501`

## 🔑 Google Maps API Setup

### Step 1: Get API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - **Geocoding API** - Convert addresses to coordinates
   - **Directions API** - Calculate routes between locations
   - **Places API** - Find points of interest
4. Create credentials (API Key)

### Step 2: Configure API Key
Add your API key to the `.env` file:
```
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

### Step 3: Set API Restrictions (Recommended)
For security, restrict your API key:
- **Application restrictions**: HTTP referrers (web sites)
- **API restrictions**: Only enable the 3 APIs mentioned above

## 💰 Google Maps API Pricing

| API | Free Tier | Price after free tier |
|-----|-----------|----------------------|
| Geocoding | 40,000 requests/month | $5 per 1,000 requests |
| Directions | 40,000 requests/month | $5 per 1,000 requests |
| Places | 2,500 requests/month | $17 per 1,000 requests |

For typical personal usage, you'll likely stay within free tiers!

## 📁 Project Structure

```
scenicsync/
├── scenicsync.py          # Main application file
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── .env.example          # Example environment file
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── assets/              # Static assets (optional)
    └── screenshots/
```

## 🎮 Usage

### Custom Routes
1. Enter start and end locations
2. Choose scenic preferences (coastal, mountains, etc.)
3. Configure route options (avoid highways, find attractions)
4. Generate your scenic route!

### Predefined Routes
- **New England Coastal** - Lighthouses and lobster shacks
- **Pacific Coast Highway** - Dramatic coastlines and redwoods
- **Blue Ridge Parkway** - Misty mountains and waterfalls
- **Rocky Mountain High** - Alpine lakes and peaks

## 🔧 Troubleshooting

### Common Issues

**"Could not find location"**
- Try full city names with state: "Boston, MA"
- Use major cities for better results
- Check spelling

**"API key error"**
- Verify API key in `.env` file
- Ensure required APIs are enabled in Google Cloud Console
- Check API key restrictions

**Import errors**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

### Fallback Mode
The app works with limited functionality even without API keys:
- Built-in database of 50+ major US cities
- OpenStreetMap fallback geocoding
- Basic route visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Maps APIs for location services
- Streamlit for the amazing web framework
- Folium for interactive maps
- OpenStreetMap for fallback mapping

## 📞 Support

Having issues? Please check:
1. This README file
2. [Google Maps API Documentation](https://developers.google.com/maps/documentation)
3. [Streamlit Documentation](https://docs.streamlit.io/)
4. Open an issue on GitHub

---

**Made with ❤️ for road trip enthusiasts**