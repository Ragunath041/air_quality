import streamlit as st
from auth_pages import login_register_page, logout
from dashboard import render_dashboard
from predict_page import render_predict_page
from explore_page import render_explore_page
from india_map_page import render_india_map_page

# Set page config
st.set_page_config(
    page_title="AirQuality.AI",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Get the current page from query parameters
query_params = st.query_params
current_page = query_params.get("page", "login")

# Main routing logic
if not st.session_state.logged_in:
    if current_page in ['login', 'signup']:
        st.session_state.page = current_page
        login_register_page()
    else:
        st.session_state.page = 'login'
        st.query_params['page'] = 'login'
        st.rerun()
else:
    if current_page in ['login', 'signup']:
        st.query_params['page'] = 'dashboard'
        st.rerun()
    else:
        # Show main application
        with st.sidebar:
            st.write(f"Welcome, {st.session_state.username}!")
            if st.button("Logout"):
                logout()
            
            # Navigation
            st.markdown("### Navigation")
            nav_page = st.radio(
                "Select a page",
                ["Dashboard", "Predict", "Explore", "India Map"],
                label_visibility="collapsed"
            )
            
            # Update page based on navigation
            if nav_page == "Dashboard":
                st.query_params['page'] = 'dashboard'
                st.rerun()
            elif nav_page == "Predict":
                st.query_params['page'] = 'predict'
                st.rerun()
            elif nav_page == "Explore":
                st.query_params['page'] = 'explore'
                st.rerun()
            else:  # India Map
                st.query_params['page'] = 'india_map'
                st.rerun()
        
        # Render the appropriate page
        if current_page == 'dashboard':
            render_dashboard()
        elif current_page == 'predict':
            render_predict_page()
        elif current_page == 'explore':
            render_explore_page()
        elif current_page == 'india_map':
            render_india_map_page()
        else:
            st.query_params['page'] = 'dashboard'
            st.rerun() 