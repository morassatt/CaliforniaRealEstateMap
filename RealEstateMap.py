import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from sklearn.datasets import fetch_california_housing

import folium
from folium import plugins

# Get California housing data
data = fetch_california_housing(as_frame=True).frame

# Create a map object
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=6)

# Get minimum and maximium price and size of houses
price_min, price_max = data['MedHouseVal'].min(), data['MedHouseVal'].max()
size_min, size_max = data['AveRooms'].min(), data['AveRooms'].max()

# Display the markers with color and popup functionality
for _, row in data.iterrows():
    normalized_price = (row['MedHouseVal'] - price_min) / (price_max - price_min)
    color = plt.cm.RdYlGn(1 - normalized_price)

    normalized_rooms = (row['AveRooms'] - size_min) / (size_max - size_min)


    popup_info = f"""Median House Value (Expressed in $100k): ${row['MedHouseVal']:.2f}<br>
    Average Rooms: {row['AveRooms']}<br>
    Population: {row['Population']}<br>
    Median Income (Expressed in $10k): ${row['MedInc']:.2f}"""

    folium.CircleMarker(
        location = [row['Latitude'], row['Longitude']],
        radius = 5 + 20 * normalized_rooms,
        color = mcolors.to_hex(color[:3]),
        fill = True,
        fill_color = mcolors.to_hex(color[:3]),
        fill_opacity = 0.7,
        popup = folium.Popup(popup_info, max_width=300)
    ).add_to(m)

# Add to the map
plugins.MiniMap().add_to(m)

m.save('RealEstate.html')
