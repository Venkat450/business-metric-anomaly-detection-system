"""Generate synthetic business metrics with injected anomalies."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def build_dataset(output_path: str = "data/raw/business_metrics.csv") -> None:
    rng = np.random.default_rng(7)
    ts = pd.date_range("2025-01-01", "2026-03-01", freq="H")

    metrics = {
        "website_traffic": {"base": 1500, "vol": 120},
        "orders": {"base": 320, "vol": 35},
        "revenue": {"base": 18000, "vol": 1800},
        "app_usage": {"base": 7800, "vol": 600},
    }

    rows = []
    for metric, cfg in metrics.items():
        for t in ts:
            daily = 1 + 0.12 * np.sin(2 * np.pi * (t.hour / 24))
            weekly = 1 + 0.08 * np.sin(2 * np.pi * (t.dayofweek / 7))
            value = cfg["base"] * daily * weekly + rng.normal(0, cfg["vol"])

            # Inject rare spikes and drops
            if rng.random() < 0.0025:
                value *= rng.uniform(1.8, 2.6)
            if rng.random() < 0.0020:
                value *= rng.uniform(0.35, 0.65)

            rows.append({
                "timestamp": t,
                "metric": metric,
                "value": max(float(value), 0.0),
            })

    df = pd.DataFrame(rows).sort_values(["metric", "timestamp"])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows at {output_path}")


if __name__ == "__main__":
    build_dataset()