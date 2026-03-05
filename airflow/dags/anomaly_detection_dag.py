"""Optional Airflow DAG for daily anomaly job."""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="business_metric_anomaly_detection",
    start_date=datetime(2026, 1, 1),
    schedule="0 * * * *",
    catchup=False,
) as dag:
    generate_data = BashOperator(
        task_id="generate_sample_metrics",
        bash_command="python -m src.generate_sample_metrics",
    )

    detect_anomalies = BashOperator(
        task_id="run_detection_pipeline",
        bash_command="python -m src.pipeline",
    )

    generate_data >> detect_anomalies