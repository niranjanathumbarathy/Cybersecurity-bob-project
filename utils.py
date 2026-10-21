"""
utils.py — Shared UI helpers for CyberShield.

Keeps table styling logic in one place so pages/events.py and
pages/search.py both render the same consistent table without
duplicating code.
"""

import pandas as pd
import streamlit as st

# ─── Colour maps ──────────────────────────────────────────────────────────────

# Severity background colours (dark-theme friendly)
_SEV_BG = {
    "High":   "#7f1d1d",   # deep red
    "Medium": "#78350f",   # deep amber
    "Low":    "#14532d",   # deep green
}
_SEV_FG = {
    "High":   "#fca5a5",
    "Medium": "#fcd34d",
    "Low":    "#86efac",
}

# Status background colours
_STA_BG = {
    "Open":          "#1e3a5f",   # dark blue
    "Investigating": "#3b2a6b",   # dark purple
    "Resolved":      "#14532d",   # dark green
}
_STA_FG = {
    "Open":          "#93c5fd",
    "Investigating": "#c4b5fd",
    "Resolved":      "#86efac",
}


def _style_severity(val: str) -> str:
    """Return a CSS string for a Severity cell."""
    bg = _SEV_BG.get(val, "")
    fg = _SEV_FG.get(val, "")
    return f"background-color:{bg}; color:{fg}; font-weight:600; border-radius:4px;"


def _style_status(val: str) -> str:
    """Return a CSS string for a Status cell."""
    bg = _STA_BG.get(val, "")
    fg = _STA_FG.get(val, "")
    return f"background-color:{bg}; color:{fg}; font-weight:600; border-radius:4px;"


def display_events_table(df: pd.DataFrame) -> None:
    """
    Render *df* as a styled Streamlit dataframe with:
      • Friendly column labels
      • Colour-coded Severity and Status columns
      • Full width, sensible column widths

    Used by both pages/events.py and pages/search.py.
    """
    if df.empty:
        st.info("No matching events found.")
        return

    # Rename columns to display-friendly labels
    display_df = df.rename(columns={
        "id":       "Event ID",
        "datetime": "Date and Time",
        "ip":       "IP Address",
        "type":     "Event Type",
        "severity": "Severity",
        "status":   "Status",
    })

    # Apply per-cell colour styling
    # (pandas 2.1+ uses .map(); older versions used .applymap())
    styler = display_df.style
    try:
        styled = (
            styler
            .map(_style_severity, subset=["Severity"])
            .map(_style_status,   subset=["Status"])
        )
    except AttributeError:
        styled = (
            styler
            .applymap(_style_severity, subset=["Severity"])
            .applymap(_style_status,   subset=["Status"])
        )

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Event ID":    st.column_config.TextColumn(width="small"),
            "Date and Time": st.column_config.TextColumn(width="medium"),
            "IP Address":  st.column_config.TextColumn(width="medium"),
            "Event Type":  st.column_config.TextColumn(width="medium"),
            "Severity":    st.column_config.TextColumn(width="small"),
            "Status":      st.column_config.TextColumn(width="medium"),
        },
    )
