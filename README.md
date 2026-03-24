# ▉ HEPHAESTUS — Financial Intelligence Terminal

A Bloomberg-style CLI dashboard that turns **any CSV** into actionable financial intelligence — powered by AI.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Rich](https://img.shields.io/badge/Rich-CLI-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini-cyan)

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Hephaestus
python run.py
```

That's it. The interactive menu will guide you through importing data and launching the dashboard.

---

## How It Works

1. **Import any CSV** → The system auto-detects your columns (numeric, categorical, currency)
2. **Analyze** → It finds value/cost/loss columns and groups data by categories
3. **Visualize** → Bloomberg-style terminal with responsive charts
4. **AI Insights** → Gemini-powered CRO-level recommendations (optional)

---

## Project Structure

```
Hephaestus/
├── run.py              ← Single entry point (start here)
├── import_data.py      ← Universal CSV importer
├── requirements.txt    ← Dependencies
├── .env                ← API key (optional, create yourself)
├── app/
│   ├── main.py         ← Bloomberg terminal dashboard
│   ├── analyzer.py     ← Auto-detecting data analyzer
│   ├── ai_engine.py    ← Gemini AI integration
│   └── database.py     ← SQLite connection manager
├── data/
│   └── revenue_leak.db ← Auto-generated database
└── sample data/
    └── Financials.csv  ← Example dataset
```

---

## AI Setup (Optional)

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Without it, the dashboard still works with static insights.

---

## Commands

| Command | What it does |
|---|---|
| `python run.py` | Interactive menu (recommended) |
| `python import_data.py "path/to/file.csv"` | Direct CSV import |
| `python app/main.py` | Launch dashboard directly |

---

Built with [Rich](https://github.com/Textualize/rich) · [Plotext](https://github.com/piccolomo/plotext) · [Google Gemini](https://ai.google.dev/)