<p align="center">
  <br>
  <code>▉ H E P H A E S T U S ▉</code>
  <br><br>
  <em>Financial Intelligence Terminal</em>
  <br><br>
  <img src="https://img.shields.io/badge/Python-3.11+-1a1a2e?style=flat-square&logo=python&logoColor=f0a500" alt="Python">
  <img src="https://img.shields.io/badge/Terminal-Rich-1a1a2e?style=flat-square&logoColor=f0a500" alt="Rich">
  <img src="https://img.shields.io/badge/AI-Gemini-1a1a2e?style=flat-square&logo=google&logoColor=f0a500" alt="Gemini">
</p>

---

A Bloomberg-style CLI dashboard that transforms **any CSV** into actionable financial intelligence.  
Import your data. Get AI-powered revenue leak diagnostics. All from the terminal.

---

### Install

```
pip install -e .
```

### Run

```
hephaestus
```

That's it. The interactive menu handles everything.

---

### What It Does

| Step | Description |
|:---|:---|
| **Import** | Feed any CSV — columns are auto-detected (numeric, categorical, currency) |
| **Analyze** | Engine identifies value, cost, loss columns and groups by categories |
| **Visualize** | Bloomberg-style terminal with responsive P&L charts |
| **Diagnose** | Gemini AI generates CRO-level revenue leak recommendations |

---

### Structure

```
hephaestus/
├── cli.py          Entry point — interactive terminal menu
├── main.py         Bloomberg dashboard renderer
├── analyzer.py     Auto-detecting universal data analyzer
├── ai_engine.py    Gemini AI integration
├── import_data.py  Universal CSV importer
└── database.py     SQLite connection manager
```

---

### AI Configuration

Place a `.env` file in the `hephaestus/` directory, your working directory, or `~/.hephaestus/`:

```
GOOGLE_API_KEY=your_key
```

The dashboard renders with or without AI — static insights are generated as fallback.

---

### Commands

| Command | Description |
|:---|:---|
| `hephaestus` | Launch the interactive terminal |
| `python -m hephaestus.cli` | Alternative entry point |

---

<p align="center">
  <sub>Built with <a href="https://github.com/Textualize/rich">Rich</a> · <a href="https://github.com/piccolomo/plotext">Plotext</a> · <a href="https://ai.google.dev/">Google Gemini</a></sub>
</p>