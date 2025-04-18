import folium
import pandas as pd
import json
from folium.plugins import HeatMap

# Load dataset
data_file = r"C:\Users\Asus\Documents\Nepal Custom Map\Custom data.csv"
df = pd.read_csv(data_file)

# Load GeoJSON data for Nepal's administrative boundaries
geojson_path = r'C:\Users\Asus\Documents\Nepal Custom Map\geoBoundaries-NPL-ADM0_simplified.geojson'
with open(geojson_path, 'r') as file:
    nepal_geojson = json.load(file)

# Create a base map centered around Nepal
m = folium.Map(location=[28.3949, 84.1240], zoom_start=7)

# Function to determine marker size based on trade value
# def marker_size(value):
#     return max(value / 10000000, 5)  # Ensuring a minimum marker size

# Feature groups for imports and exports
imports_layer = folium.FeatureGroup(name="Imports (Red)", show=True)
exports_layer = folium.FeatureGroup(name="Exports (Green)", show=True)

# Collect data for the heatmap
heat_data = []

# Add customs locations to the map
for _, row in df.iterrows():
    import_value = row['Imports_Value']
    export_value = row['Exports_Value']

    # Heatmap intensity based on total trade value
    total_trade = import_value + export_value
    heat_data.append([row['Latitude'], row['Longitude'], 1])

    # Import marker (Red)
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=folium.Popup(
            f"Customs: {row['Customs']}<br>"
            f"<b>Imports:</b> NPR {import_value:,}<br>"
            f"<b>Exports:</b> NPR {export_value:,}",
            max_width=250
        )
    ).add_to(imports_layer)

    # Export marker (Green)
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.6,
        popup=folium.Popup(
            f"Customs: {row['Customs']}<br>"
            f"<b>Imports:</b> NPR {import_value:,}<br>"
            f"<b>Exports:</b> NPR {export_value:,}",
            max_width=250
        )
    ).add_to(exports_layer)

# Overlay the administrative boundaries
folium.GeoJson(
    nepal_geojson,
    name='Nepal Administrative Boundaries'
).add_to(m)
blue_gradient = {
    '0.2': 'blue',
    '0.4': 'blue',
    '0.6': 'blue',
    '0.8': 'blue',
    '1.0': 'blue'
}
# Modify heat_data to set uniform intensity (value=1 for all points)
uniform_heat_data = [[lat, lon,0.1] for lat, lon, _ in heat_data]

# Add heatmap layer for trade intensity
heatmap_layer = HeatMap(uniform_heat_data, name="Trade Intensity Heatmap", min_opacity=0.4, max_zoom=10, radius=15, blur=10, gradient= blue_gradient)
m.add_child(heatmap_layer)

# Add feature groups to the map
m.add_child(imports_layer)
m.add_child(exports_layer)

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)


# Save the map to an HTML file
m.save('nepal_customs_trade_map.html')
