"""Anomaly detection methods: Isolation Forest, STL residual, and Z-score."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.seasonal import STL

from src import config


class MetricAnomalyDetector:
    def __init__(self, contamination: float = 0.015, random_state: int = 42) -> None:
        self.contamination = contamination
        self.random_state = random_state
        self.iso = IsolationForest(
            contamination=contamination,
            n_estimators=300,
            random_state=random_state,
        )

    @staticmethod
    def _add_time_features(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy().sort_values(config.TIMESTAMP_COL)
        t = pd.to_datetime(out[config.TIMESTAMP_COL])
        out["hour"] = t.dt.hour
        out["dayofweek"] = t.dt.dayofweek
        out["is_weekend"] = (out["dayofweek"] >= 5).astype(int)
        out["lag_1"] = out[config.VALUE_COL].shift(1).bfill()
        out["rolling_mean_24"] = out[config.VALUE_COL].rolling(24, min_periods=6).mean().bfill()
        out["rolling_std_24"] = out[config.VALUE_COL].rolling(24, min_periods=6).std().fillna(0.0)
        return out

    @staticmethod
    def _stl_anomaly_flags(values: pd.Series, period: int = 24, threshold: float = 3.0) -> pd.Series:
        stl = STL(values, period=period, robust=True)
        res = stl.fit()
        resid = res.resid
        z = (resid - resid.mean()) / (resid.std() + 1e-9)
        return (z.abs() > threshold).astype(int)

    @staticmethod
    def _zscore_flags(values: pd.Series, window: int = 24, threshold: float = 3.0) -> pd.Series:
        rolling_mean = values.rolling(window, min_periods=6).mean()
        rolling_std = values.rolling(window, min_periods=6).std().replace(0, np.nan)
        z = (values - rolling_mean) / rolling_std
        return (z.abs() > threshold).fillna(False).astype(int)

    def fit_predict_metric(self, metric_df: pd.DataFrame) -> pd.DataFrame:
        df = self._add_time_features(metric_df)
        feature_cols = ["value", "hour", "dayofweek", "is_weekend", "lag_1", "rolling_mean_24", "rolling_std_24"]

        x = df[feature_cols].values
        self.iso.fit(x)
        iso_preds = self.iso.predict(x)
        iso_scores = -self.iso.decision_function(x)

        df["iso_anomaly"] = (iso_preds == -1).astype(int)
        df["iso_score"] = iso_scores
        df["stl_anomaly"] = self._stl_anomaly_flags(df[config.VALUE_COL])
        df["z_anomaly"] = self._zscore_flags(df[config.VALUE_COL])
        df["anomaly_votes"] = df[["iso_anomaly", "stl_anomaly", "z_anomaly"]].sum(axis=1)
        df["is_anomaly"] = (df["anomaly_votes"] >= 2).astype(int)

        return df

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        outputs = []
        for metric, group in df.groupby(config.METRIC_COL):
            out = self.fit_predict_metric(group.copy())
            out[config.METRIC_COL] = metric
            outputs.append(out)

        return pd.concat(outputs).sort_values([config.METRIC_COL, config.TIMESTAMP_COL]).reset_index(drop=True)