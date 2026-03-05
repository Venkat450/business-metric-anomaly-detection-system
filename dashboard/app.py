"""Streamlit dashboard for business metric anomaly monitoring."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src import config

st.set_page_config(page_title="Business Metric Anomaly Monitor", layout="wide")
st.title("Real-Time Anomaly Detection for Business Metrics")

@st.cache_data
def load_results() -> pd.DataFrame:
    df = pd.read_csv(config.PROCESSED_PATH)
    df[config.TIMESTAMP_COL] = pd.to_datetime(df[config.TIMESTAMP_COL])
    return df

try:
    data = load_results()
except FileNotFoundError:
    st.warning("No processed results found. Run `python -m src.generate_sample_metrics` then `python -m src.pipeline`.")
    st.stop()

metric = st.selectbox("Metric", sorted(data[config.METRIC_COL].unique()))
subset = data[data[config.METRIC_COL] == metric].copy()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Rows", len(subset))
with c2:
    st.metric("Anomalies", int(subset["is_anomaly"].sum()))
with c3:
    rate = 100 * subset["is_anomaly"].mean()
    st.metric("Anomaly Rate", f"{rate:.2f}%")

fig = px.line(subset, x=config.TIMESTAMP_COL, y=config.VALUE_COL, title=f"{metric} time series")
anoms = subset[subset["is_anomaly"] == 1]
fig.add_scatter(
    x=anoms[config.TIMESTAMP_COL],
    y=anoms[config.VALUE_COL],
    mode="markers",
    marker=dict(color="red", size=7),
    name="Anomaly",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Latest Alerts")
latest = anoms.sort_values(config.TIMESTAMP_COL, ascending=False).head(25)
st.dataframe(latest[[config.TIMESTAMP_COL, config.METRIC_COL, config.VALUE_COL, "anomaly_votes", "iso_score"]])