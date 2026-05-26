# NovaRetail Analytics Command Center

**Portfolio prototype for Konrad — Data Analyst (Entry Level, NYC, Hybrid)**

A consulting-style Streamlit app that mirrors what you'd deliver on a Konrad client engagement: translate business questions into KPI definitions, build recurring reporting, run A/B test readouts, and document the data model for engineering handoff.

## What this demonstrates (mapped to the job posting)

| Konrad requirement | Where it shows up in this project |
|--------------------|----------------------------------|
| Translate business questions → analytical requirements | **Business requirements** tab |
| KPI definition & tracking | `data/kpi_definitions.csv` + scorecard |
| Dashboards & recurring reports | Executive summary, funnel charts |
| A/B testing & causal analysis | Experiment readouts with z-test + lift |
| SQL proficiency | Example warehouse SQL in KPI tab |
| Data modeling | MART layer diagram + ER model tab |
| Cross-functional consulting delivery | README + one-page narrative for PDF |

## Quick start (local)

```bash
cd konrad_analytics_demo
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

## Deploy to GitHub + Streamlit Cloud

### Step 1 — Create a GitHub repo

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `konrad-analytics-demo` (or any name)
3. Set to **Public** (required for free Streamlit Cloud)
4. Do **not** add README, `.gitignore`, or license (this folder already has them)
5. Click **Create repository**

### Step 2 — Push this project

In PowerShell (replace `YOUR_USERNAME` with your GitHub username):

```powershell
cd c:\Users\SHRUTI\Downloads\Shruti_Projects\konrad_analytics_demo
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/konrad-analytics-demo.git
git push -u origin main
```

Sign in when GitHub prompts you (browser or token).

> First time using git on this PC? Set your name once (only you should run this):
> `git config --global user.name "Your Name"`
> `git config --global user.email "your-email@example.com"`

### Step 3 — Deploy on Streamlit Cloud (live link)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with **GitHub**
3. Click **New app**
4. Pick your repo `konrad-analytics-demo`
5. **Main file path:** `app.py`
6. Click **Deploy**

You’ll get a public URL like `https://konrad-analytics-demo.streamlit.app` — put that in your Konrad application.

## Share with Konrad (3 options)

### Option A — Live link (best)
1. Push this folder to a **public GitHub repo**
2. Deploy free on [Streamlit Community Cloud](https://share.streamlit.io) → New app → point to `app.py`
3. Put the URL in your application / LinkedIn message

### Option B — PDF one-pager
1. Run the app locally
2. Screenshot Executive summary + A/B experiments + KPI dictionary
3. Paste into a 1-page PDF with 2–3 bullet "impact" lines (template below)

### Option C — GitHub only
Link the repo in your cover letter; recruiters often click through.

## Suggested cover-letter bullets

- Built an end-to-end analytics prototype (Python/Streamlit) modeling a multi-platform retail client: KPI governance, executive dashboards, funnel diagnostics, and A/B test readouts with statistical significance.
- Documented metric definitions, SQL reporting patterns, and a logical data model to show how I partner with data engineering on analytics layers.

## Stack

- Python, pandas, SciPy (proportion z-test)
- Streamlit, Plotly
- Synthetic but realistic CSV data (no API keys required)

## Note

This uses **fictional client data** ("NovaRetail") for demonstration. Replace with your name/branding as needed.
