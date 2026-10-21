# 🛡️ CyberShield — Security Event Analysis System

CyberShield is a beginner-level college project that simulates a
Security Operations Centre (SOC) dashboard.  It displays fictional security
events in a dark-themed, professional-looking web interface built entirely with
Python and Streamlit.  There is no real network monitoring, no database, and no
login — just clean, educational code you can read, modify, and learn from.

---

## ✨ Features

- **Overview Dashboard** — 4 live metric cards plus 3 interactive Plotly charts
  (donut, bar, and line) that update when you generate a new dataset.
- **Security Event Logs** — Full colour-coded table (red = High, amber = Medium,
  green = Low severity).
- **Event Search** — Search by event ID, IP address, or event type with optional
  Severity and Status filters that all work together.
- **Generate Dataset** — Creates a fresh batch of 24–30 random events and saves
  them so they survive a browser refresh.
- **About Project** — Plain-English explanation of each feature.

---

## 📁 Folder Structure

```
CyberShield/
├── app.py                    ← Entry point; run this file
├── data.py                   ← All shared data logic
├── utils.py                  ← Shared table-rendering helper
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
├── .streamlit/
│   └── config.toml           ← Dark navy theme
├── pages/
│   ├── overview.py           ← Page 1: Overview
│   ├── events.py             ← Page 2: Security Events
│   ├── search.py             ← Page 3: Event Search
│   └── about.py              ← Page 4: About Project
└── data/
    └── events.json           ← Auto-created when you generate events
```

---

## ⚙️ Requirements

| Item       | Minimum Version |
|------------|-----------------|
| Python     | 3.10            |
| streamlit  | 1.32.0          |
| pandas     | 2.0.0           |
| plotly     | 5.18.0          |

---

## 🚀 Installation

### Step 1 — Clone or download the project

If you downloaded a ZIP, unzip it and open a terminal inside the project folder.

### Step 2 — (Recommended) Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**  `venv\Scripts\activate`
- **Mac / Linux:**  `source venv/bin/activate`

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

You should see packages installing.  This takes about 30–60 seconds.

### Step 4 — Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL such as `http://localhost:8501`.
Open that URL in your browser.

---

## 🧪 How to Test Each Feature

### ✅ Test 1 — Default data loads

1. Open `http://localhost:8501` in your browser.
2. The **Overview** page opens automatically.
3. You should see 4 metric cards (Total Events = 24, etc.) and 3 charts.
4. If the cards show data → **PASS**.

### ✅ Test 2 — Generate Dataset (Overview page)

1. Stay on the Overview page.
2. Click the **⚡ Generate Dataset** button.
3. The metric cards and all 3 charts update immediately with new numbers.
4. If everything refreshes without a page error → **PASS**.

### ✅ Test 3 — Security Events page

1. Click **🚨 Security Events** in the left sidebar (or click **View Security Event Logs** on the Overview page).
2. You should see a table with columns: Event ID, Date and Time, IP Address, Event Type, Severity, Status.
3. Severity cells should be coloured (red/amber/green).
4. Click **⚡ Generate Dataset** — the table should reload with new events.
5. If the table shows and updates → **PASS**.

### ✅ Test 4 — Event Search by ID

1. Click **🔍 Event Search** in the sidebar.
2. Type `INC1004` in the search box and press **Enter**.
3. The result should show exactly **1 event** (INC1004).
4. If the count says "Showing 1 of …" → **PASS**.

### ✅ Test 5 — Search by IP address

1. Clear the search box (click **✖ Clear**).
2. Type `192.168.1.15` and press **Enter**.
3. You should see events whose IP is 192.168.1.15.
4. If at least 1 result appears → **PASS**.

### ✅ Test 6 — Search by event type

1. Clear, then type `failed login` (lowercase is fine) and press **Enter**.
2. All results should have Event Type = Failed Login.
3. If results appear and all are Failed Login → **PASS**.

### ✅ Test 7 — Combined filters

1. Clear, then type `malware` in the search box.
2. Set the **Severity** dropdown to **High**.
3. Only High-severity Malware Alert events should appear.
4. If the count drops and all remaining rows are correct → **PASS**.

### ✅ Test 8 — Clear button

1. Have some text in the search box and a filter selected.
2. Click **✖ Clear**.
3. The search box should empty and both dropdowns should return to **All**.
4. If everything resets → **PASS**.

### ✅ Test 9 — No results message

1. Type `zzznothing` in the search box.
2. You should see the message: *"No matching events found."*
3. If the message appears and no table is shown → **PASS**.

### ✅ Test 10 — About page

1. Click **ℹ️ About Project** in the sidebar.
2. You should see sections: Project Purpose, What is a Security Event?, Features, Technologies Used.
3. If the page renders without errors → **PASS**.

---

## 🛠️ Common Problems and Fixes

### ❌ "streamlit is not recognized" or "'streamlit' is not recognized as a command"

**Cause:** Streamlit is not installed or your virtual environment is not active.

**Fix:**
1. Make sure you ran `pip install -r requirements.txt`.
2. If using a virtual environment, make sure it is activated (`venv\Scripts\activate` on Windows).
3. Try `python -m streamlit run app.py` instead.

---

### ❌ "Port 8501 is already in use"

**Cause:** Another Streamlit app (or another run of this one) is already using that port.

**Fix:**
- Run on a different port: `streamlit run app.py --server.port 8502`
- Or stop the other process (check your Task Manager / Activity Monitor).

---

### ❌ "ModuleNotFoundError: No module named 'plotly'"

**Cause:** Plotly was not installed.

**Fix:** `pip install plotly`

---

### ❌ Charts / cards show nothing

**Cause:** The DataFrame might be empty.

**Fix:** Click **⚡ Generate Dataset** to create fresh data.

---

### ❌ Search doesn't update when I type

**Cause:** Streamlit reruns when you press **Enter** or change a widget.

**Fix:** Press **Enter** inside the search box after typing.

---

## 📝 Notes

- All data is **100% simulated**.  No real network is monitored.
- Events are stored in `data/events.json`.  Delete this file to reset to the built-in default dataset.
- The project is intentionally simple and well-commented so you can read and modify every line.
