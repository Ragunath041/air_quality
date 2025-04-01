import streamlit as st
# Must be the first Streamlit command
st.set_page_config(
    page_title="AirQuality.AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px
import base64
import pickle
from india_map import show_india_map_page
from auth_pages import login_register_page, logout

# Load model
def load_model():
    with open('./model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# Load animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Predict page
def show_predict_page():
    st.title("AQI prediction")
    st.write("""Input info. to predict AQI""")
    PM2_5 = st.number_input("PM2.5 (Usually ranges from 0.1 to 120)", min_value=0.0, max_value=950.0, step=0.01, format="%.2f")
    NO2 = st.number_input("NO2 (Usually ranges from 0.01 to 60)", min_value=0.0, max_value=362.0, step=0.01, format="%.2f")
    CO = st.number_input("CO (Usually ranges from 0 to 3)", min_value=0.0, max_value=1756.0, step=0.01, format="%.2f")
    SO2 = st.number_input("SO2 (Usually ranges from 0.01 to 25)", min_value=0.0, max_value=194.0, step=0.01, format="%.2f")
    O3 = st.number_input("O3 (Usually ranges from 0.01 to 65)", min_value=0.0, max_value=258.0, step=0.01, format="%.2f")

    ok = st.button("Calculate AQI")
    if ok:
        # Load model
        data = load_model()
        regressor = data["model"]
        
        X = np.array([[PM2_5, NO2, CO, SO2, O3]])
        X = X.astype(float)
        AQI = regressor.predict(X)

        if round(AQI[0], 0) >= 0 and round(AQI[0], 0) <= 55:
            st.subheader(f"The estimated AQI is Good")
        elif round(AQI[0], 0) >= 56 and round(AQI[0], 0) <= 100:
            st.subheader(f"The estimated AQI is Satisfactory")
        elif round(AQI[0], 0) >= 101 and round(AQI[0], 0) <= 200:
            st.subheader(f"The estimated AQI is Moderate")
        elif round(AQI[0], 0) >= 201 and round(AQI[0], 0) <= 300:
            st.subheader(f"The estimated AQI is Poor")
        else:
            st.subheader(f"The estimated AQI is Severe")

# Explore page
def show_explore_page():
    # title
    st.title("Data Exploration")
    st.sidebar.subheader("Visualization Settings")

    def load_data():
        df = pd.read_csv("./final_data.csv")
        return df

    df = load_data()

    def get_table_download_link_csv(df):
        csv = df.to_csv().encode()
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="sample.csv" target="_blank">Download dataset</a>'
        return href

    st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)

    st.write(df)

    st.write('(Rows,Columns) =', df.shape)

    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)

    # adding select widget to sidebar - chart select
    chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=["Scatterplot", "Boxplot", "Histograms",
                 "Density Contour", "Density Heatmap"])
    if chart_select == "Scatterplot":
        st.sidebar.subheader("Scatterplot options")
        try:
            x_values = st.sidebar.selectbox("X axis", options=numeric_columns)
            y_values = st.sidebar.selectbox("Y axis", options=numeric_columns)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values)
            # displaying the chart
            st.plotly_chart(plot)
        except Exception as e:
            st.error(f"Error: {e}")

    if chart_select == "Boxplot":
        st.sidebar.subheader("Boxplot options")
        try:
            x_values = st.sidebar.selectbox("Feature", options=numeric_columns)
            bxplot = px.box(df[x_values])
            # displaying the chart
            st.plotly_chart(bxplot)
        except Exception as e:
            st.error(f"Error: {e}")

    if chart_select == "Histograms":
        st.sidebar.subheader("Histogram options")
        try:
            x_values = st.sidebar.selectbox("Feature", options=numeric_columns)
            bins = st.sidebar.slider("No. of bins", 0, 100, 50)
            histplot = px.histogram(df[x_values], nbins=bins)
            # displaying the chart
            st.plotly_chart(histplot)
        except Exception as e:
            st.error(f"Error: {e}")

    if chart_select == "Density Contour":
        st.sidebar.subheader("Density Contour options")
        try:
            x_values = st.sidebar.selectbox("X axis", options=numeric_columns)
            y_values = st.sidebar.selectbox("Y axis", options=numeric_columns)
            dencplot = px.density_contour(data_frame=df,
                                          x=x_values, y=y_values)
            # displaying the chart
            st.plotly_chart(dencplot)
        except Exception as e:
            st.error(f"Error: {e}")

    if chart_select == "Density Heatmap":
        st.sidebar.subheader("Density Heatmap options")
        try:
            x_values = st.sidebar.selectbox("X axis", options=numeric_columns)
            y_values = st.sidebar.selectbox("Y axis", options=numeric_columns)
            denhplot = px.density_heatmap(data_frame=df, x=x_values, y=y_values,
                                          marginal_x="box", marginal_y="violin")
            # displaying the chart
            st.plotly_chart(denhplot)
        except Exception as e:
            st.error(f"Error: {e}")

# Main app
def load_lottie_india_map():
    url = "https://assets3.lottiefiles.com/packages/lf20_WsHecI.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Add India Map animation to the sidebar
india_map_animation = load_lottie_india_map()

def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    # Handle page routing
    params = st.query_params
    if 'page' in params:
        st.session_state.page = params['page']

    if not st.session_state.logged_in:
        login_register_page()
    else:
        # Show main application
        with st.sidebar:
            st.write(f"Welcome, {st.session_state.username}!")
            if st.button("Logout"):
                logout()

        # Main navigation
        page = st.sidebar.selectbox("Navigation", ("Predict", "Explore", "India Map"))
        
        if page == "Predict":
            show_predict_page()
        elif page == "Explore":
            show_explore_page()
        else:  # India Map page
            show_india_map_page()

if __name__ == "__main__":
    main() 