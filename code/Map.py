import folium
from folium.plugins import MarkerCluster
import pandas as pd

def create_weather_geomap(weather_df: pd.DataFrame, save_path="weather_map.html"):
    """
    Create interactive maps based on weather data
    weather_df: DataFrame containing city weather data
    save_path: map save path    
    """
    column_mapping = {
        "lat": "latitude",
        "lon": "longitude",
        "name": "city",
        "temperature": "temperature_c",
        "weather_descriptions": "weather_description"
    }
    weather_df.rename(columns=column_mapping, inplace=True)

    # Convert columns to numeric types
    weather_df["latitude"] = pd.to_numeric(weather_df["latitude"], errors="coerce")
    weather_df["longitude"] = pd.to_numeric(weather_df["longitude"], errors="coerce")

    # Check required columns
    required_columns = {"latitude", "longitude", "city"}
    if not required_columns.issubset(set(weather_df.columns)):
        raise ValueError(f"Missing column: {required_columns - set(weather_df.columns)}")

    center_lat = weather_df["latitude"].mean()
    center_lon = weather_df["longitude"].mean()
    weather_map = folium.Map(location=[center_lat, center_lon], zoom_start=3)

    # Use MarkerCluster to aggregate points
    marker_cluster = MarkerCluster().add_to(weather_map)

    # Traverse the data and add markers
    for _, row in weather_df.iterrows():
        popup_info = (
            f"<b>City:</b> {row['city']}<br>"
            f"<b>Temperature:</b> {row.get('temperature_c', 'N/A')}°C<br>"
            f"<b>Weather:</b> {row.get('weather_description', 'N/A')}<br>"
        )
        icon_color = "red" if row.get("temperature_c", 0) > 30 else "blue"  
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_info,
            icon=folium.Icon(color=icon_color, icon="cloud")
        ).add_to(marker_cluster)

    weather_map.save(save_path)