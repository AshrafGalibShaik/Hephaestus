<p align="center">
  <br>
  <code>▉ H E P H A E S T U S ▉</code>
  <br><br>
  <em>Financial Intelligence Terminal</em>
  <br><br>
  <img src="https://img.shields.io/badge/Python-3.9+-1a1a2e?style=flat-square&logo=python&logoColor=f0a500" alt="Python">
  <img src="https://img.shields.io/badge/Terminal-Rich-1a1a2e?style=flat-square&logoColor=f0a500" alt="Rich">
  <img src="https://img.shields.io/badge/AI-Gemini%20%7C%20OpenAI-1a1a2e?style=flat-square&logo=google&logoColor=f0a500" alt="AI">
  <img src="https://img.shields.io/badge/PyPI-hephaestus--pro-1a1a2e?style=flat-square&logo=pypi&logoColor=f0a500" alt="PyPI">
</p>

---

A Bloomberg-style CLI dashboard that transforms **any CSV** into actionable financial intelligence.  
Import your data. Pick your AI model. Get revenue leak diagnostics. All from the terminal.

---
<img width="1516" height="500" alt="Hephaestus" src="https://github.com/user-attachments/assets/03adf6ba-87b9-4faa-9b2c-d77f47539d60" />

### Install

```
pip install hephaestus-pro
```

### Run

```
hephaestus
```

On first launch, a setup wizard walks you through:

```
────────────── FIRST-TIME SETUP ──────────────

  Select your AI model:

  ── Google Gemini ──
  1  │  Gemini 2.5 Flash
  2  │  Gemini 2.0 Flash
  3  │  Gemini 1.5 Flash

  ── OpenAI ──
  4  │  GPT-4o
  5  │  GPT-4o Mini
  6  │  GPT-3.5 Turbo

  MODEL (1): _
  GOOGLE_API_KEY: _

────────────── LOAD YOUR DATA ────────────────

  CSV files detected:
  1  │  sample data/Financials.csv  68KB
  SELECT (1): _
```

After setup, the Bloomberg terminal renders your financial data with AI-powered insights.

---

### What It Does

| Step | Description |
|:---|:---|
| **Setup** | First-run wizard asks for AI model and API key |
| **Import** | Feed any CSV — columns are auto-detected (numeric, categorical, currency) |
| **Analyze** | Engine identifies value, cost, loss columns and groups by categories |
| **Visualize** | Bloomberg-style terminal with responsive P&L charts |
| **Diagnose** | AI generates CRO-level revenue leak recommendations |

---

### Supported AI Models

| Provider | Models |
|:---|:---|
| Google Gemini | Gemini 2.5 Flash, 2.0 Flash, 1.5 Flash |
| OpenAI | GPT-4o, GPT-4o Mini, GPT-3.5 Turbo |

You can change your model anytime via the **Settings** menu.

---

### Structure

```
hephaestus/
├── cli.py          Interactive terminal menu + setup wizard
├── config.py       Persistent config manager (~/.hephaestus/)
├── main.py         Bloomberg dashboard renderer
├── analyzer.py     Auto-detecting universal data analyzer
├── ai_engine.py    Multi-provider AI engine (Gemini / OpenAI)
├── import_data.py  Universal CSV importer
└── database.py     SQLite connection manager
```

---

### Configuration

All config is stored at `~/.hephaestus/`:

| File | Purpose |
|:---|:---|
| `config.json` | AI model selection and API key |
| `revenue_leak.db` | Imported financial data |

---

### Development

```bash
git clone https://github.com/AshrafGalibShaik/Hephaestus.git
cd Hephaestus
pip install -e .
hephaestus
```

---

<p align="center">
  <sub>Built with <a href="https://github.com/Textualize/rich">Rich</a> · <a href="https://github.com/piccolomo/plotext">Plotext</a> · <a href="https://ai.google.dev/">Google Gemini</a> · <a href="https://openai.com/">OpenAI</a></sub>
</p>
