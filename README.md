```
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║  ██╗  ██╗███████╗██████╗ ██╗  ██╗ █████╗ ███████╗███████╗████████╗██╗   ██╗███████╗     ║
║  ██║  ██║██╔════╝██╔══██╗██║  ██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔════╝     ║
║  ███████║█████╗  ██████╔╝███████║███████║█████╗  ███████╗   ██║   ██║   ██║███████╗     ║
║  ██╔══██║██╔══╝  ██╔═══╝ ██╔══██║██╔══██║██╔══╝  ╚════██║   ██║   ██║   ██║╚════██║     ║
║  ██║  ██║███████╗██║     ██║  ██║██║  ██║███████╗███████║   ██║   ╚██████╔╝███████║     ║
║  ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝     ║
╠═══════════════════════════════════════════════════════════════════════════════════════════╣
║  ▸ FINANCIAL INTELLIGENCE TERMINAL  ▸ v1.0.0  ▸ SYSTEM: ARMED & OPERATIONAL             ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
```

> **"Every dollar leaking through your funnel is a dollar funding your competitor."**

---

## ▸ SITUATION REPORT

```
ASSET CLASS  : Customer Conversion Intelligence
RISK LEVEL   : CRITICAL — Revenue hemorrhage detected
UPTIME REQ   : 24/7 terminal access
AI ENGINE    : Gemini 2.5 Flash (real-time analysis)
DATA LAYER   : SQLite / Pandas
STATUS       : ████████████████████ LIVE
```

**HEPHAESTUS** is a high-intensity, Wall Street–grade CLI terminal that dissects your customer behavior pipeline, exposes conversion failures in real time, and deploys AI-driven strike recommendations — all rendered in a fire-breathing terminal interface built with `rich` and `plotext`.

No dashboards. No browsers. No fluff. **Pure signal.**

---

## ▸ INTELLIGENCE MODULES

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MODULE                   │  FUNCTION                         │  STATUS     │
├───────────────────────────┼───────────────────────────────────┼─────────────┤
│  FUNNEL ANALYZER          │  Drop-off detection & stage maps  │  ● ACTIVE   │
│  ROI TRACKER              │  Channel P&L — red/green signals  │  ● ACTIVE   │
│  AI STRIKE ENGINE         │  Gemini-powered CRO directives    │  ● ACTIVE   │
│  IMPACT ALERTS            │  Monthly recovery $ quantified    │  ● ACTIVE   │
└───────────────────────────┴───────────────────────────────────┴─────────────┘
```

**Funnel Drop-off Analysis** — Horizontal bar charts render stage-by-stage user attrition. The moment your pipeline starts bleeding, you see it in ticks.

**Marketing ROI Tracking** — Color-coded P&L bars per channel. Green means go. Red means cut. No ambiguity.

**AI Recommendations** — Gemini reads the numbers and issues targeted CRO directives. Not generic. Not fluffy. Actionable intelligence.

**Financial Impact Alerts** — The terminal surfaces your single highest-leverage fix and attaches a dollar figure to the inaction. Every. Single. Run.

---

## ▸ SYSTEM ARCHITECTURE

```
hephaestus/
│
├── app/
│   ├── main.py          ◀  Terminal UI  ·  Rich + Plotext
│   ├── analyzer.py      ◀  DB pipeline  ·  Pandas DataFrames
│   ├── ai_engine.py     ◀  LLM bridge   ·  Gemini 2.5 Flash
│   └── database.py      ◀  Conn layer   ·  SQLite utilities
│
├── data/
│   ├── revenue_leak.db  ◀  Operational database
│   └── schema.sql       ◀  Table definitions
│
├── data_generator.py    ◀  Seed script  ·  Mock data generation
├── requirements.txt     ◀  Dependency manifest
├── .env                 ◀  SECRETS — keep dark, keep safe
└── README.md            ◀  You are here
```

---

## ▸ DEPLOYMENT SEQUENCE

### STEP 01 — PREREQUISITES

```
REQUIRED    Python 3.9+
CONFIRMED   pip, venv
```

### STEP 02 — ESTABLISH POSITION

```bash
# Isolate your environment — no contamination
python -m venv venv

# Engage
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Load the arsenal
pip install -r requirements.txt
```

### STEP 03 — CREDENTIALS

Create `.env` in root. This file does not leave your machine.

```env
GEMINI_API_KEY=your_actual_api_key_here
```

> ⚠ `.env` is git-ignored by default. **Do not commit your key. Ever.**

### STEP 04 — SEED THE DATABASE

Only required on first run. Seeds mock transactional data into `revenue_leak.db`.

```bash
python data_generator.py
```

```
▸ Generating customer journey records   [████████████████████] 100%
▸ Seeding marketing channel data        [████████████████████] 100%
▸ Database armed. Ready for analysis.
```

### STEP 05 — IGNITION

```bash
python app/main.py
```

The terminal initializes. The bleeding stops here.

---

## ▸ TECH STACK

```
┌─────────────────┬────────────────────────────────────────────┐
│  LAYER          │  TECHNOLOGY                                │
├─────────────────┼────────────────────────────────────────────┤
│  Terminal UI    │  Rich · Plotext                            │
│  Data Engine    │  Pandas · NumPy · SQLite                   │
│  AI Layer       │  Google Generative AI — gemini-2.5-flash   │
│  Runtime        │  Python 3.9+                               │
└─────────────────┴────────────────────────────────────────────┘
```

---

## ▸ RISK DISCLOSURE

```
╔══════════════════════════════════════════════════════════════╗
║  ⚡  THIS SYSTEM WILL SURFACE UNCOMFORTABLE TRUTHS.          ║
║  ⚡  REVENUE LEAKS SHOWN ARE REAL (EVEN IN MOCK DATA).       ║
║  ⚡  AI OUTPUT IS ADVISORY — HUMAN JUDGMENT REQUIRED.        ║
╚══════════════════════════════════════════════════════════════╝
```

---

```
▸ HEPHAESTUS FINANCIAL TERMINAL  ·  POSITION: LONG ON DATA, SHORT ON EXCUSES
████████████████████████████████████████████████████████████████████████  END
```