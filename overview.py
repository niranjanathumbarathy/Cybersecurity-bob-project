"""
pages/overview.py — Overview page for CyberShield.

Shows 4 summary metric cards, 3 Plotly charts (donut, bar, line),
a "Generate Dataset" button, and a link to the Security Events page.
"""

import plotly.express as px
import streamlit as st

from data import get_stats, handle_generate, load_events

# ─── Page heading ─────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='margin-bottom:4px;'>📊 Security Overview</h1>",
    unsafe_allow_html=True,
)
st.caption("Real-time summary of simulated security events in your environment.")
st.divider()

# ─── Load data ────────────────────────────────────────────────────────────────

df    = load_events()
stats = get_stats(df)

# ─── Summary metric cards ─────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="🗂️ Total Events",
    value=stats["total"],
)
col2.metric(
    label="🔴 High-Risk Events",
    value=stats["high_risk"],
)
col3.metric(
    label="🔑 Failed Login Attempts",
    value=stats["failed_logins"],
)
col4.metric(
    label="✅ Resolved Events",
    value=stats["resolved"],
)

st.divider()

# ─── Charts row ───────────────────────────────────────────────────────────────

chart_col1, chart_col2, chart_col3 = st.columns([1, 1, 1.4])

# 1. Events by Severity — donut chart
with chart_col1:
    st.subheader("Events by Severity")
    sev_counts = df["severity"].value_counts().reset_index()
    sev_counts.columns = ["Severity", "Count"]

    # Fixed colour map so the colours are always meaningful
    sev_colors = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"}

    fig_donut = px.pie(
        sev_counts,
        names="Severity",
        values="Count",
        hole=0.55,
        color="Severity",
        color_discrete_map=sev_colors,
        title="",
    )
    fig_donut.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
    )
    fig_donut.update_layout(
        legend_title_text="Severity",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# 2. Event Categories — bar chart
with chart_col2:
    st.subheader("Event Categories")
    type_counts = df["type"].value_counts().reset_index()
    type_counts.columns = ["Event Type", "Count"]

    fig_bar = px.bar(
        type_counts,
        x="Count",
        y="Event Type",
        orientation="h",
        color="Count",
        color_continuous_scale="Blues",
        title="",
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
    )
    fig_bar.update_layout(
        xaxis_title="Number of Events",
        yaxis_title="",
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        margin=dict(t=10, b=10, l=10, r=10),
        yaxis=dict(categoryorder="total ascending"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 3. Incident Trends — line chart
with chart_col3:
    st.subheader("Incident Trends (by Date)")

    # Group events by date and severity for the line chart
    trend_df = df.copy()
    trend_df["date"] = trend_df["datetime"].str[:10]           # YYYY-MM-DD
    trend_counts = (
        trend_df.groupby(["date", "severity"])
        .size()
        .reset_index(name="Count")
    )
    trend_counts = trend_counts.sort_values("date")

    sev_colors_line = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"}

    fig_line = px.line(
        trend_counts,
        x="date",
        y="Count",
        color="severity",
        color_discrete_map=sev_colors_line,
        markers=True,
        title="",
    )
    fig_line.update_traces(
        hovertemplate="Date: %{x}<br>Count: %{y}<extra></extra>",
    )
    fig_line.update_layout(
        xaxis_title="Date",
        yaxis_title="Events",
        legend_title_text="Severity",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ─── Action buttons ───────────────────────────────────────────────────────────

btn_col1, btn_col2, _ = st.columns([1, 1.6, 2])

with btn_col1:
    if st.button("⚡ Generate Dataset", use_container_width=True, type="primary"):
        handle_generate()
        st.rerun()

with btn_col2:
    # Navigate to the Security Events page
    st.page_link("pages/events.py", label="🚨 View Security Event Logs", use_container_width=True)

# ─── Footer note ──────────────────────────────────────────────────────────────

st.markdown(
    "<p style='margin-top:18px; color:#8b949e; font-size:0.8rem;'>"
    "⚠️ Simulated data for educational use. "
    "This dashboard does not monitor a real network.</p>",
    unsafe_allow_html=True,
)
