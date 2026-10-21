"""
data.py — Shared data logic for CyberShield.

All pages import from this module.  No database is used; events are stored in
st.session_state (for in-memory speed) and synced to data/events.json so they
survive a browser refresh.
"""

import json
import os
import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# ─── Constants ────────────────────────────────────────────────────────────────

EVENT_TYPES = [
    "Failed Login",
    "Malware Alert",
    "Suspicious Traffic",
    "Unauthorized Access",
    "Unusual Network Activity",
    "Port Scan",
]

SEVERITIES = ["High", "Medium", "Low"]
STATUSES   = ["Open", "Investigating", "Resolved"]

DATA_DIR  = "data"
DATA_FILE = os.path.join(DATA_DIR, "events.json")


# ─── Default (built-in) dataset ───────────────────────────────────────────────

def default_events() -> list[dict]:
    """
    Return a hard-coded list of 24 fictional security events used as a
    fallback when the JSON file is missing or invalid.

    Rules guaranteed by this dataset:
      • INC1004 is present
      • IP 192.168.1.15 appears at least once
      • At least one Failed Login and one Malware Alert
    """
    base_date = datetime(2024, 6, 1, 8, 0, 0)

    rows = [
        # id,      delta_h, ip,                type,                      severity, status
        ("INC1001",  0,  "192.168.1.10",  "Failed Login",             "High",   "Open"),
        ("INC1002",  2,  "10.0.0.25",     "Malware Alert",            "High",   "Investigating"),
        ("INC1003",  5,  "192.168.1.30",  "Suspicious Traffic",       "Medium", "Open"),
        ("INC1004",  7,  "192.168.1.15",  "Unauthorized Access",      "High",   "Resolved"),
        ("INC1005", 10,  "10.0.1.5",      "Unusual Network Activity",  "Low",    "Resolved"),
        ("INC1006", 13,  "192.168.2.20",  "Port Scan",                "Medium", "Open"),
        ("INC1007", 15,  "10.0.0.80",     "Failed Login",             "Medium", "Investigating"),
        ("INC1008", 18,  "192.168.1.50",  "Malware Alert",            "High",   "Open"),
        ("INC1009", 22,  "10.0.2.15",     "Suspicious Traffic",       "Low",    "Resolved"),
        ("INC1010", 25,  "192.168.3.11",  "Port Scan",                "Medium", "Open"),
        ("INC1011", 28,  "10.0.0.100",    "Unusual Network Activity",  "High",   "Investigating"),
        ("INC1012", 30,  "192.168.1.15",  "Failed Login",             "High",   "Open"),
        ("INC1013", 33,  "10.0.1.22",     "Unauthorized Access",      "Medium", "Resolved"),
        ("INC1014", 36,  "192.168.4.5",   "Malware Alert",            "High",   "Investigating"),
        ("INC1015", 40,  "10.0.3.9",      "Port Scan",                "Low",    "Resolved"),
        ("INC1016", 43,  "192.168.1.77",  "Suspicious Traffic",       "Medium", "Open"),
        ("INC1017", 46,  "10.0.0.55",     "Failed Login",             "Low",    "Resolved"),
        ("INC1018", 50,  "192.168.2.45",  "Unusual Network Activity",  "Medium", "Investigating"),
        ("INC1019", 53,  "10.0.4.3",      "Malware Alert",            "High",   "Open"),
        ("INC1020", 56,  "192.168.1.90",  "Unauthorized Access",      "High",   "Investigating"),
        ("INC1021", 60,  "10.0.1.60",     "Port Scan",                "Medium", "Resolved"),
        ("INC1022", 63,  "192.168.5.8",   "Failed Login",             "High",   "Open"),
        ("INC1023", 66,  "10.0.2.40",     "Suspicious Traffic",       "Low",    "Resolved"),
        ("INC1024", 70,  "192.168.3.22",  "Unusual Network Activity",  "Medium", "Open"),
    ]

    events = []
    for (eid, delta_h, ip, etype, severity, status) in rows:
        dt = base_date + timedelta(hours=delta_h)
        events.append({
            "id":       eid,
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "ip":       ip,
            "type":     etype,
            "severity": severity,
            "status":   status,
        })
    return events


# ─── Random event generator ───────────────────────────────────────────────────

def generate_events() -> list[dict]:
    """
    Create 24–30 new random security events spread over the last 7 days.
    IDs start from INC2001 to avoid collisions with the default set.
    """
    count    = random.randint(24, 30)
    now      = datetime.now()
    events   = []

    # Weight severities so High events aren't too rare
    sev_weights = [3, 4, 3]   # High / Medium / Low

    for i in range(count):
        eid      = f"INC{2001 + i}"
        delta    = timedelta(
            days=random.uniform(0, 7),
            hours=random.uniform(0, 23),
            minutes=random.uniform(0, 59),
        )
        dt       = now - delta
        ip       = (
            f"192.168.{random.randint(0, 5)}.{random.randint(1, 254)}"
            if random.random() < 0.6
            else f"10.0.{random.randint(0, 5)}.{random.randint(1, 254)}"
        )
        events.append({
            "id":       eid,
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "ip":       ip,
            "type":     random.choice(EVENT_TYPES),
            "severity": random.choices(SEVERITIES, weights=sev_weights, k=1)[0],
            "status":   random.choice(STATUSES),
        })

    # Sort newest first
    events.sort(key=lambda e: e["datetime"], reverse=True)
    return events


# ─── Persistence helpers ──────────────────────────────────────────────────────

def save_events(events: list[dict]) -> None:
    """Persist *events* to data/events.json, creating the folder if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as fh:
        json.dump(events, fh, indent=2)


def load_events() -> pd.DataFrame:
    """
    Load events into a DataFrame.

    Priority:
      1. st.session_state["events"]  (already loaded this session)
      2. data/events.json            (persisted from a previous run)
      3. default_events()            (hard-coded fallback)

    Returns a DataFrame with columns:
        id | datetime | ip | type | severity | status
    """
    if "events" not in st.session_state:
        # Try reading from file first
        raw = _read_json_file()
        if raw is None:
            raw = default_events()
        st.session_state["events"] = raw

    return pd.DataFrame(st.session_state["events"])


def _read_json_file() -> list[dict] | None:
    """Read events.json; return None if missing, empty, or malformed."""
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE) as fh:
            data = json.load(fh)
        if not isinstance(data, list) or len(data) == 0:
            return None
        return data
    except (json.JSONDecodeError, OSError):
        return None


# ─── Statistics helper ────────────────────────────────────────────────────────

def get_stats(df: pd.DataFrame) -> dict:
    """
    Return a dict of summary statistics used by the Overview cards.

    Keys: total, high_risk, failed_logins, resolved
    """
    return {
        "total":         len(df),
        "high_risk":     int((df["severity"] == "High").sum()),
        "failed_logins": int((df["type"] == "Failed Login").sum()),
        "resolved":      int((df["status"] == "Resolved").sum()),
    }


# ─── Action handler ───────────────────────────────────────────────────────────

def handle_generate() -> None:
    """
    Generate a fresh random dataset, persist it to JSON, and update
    st.session_state so every page sees the new data instantly.

    This is the ONLY place generate+save+update logic lives.
    Both 'Generate Dataset' buttons (Overview and Events page) call this.
    """
    new_events = generate_events()
    save_events(new_events)
    st.session_state["events"] = new_events
