# ▉ HEPHAESTUS — Financial Intelligence Terminal

A Bloomberg-style CLI dashboard that turns **any CSV** into actionable financial intelligence — powered by AI.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Rich](https://img.shields.io/badge/Rich-CLI-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini-cyan)

---

## Quick Start

```bash
# 1. Clone the repository and install the application
pip install -e .

# 2. Run Hephaestus from anywhere!
hephaestus
```

That's it. The interactive menu will guide you through importing data and launching the dashboard.

---

## How It Works

1. **Import any CSV** → The system auto-detects your columns (numeric, categorical, currency)
2. **Analyze** → It finds value/cost/loss columns and groups data by categories
3. **Visualize** → Bloomberg-style terminal with responsive charts
4. **AI Insights** → Gemini-powered CRO-level recommendations (optional)
5. **Persistent** → Your data is saved globally at `~/.hephaestus/revenue_leak.db`, so you can launch the terminal from any folder.

---

## Project Structure

```
Hephaestus/
├── setup.py            ← Installation package config
├── requirements.txt    ← Dependencies
├── hephaestus/         ← Core application package
│   ├── cli.py          ← Interactive CLI menu (entry point)
│   ├── main.py         ← Bloomberg terminal dashboard
│   ├── analyzer.py     ← Auto-detecting data analyzer
│   ├── ai_engine.py    ← Gemini AI integration
│   ├── import_data.py  ← Universal CSV importer
│   └── database.py     ← SQLite connection manager
└── sample data/
    └── Financials.csv  ← Example dataset
```

---

## AI Setup (Optional)

Create a `.env` file either in your current directory or globally at `~/.hephaestus/.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Without it, the dashboard still works with static insights.

---

## Commands

| Command | What it does |
|---|---|
| `hephaestus` | Interactive main menu (Launch terminal or Import data) |
| `python -m hephaestus.cli` | Alternative way to run the menu |

---

Built with [Rich](https://github.com/Textualize/rich) · [Plotext](https://github.com/piccolomo/plotext) · [Google Gemini](https://ai.google.dev/)