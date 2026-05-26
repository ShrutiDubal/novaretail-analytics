# Novaretail Analytics Command Center

**Portfolio project by [ShrutiDubal](https://github.com/ShrutiDubal)** — multi-platform retail analytics dashboard (Streamlit).

A consulting-style app for a fictional retail client (**Novaretail**): translate business questions into KPI definitions, build recurring reporting, run A/B test readouts, and document the data model for engineering handoff.

## What this demonstrates

| Skill area | Where it shows up |
|------------|-------------------|
| Business questions → analytics requirements | **Business requirements** tab |
| KPI definition & tracking | `data/kpi_definitions.csv` + scorecard |
| Dashboards & recurring reports | Executive summary, funnel charts |
| A/B testing & causal analysis | Experiment readouts with z-test + lift |
| SQL proficiency | Example warehouse SQL in KPI tab |
| Data modeling | MART layer diagram + ER model tab |

## Quick start (local)

```bash
cd novaretail-analytics
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

## Deploy to GitHub + Streamlit Cloud

### Step 1 — Create a GitHub repo

1. Go to [github.com/new](https://github.com/new)
2. Repository name: **`novaretail-analytics`**
3. Set to **Public** (required for free Streamlit Cloud)
4. Do **not** add README, `.gitignore`, or license
5. Click **Create repository**

### Step 2 — Push this project

```powershell
cd c:\Users\SHRUTI\Downloads\Shruti_Projects\novaretail-analytics
git branch -M main
git remote add origin https://github.com/ShrutiDubal/novaretail-analytics.git
git push -u origin main
```

If you already added a remote, update it:

```powershell
git remote set-url origin https://github.com/ShrutiDubal/novaretail-analytics.git
git push -u origin main
```

### Step 3 — Deploy on Streamlit Cloud

1. [share.streamlit.io](https://share.streamlit.io) → Sign in with GitHub
2. **New app** → repo: `ShrutiDubal/novaretail-analytics`
3. **Main file path:** `app.py`
4. **Deploy**

Live URL: `https://novaretail-analytics.streamlit.app`

## Suggested repo description (GitHub)

> Novaretail Analytics Command Center — Streamlit dashboard with KPI tracking, funnel analysis, A/B test readouts, and data modeling for a multi-platform retail client.

## Stack

- Python, pandas, SciPy
- Streamlit, Plotly
- Synthetic demo data (no API keys)

## Note

Uses **fictional Novaretail data** for demonstration purposes.
