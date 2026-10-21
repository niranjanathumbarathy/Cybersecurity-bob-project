"""
pages/search.py — Event Search page for CyberShield.

Lets the user filter events by free-text query (ID / IP / type) plus
dropdown filters for Severity and Status.  Results are shown in the
same styled table used by the Events page.
"""

import streamlit as st

from data import load_events
from utils import display_events_table

# ─── Page heading ─────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='margin-bottom:4px;'>🔍 Event Search</h1>",
    unsafe_allow_html=True,
)
st.write("Search and filter security events by ID, IP address, or event type.")
st.divider()

# ─── Session-state keys for resettable widgets ────────────────────────────────
# We use explicit keys so the "Clear" button can reset them via session_state.

_KEY_QUERY   = "search_query"
_KEY_SEV     = "search_severity"
_KEY_STATUS  = "search_status"


def _clear_search() -> None:
    """Callback: reset all search-related session-state keys."""
    st.session_state[_KEY_QUERY]  = ""
    st.session_state[_KEY_SEV]    = "All"
    st.session_state[_KEY_STATUS] = "All"


# Initialise keys on first run
if _KEY_QUERY  not in st.session_state:
    st.session_state[_KEY_QUERY]  = ""
if _KEY_SEV    not in st.session_state:
    st.session_state[_KEY_SEV]    = "All"
if _KEY_STATUS not in st.session_state:
    st.session_state[_KEY_STATUS] = "All"

# ─── Search controls ──────────────────────────────────────────────────────────

query = st.text_input(
    label="Search events",
    placeholder="Search by event ID, IP address, or event type…",
    key=_KEY_QUERY,
    label_visibility="collapsed",
)
st.caption("💡 Press **Enter** to update results.")

filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 0.4])

with filter_col1:
    severity_filter = st.selectbox(
        "Severity",
        options=["All", "High", "Medium", "Low"],
        key=_KEY_SEV,
    )

with filter_col2:
    status_filter = st.selectbox(
        "Status",
        options=["All", "Open", "Investigating", "Resolved"],
        key=_KEY_STATUS,
    )

with filter_col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.button("✖ Clear", on_click=_clear_search, use_container_width=True)

# ─── Load and filter data ─────────────────────────────────────────────────────

df       = load_events()
filtered = df.copy()

# Text search — case-insensitive match in id, ip, or type columns
if query.strip():
    q = query.strip().lower()
    mask = (
        filtered["id"].str.lower().str.contains(q, na=False)
        | filtered["ip"].str.lower().str.contains(q, na=False)
        | filtered["type"].str.lower().str.contains(q, na=False)
    )
    filtered = filtered[mask]

# Severity filter
if severity_filter != "All":
    filtered = filtered[filtered["severity"] == severity_filter]

# Status filter
if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]

# ─── Results summary ──────────────────────────────────────────────────────────

total_events   = len(df)
matched_events = len(filtered)

st.markdown(
    f"<p style='color:#8b949e; margin:10px 0 6px 0;'>"
    f"Showing <strong style='color:#e6edf3;'>{matched_events}</strong> "
    f"of <strong style='color:#e6edf3;'>{total_events}</strong> events.</p>",
    unsafe_allow_html=True,
)

# ─── Results table ────────────────────────────────────────────────────────────

if matched_events == 0:
    st.warning("No matching events found. Try a different search term or clear your filters.")
else:
    display_events_table(filtered)
