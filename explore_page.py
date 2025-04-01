import streamlit as st
import streamlit.components as stc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
import matplotlib
import plotly_express as px
import base64
from auth_pages import render_navbar, local_css


def get_table_download_link_csv(df):
    csv = df.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="air_quality_data.csv" target="_blank">Download dataset</a>'
    return href

def render_explore_page():
    local_css()
    render_navbar()
    
    # Main content
    st.title("Data Exploration")
    st.markdown("<p style='color: #5f6368; font-size: 1.1rem; margin-bottom: 2rem;'>Explore and visualize air quality data</p>", unsafe_allow_html=True)
    
    # Load data
    try:
        df = pd.read_csv("./final_data.csv")
        
        # Data overview card
        with st.container():
            st.markdown("""
                <div style='background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;'>
                    <h3 style='color: #202124; margin-bottom: 1rem;'>Dataset Overview</h3>
                    <div style='display: flex; gap: 2rem;'>
                        <div>
                            <div style='color: #5f6368; font-size: 0.9rem;'>Total Records</div>
                            <div style='color: #202124; font-size: 1.5rem; font-weight: 500;'>{}</div>
                        </div>
                        <div>
                            <div style='color: #5f6368; font-size: 0.9rem;'>Features</div>
                            <div style='color: #202124; font-size: 1.5rem; font-weight: 500;'>{}</div>
                        </div>
                    </div>
                </div>
            """.format(df.shape[0], df.shape[1]), unsafe_allow_html=True)
        
        # Download button
        st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)
        
        # Visualization section
        st.subheader("Data Visualization")
        
        # Get numeric columns
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        
        # Create two columns for visualization controls
        col1, col2 = st.columns(2)
        
        with col1:
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Scatterplot", "Boxplot", "Histogram", "Density Contour", "Density Heatmap"]
            )
        
        with col2:
            if chart_type in ["Scatterplot", "Density Contour", "Density Heatmap"]:
                x_axis = st.selectbox("Select X-axis", numeric_columns)
                y_axis = st.selectbox("Select Y-axis", numeric_columns)
            else:
                feature = st.selectbox("Select Feature", numeric_columns)
        
        # Create visualization
        try:
            if chart_type == "Scatterplot":
                fig = px.scatter(data_frame=df, x=x_axis, y=y_axis)
            elif chart_type == "Boxplot":
                fig = px.box(df[feature])
            elif chart_type == "Histogram":
                fig = px.histogram(df[feature])
            elif chart_type == "Density Contour":
                fig = px.density_contour(data_frame=df, x=x_axis, y=y_axis)
            else:  # Density Heatmap
                fig = px.density_heatmap(data_frame=df, x=x_axis, y=y_axis,
                                      marginal_x="box", marginal_y="violin")
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
        
        # Data table
        st.subheader("Raw Data")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
