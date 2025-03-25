import folium
import pandas as pd
from folium.plugins import HeatMap

df = pd.read_csv("processed_crime_data.csv")

city_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

heat_data = df[['Latitude', 'Longitude']].values.tolist()
HeatMap(heat_data).add_to(city_map)

city_map.save("crime_heatmap.html")
print("Heatmap Generated! Open crime_heatmap.html to view.")

