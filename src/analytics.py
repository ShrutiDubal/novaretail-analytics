"""Core analytics helpers for the Konrad-style consulting demo."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"])
    out["signup_cvr"] = out["signups"] / out["landing_visitors"].replace(0, np.nan)
    out["checkout_cvr"] = out["completed_orders"] / out["checkout_starts"].replace(0, np.nan)
    out["aov"] = out["gmv_usd"] / out["completed_orders"].replace(0, np.nan)
    out["crash_free_rate"] = 1 - (out["crash_sessions"] / out["total_sessions"].replace(0, np.nan))
    return out


def aggregate_kpis(df: pd.DataFrame, days: int = 28) -> dict[str, float]:
    recent = df.sort_values("date").tail(days)
    totals = recent.sum(numeric_only=True)
    wau = recent.groupby("date")["active_users"].sum().mean()
    signup_cvr = totals["signups"] / totals["landing_visitors"]
    checkout_cvr = totals["completed_orders"] / totals["checkout_starts"]
    aov = totals["gmv_usd"] / totals["completed_orders"]
    crash_free = 1 - (totals["crash_sessions"] / totals["total_sessions"])
    ticket_rate = (totals["support_tickets"] / totals["active_users"]) * 1000
    return {
        "wau": round(wau, 0),
        "signup_cvr": round(signup_cvr, 4),
        "checkout_cvr": round(checkout_cvr, 4),
        "aov": round(aov, 2),
        "crash_free_rate": round(crash_free, 4),
        "ticket_rate": round(ticket_rate, 2),
        "gmv": round(totals["gmv_usd"], 0),
    }


def kpi_status(actual: float, target: float, direction: str) -> str:
    if direction == "higher":
        if actual >= target:
            return "On track"
        if actual >= target * 0.95:
            return "Watch"
        return "Below target"
    if actual <= target:
        return "On track"
    if actual <= target * 1.05:
        return "Watch"
    return "Above target"


def ab_test_result(
    control_successes: int,
    control_trials: int,
    treatment_successes: int,
    treatment_trials: int,
) -> dict[str, float | str | bool]:
    p_c = control_successes / control_trials
    p_t = treatment_successes / treatment_trials
    lift = (p_t - p_c) / p_c if p_c else 0.0

    # Two-proportion z-test
    pooled = (control_successes + treatment_successes) / (control_trials + treatment_trials)
    se = np.sqrt(pooled * (1 - pooled) * (1 / control_trials + 1 / treatment_trials))
    z = (p_t - p_c) / se if se else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        "control_rate": round(p_c, 4),
        "treatment_rate": round(p_t, 4),
        "absolute_lift": round(p_t - p_c, 4),
        "relative_lift_pct": round(lift * 100, 2),
        "p_value": round(p_value, 4),
        "significant_95": p_value < 0.05,
        "recommendation": "Ship" if p_value < 0.05 and lift > 0 else "Continue test",
    }


def build_experiment_summary(experiments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for exp_id, group in experiments.groupby("experiment_id"):
        control = group[group["variant"] == "control"].iloc[0]
        treatment = group[group["variant"] != "control"].iloc[0]
        result = ab_test_result(
            int(control["completed_orders"]),
            int(control["checkout_starts"]),
            int(treatment["completed_orders"]),
            int(treatment["checkout_starts"]),
        )
        rows.append(
            {
                "experiment_id": exp_id,
                "experiment_name": control["experiment_name"],
                "status": control["status"],
                "platform": control["platform"],
                "control_rate": result["control_rate"],
                "treatment_rate": result["treatment_rate"],
                "relative_lift_pct": result["relative_lift_pct"],
                "p_value": result["p_value"],
                "significant_95": result["significant_95"],
                "recommendation": result["recommendation"],
            }
        )
    return pd.DataFrame(rows)
