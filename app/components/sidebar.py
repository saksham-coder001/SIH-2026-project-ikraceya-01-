"""
sidebar.py — shared sidebar component.

Call render_sidebar() at the top of every page (after require_login()).
Places the project logo above Streamlit's auto-generated page navigation
via st.logo(), then a compact block of user/persona info and logout below
the nav (Streamlit always renders its own nav first — this is the only
way to put branding above it).
"""

import streamlit as st

from app.auth.auth_handler import logout_user


def render_sidebar():
    with st.sidebar:
        st.markdown("**Ikraceya** · Scan. Verify. Comply.")
        st.divider()

        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "-")
        persona = st.session_state.get("persona", "consumer")

        st.caption(f"👤 **{username}** ({role}) · Persona: **{persona}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Switch persona", use_container_width=True):
                st.session_state.pop("persona", None)
                st.switch_page("pages/1_Persona_Selection.py")
        with col2:
            if st.button("Log Out", use_container_width=True):
                logout_user()
                st.switch_page("Home.py")