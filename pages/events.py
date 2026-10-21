"""
pages/events.py — Security Event Logs page for CyberShield.

Displays the full events table with colour-coded Severity and Status columns,
plus a "Generate Dataset" button.
"""

import streamlit as st

from data import handle_generate, load_events
from utils import display_events_table

# ─── Page heading ─────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='margin-bottom:4px;'>🚨 Security Event Logs</h1>",
    unsafe_allow_html=True,
)
st.write(
    "A complete log of all recorded security incidents detected in the "
    "simulated environment."
)
st.caption("⚠️ All data shown here is simulated and generated for educational purposes only.")
st.divider()

# ─── Load and display data ────────────────────────────────────────────────────

df = load_events()

st.markdown(f"**{len(df)} events** in the current dataset.")

display_events_table(df)

st.divider()

# ─── Generate button ──────────────────────────────────────────────────────────

if st.button("⚡ Generate Dataset", type="primary"):
    handle_generate()
    st.rerun()
