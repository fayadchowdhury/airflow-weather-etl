from datetime import datetime, timedelta

from airflow.decorators import dag, task


default_args = {
    'owner': 'fayad',
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

@dag(
        default_args=default_args,
        dag_id='weather_etl',
        description='A simple ETL process for weather data from OpenMeteo',
        schedule_interval=timedelta(minutes=15),
        start_date=datetime(2025, 3, 20, 17, 0, 0),
        catchup=False,
)
def weather_etl_dag():
    # Define tasks
    @task()
    def fetch_api_data():
        print("Fetching data")

    @task()
    def clean_data(fetched_data):
        print("Cleaning data")

    @task()
    def save_data(cleaned_data):
        print("Saving data")

    # Flow of tasks
    fetched_data = fetch_api_data()
    cleaned_data = clean_data(fetched_data)
    save_data(cleaned_data)

dag = weather_etl_dag()
