import os
import json
import requests

# Create directory if not exists
os.makedirs('Data/India_Map', exist_ok=True)

# Download simpler India GeoJSON
def download_simple_india_geojson():
    """Download a simpler India GeoJSON file"""
    url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
    response = requests.get(url)
    if response.status_code == 200:
        with open('Data/India_Map/india_states_simple.geojson', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Simple GeoJSON data downloaded successfully!")
        return True
    else:
        print(f"Failed to download GeoJSON data. Status code: {response.status_code}")
        return False

if __name__ == "__main__":
    # Download simple GeoJSON
    download_simple_india_geojson() 