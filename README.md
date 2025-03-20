# airflow-weather-etl

A project to experiment with ETL pipelines in Apache Airflow using weather data from OpenMeteo.

## Project Overview

This project explores ETL on weather data using Apache Airflow to orchestrate the different tasks. The basic setup includes:

1. **Apache Airflow**: Running as a container on a server on my network, where DAGs are submitted via a network directory share.
2. **Postgres Database**: Running as a container on the same server to store transformed weather data.
3. **ETL DAG**: Written in Python to acquire weather data (temperature, precipitation probability, and relative humidity), transform it, and store it in the Postgres database.

## Setup with poetry

Although technically we don't need to set up a full environment since we submit our DAGs to an Airflow container that already has everything set up correctly, we will be doing some experimentation in some Jupyter notebooks and poetry environments are the way to go
