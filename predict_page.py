import streamlit as st
import numpy as np
import pickle
from auth_pages import render_navbar, local_css

def load_model():
    with open('./model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def render_predict_page():
    local_css()
    render_navbar()
    
    # Custom CSS for enhanced design with dark mode support
    st.markdown("""
        <style>
        /* Light mode styles */
        [data-theme="light"] .input-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        /* Dark mode styles */
        [data-theme="dark"] .input-container {
            background-color: #262730;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
            border: 1px solid #464854;
        }
        
        .input-label {
            font-weight: 500;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        
        [data-theme="light"] .input-label {
            color: #202124;
        }
        
        [data-theme="dark"] .input-label {
            color: #ffffff;
        }
        
        .input-help {
            font-size: 0.8rem;
            margin-top: 0.25rem;
        }
        
        [data-theme="light"] .input-help {
            color: #5f6368;
        }
        
        [data-theme="dark"] .input-help {
            color: #9ba1a6;
        }
        
        /* Input field styles */
        [data-theme="dark"] .stNumberInput input {
            color: white !important;
            background-color: #3b3b3b !important;
            border-color: #464854 !important;
        }
        
        [data-theme="dark"] .stNumberInput input::placeholder {
            color: #9ba1a6 !important;
        }
        
        /* Prediction card styles */
        [data-theme="light"] .prediction-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 1px solid #e0e0e0;
        }
        
        [data-theme="dark"] .prediction-card {
            background: linear-gradient(135deg, #262730 0%, #1e1e1e 100%);
            border: 1px solid #464854;
        }
        
        .prediction-card {
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-top: 2rem;
        }
        
        /* Info card styles */
        [data-theme="light"] .info-card {
            background-color: #f8f9fa;
        }
        
        [data-theme="dark"] .info-card {
            background-color: #1e1e1e;
            border: 1px solid #464854;
        }
        
        .info-card {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        /* Button styles */
        .calculate-button {
            background-color: #1a73e8;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .calculate-button:hover {
            background-color: #1557b0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Text colors for dark mode */
        [data-theme="dark"] h1, 
        [data-theme="dark"] h2, 
        [data-theme="dark"] h3 {
            color: #ffffff !important;
        }
        
        [data-theme="dark"] p {
            color: #9ba1a6 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header section with info card
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>AQI Prediction</h1>
            <div class='info-card'>
                <p style='font-size: 1.1rem; margin: 0;'>
                    Enter the pollutant levels below to predict the Air Quality Index (AQI).
                    Our machine learning model will analyze the data and provide you with an accurate prediction.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section
    with st.container():
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Pollutant Measurements</h3>", unsafe_allow_html=True)
        
        # Create two columns for input fields
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='input-label'>PM2.5 (μg/m³)</div>", unsafe_allow_html=True)
            PM2_5 = st.number_input(
                "PM2.5 input",
                min_value=0.0,
                max_value=950.0,
                step=0.01,
                format="%.2f",
                label_visibility="collapsed"
            )
            st.markdown("<div class='input-help'>Usually ranges from 0.1 to 120 μg/m³</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-label' style='margin-top: 1.5rem;'>NO2 (ppb)</div>", unsafe_allow_html=True)
            NO2 = st.number_input(
                "NO2 input",
                min_value=0.0,
                max_value=362.0,
                step=0.01,
                format="%.2f",
                label_visibility="collapsed"
            )
            st.markdown("<div class='input-help'>Usually ranges from 0.01 to 60 ppb</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-label' style='margin-top: 1.5rem;'>CO (ppm)</div>", unsafe_allow_html=True)
            CO = st.number_input(
                "CO input",
                min_value=0.0,
                max_value=1756.0,
                step=0.01,
                format="%.2f",
                label_visibility="collapsed"
            )
            st.markdown("<div class='input-help'>Usually ranges from 0 to 3 ppm</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='input-label'>SO2 (ppb)</div>", unsafe_allow_html=True)
            SO2 = st.number_input(
                "SO2 input",
                min_value=0.0,
                max_value=194.0,
                step=0.01,
                format="%.2f",
                label_visibility="collapsed"
            )
            st.markdown("<div class='input-help'>Usually ranges from 0.01 to 25 ppb</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-label' style='margin-top: 1.5rem;'>O3 (ppb)</div>", unsafe_allow_html=True)
            O3 = st.number_input(
                "O3 input",
                min_value=0.0,
                max_value=258.0,
                step=0.01,
                format="%.2f",
                label_visibility="collapsed"
            )
            st.markdown("<div class='input-help'>Usually ranges from 0.01 to 65 ppb</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Calculate button with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        calculate_clicked = st.button(
            "Calculate AQI",
            use_container_width=True,
            type="primary"
        )
    
    # Prediction section
    if calculate_clicked:
        try:
            # Load model and make prediction
            data = load_model()
            regressor = data["model"]
            X = np.array([[PM2_5, NO2, CO, SO2, O3]])
            X = X.astype(float)
            AQI = regressor.predict(X)
            aqi_value = round(AQI[0], 0)
            
            # Determine AQI category and color
            if aqi_value <= 50:
                category = "Good"
                color = "#00C853"
                description = "Air quality is satisfactory, and air pollution poses little or no risk."
                icon = "✅"
            elif aqi_value <= 100:
                category = "Moderate"
                color = "#FFD600"
                description = "Air quality is acceptable. However, there may be a risk for some people."
                icon = "⚠️"
            elif aqi_value <= 150:
                category = "Unhealthy for Sensitive Groups"
                color = "#FF9800"
                description = "Members of sensitive groups may experience health effects."
                icon = "⚡"
            elif aqi_value <= 200:
                category = "Unhealthy"
                color = "#F44336"
                description = "Everyone may begin to experience health effects."
                icon = "❗"
            elif aqi_value <= 300:
                category = "Very Unhealthy"
                color = "#8E24AA"
                description = "Health alert: everyone may experience more serious health effects."
                icon = "🚨"
            else:
                category = "Hazardous"
                color = "#B71C1C"
                description = "Health warning of emergency conditions. Everyone is likely to be affected."
                icon = "☠️"
            
            # Display result with enhanced design
            st.markdown(f"""
                <div class='prediction-card'>
                    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;'>
                        <h2 style='margin: 0;'>Prediction Result</h2>
                        <span style='font-size: 2rem;'>{icon}</span>
                    </div>
                    <div style='display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem;'>
                        <div style='font-size: 3.5rem; font-weight: bold; color: {color};'>{aqi_value}</div>
                        <div>
                            <div style='font-size: 1.2rem; color: #5f6368;'>AQI</div>
                            <div style='font-size: 1.5rem; color: {color}; font-weight: 500;'>{category}</div>
                        </div>
                    </div>
                    <div style='background-color: {color}15; padding: 1rem; border-radius: 8px; border-left: 4px solid {color};'>
                        <p style='margin: 0;'>{description}</p>
                    </div>
                    <div style='margin-top: 1.5rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;'>
                        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px;'>
                            <div style='color: #5f6368; font-size: 0.9rem;'>Primary Pollutant</div>
                            <div style='color: #202124; font-size: 1.2rem; font-weight: 500;'>PM2.5</div>
                        </div>
                        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px;'>
                            <div style='color: #5f6368; font-size: 0.9rem;'>Health Impact</div>
                            <div style='color: #202124; font-size: 1.2rem; font-weight: 500;'>{category}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 