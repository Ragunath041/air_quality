import os
import json
import numpy as np
import pandas as pd
import requests
from datetime import datetime
import random

# Create directory if not exists
os.makedirs('Data/India_Map', exist_ok=True)

# Download India States GeoJSON data from GitHub
def download_india_geojson():
    """Download India states GeoJSON data"""
    url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
    response = requests.get(url)
    if response.status_code == 200:
        with open('Data/India_Map/india_states.geojson', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("GeoJSON data downloaded successfully!")
        return True
    else:
        print(f"Failed to download GeoJSON data. Status code: {response.status_code}")
        return False

# Create synthetic monthly AQI data for each Indian state
def create_synthetic_aqi_data():
    """Create synthetic AQI data for Indian states by month"""
    # List of Indian states with their region classification
    states = [
        # North India
        {"state": "Jammu and Kashmir", "region": "North", "base_aqi": 110},
        {"state": "Himachal Pradesh", "region": "North", "base_aqi": 85},
        {"state": "Punjab", "region": "North", "base_aqi": 160},
        {"state": "Uttarakhand", "region": "North", "base_aqi": 95},
        {"state": "Haryana", "region": "North", "base_aqi": 170},
        {"state": "Delhi", "region": "North", "base_aqi": 220},
        {"state": "Rajasthan", "region": "North", "base_aqi": 140},
        {"state": "Uttar Pradesh", "region": "North", "base_aqi": 190},
        
        # East India
        {"state": "Bihar", "region": "East", "base_aqi": 150},
        {"state": "West Bengal", "region": "East", "base_aqi": 160},
        {"state": "Jharkhand", "region": "East", "base_aqi": 130},
        {"state": "Odisha", "region": "East", "base_aqi": 120},
        
        # Northeast India
        {"state": "Sikkim", "region": "Northeast", "base_aqi": 70},
        {"state": "Assam", "region": "Northeast", "base_aqi": 100},
        {"state": "Arunachal Pradesh", "region": "Northeast", "base_aqi": 60},
        {"state": "Nagaland", "region": "Northeast", "base_aqi": 75},
        {"state": "Manipur", "region": "Northeast", "base_aqi": 80},
        {"state": "Mizoram", "region": "Northeast", "base_aqi": 65},
        {"state": "Tripura", "region": "Northeast", "base_aqi": 90},
        {"state": "Meghalaya", "region": "Northeast", "base_aqi": 75},
        
        # West India
        {"state": "Gujarat", "region": "West", "base_aqi": 140},
        {"state": "Maharashtra", "region": "West", "base_aqi": 150},
        {"state": "Goa", "region": "West", "base_aqi": 80},
        
        # Central India
        {"state": "Madhya Pradesh", "region": "Central", "base_aqi": 130},
        {"state": "Chhattisgarh", "region": "Central", "base_aqi": 120},
        
        # South India
        {"state": "Andhra Pradesh", "region": "South", "base_aqi": 100},
        {"state": "Karnataka", "region": "South", "base_aqi": 110},
        {"state": "Tamil Nadu", "region": "South", "base_aqi": 120},
        {"state": "Kerala", "region": "South", "base_aqi": 70},
        {"state": "Telangana", "region": "South", "base_aqi": 130}
    ]
    
    # Create monthly variations (higher in winter, lower in monsoon)
    months = [
        {"month": "January", "multiplier": 1.4},
        {"month": "February", "multiplier": 1.2},
        {"month": "March", "multiplier": 1.0},
        {"month": "April", "multiplier": 0.9},
        {"month": "May", "multiplier": 0.8},
        {"month": "June", "multiplier": 0.7},
        {"month": "July", "multiplier": 0.6},
        {"month": "August", "multiplier": 0.6},
        {"month": "September", "multiplier": 0.7},
        {"month": "October", "multiplier": 0.9},
        {"month": "November", "multiplier": 1.2},
        {"month": "December", "multiplier": 1.5}
    ]
    
    # Generate data
    data = []
    
    for state in states:
        for month in months:
            # Add randomness to make data more realistic
            random_factor = random.uniform(0.8, 1.2)
            aqi = int(state["base_aqi"] * month["multiplier"] * random_factor)
            
            # Generate pollutant data based on AQI
            pm25 = max(10, min(300, aqi * random.uniform(0.3, 0.5)))
            no2 = max(5, min(100, aqi * random.uniform(0.1, 0.2)))
            co = max(0.5, min(20, aqi * random.uniform(0.02, 0.04)))
            so2 = max(2, min(80, aqi * random.uniform(0.05, 0.15)))
            o3 = max(10, min(200, aqi * random.uniform(0.2, 0.3)))
            
            row = {
                "state": state["state"],
                "region": state["region"],
                "month": month["month"],
                "aqi": aqi,
                "PM2.5": round(pm25, 2),
                "NO2": round(no2, 2),
                "CO": round(co, 2),
                "SO2": round(so2, 2),
                "O3": round(o3, 2),
                "health_risk": get_health_risk(aqi)
            }
            data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv('Data/India_Map/india_aqi_monthly.csv', index=False)
    print("Synthetic AQI data created successfully!")
    return df

def get_health_risk(aqi):
    """Get health risk category based on AQI"""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

if __name__ == "__main__":
    # Download GeoJSON data
    download_india_geojson()
    
    # Create synthetic AQI data
    create_synthetic_aqi_data() 