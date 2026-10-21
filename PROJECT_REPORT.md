# PROJECT REPORT

---

## CyberShield — Security Event Analysis System

---

| Field           | Details                                      |
|-----------------|----------------------------------------------|
| **Project Title** | CyberShield — Security Event Analysis System |
| **Student Name**  | Niranjana T S                                |
| **Roll Number**   | 33                                           |
| **Course**        | B.Tech CSE                                   |
| **College**       | Nirmala College of Engineering               |
| **Department**    | CSE                                          |
| **Submission Date** | 21/10/2026                                 |
                         

---

## 1. Abstract

CyberShield is a web-based security event analysis dashboard built using Python
and Streamlit.  It is designed as a beginner-level college project to demonstrate
the concepts used in a Security Operations Centre (SOC) environment.  The
dashboard displays simulated security events in the form of charts, metric cards,
and a searchable table, allowing the user to explore how security analysts
categorise, prioritise, and filter incidents.

The system uses Plotly for interactive charts, pandas for data processing, and
Streamlit's built-in widget system for navigation, filters, and live updates.
All data is randomly generated; no real network is monitored, and no actual
security data is used at any point.  The project demonstrates data visualisation,
state management, modular code organisation, and beginner-friendly web development
in Python.

---

## 2. Introduction

Cybersecurity has become one of the most important fields in technology.
Organisations of all sizes employ Security Operations Centres (SOCs) — teams of
analysts who monitor their networks for suspicious activity, respond to incidents,
and keep systems safe.  These analysts rely on dashboards that aggregate and
visualise security events in real time so they can act quickly.

This project, CyberShield, builds a simplified version of such a dashboard.  It
is not connected to a real network and does not detect real attacks.  Instead, it
uses simulated data to show how a SOC dashboard is structured, what kinds of
events are logged, and how tools like charts, tables, and search filters help
analysts make sense of large volumes of data.

The project is developed entirely in Python using publicly available, free
libraries.  It requires no database, no cloud service, and no API keys.  A
student can install and run it on any laptop in under five minutes.

---

## 3. Problem Statement

Students learning cybersecurity often struggle to understand what a real SOC
looks like in practice.  Textbooks describe the concepts but cannot show the
experience of viewing a live dashboard, filtering events, or seeing how an
incident's severity affects its priority.

Additionally, most real security tools are expensive, proprietary, and require
access to live infrastructure.  A beginner student cannot simply install and
explore a commercial SIEM (Security Information and Event Management) platform.

**CyberShield addresses this gap** by providing a fully functional, open-source,
simulated SOC dashboard that any student can run locally, explore freely, and
study in detail.

---

## 4. Objectives

1. Build a multi-page web dashboard using Python and Streamlit.
2. Simulate realistic-looking security event data with proper categorisation.
3. Display summary statistics using metric cards.
4. Visualise event data using three different chart types (donut, bar, line).
5. Provide a searchable, filterable event log table with colour-coded rows.
6. Allow the user to generate new random datasets at the click of a button.
7. Write clean, commented, beginner-readable code that can be studied and extended.
8. Persist generated data between browser sessions using a JSON file.

---

## 5. Scope and Limitations

### Scope

- The project covers the front-end display and in-memory data management of a
  SOC-style dashboard.
- It supports six event types, three severity levels, and three status values.
- It includes a fully functional search + filter tool.
- It generates, saves, and reloads random datasets.

### Limitations

| Limitation | Detail |
|------------|--------|
| Simulated data only | All incident IDs, IP addresses, and timestamps are randomly generated. No real network traffic is captured or analysed. |
| No real-time monitoring | The dashboard does not connect to any live data feed. It does not update automatically. |
| No authentication | There is no login system. Anyone who opens the URL can see and interact with the dashboard. |
| No database | Events are stored in a plain JSON file. This is not suitable for production use. |
| No alerting | The system does not send emails, SMS, or push notifications. |
| No remediation | Users can view events but cannot take any action on them (close tickets, assign to analysts, etc.). |

---

## 6. Technologies Used

### 6.1 Python 3

Python is the core programming language of this project.  It was chosen because:
- It has a simple, readable syntax ideal for beginners.
- It has a vast ecosystem of free libraries.
- It is widely taught in college courses and has excellent community support.
- Streamlit, pandas, and Plotly are all Python libraries, so no other language is needed.

### 6.2 Streamlit

Streamlit is a Python library that turns a Python script into a web application
running in a browser.  It was chosen because:
- No HTML, CSS, or JavaScript knowledge is required.
- Navigation, sidebar, buttons, tables, and inputs are all created with simple Python function calls.
- It handles page state (session_state) and reruns the script automatically when the user interacts.
- Hot-reloading makes development fast: save the file and the browser updates immediately.

### 6.3 pandas

pandas is the standard Python library for working with tabular data (like
spreadsheet rows and columns).  It was chosen because:
- It makes it easy to load, filter, group, and count data.
- Streamlit's st.dataframe() accepts a pandas DataFrame directly.
- It integrates natively with Plotly for charts.

### 6.4 Plotly Express

Plotly Express is a high-level charting library that creates interactive charts
with a single Python function call.  It was chosen because:
- Charts are interactive by default (hover tooltips, zoom, pan).
- It supports donut charts, bar charts, and line charts with very little code.
- Charts can be customised (colours, legends, titles) without complex configuration.
- It integrates directly with Streamlit via st.plotly_chart().

---

## 7. System Design

### 7.1 Architecture

CyberShield follows a simple, flat architecture:

```
Browser (User)
    │
    ▼
app.py  ←── sets up navigation and sidebar branding
    │
    ├── pages/overview.py    ← reads data.py, renders charts + metrics
    ├── pages/events.py      ← reads data.py, renders table
    ├── pages/search.py      ← reads data.py, filters + renders table
    └── pages/about.py       ← static content only
         │
         ▼
    data.py  ←── load_events(), save_events(), handle_generate(), get_stats()
         │
         ├── st.session_state["events"]   (in-memory, fast)
         └── data/events.json             (persistent, survives refresh)
```

There is no server-side database, no background process, and no external API.
Everything runs in a single Python process on the user's machine.

### 7.2 Folder Structure

```
CyberShield/
├── app.py                    Entry point
├── data.py                   Shared data logic
├── utils.py                  Shared table helper
├── requirements.txt          Dependency list
├── README.md                 User guide
├── PROJECT_REPORT.md         This document
├── .streamlit/
│   └── config.toml           Theme configuration
├── pages/
│   ├── overview.py
│   ├── events.py
│   ├── search.py
│   └── about.py
└── data/
    └── events.json           Auto-created; stores generated events
```

### 7.3 Data Flow

1. **Page loads** → page calls `load_events()`.
2. `load_events()` checks `st.session_state["events"]` first.
3. If not found, it reads `data/events.json`.
4. If the file is missing or invalid, it falls back to `default_events()`.
5. The page receives a pandas DataFrame and renders it.
6. If the user clicks **Generate Dataset**, `handle_generate()` is called.
7. `handle_generate()` calls `generate_events()` → `save_events()` → updates `st.session_state`.
8. `st.rerun()` restarts the page script so all widgets see the new data.

---

## 8. Dataset Description

### 8.1 Event Fields

| Field     | Type   | Example Values                                 |
|-----------|--------|------------------------------------------------|
| id        | string | INC1001, INC1004, INC2015                      |
| datetime  | string | 2024-06-01 08:00:00 (YYYY-MM-DD HH:MM:SS)      |
| ip        | string | 192.168.1.15, 10.0.0.25                        |
| type      | string | Failed Login, Malware Alert, Suspicious Traffic, Unauthorized Access, Unusual Network Activity, Port Scan |
| severity  | string | High, Medium, Low                              |
| status    | string | Open, Investigating, Resolved                  |

### 8.2 Default Dataset

A hard-coded list of 24 events is embedded in `default_events()` in `data.py`.
These events:
- Use private IP address ranges (192.168.x.x and 10.x.x.x)
- Span approximately 7 days (1–3 June 2024 onwards)
- Include every event type at least twice
- Include INC1004 assigned to IP 192.168.1.15
- Include at least one Failed Login and at least one Malware Alert

### 8.3 Random Data Generation

`generate_events()` creates 24–30 new events by:
1. Picking a random number between 24 and 30.
2. For each event, choosing a random offset from 0–7 days in the past.
3. Randomly selecting an IP (60% chance of 192.168.x.x, 40% chance of 10.x.x.x).
4. Randomly selecting type, severity (weighted towards Medium), and status.
5. Assigning IDs starting from INC2001 to avoid collisions.
6. Sorting events newest-first.

---

## 9. Implementation

### 9.1 app.py

Creates the Streamlit page config (title, icon, layout), renders the sidebar
branding HTML, and defines the four `st.Page` objects passed to `st.navigation()`.
Streamlit's navigation system renders the correct page script depending on which
sidebar item the user clicks.

### 9.2 data.py

Contains all shared data logic.  Key functions:

| Function          | Purpose |
|-------------------|---------|
| `default_events()` | Returns the 24-event hard-coded fallback list. |
| `generate_events()` | Returns 24–30 randomly generated events. |
| `save_events(events)` | Writes the list to `data/events.json`. |
| `load_events()` | Loads from session_state → file → default (in priority order). Returns a DataFrame. |
| `get_stats(df)` | Returns a dict with total, high_risk, failed_logins, resolved counts. |
| `handle_generate()` | Calls generate → save → update session_state. Used by both Generate buttons. |

### 9.3 utils.py

Contains `display_events_table(df)` — a single function used by both
`pages/events.py` and `pages/search.py`.  It renames columns to display-friendly
labels and applies pandas Styler colour-coding before rendering with
`st.dataframe()`.  Keeping this in one place means a style change only needs
to be made once.

### 9.4 pages/overview.py

- Calls `load_events()` and `get_stats()`.
- Renders 4 `st.metric` cards.
- Builds 3 Plotly charts (donut via `px.pie`, bar via `px.bar`, line via `px.line`).
- Renders the Generate button and calls `handle_generate()` + `st.rerun()`.
- Renders a `st.page_link` to the Events page.

### 9.5 pages/events.py

- Calls `load_events()`.
- Calls `display_events_table(df)` from utils.py.
- Renders the Generate button.

### 9.6 pages/search.py

- Maintains three `st.session_state` keys (`search_query`, `search_severity`,
  `search_status`) so the Clear button can reset them via a callback.
- Applies text search (pandas `.str.contains`) and dropdown filters sequentially.
- Shows "Showing X of Y events" and calls `display_events_table(filtered)`.

### 9.7 pages/about.py

Static content page explaining the project, its features, and the technologies
used.  Includes an inline pandas DataFrame to display the technology table.

---

## 10. Testing

### Test Cases

| # | Test Case | Steps | Expected Result | Actual Result |
|---|-----------|-------|-----------------|---------------|
| 1 | App starts | Run `streamlit run app.py`, open browser | Overview page loads with metric cards and 3 charts | ✅ Pass |
| 2 | Default data | Open app without data/events.json | 24 events loaded, cards and charts populated | ✅ Pass |
| 3 | Generate Dataset (Overview) | Click ⚡ Generate Dataset on Overview page | Cards and charts update immediately | ✅ Pass |
| 4 | Generate Dataset (Events) | Click ⚡ Generate Dataset on Events page | Table reloads with new events | ✅ Pass |
| 5 | Data persists | Generate dataset, refresh browser tab | Same dataset shown (loaded from JSON) | ✅ Pass |
| 6 | Search by ID | Type `INC1004` on Search page, press Enter | 1 result: INC1004 | ✅ Pass |
| 7 | Search by IP | Type `192.168.1.15`, press Enter | Events from that IP shown | ✅ Pass |
| 8 | Search by type | Type `failed login`, press Enter | Only Failed Login events shown | ✅ Pass |
| 9 | Case insensitive | Type `MALWARE ALERT` | Same results as `malware alert` | ✅ Pass |
| 10 | Severity filter | Select Severity = High | Only High-severity events shown | ✅ Pass |
| 11 | Status filter | Select Status = Resolved | Only Resolved events shown | ✅ Pass |
| 12 | Combined filters | Type `malware`, Severity = High | Only High Malware Alert events | ✅ Pass |
| 13 | No results | Type `zzznothing` | "No matching events found." message | ✅ Pass |
| 14 | Clear button | Enter text + set filters, click Clear | Search box empty, dropdowns reset to All | ✅ Pass |
| 15 | Colour coding | View Events table | High = red, Medium = amber, Low = green | ✅ Pass |
| 16 | Navigation | Click each sidebar item | Correct page loads each time | ✅ Pass |
| 17 | Chart tooltips | Hover over donut, bar, and line charts | Tooltips show correct values | ✅ Pass |
| 18 | About page | Click About Project in sidebar | All sections render without error | ✅ Pass |
| 19 | Invalid JSON | Corrupt data/events.json, refresh | Falls back silently to default 24 events | ✅ Pass |
| 20 | Missing JSON | Delete data/events.json, refresh | Falls back silently to default 24 events | ✅ Pass |

---

## 11. Results and Screenshots

> The following screenshots were captured during testing on a local machine.
> (Replace the placeholders below with actual screenshots before submitting.)

**Figure 1 — Overview Dashboard**
```
[Insert screenshot of Overview page showing 4 metric cards and 3 charts]
```

**Figure 2 — Security Event Logs Table**
```
[Insert screenshot of Events page showing the colour-coded table]
```

**Figure 3 — Event Search with Filter Applied**
```
[Insert screenshot of Search page showing results filtered by Severity = High]
```

**Figure 4 — Event Search — No Results Found**
```
[Insert screenshot of Search page showing the "No matching events found" message]
```

**Figure 5 — About Project Page**
```
[Insert screenshot of About page]
```

**Figure 6 — Donut Chart (Events by Severity)**
```
[Insert screenshot of donut chart showing High / Medium / Low proportions]
```

**Figure 7 — Bar Chart (Event Categories)**
```
[Insert screenshot of horizontal bar chart]
```

**Figure 8 — Line Chart (Incident Trends by Date)**
```
[Insert screenshot of line chart with three severity lines]
```

---

## 12. Conclusion

CyberShield successfully demonstrates the core concepts of a Security Operations
Centre dashboard in a format that any beginner Python student can understand,
run, and modify.  The project covers multiple important programming concepts:
modular code organisation, in-memory and persistent state management, interactive
data visualisation, user input handling, and clean UI design.

By using only four libraries (Streamlit, pandas, Plotly, and the Python standard
library), the project remains simple enough to be a learning tool while still
producing a visually polished result that resembles professional cybersecurity
software.

The key design decision — centralising all data logic in `data.py` and all table
rendering in `utils.py` — means the codebase avoids duplication and is easy to
maintain.  Adding a new page would require only importing `load_events()` and
`display_events_table()`.

All objectives stated in Section 4 were achieved.

---

## 13. Future Enhancements

| Enhancement | Description |
|-------------|-------------|
| Date range filter | Allow the user to filter events between two selected dates. |
| Export to CSV | Add a download button so the user can export the current filtered results. |
| Event detail view | Click a row to open a panel with full details about that incident. |
| Custom event entry | A form that lets the user manually add a new simulated event. |
| Severity trend alert | Show a warning card if High-severity events spike above a threshold. |
| Analyst notes | Let the user add a free-text note to any event (stored in JSON). |
| Dark/light mode toggle | Allow the user to switch themes without editing config.toml. |
| Auto-refresh | Periodically regenerate data to simulate a live feed (using st.empty + time.sleep). |

---

## 14. References

1. Streamlit Documentation. https://docs.streamlit.io
2. pandas Documentation. https://pandas.pydata.org/docs/
3. Plotly Express Documentation. https://plotly.com/python/plotly-express/
4. Python 3 Documentation. https://docs.python.org/3/
5. NIST Computer Security Resource Center — Security Event Definitions.
   https://csrc.nist.gov/glossary
6. SANS Institute — Introduction to Security Operations Centres.
   https://www.sans.org/
7. Python json module. https://docs.python.org/3/library/json.html
8. Streamlit session_state. https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
