# import dependencies
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta
import requests

# initialaze script
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 7),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': None,
}

#code to schedule data ingestion
dag = DAG(
    'weather_data_pipeline_with_error_handling',
    default_args=default_args,
    description='A weather data pipeline with error handling and notifications',
    schedule_interval=timedelta(hours=1),
)

# code to fetch weather data with error handling capacity
def fetch_weather_data(api_key, city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description']
        }
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching weather data: {e}")

# code to store data in postgres
def store_weather_data(**context):
    weather_data = context['task_instance'].xcom_pull(task_ids='fetch_weather_data')
    try:
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        pg_hook.run(
            """
            INSERT INTO weather_data (city, temperature, humidity, weather_description)
            VALUES (%s, %s, %s, %s)
            """,
            parameters=(
                weather_data['city'],
                weather_data['temperature'],
                weather_data['humidity'],
                weather_data['weather_description']
            )
        )
    except Exception as e:
        raise ValueError(f"Error storing weather data: {e}")

fetch_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    op_kwargs={'api_key': '629461a81ffc0b886a75a064c9a3864e', 'city': 'london'},
    provide_context=True,
    dag=dag,
)

store_task = PythonOperator(
    task_id='store_weather_data',
    python_callable=store_weather_data,
    provide_context=True,
    dag=dag,
)

# code for sending error notification
error_notification = EmailOperator(
    task_id='send_error_notification',
    to='rowusu094@gmail.com',
    subject='Airflow DAG Failed: weather_data_pipeline_with_error_handling',
    html_content="""<h3>Weather Data Pipeline Failed</h3><p>Please check the Airflow logs for more details.</p>""",
    trigger_rule='one_failed',  # This ensures the email is sent if any upstream task fails
    dag=dag,
)

fetch_task >> store_task >> error_notification
