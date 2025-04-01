import streamlit as st
import requests
import json
from datetime import datetime

def local_css():
    st.markdown("""
        <style>
        /* Base styles */
        [data-testid="stAppViewContainer"] {
            background-color: #fafafa;
        }
        
        /* Navigation bar styling */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 2rem;
            background-color: white;
            border-bottom: 1px solid #eee;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        /* Brand/Logo styling */
        .nav-brand {
            display: flex;
            align-items: center;
            font-size: 1.35rem;
            font-weight: 600;
            text-decoration: none;
            letter-spacing: -0.5px;
        }
        .nav-brand .brand-air {
            color: #202124;
        }
        .nav-brand .brand-quality {
            color: #202124;
            font-weight: 400;
        }
        .nav-brand .brand-ai {
            color: #31d2f2;
            margin-left: 1px;
        }
        
        /* Navigation links container */
        .nav-links {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Individual nav links */
        .nav-link {
            color: #5f6368;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        .nav-link:hover {
            color: #202124;
            background-color: #f8f9fa;
        }
        .nav-link.active {
            color: #31d2f2;
            background-color: #e8f9fc;
        }
        
        /* Deploy button styling */
        .nav-link.deploy {
            color: white;
            background-color: #31d2f2;
            padding: 0.5rem 1rem;
            margin-left: 0.5rem;
            border-radius: 6px;
            font-weight: 500;
        }
        .nav-link.deploy:hover {
            background-color: #23c1e1;
            color: white;
        }
        
        /* Form container styling */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
            background: white;
            max-width: 400px !important;
            margin: 8rem auto 0;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Input field styling */
        div[data-testid="stTextInput"] {
            margin-bottom: 1rem;
        }
        div[data-testid="stTextInput"] input {
            background-color: white;
            border: 1px solid #dadce0;
            border-radius: 4px;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            color: #202124;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #1a73e8;
            box-shadow: 0 0 0 1px #1a73e8;
        }
        
        /* Button styling */
        div[data-testid="stButton"] button {
            background-color: #31d2f2;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.75rem 1rem;
            width: 100%;
            font-weight: 500;
            font-size: 0.95rem;
            margin-top: 1rem;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #23c1e1;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

def render_navbar():
    st.markdown("""
        <div class="navbar">
            <a href="#" class="nav-brand">
                <span class="brand-air">Air</span><span class="brand-quality">Quality</span><span class="brand-ai">.AI</span>
            </a>
            <div class="nav-links">
                <a href="#" class="nav-link active">Dashboard</a>
                <a href="#" class="nav-link">Map</a>
                <a href="#" class="nav-link">Alerts</a>
                <a href="#" class="nav-link">Analytics</a>
                <a href="#" class="nav-link">Profile</a>
                <a href="#" class="nav-link deploy">Deploy</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

def switch_page(page_name):
    st.query_params['page'] = page_name
    st.rerun()

def login_register_page():
    local_css()
    render_navbar()
    
    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_token' not in st.session_state:
        st.session_state.user_token = None
    if 'username' not in st.session_state:
        st.session_state.username = None

    # Create columns for centering
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.page == 'signup':
            render_signup_page()
        else:
            render_login_page()

def render_login_page():
    # Shield icon as SVG
    st.markdown("""
        <svg style="display: block; margin: 0 auto 1.5rem; width: 48px; height: 48px;" viewBox="0 0 24 24" fill="#31d2f2">
            <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.67-3.13 8.96-7 10.12-3.87-1.16-7-5.45-7-10.12V6.3l7-3.12z"/>
        </svg>
    """, unsafe_allow_html=True)
    
    # Title and subtitle
    st.markdown("<h1 style='text-align: center; color: #202124; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.5rem;'>Welcome Back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5f6368; font-size: 0.95rem; margin-bottom: 2rem;'>Sign in to your account</p>", unsafe_allow_html=True)
    
    # Login Form
    email = st.text_input("Email", placeholder="Enter your email", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
    
    # Sign In button
    if st.button("Sign In", use_container_width=True):
        try:
            response = requests.post(
                "http://localhost:5000/login",
                json={"email": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.logged_in = True
                st.session_state.user_token = data["token"]
                st.session_state.username = data["user"]["username"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(response.json().get("error", "Login failed"))
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend is running.")
    
    # Links
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div style='text-align: left;'><a href='#' style='color: #31d2f2; text-decoration: none; font-size: 0.875rem;'>Forgot password?</a></div>", unsafe_allow_html=True)
    with col2:
        if st.button("Create account", type="secondary"):
            switch_page('signup')

def render_signup_page():
    # Shield icon as SVG
    st.markdown("""
        <svg style="display: block; margin: 0 auto 1.5rem; width: 48px; height: 48px;" viewBox="0 0 24 24" fill="#31d2f2">
            <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.67-3.13 8.96-7 10.12-3.87-1.16-7-5.45-7-10.12V6.3l7-3.12z"/>
        </svg>
    """, unsafe_allow_html=True)
    
    # Title and subtitle
    st.markdown("<h1 style='text-align: center; color: #202124; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.5rem;'>Create Account</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5f6368; font-size: 0.95rem; margin-bottom: 2rem;'>Sign up for a new account</p>", unsafe_allow_html=True)
    
    # Registration Form
    username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
    email = st.text_input("Email", placeholder="Enter your email", key="reg_email")
    password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm_password")
    
    # Sign Up button
    if st.button("Create Account", use_container_width=True):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return
            
        try:
            response = requests.post(
                "http://localhost:5000/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                }
            )
            
            if response.status_code == 201:
                st.success("Registration successful! Please log in.")
                switch_page('login')
            else:
                st.error(response.json().get("error", "Registration failed"))
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend is running.")
    
    # Back to login link
    if st.button("Already have an account? Sign in", type="secondary"):
        switch_page('login')

def logout():
    st.session_state.logged_in = False
    st.session_state.user_token = None
    st.session_state.username = None
    st.rerun() 