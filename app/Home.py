"""
Home.py — Streamlit entry point.
Run with: streamlit run app/Home.py
"""

import sys
import os

# Streamlit only adds this file's own folder (app/) to sys.path, not the
# project root above it — so "from app.auth..." would fail without this.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from app.auth.auth_handler import login_user, signup_user, logout_user
from app.components.sidebar import render_sidebar

st.set_page_config(page_title="Ikraceya — Compliance Checker", page_icon="✅", layout="wide")

# Initialize session state defaults on first load
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


def show_login_signup():
    st.title("Ikraceya")
    st.caption("Scan. Verify. Comply.")

    tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log In")

            if submitted:
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    # Go straight into the app instead of landing on a static
                    # welcome screen — persona defaults to "consumer" already
                    # (set in login_user), so users can head straight to Scan.
                    st.switch_page("pages/2_Scan.py")
                else:
                    st.error(message)

    with tab_signup:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username", key="signup_username")
            new_password = st.text_input("Choose a password", type="password", key="signup_password")
            role = st.selectbox("I am a...", ["consumer", "seller"], key="signup_role")
            submitted = st.form_submit_button("Sign Up")

            if submitted:
                success, message = signup_user(new_username, new_password, role)
                if success:
                    st.success(message)
                else:
                    st.error(message)


def show_logged_in_home():
    render_sidebar()

    st.title(f"Welcome, {st.session_state['username']}")
    st.write(f"Role: **{st.session_state['role']}**")
    st.write(f"Current persona: **{st.session_state.get('persona', 'consumer')}**")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧭 Persona Selection", use_container_width=True):
            st.switch_page("pages/1_Persona_Selection.py")
    with col2:
        if st.button("📷 Go to Scan", use_container_width=True):
            st.switch_page("pages/2_Scan.py")


# --- Router ---
if st.session_state["logged_in"]:
    show_logged_in_home()
else:
    show_login_signup()