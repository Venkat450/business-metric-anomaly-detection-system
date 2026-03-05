"""Batch pipeline to run anomaly detection and persist outputs."""

from __future__ import annotations

import argparse

import joblib
import pandas as pd

from src import config
from src.detectors import MetricAnomalyDetector


def run_pipeline(input_path: str | None = None, output_path: str | None = None) -> None:
    input_csv = input_path or str(config.RAW_DATA_PATH)
    output_csv = output_path or str(config.PROCESSED_PATH)

    df = pd.read_csv(input_csv)
    df[config.TIMESTAMP_COL] = pd.to_datetime(df[config.TIMESTAMP_COL])

    detector = MetricAnomalyDetector()
    results = detector.run(df)

    results.to_csv(output_csv, index=False)
    joblib.dump(detector, config.MODEL_PATH)

    anomaly_count = int(results["is_anomaly"].sum())
    print(f"Saved {len(results)} rows to {output_csv}")
    print(f"Detected anomalies: {anomaly_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run anomaly detection batch pipeline")
    parser.add_argument("--input", default=None, help="Input CSV path")
    parser.add_argument("--output", default=None, help="Output CSV path")
    args = parser.parse_args()

    run_pipeline(args.input, args.output)