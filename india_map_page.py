import streamlit as st
import requests
from streamlit_lottie import st_lottie
from auth_pages import render_navbar, local_css

def load_lottie_india_map():
    url = "https://assets3.lottiefiles.com/packages/lf20_WsHecI.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def render_india_map_page():
    local_css()
    render_navbar()
    
    # Main content
    st.title("India Air Quality Map")
    st.markdown("<p style='color: #5f6368; font-size: 1.1rem; margin-bottom: 2rem;'>Visualize air quality across different regions of India</p>", unsafe_allow_html=True)
    
    # Load and display Lottie animation
    india_map_animation = load_lottie_india_map()
    if india_map_animation:
        st_lottie(india_map_animation, height=300)
    
    # Map controls
    with st.container():
        st.markdown("""
            <div style='background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;'>
                <h3 style='color: #202124; margin-bottom: 1rem;'>Map Controls</h3>
                <div style='display: flex; gap: 1rem; flex-wrap: wrap;'>
                    <div style='flex: 1; min-width: 200px;'>
                        <label style='color: #5f6368; font-size: 0.9rem;'>Select Region</label>
                        <select style='width: 100%; padding: 0.5rem; border: 1px solid #dadce0; border-radius: 4px;'>
                            <option>All Regions</option>
                            <option>North India</option>
                            <option>South India</option>
                            <option>East India</option>
                            <option>West India</option>
                            <option>Central India</option>
                        </select>
                    </div>
                    <div style='flex: 1; min-width: 200px;'>
                        <label style='color: #5f6368; font-size: 0.9rem;'>Time Period</label>
                        <select style='width: 100%; padding: 0.5rem; border: 1px solid #dadce0; border-radius: 4px;'>
                            <option>Last 24 Hours</option>
                            <option>Last 7 Days</option>
                            <option>Last 30 Days</option>
                            <option>Last Year</option>
                        </select>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Map visualization
    with st.container():
        st.markdown("""
            <div style='background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #202124; margin-bottom: 1rem;'>Air Quality Map</h3>
                <div style='height: 500px; background-color: #f8f9fa; border-radius: 4px; display: flex; align-items: center; justify-content: center;'>
                    <div style='color: #5f6368;'>Map visualization will be implemented here</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Region statistics
    with st.container():
        st.markdown("""
            <div style='background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 2rem;'>
                <h3 style='color: #202124; margin-bottom: 1rem;'>Region Statistics</h3>
                <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;'>
                    <div style='text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 4px;'>
                        <div style='color: #5f6368; font-size: 0.9rem;'>Average AQI</div>
                        <div style='color: #202124; font-size: 1.5rem; font-weight: 500;'>156</div>
                    </div>
                    <div style='text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 4px;'>
                        <div style='color: #5f6368; font-size: 0.9rem;'>Most Polluted City</div>
                        <div style='color: #202124; font-size: 1.5rem; font-weight: 500;'>Delhi</div>
                    </div>
                    <div style='text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 4px;'>
                        <div style='color: #5f6368; font-size: 0.9rem;'>Cleanest City</div>
                        <div style='color: #202124; font-size: 1.5rem; font-weight: 500;'>Bangalore</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True) 