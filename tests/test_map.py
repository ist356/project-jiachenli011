import pytest
import os
import pandas as pd
from code.Map import create_weather_geomap

def test_create_weather_geomap():
    
    test_data = pd.DataFrame({
        "city": ["Shanghai", "New York"],
        "latitude": [31.23, 40.71],
        "longitude": [121.47, -74.01],
        "temperature_c": [12, 8],
        "weather_description": ["Clear", "Rain"]
    })
    output_file = "test_weather_map.html"

    print("\nTESTING: create_weather_geomap() generates map file")
    create_weather_geomap(test_data, save_path=output_file)


    assert os.path.exists(output_file), "Map file was not created"


    os.remove(output_file)

if __name__ == "__main__":
    test_create_weather_geomap()