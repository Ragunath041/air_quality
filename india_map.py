import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
from streamlit_lottie import st_lottie
import requests
import os
from datetime import datetime
import time
import random

# Load Lottie animation for map loading
def load_lottie_map():
    url = "https://assets9.lottiefiles.com/packages/lf20_pJVNw6.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Load map animation
def load_lottie_map_select():
    url = "https://assets1.lottiefiles.com/packages/lf20_48yo3jor.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Load data animation
def load_lottie_data():
    url = "https://assets5.lottiefiles.com/packages/lf20_bkmcTw.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Load AQI data
@st.cache_data
def load_aqi_data():
    df = pd.read_csv('Data/India_Map/india_aqi_monthly.csv')
    return df

# Load India GeoJSON
@st.cache_data
def load_india_geojson():
    try:
        # Try loading the simpler GeoJSON first
        with open('Data/India_Map/india_states_simple.geojson', 'r', encoding='utf-8') as f:
            geojson = json.load(f)
            return geojson
    except (FileNotFoundError, json.JSONDecodeError):
        try:
            # Fall back to the original GeoJSON if the simpler one fails
            with open('Data/India_Map/india_states.geojson', 'r', encoding='utf-8') as f:
                geojson = json.load(f)
                return geojson
        except (FileNotFoundError, json.JSONDecodeError):
            # Create a minimal GeoJSON if everything fails
            st.error("GeoJSON files not found or invalid. Using a minimal fallback.")
            return {"type": "FeatureCollection", "features": []}

# Get color based on AQI
def get_color_by_aqi(aqi):
    if aqi <= 50:
        return 'green'
    elif aqi <= 100:
        return 'lightgreen'
    elif aqi <= 200:
        return 'yellow'
    elif aqi <= 300:
        return 'orange'
    elif aqi <= 400:
        return 'red'
    else:
        return 'darkred'

# Get health risk category based on AQI
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

# Create India choropleth map
def create_india_map(df, selected_month="January"):
    """Create an interactive India map showing AQI by state"""
    # Filter data for selected month
    month_df = df[df['month'] == selected_month]
    
    # Load GeoJSON
    geojson = load_india_geojson()
    
    # Check if we have any features
    if not geojson.get("features"):
        st.error("No GeoJSON features found. Map cannot be displayed.")
        return None
    
    # Determine the featureidkey based on GeoJSON structure
    feature_properties = geojson["features"][0].get("properties", {})
    if "NAME_1" in feature_properties:
        featureidkey = "properties.NAME_1"
    elif "st_nm" in feature_properties:
        featureidkey = "properties.st_nm"
    elif "name" in feature_properties:
        featureidkey = "properties.name"
    else:
        # Try to find a property that looks like a name
        name_candidates = [prop for prop in feature_properties.keys() 
                          if "name" in prop.lower() or "nm" in prop.lower()]
        if name_candidates:
            featureidkey = f"properties.{name_candidates[0]}"
        else:
            st.error("Could not determine state name property in GeoJSON.")
            return None
    
    # Create map
    try:
        fig = px.choropleth_mapbox(
            month_df,
            geojson=geojson,
            locations='state',
            featureidkey=featureidkey,
            color='aqi',
            color_continuous_scale=[
                (0, 'green'), 
                (0.2, 'lightgreen'), 
                (0.4, 'yellow'), 
                (0.6, 'orange'), 
                (0.8, 'red'), 
                (1, 'darkred')
            ],
            range_color=(0, 500),
            mapbox_style="carto-positron",
            zoom=3.5,
            center={"lat": 20.5937, "lon": 78.9629},
            opacity=0.8,
            labels={'aqi':'Air Quality Index'},
            hover_data=['PM2.5', 'NO2', 'CO', 'SO2', 'O3', 'health_risk']
        )
        
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            height=550,
            autosize=True,
            title={
                'text': f"India Air Quality Index - {selected_month}",
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating map: {e}")
        
        # Fall back to a simple bar chart of states
        fig = px.bar(
            month_df.sort_values('aqi', ascending=False),
            x='state',
            y='aqi',
            color='aqi',
            color_continuous_scale=[
                (0, 'green'), 
                (0.2, 'lightgreen'), 
                (0.4, 'yellow'), 
                (0.6, 'orange'), 
                (0.8, 'red'), 
                (1, 'darkred')
            ],
            labels={'aqi':'Air Quality Index', 'state': 'State'},
            title=f"India Air Quality Index - {selected_month}"
        )
        
        return fig

# Create monthly AQI graph
def create_monthly_chart(df, selected_state):
    """Create an interactive chart showing monthly AQI for a selected state"""
    
    # Filter data for selected state
    state_df = df[df['state'] == selected_state].sort_values(by=['month'])
    
    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    # Convert month to category with the right order
    state_df['month'] = pd.Categorical(state_df['month'], categories=month_order, ordered=True)
    
    # Sort by month
    state_df = state_df.sort_values('month')
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add AQI bars
    fig.add_trace(
        go.Bar(
            x=state_df['month'],
            y=state_df['aqi'],
            name="AQI",
            marker_color=state_df['aqi'].apply(get_color_by_aqi),
            opacity=0.8
        ),
        secondary_y=False,
    )
    
    # Add PM2.5 line
    fig.add_trace(
        go.Scatter(
            x=state_df['month'],
            y=state_df['PM2.5'],
            name="PM2.5",
            mode='lines+markers',
            line=dict(width=3, color='red'),
            marker=dict(size=8)
        ),
        secondary_y=True,
    )
    
    # Add animation effects
    fig.update_layout(
        title={
            'text': f"Monthly Air Quality Index for {selected_state}",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Month",
        yaxis_title="AQI",
        yaxis2_title="PM2.5",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        autosize=True,
    )
    
    return fig

# Create pollutants comparison chart
def create_pollutants_chart(df, selected_state):
    """Create a radar chart comparing pollutants for a selected state"""
    
    # Filter data for selected state
    state_df = df[df['state'] == selected_state].copy()
    
    # Calculate average of each pollutant
    avg_data = state_df[['PM2.5', 'NO2', 'CO', 'SO2', 'O3']].mean().reset_index()
    avg_data.columns = ['Pollutant', 'Value']
    
    # Normalize values for radar chart
    max_values = {'PM2.5': 300, 'NO2': 100, 'CO': 20, 'SO2': 80, 'O3': 200}
    avg_data['Normalized'] = avg_data.apply(lambda x: (x['Value'] / max_values[x['Pollutant']]) * 100, axis=1)
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=avg_data['Normalized'],
        theta=avg_data['Pollutant'],
        fill='toself',
        name=selected_state,
        line_color='rgba(72, 99, 255, 0.8)',
        fillcolor='rgba(72, 99, 255, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title={
            'text': f"Pollutant Profile for {selected_state}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=450,
        autosize=True,
        showlegend=False
    )
    
    return fig

# Create health risk pie chart
def create_health_risk_chart(df, selected_state):
    """Create a pie chart showing the distribution of health risk categories by month"""
    
    # Filter data for selected state
    state_df = df[df['state'] == selected_state].copy()
    
    # Count occurrences of each health risk category
    risk_counts = state_df['health_risk'].value_counts().reset_index()
    risk_counts.columns = ['health_risk', 'count']
    
    # Colors for health risk categories
    colors = {
        'Good': 'green',
        'Satisfactory': 'lightgreen',
        'Moderate': 'yellow',
        'Poor': 'orange',
        'Very Poor': 'red',
        'Severe': 'darkred'
    }
    
    # Create color list based on categories in the data
    color_list = [colors[risk] for risk in risk_counts['health_risk']]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts['health_risk'],
        values=risk_counts['count'],
        hole=.4,
        marker_colors=color_list
    )])
    
    fig.update_layout(
        title={
            'text': f"Health Risk Distribution for {selected_state}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=450,
        autosize=True
    )
    
    # Add animation
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

# Show India map page
def show_india_map_page():
    """Display the India Map page with interactive visualizations"""
    st.title("India Air Quality Map")
    
    # Display Lottie animation
    lottie_map = load_lottie_map()
    if lottie_map:
        st_lottie(lottie_map, speed=1, height=300, key="map_animation")
    
    # Load data
    df = load_aqi_data()
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["India Map", "State-wise Analysis"])
    
    with tab1:
        # Add month selection for map
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected_month = st.selectbox("Select Month:", months)
            
            st.write("### AQI Legend")
            st.markdown("""
            - 0-50: **Good** (Green)
            - 51-100: **Satisfactory** (Light Green)
            - 101-200: **Moderate** (Yellow)
            - 201-300: **Poor** (Orange)
            - 301-400: **Very Poor** (Red)
            - 401+: **Severe** (Dark Red)
            """)
            
            # Add a small animation
            lottie_data = load_lottie_data()
            if lottie_data:
                st_lottie(lottie_data, speed=1, height=150, key="data_animation")
            
        with col2:
            # Create and display map
            fig = create_india_map(df, selected_month)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Show a fallback table if the map can't be created
                st.write("### AQI by State")
                month_data = df[df['month'] == selected_month].sort_values('aqi', ascending=False)
                styled_df = month_data[['state', 'region', 'aqi', 'health_risk']].reset_index(drop=True)
                
                # Apply color styling to the health_risk column
                def color_health_risk(val):
                    color_map = {
                        'Good': 'green',
                        'Satisfactory': 'lightgreen',
                        'Moderate': 'yellow',
                        'Poor': 'orange',
                        'Very Poor': 'red',
                        'Severe': 'darkred'
                    }
                    color = color_map.get(val, 'white')
                    return f'background-color: {color}; color: {"black" if color in ["yellow", "lightgreen"] else "white"}'
                
                st.dataframe(styled_df.style.applymap(color_health_risk, subset=['health_risk']), height=500)
    
    with tab2:
        # Add state selection
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Get unique states
            states = sorted(df['state'].unique())
            selected_state = st.selectbox("Select State:", states)
            
            # Add a small animation
            lottie_select = load_lottie_map_select()
            if lottie_select:
                st_lottie(lottie_select, speed=1, height=150, key="select_animation")
                
            # Show state region and average AQI
            state_info = df[df['state'] == selected_state].iloc[0]
            region = state_info['region']
            avg_aqi = round(df[df['state'] == selected_state]['aqi'].mean(), 1)
            
            st.write(f"### Region: {region}")
            st.write(f"### Average AQI: {avg_aqi}")
            
            # Show health risk category
            health_risk = get_health_risk(avg_aqi)
            color = get_color_by_aqi(avg_aqi)
            st.markdown(f"### Health Risk: <span style='color:{color}'>{health_risk}</span>", unsafe_allow_html=True)
            
        with col2:
            # Create tabs for different visualizations
            subtab1, subtab2, subtab3 = st.tabs(["Monthly Trend", "Pollutant Profile", "Health Risk"])
            
            with subtab1:
                # Show monthly trend chart
                fig1 = create_monthly_chart(df, selected_state)
                st.plotly_chart(fig1, use_container_width=True)
                
            with subtab2:
                # Show pollutants comparison chart
                fig2 = create_pollutants_chart(df, selected_state)
                st.plotly_chart(fig2, use_container_width=True)
                
            with subtab3:
                # Show health risk distribution chart
                fig3 = create_health_risk_chart(df, selected_state)
                st.plotly_chart(fig3, use_container_width=True) 