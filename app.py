"""
Novaretail Analytics Command Center — portfolio demo.

Translates business questions into KPI tracking, recurring reporting,
A/B test readouts, and governed metric definitions for a multi-platform retail client.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.analytics import (  # noqa: E402
    ab_test_result,
    add_derived_metrics,
    aggregate_kpis,
    build_experiment_summary,
    kpi_status,
)

st.set_page_config(
    page_title="Novaretail | Analytics Command Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = ROOT / "data"


@st.cache_data
def load_data():
    daily = pd.read_csv(DATA_DIR / "daily_metrics.csv", parse_dates=["date"])
    kpis = pd.read_csv(DATA_DIR / "kpi_definitions.csv")
    experiments = pd.read_csv(DATA_DIR / "ab_experiments.csv")
    return daily, kpis, experiments


def inject_styles():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

:root {
    --bg: #0f1419;
    --panel: #1a2332;
    --panel-2: #243044;
    --text: #e8edf4;
    --muted: #8b9cb3;
    --accent: #3d8bfd;
    --accent-2: #00c2a8;
    --warn: #f0b429;
    --bad: #f56565;
    --good: #48bb78;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #0b0f14 0%, #121a24 45%, #0f1419 100%);
}

[data-testid="stSidebar"] {
    background: #121a24;
    border-right: 1px solid #2a3548;
}

h1, h2, h3, p, label, .stMarkdown {
    color: var(--text);
}

.hero {
    background: linear-gradient(120deg, #1a2a44 0%, #1e3a5f 50%, #163d4a 100%);
    border: 1px solid #2f4568;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0 0 0.35rem 0;
    font-size: 1.75rem;
}

.hero p {
    color: var(--muted);
    margin: 0;
    font-size: 0.95rem;
}

.tag {
    display: inline-block;
    background: #243044;
    color: #9ec5ff;
    border: 1px solid #3d5a80;
    border-radius: 999px;
    padding: 0.15rem 0.65rem;
    font-size: 0.75rem;
    margin-right: 0.35rem;
}

[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid #2a3548;
    border-radius: 12px;
    padding: 0.75rem 1rem;
}

[data-testid="stMetricValue"] {
    color: var(--accent-2);
    font-size: 1.6rem;
}

.insight-card {
    background: var(--panel);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
}

.insight-card strong { color: #9ec5ff; }
</style>
        """,
        unsafe_allow_html=True,
    )


def hero():
    st.markdown(
        """
<div class="hero">
  <span class="tag">Consulting analytics prototype</span>
  <span class="tag">Python · SQL · KPI governance · A/B testing</span>
  <h1>Novaretail — Client Analytics Command Center</h1>
  <p>Sample engagement deliverable: business questions → metric definitions → dashboards → experiment readouts.
  Built by Shruti Dubal — product & consulting analytics portfolio.</p>
</div>
        """,
        unsafe_allow_html=True,
    )


def filter_data(daily: pd.DataFrame) -> pd.DataFrame:
    platforms = st.sidebar.multiselect(
        "Platform",
        options=sorted(daily["platform"].unique()),
        default=sorted(daily["platform"].unique()),
    )
    min_date, max_date = daily["date"].min(), daily["date"].max()
    date_range = st.sidebar.slider(
        "Date range",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=(max_date.date() - pd.Timedelta(days=89), max_date.date()),
    )
    mask = (
        daily["platform"].isin(platforms)
        & (daily["date"].dt.date >= date_range[0])
        & (daily["date"].dt.date <= date_range[1])
    )
    return daily.loc[mask].copy()


def page_executive(daily: pd.DataFrame, kpis: pd.DataFrame, experiments: pd.DataFrame):
    st.subheader("Executive summary")
    kpis_now = aggregate_kpis(daily, days=28)
    prev = aggregate_kpis(
        daily[daily["date"] < daily["date"].max() - pd.Timedelta(days=28)],
        days=28,
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("WAU (avg daily)", f"{kpis_now['wau']:,.0f}", f"{kpis_now['wau'] - prev['wau']:+,.0f}")
    c2.metric("Signup CVR", f"{kpis_now['signup_cvr']:.2%}", f"{(kpis_now['signup_cvr']-prev['signup_cvr'])*100:+.2f} pts")
    c3.metric("Checkout CVR", f"{kpis_now['checkout_cvr']:.2%}", f"{(kpis_now['checkout_cvr']-prev['checkout_cvr'])*100:+.2f} pts")
    c4.metric("AOV", f"${kpis_now['aov']:.2f}", f"{kpis_now['aov']-prev['aov']:+.2f}")
    c5.metric("Crash-free", f"{kpis_now['crash_free_rate']:.2%}", f"{(kpis_now['crash_free_rate']-prev['crash_free_rate'])*100:+.2f} pts")
    c6.metric("28d GMV", f"${kpis_now['gmv']:,.0f}", "")

    daily_agg = (
        daily.groupby("date", as_index=False)[
            ["gmv_usd", "active_users", "completed_orders", "checkout_starts"]
        ]
        .sum()
    )
    daily_agg["checkout_cvr"] = daily_agg["completed_orders"] / daily_agg["checkout_starts"]

    left, right = st.columns(2)
    with left:
        fig = px.area(
            daily_agg,
            x="date",
            y="gmv_usd",
            title="Gross merchandise value trend",
            template="plotly_dark",
            color_discrete_sequence=["#3d8bfd"],
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=320)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig2 = px.line(
            daily_agg,
            x="date",
            y="checkout_cvr",
            title="Checkout completion rate",
            template="plotly_dark",
            color_discrete_sequence=["#00c2a8"],
        )
        fig2.update_yaxes(tickformat=".1%")
        fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=320)
        st.plotly_chart(fig2, use_container_width=True)

    exp_summary = build_experiment_summary(experiments)
    st.markdown("#### Analyst recommendations")
    exp_row = exp_summary.loc[exp_summary["experiment_id"] == "EXP-2026-01"]
    p_val = exp_row["p_value"].iloc[0] if len(exp_row) else 0.0
    lift = exp_row["relative_lift_pct"].iloc[0] if len(exp_row) else 0.0
    insights = [
        (
            "Checkout CVR is trending up (+1.2 pts vs prior 28d) driven by iOS/Android; "
            "web still lags — recommend a focused funnel diagnostic."
        ),
        (
            f"Experiment **One-tap checkout CTA** showed **{lift:+.1f}% relative lift** "
            f"(p={p_val:.3f}) — ship to 100%."
        ),
        (
            "Support ticket rate improved to 6.1 per 1k MAU (target 7.0) — validate with CS "
            "that deflection from in-app help is not masking unresolved issues."
        ),
    ]
    for text in insights:
        st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)

    st.markdown("#### KPI scorecard vs targets")
    score_rows = []
    for _, row in kpis.iterrows():
        key_map = {
            "KPI-001": "wau",
            "KPI-002": "signup_cvr",
            "KPI-004": "checkout_cvr",
            "KPI-005": "aov",
            "KPI-006": "crash_free_rate",
            "KPI-007": "ticket_rate",
        }
        key = key_map.get(row["kpi_id"])
        if not key:
            continue
        actual = kpis_now[key]
        score_rows.append(
            {
                "KPI": row["kpi_name"],
                "Actual": actual,
                "Target": row["target_value"],
                "Status": kpi_status(actual, row["target_value"], row["target_direction"]),
            }
        )
    st.dataframe(pd.DataFrame(score_rows), use_container_width=True, hide_index=True)


def page_kpi_dictionary(kpis: pd.DataFrame):
    st.subheader("KPI dictionary & governance")
    st.caption("Documents metric definitions, owners, and refresh cadence — core BA deliverable on consulting engagements.")

    search = st.text_input("Search KPIs", placeholder="e.g. retention, conversion, crash")
    view = kpis.copy()
    if search:
        mask = view.apply(lambda r: search.lower() in " ".join(r.astype(str)).lower(), axis=1)
        view = view[mask]

    st.dataframe(
        view[
            [
                "kpi_id",
                "kpi_name",
                "category",
                "definition",
                "formula",
                "owner",
                "refresh_cadence",
                "baseline_value",
                "target_value",
                "unit",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Example SQL — recurring executive report")
    st.code(
        """
-- Weekly executive KPI rollup (warehouse layer: analytics.mart_daily_platform)
SELECT
    DATE_TRUNC('week', event_date) AS report_week,
    platform,
    SUM(gmv_usd) AS gmv,
    SUM(completed_orders)::FLOAT / NULLIF(SUM(checkout_starts), 0) AS checkout_cvr,
    SUM(signups)::FLOAT / NULLIF(SUM(landing_visitors), 0) AS signup_cvr,
    1 - SUM(crash_sessions)::FLOAT / NULLIF(SUM(total_sessions), 0) AS crash_free_rate
FROM analytics.mart_daily_platform
WHERE event_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY 1, 2
ORDER BY 1 DESC, 2;
        """.strip(),
        language="sql",
    )


def page_funnel(daily: pd.DataFrame):
    st.subheader("Acquisition → revenue funnel")
    totals = daily.sum(numeric_only=True)
    stages = ["Landing visitors", "Signups", "Active users", "Checkout starts", "Completed orders"]
    values = [
        totals["landing_visitors"],
        totals["signups"],
        totals["active_users"],
        totals["checkout_starts"],
        totals["completed_orders"],
    ]
    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker={"color": ["#3d8bfd", "#5b9dff", "#00c2a8", "#48bb78", "#9ae6b4"]},
        )
    )
    fig.update_layout(template="plotly_dark", height=420, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

    by_platform = daily.groupby("platform", as_index=False).agg(
        landing_visitors=("landing_visitors", "sum"),
        signups=("signups", "sum"),
        checkout_starts=("checkout_starts", "sum"),
        completed_orders=("completed_orders", "sum"),
        gmv_usd=("gmv_usd", "sum"),
    )
    by_platform["signup_cvr"] = by_platform["signups"] / by_platform["landing_visitors"]
    by_platform["checkout_cvr"] = by_platform["completed_orders"] / by_platform["checkout_starts"]

    st.dataframe(
        by_platform.assign(
            signup_cvr=lambda d: (d["signup_cvr"] * 100).round(2).astype(str) + "%",
            checkout_cvr=lambda d: (d["checkout_cvr"] * 100).round(2).astype(str) + "%",
            gmv_usd=lambda d: d["gmv_usd"].map("${:,.0f}".format),
        )[
            [
                "platform",
                "landing_visitors",
                "signups",
                "signup_cvr",
                "checkout_starts",
                "completed_orders",
                "checkout_cvr",
                "gmv_usd",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


def page_experiments(experiments: pd.DataFrame):
    st.subheader("A/B testing & causal readouts")
    summary = build_experiment_summary(experiments)
    st.dataframe(summary, use_container_width=True, hide_index=True)

    exp_pick = st.selectbox(
        "Deep-dive experiment",
        experiments["experiment_id"].unique(),
        format_func=lambda x: experiments.loc[
            experiments["experiment_id"] == x, "experiment_name"
        ].iloc[0],
    )
    subset = experiments[experiments["experiment_id"] == exp_pick]
    control = subset[subset["variant"] == "control"].iloc[0]
    treatment = subset[subset["variant"] != "control"].iloc[0]

    result = ab_test_result(
        int(control["completed_orders"]),
        int(control["checkout_starts"]),
        int(treatment["completed_orders"]),
        int(treatment["checkout_starts"]),
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Control rate", f"{result['control_rate']:.2%}")
    m2.metric("Treatment rate", f"{result['treatment_rate']:.2%}")
    m3.metric("Relative lift", f"{result['relative_lift_pct']:+.2f}%")
    m4.metric("p-value", f"{result['p_value']:.4f}")

    st.info(
        f"**Recommendation:** {result['recommendation']} "
        f"({'statistically significant at 95%' if result['significant_95'] else 'not yet significant'})"
    )

    chart_df = subset.assign(
        rate=subset["completed_orders"] / subset["checkout_starts"],
    )
    fig = px.bar(
        chart_df,
        x="variant",
        y="rate",
        color="variant",
        title="Primary metric: checkout completion rate",
        text=chart_df["rate"].map(lambda v: f"{v:.1%}"),
        template="plotly_dark",
        color_discrete_sequence=["#8b9cb3", "#00c2a8"],
    )
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=40, b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Causal analysis note")
    st.write(
        "For production readouts I pair frequentist tests with guardrail metrics (crash rate, support tickets) "
        "and segment checks (platform, new vs returning). If assignment is clustered, I switch to "
        "cluster-robust SEs or Bayesian partial pooling for low-traffic cells."
    )


def page_data_model():
    st.subheader("Logical data model")
    st.caption("How source events roll up to reporting-ready marts — typical handoff with data engineering.")

    st.markdown(
        """
```mermaid
erDiagram
    RAW_EVENTS ||--o{ STG_EVENTS : cleanses
    STG_EVENTS ||--o{ DIM_USER : keys
    STG_EVENTS ||--o{ FACT_SESSIONS : aggregates
    FACT_SESSIONS ||--o{ MART_DAILY_PLATFORM : rolls_up
    FACT_ORDERS ||--o{ MART_DAILY_PLATFORM : joins
    MART_DAILY_PLATFORM ||--o{ KPI_SCORECARD : metrics
    MART_DAILY_PLATFORM ||--o{ EXP_ASSIGNMENTS : experiment_join
```
        """
    )

    st.markdown(
        """
| Layer | Table | Grain | Purpose |
|-------|--------|-------|---------|
| Raw | `raw.mobile_events` | event | Clickstream from iOS/Android SDK |
| Staging | `stg.events` | event | Typed columns, bot filtering, PII hashing |
| Mart | `mart.daily_platform` | date × platform | KPI dashboards & exec reporting |
| Mart | `mart.experiment_assignments` | user × experiment | A/B analysis joins |
| Semantic | `kpi.definitions` | kpi_id | Governed definitions & owners |
        """
    )


def page_requirements():
    st.subheader("Business question → analytics requirements")
    st.caption("Mirrors discovery workshops with client stakeholders.")

    questions = pd.DataFrame(
        [
            {
                "Business question": "Are we on track for Q1 revenue?",
                "Analytical requirement": "Weekly GMV, checkout CVR, AOV by platform with 28d rolling baseline",
                "Deliverable": "Executive dashboard + KPI scorecard",
                "Priority": "P0",
            },
            {
                "Business question": "Did the checkout CTA test win?",
                "Analytical requirement": "Randomized experiment analysis on checkout completion; guardrail on crash rate",
                "Deliverable": "Experiment readout memo + ship/no-ship recommendation",
                "Priority": "P0",
            },
            {
                "Business question": "Why is web conversion lagging mobile?",
                "Analytical requirement": "Funnel drop-off by step, device, and traffic source",
                "Deliverable": "Diagnostic deck + backlog for product",
                "Priority": "P1",
            },
            {
                "Business question": "Can we trust the numbers?",
                "Analytical requirement": "DQ checks: null keys, duplicate sessions, late-arriving events",
                "Deliverable": "Data quality monitor in reporting layer",
                "Priority": "P1",
            },
        ]
    )
    st.dataframe(questions, use_container_width=True, hide_index=True)


def main():
    inject_styles()
    daily_raw, kpis, experiments = load_data()
    daily = add_derived_metrics(daily_raw)

    hero()
    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Section",
        [
            "Executive summary",
            "Business requirements",
            "KPI dictionary",
            "Funnel & platforms",
            "A/B experiments",
            "Data model",
        ],
        label_visibility="collapsed",
    )

    filtered = filter_data(daily)

    if page == "Executive summary":
        page_executive(filtered, kpis, experiments)
    elif page == "Business requirements":
        page_requirements()
    elif page == "KPI dictionary":
        page_kpi_dictionary(kpis)
    elif page == "Funnel & platforms":
        page_funnel(filtered)
    elif page == "A/B experiments":
        page_experiments(experiments)
    else:
        page_data_model()

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Deploy for recruiters**\n\n"
        "1. `pip install -r requirements.txt`\n"
        "2. `streamlit run app.py`\n"
        "3. Share via [Streamlit Community Cloud](https://share.streamlit.io) or export PDF (browser Print → Save as PDF)"
    )


if __name__ == "__main__":
    main()
