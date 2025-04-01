import streamlit as st
import requests
from auth_pages import set_page_config, local_css, render_navbar

def register_page():
    set_page_config()
    local_css()
    render_navbar()
    
    # Shield icon
    shield_icon = """
    <svg style="width:60px;height:60px;margin:20px" viewBox="0 0 24 24" fill="#26c6da">
        <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.67-3.13 8.96-7 10.12-3.87-1.16-7-5.45-7-10.12V6.3l7-3.12z"/>
    </svg>
    """
    
    st.markdown(f"""
        <div class="auth-container">
            {shield_icon}
            <h1 class="auth-title">Create Account</h1>
            <p class="auth-subtitle">Sign up for a new account</p>
    """, unsafe_allow_html=True)

    # Registration Form
    reg_username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
    reg_email = st.text_input("Email", placeholder="Enter your email", key="reg_email")
    reg_password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
    reg_confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm_password")
    
    if st.button("Create Account", key="register_button"):
        if reg_password != reg_confirm_password:
            st.error("Passwords do not match!")
            return
            
        try:
            response = requests.post(
                "http://localhost:5000/register",
                json={
                    "username": reg_username,
                    "email": reg_email,
                    "password": reg_password
                }
            )
            
            if response.status_code == 201:
                st.success("Registration successful! Please login.")
                # Redirect to login page
                st.session_state.current_tab = "login"
                st.rerun()
            else:
                st.error(response.json().get("error", "Registration failed"))
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend is running.")

    st.markdown("""
        <p style="text-align: center; margin-top: 1rem;">
            Already have an account? 
            <a href="#" style="color: #26c6da; text-decoration: none;" onclick="window.location.href='/'">Sign in</a>
        </p>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True) 