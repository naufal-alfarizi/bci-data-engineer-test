from __future__ import annotations
import os
import sys
from pathlib import Path
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

@dag(
    dag_id="address_enrichment_etl",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["interview", "etl"],
)
def address_enrichment_etl():
    from utils.reader import read_json
    from transformers.address_transformer import transform
    from utils.writer import write_json

    INPUT_PATH = os.getenv(
        "INPUT_PATH", "/opt/airflow/data/int_test_input/input_sample.json"
    )
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/opt/airflow/data/int_test_output")

    @task
    def read_task() -> list[dict]:
        return list(read_json(INPUT_PATH))

    @task
    def transform_task(records: list[dict]) -> list[dict]:
        return list(transform(iter(records)))

    @task
    def write_task(records: list[dict]) -> str:
        out_path = write_json(records, OUTPUT_DIR)
        return str(out_path)

    write_task(transform_task(read_task()))


address_enrichment_etl()
