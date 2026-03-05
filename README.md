# Business Metric Anomaly Detection System

Unsupervised anomaly detection for operational business metrics using ensemble detectors.

## Tech Stack
- Python
- Isolation Forest
- STL decomposition
- Z-score detection
- Streamlit
- PySpark
- Airflow (optional)

## Metrics Supported
- website traffic
- orders
- revenue
- app usage

## Project Structure
- `src/generate_sample_metrics.py`: synthetic metric generator with injected spikes/drops
- `src/detectors.py`: Isolation Forest + STL + Z-score ensemble
- `src/pipeline.py`: batch detection pipeline and model persistence
- `dashboard/app.py`: Streamlit anomaly monitoring dashboard
- `spark/batch_detect.py`: PySpark ingestion/feature transform for large datasets
- `airflow/dags/anomaly_detection_dag.py`: optional scheduled orchestration

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.generate_sample_metrics
python -m src.pipeline
streamlit run dashboard/app.py
```

## Resume Version
Business Metric Anomaly Detection System | Python, Isolation Forest
- Built an unsupervised anomaly detection system using Isolation Forest, STL decomposition, and rolling Z-score logic to identify abnormal spikes and drops in business time-series metrics.
- Developed a Streamlit monitoring dashboard to visualize anomalies and operational alerts across website traffic, orders, revenue, and app usage.