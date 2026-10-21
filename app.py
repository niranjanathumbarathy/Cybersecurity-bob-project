"""
app.py — Entry point for CyberShield Security Event Analysis System.

Sets up navigation and the sidebar header, then hands control to the
individual page modules.
"""

import streamlit as st

# ─── Page configuration (must be first Streamlit call) ────────────────────────

st.set_page_config(
    page_title="CyberShield — Security Event Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Sidebar branding ─────────────────────────────────────────────────────────

st.sidebar.markdown(
    """
    <div style="text-align:center; padding: 10px 0 18px 0;">
        <span style="font-size:2rem;">🛡️</span><br>
        <span style="font-size:1.35rem; font-weight:700; color:#e6edf3;
                     letter-spacing:0.04em;">CyberShield</span><br>
        <span style="font-size:0.72rem; color:#8b949e;">
            Security Event Analysis System
        </span>
    </div>
    <hr style="border-color:#30363d; margin:0 0 10px 0;">
    """,
    unsafe_allow_html=True,
)

# ─── Navigation ───────────────────────────────────────────────────────────────

overview_page = st.Page(
    "pages/overview.py",
    title="Overview",
    icon="📊",
    default=True,
)
events_page = st.Page(
    "pages/events.py",
    title="Security Events",
    icon="🚨",
)
search_page = st.Page(
    "pages/search.py",
    title="Event Search",
    icon="🔍",
)
about_page = st.Page(
    "pages/about.py",
    title="About Project",
    icon="ℹ️",
)

nav = st.navigation(
    [overview_page, events_page, search_page, about_page],
    position="sidebar",
)

nav.run()
