import streamlit as st
import requests
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Streamlit App Title
st.title("🛡️ Crime Rate Prediction System")

# Input Fields for Prediction
lat = st.number_input("📍 Enter Latitude", format="%.6f")
lon = st.number_input("📍 Enter Longitude", format="%.6f")
hour = st.slider("⏰ Select Hour", 0, 23)
dayofweek = st.slider("📆 Select Day of the Week", 0, 6)
month = st.slider("📅 Select Month", 1, 12)

# Button to Predict Crime Risk
if st.button("🚨 Predict Crime Risk"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json={"Latitude": lat, "Longitude": lon, "Hour": hour, "DayOfWeek": dayofweek, "Month": month},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        risk = data.get("Crime Risk Score", "Unknown")
        st.success(f"🔴 Predicted Crime Risk Score: {risk}")

    except requests.exceptions.ConnectionError:
        st.error("🚨 Error: Could not connect to the Flask API. Make sure the server is running.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Request Error: {e}")

# 📌 Load Crime Data for Heatmap
@st.cache_data  # Cache the data for performance
def load_data():
    try:
        df = pd.read_csv("processed_crime_data.csv")
        df = df[['Latitude', 'Longitude']].dropna()  # Ensure clean data
        return df
    except Exception as e:
        st.error(f"⚠️ Error loading crime data: {e}")
        return None

df = load_data()

# 📌 Display Heatmap in Streamlit
if df is not None:
    st.subheader("📍 Crime Hotspot Map")

    # Center map on a predefined city (Change this as needed)
    city_lat, city_lon = 28.7041, 77.1025  # New Delhi, change as needed
    city_map = folium.Map(location=[city_lat, city_lon], zoom_start=12)

    # Add HeatMap layer
    heat_data = df.values.tolist()
    HeatMap(heat_data).add_to(city_map)

    # Display in Streamlit
    folium_static(city_map)

st.write("ℹ️ **Tip:** The red areas indicate high crime intensity. Stay aware & plan safe routes!")
