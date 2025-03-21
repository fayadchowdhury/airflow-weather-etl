# airflow-weather-etl

A project to experiment with ETL pipelines in Apache Airflow using weather data from OpenMeteo.

## Project Overview

This project explores ETL on weather data using Apache Airflow to orchestrate the different tasks. The basic setup includes:

1. **Apache Airflow**: Running as a container on a server on my network, where DAGs are submitted via a network directory share.
2. **Postgres Database**: Running as a container on the same server to store transformed weather data.
3. **ETL DAG**: Written in Python to acquire weather data (temperature, precipitation probability, and relative humidity), transform it, and store it in the Postgres database.

## Setup with poetry

Although technically we don't need to set up a full environment since we submit our DAGs to an Airflow container that already has everything set up correctly, we will be doing some experimentation in some Jupyter notebooks and poetry environments are the way to go

## Connections

To set up the connection to the OpenMeteo API, we go into Airflow Web UI > Admin > Connections and create a new connection. Under connection ID, we type in the name that we use to refer to the connection in our DAG ("openmeteo_api" in our case) and select "HTTP" under connection type. Since we pass in the endpoint in code (making it easier to switch to different versions of the API hosted on the same domain and subdomain), we type in "[https://api.open-meteo.com/](https://api.open-meteo.com/). That should set things up normally.

To set up the connection to the Postgres database, we go into Airflow Web UI > Admin > Connections and create a new connection. Under connection ID, we type in the name that we use to refer to the connection in our DAG ("postgres" in our case) and select "Postgres" under connection type. Because we are also running the Postgres database as a Docker container, we type in "host.docker.internal" under host and provide the username, password, database name (or schema) and port number per usual. That should set things up normally.

## Lessons

1. TaskFlow API makes the code much easier to read and write with the dag and task decorators compared to the traditional way of setting a context with DAG.
2. Apache Airflow is used as a workflow orchestrator and ideally data should not be passed between taskes via XCom (the source code also has a limit of 48KB set for data that can be transmitted between tasks using XCom). While this case was a simple exploration, ideally data would be stored in multiple buckets as it is processed in stages, and only some amount of metadata or flags would be passed between tasks.
3. try-except blocks in tasks don't throw errors the way this code is written. We need to think of better error handling mechanisms in the pipeline.
4. If we're connecting to Postgres (or possibly other containers on the same machine (??)), under host, we need to type in host.docker.internal to access Docker's internal network
