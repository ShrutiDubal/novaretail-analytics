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

## Quick start

```bash
cd konrad_analytics_demo
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

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
