"""
pages/about.py — About Project page for CyberShield.

Explains the project purpose, features, technologies, and design decisions.
Makes it clear this is an educational demo using simulated data only.
"""

import streamlit as st

# ─── Page heading ─────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='margin-bottom:4px;'>ℹ️ About CyberShield</h1>",
    unsafe_allow_html=True,
)
st.caption("Security Event Analysis System — Educational Demonstration")
st.divider()

# ─── Important disclaimer (first thing the reader sees) ──────────────────────

st.warning(
    "⚠️ **Educational Use Only** — CyberShield uses entirely **simulated data**. "
    "It does **not** connect to a real network, detect real attacks, or monitor "
    "any actual infrastructure. All incident IDs, IP addresses, and event details "
    "are randomly generated for learning purposes."
)

# ─── Project Purpose ─────────────────────────────────────────────────────────

st.subheader("🎯 Project Purpose")
st.write(
    """
    CyberShield is a beginner-level college project that simulates a
    **Security Operations Centre (SOC)** dashboard. A real SOC is a team of
    cybersecurity analysts who monitor an organisation's network around the clock,
    looking for suspicious activity and responding to incidents.

    This project recreates the *look and feel* of such a dashboard using Python and
    Streamlit so students can understand:
    - What kinds of security events analysts track (failed logins, malware alerts, etc.)
    - How events are categorised by **severity** (High / Medium / Low) and
      **status** (Open / Investigating / Resolved)
    - How dashboards use charts and tables to give analysts a quick overview
    - How search and filter tools help find specific incidents in a large log
    """
)

# ─── What is a Security Event? ────────────────────────────────────────────────

st.subheader("🔐 What is a Security Event?")
st.write(
    """
    A **security event** is any observable occurrence in a network or system that
    might have security implications.  Not every event is an attack, but each one
    deserves to be logged and reviewed.  Examples include:
    """
)

event_descriptions = {
    "Failed Login":             "Multiple failed attempts to authenticate to a system — could indicate a brute-force attack.",
    "Malware Alert":            "Antivirus or endpoint-detection software flagged a file or process as malicious.",
    "Suspicious Traffic":       "Unusual data packets detected on the network — unexpected volume, destination, or protocol.",
    "Unauthorized Access":      "A user or process tried to access a resource they do not have permission to view.",
    "Unusual Network Activity": "Network behaviour that deviates from the normal baseline (e.g. large data transfers at midnight).",
    "Port Scan":                "An automated tool probing many ports to discover which services are running — common first step in an attack.",
}

for etype, desc in event_descriptions.items():
    st.markdown(f"- **{etype}** — {desc}")

# ─── Dashboard Features ───────────────────────────────────────────────────────

st.subheader("✨ Dashboard Features")

features = [
    ("📊 Overview Dashboard",
     "4 metric cards (total events, high-risk, failed logins, resolved) plus "
     "three interactive Plotly charts: a donut chart for severity distribution, "
     "a horizontal bar chart for event categories, and a line chart showing "
     "how incidents trend over time."),

    ("🚨 Security Event Logs",
     "A full colour-coded table listing every event with Event ID, timestamp, "
     "IP address, type, severity, and status.  Severity is highlighted in red "
     "(High), amber (Medium), or green (Low).  Status uses matching colours."),

    ("🔍 Event Search",
     "A combined search + filter tool.  Type any term (event ID, IP, or event "
     "type) in the text box and optionally restrict results by Severity or Status "
     "using the dropdowns.  All three filters work together.  A Clear button "
     "resets everything in one click."),

    ("⚡ Generate Dataset",
     "Press 'Generate Dataset' on the Overview or Events page to create a fresh "
     "batch of 24–30 randomly generated events.  The new data is saved to "
     "data/events.json so it persists across browser refreshes."),
]

for title, description in features:
    with st.expander(title, expanded=True):
        st.write(description)

# ─── How the Charts Work ─────────────────────────────────────────────────────

st.subheader("📈 How the Charts Work")
st.write(
    """
    All three charts on the Overview page are built with **Plotly Express** and
    read from the same dataset that powers the Events table.  This means the
    charts always stay in sync with the table — if you generate a new dataset,
    the cards, table, and charts all update at once.

    - **Donut chart**: counts events in each severity bucket and draws them as
      proportional arc segments.
    - **Bar chart**: counts events in each event-type bucket and draws horizontal
      bars (easiest to read when labels are long).
    - **Line chart**: groups events by date and severity, then plots each severity
      as a separate coloured line so you can see whether High-severity events are
      clustering on certain days.

    Hover your cursor over any chart element to see exact numbers in a tooltip.
    """
)

# ─── How Search & Filters Work ────────────────────────────────────────────────

st.subheader("🔍 How Search and Filters Work")
st.write(
    """
    The Event Search page applies three independent filters on top of each other:

    1. **Text search** — checks whether your query appears anywhere in the
       Event ID, IP Address, or Event Type columns (case-insensitive).
    2. **Severity dropdown** — hides events that don't match the chosen severity.
    3. **Status dropdown** — hides events that don't match the chosen status.

    All three filters are applied together, so selecting "High" severity AND
    searching for "192.168" will only show High-severity events from that IP range.
    Press **Enter** in the search box (or change a dropdown) to update results
    instantly.  Click **Clear** to reset everything.

    Try these examples:
    - Search `INC1004` → finds one exact event.
    - Search `192.168.1.15` → finds all events from that IP.
    - Search `failed login` → finds all failed-login events.
    - Search `malware` → finds all malware alerts.
    """
)

# ─── Technologies Used ────────────────────────────────────────────────────────

st.subheader("🛠️ Technologies Used")

tech_data = {
    "Technology": ["Python 3", "Streamlit", "pandas", "Plotly Express"],
    "Role": [
        "Core programming language",
        "Web framework — turns Python scripts into a browser app",
        "Data loading, filtering, and statistics",
        "Interactive charts (donut, bar, line)",
    ],
    "Why Chosen": [
        "Simple syntax, vast ecosystem, widely taught in colleges",
        "Requires no HTML/CSS/JS knowledge — ideal for data science projects",
        "Industry-standard library for tabular data in Python",
        "Beautiful, interactive charts with a single line of code",
    ],
}

import pandas as pd  # noqa: E402 (local import to keep top clean)
st.dataframe(pd.DataFrame(tech_data), use_container_width=True, hide_index=True)

# ─── Footer ──────────────────────────────────────────────────────────────────

st.divider()
st.markdown(
    "<p style='color:#8b949e; font-size:0.8rem;'>"
    "CyberShield — Built with Python &amp; Streamlit · "
    "Simulated data only · No real network is monitored.</p>",
    unsafe_allow_html=True,
)
