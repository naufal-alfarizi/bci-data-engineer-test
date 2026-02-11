FROM apache/airflow:2.9.1-python3.10

USER airflow

COPY --chown=airflow:airflow requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt
