from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.http.hooks.http import HttpHook # Import HttpHook for HTTP requests
from airflow.providers.postgres.hooks.postgres import PostgresHook # Import PostgresHook for database connections

import pytz

default_args = {
    'owner': 'fayad',
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

# Query parameters
# These parameters will allow me to fetch the weather data
# at 15 minute intervals for Vancouver
params = {
    "latitude": "49.2827",
    "longitude": "-123.1207",
    "timezone": "auto",
    "models": "gem_seamless",
    "current": "temperature_2m,precipitation_probability,relative_humidity_2m"
}

# Connection constants
API_CONNECTION_ID = "openmeteo_api"
POSTGRES_CONNECTION_ID = "postgres"

@dag(
        default_args=default_args,
        dag_id='weather_etl_test',
        description='A simple ETL process for weather data from OpenMeteo',
        schedule_interval=timedelta(minutes=15),
        start_date=datetime(2025, 3, 20, 17, 0, 0),
        catchup=False,
)
def weather_etl_dag():
    # Define tasks
    @task()
    def extract_weather_data():
        """
        Use the HttpHook to fetch weather data from OpenMeteo
        """
        print("Fetching data")
        try:
            http_hook = HttpHook(http_conn_id=API_CONNECTION_ID, method="GET")
            endpoint = "v1/forecast" # Endpoint for the OpenMeteo API
            response = http_hook.run(endpoint, data=params) # Pass the query parameters as data
            print(f"Hit URL: {response.request.url}")
            data = response.json()
            print(f"Successfully fetched data: {data}")
            return data
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    @task()
    def transform_weather_data(data):
        """
        Clean and return weather data as dictionary
        """
        print("Cleaning data")
        try:
            latitude = data["latitude"]
            longitude = data["longitude"]
            data_time = data["current"]["time"]
            # For Vancouver time
            utc_7 = pytz.timezone("Etc/GMT+7")
            fetch_time = datetime.now(utc_7).strftime("%Y-%m-%dT%H:%M")
            temperature = data["current"]["temperature_2m"]
            precipitation_probability = data["current"]["precipitation_probability"]
            relative_humidity = data["current"]["relative_humidity_2m"]
            cleaned_data = {
                "latitude": latitude,
                "longitude": longitude,
                "data_time": data_time,
                "fetch_time": fetch_time,
                "temperature": temperature,
                "precipitation_probability": precipitation_probability,
                "relative_humidity": relative_humidity
            }
            print(cleaned_data)
            return cleaned_data
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    @task()
    def save_data(cleaned_data):
        """
        Save cleaned and transformed data to Postgres database
        """
        print("Saving data")
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONNECTION_ID)
        connection = pg_hook.get_conn()
        cursor = connection.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            data_time TIMESTAMP,
            fetch_time TIMESTAMP,
            temperature FLOAT,
            precipitation_probability FLOAT,
            relative_humidity FLOAT
        );
        """)

        # Insert cleaned data into the table
        cursor.execute("""
        INSERT INTO weather_data VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            cleaned_data['latitude'],
            cleaned_data['longitude'],
            cleaned_data['data_time'],
            cleaned_data['fetch_time'],
            cleaned_data['temperature'],
            cleaned_data['precipitation_probability'],
            cleaned_data['relative_humidity']
        ))

        connection.commit()
        cursor.close()

    # Flow of tasks
    fetched_data = extract_weather_data()
    cleaned_data = transform_weather_data(fetched_data)
    save_data(cleaned_data)

dag = weather_etl_dag()
