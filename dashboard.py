import streamlit as st
from auth_pages import render_navbar, local_css, logout

def render_dashboard():
    local_css()
    render_navbar()
    
    # Add logout button in the top right
    with st.container():
        col1, col2 = st.columns([11, 1])
        with col2:
            if st.button("Logout"):
                logout()
    
    # Dashboard content
    st.title("Air Quality Dashboard")
    
    # Create a 2x2 grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        # AQI Overview Card
        with st.container():
            st.subheader("Current AQI")
            st.metric(label="Air Quality Index", value="45", delta="-5")
            st.markdown("**Status:** Good")
    
        # Historical Data Card
        with st.container():
            st.subheader("Historical Data")
            # Placeholder for historical chart
            st.line_chart({"AQI": [50, 45, 48, 52, 43, 41, 45]})
    
    with col2:
        # Pollutant Breakdown Card
        with st.container():
            st.subheader("Pollutant Breakdown")
            pollutants = {
                "PM2.5": 12,
                "PM10": 25,
                "NO2": 15,
                "SO2": 8,
                "CO": 0.8
            }
            for pollutant, value in pollutants.items():
                st.metric(label=pollutant, value=value)
        
        # Weather Conditions Card
        with st.container():
            st.subheader("Weather Conditions")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Temperature", "24°C")
                st.metric("Wind Speed", "5 km/h")
            with col_b:
                st.metric("Humidity", "65%")
                st.metric("Pressure", "1013 hPa") 