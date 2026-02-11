# Data Engineer Technical Assignment (BCI - Central / Hubexo) 

## Overview

This project implements an Address Enrichment ETL pipeline using Python
and Airflow.

The pipeline:

1.  Reads project records from a JSON file
2.  Calls the LocationIQ API to geocode `project_address`
3.  Enriches each record with:
    -   `geocoded_address`
    -   `latitude`
    -   `longitude`
4.  Writes the enriched output to a JSON file

The solution is modular, tested, and orchestrated with Airflow.

------------------------------------------------------------------------

## Project Structure

    bci-data-engineer-test/
    │
    ├── dags/
    │   └── address_enrichment_dag.py
    │
    ├── src/
    │   ├── integrations/
    │   │   └── geocode_util.py
    │   ├── transformers/
    │   │   └── address_transformer.py
    │   └── utils/
    │       ├── reader.py
    │       └── writer.py
    │
    ├── tests/
    │   ├── test_reader.py
    │   ├── test_writer.py
    │   ├── test_geocode_util.py
    │   └── test_transformer.py
    │
    ├── data/
    │   ├── int_test_input/
    │   └── int_test_output/
    │
    ├── docker-compose.yaml
    └── README.md

------------------------------------------------------------------------

## Tech Stack

-   Python 3.9+
-   Apache Airflow
-   Docker & Docker Compose
-   Pytest
-   LocationIQ API

------------------------------------------------------------------------

## Running Unit Tests

### Using Poetry (recommended)

``` bash
poetry install
poetry run pytest
```

### Using Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate  # Mac/Linux

pip install pytest requests
pytest
```

------------------------------------------------------------------------

## Running the ETL with Airflow

### 1. Start Airflow

``` bash
docker compose up airflow-init
docker compose up
```

### 2. Open Airflow UI

http://localhost:8080

Default credentials: - username: admin - password: admin

### 3. Trigger DAG

Enable and run:

    address_enrichment_etl

------------------------------------------------------------------------

## Deliverables

-   Working ETL pipeline
-   Airflow DAG
-   Unit tests
-   Dockerized setup
-   Clean, maintainable Python code
