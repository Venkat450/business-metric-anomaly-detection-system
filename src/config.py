"""Business metric anomaly detection configuration."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "business_metrics.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "anomaly_results.csv"
MODEL_PATH = BASE_DIR / "models" / "isolation_forest.joblib"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

TIMESTAMP_COL = "timestamp"
METRIC_COL = "metric"
VALUE_COL = "value"