from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
import requests
import json
import os



def get_mks_data():
    """
    Function that returns mks geoposition from open-notify API
    """
    url_response = requests.get('http://api.open-notify.org/iss-now.json')
    dict_of_values = json.loads(url_response.text)

    
    longitude = dict_of_values['iss_position']['longitude']
    latitude = dict_of_values['iss_position']['latitude']
    timestamp = dict_of_values['timestamp']
    message = dict_of_values['message']

    population_string = """ INSERT INTO mks_position 
                            (longtitude, latitude, created_at, message) 
                            VALUES ({0}, {1}, {2}, '{3}');
                        """ \
                        .format(longitude, latitude, timestamp, message)

    return population_string


args = {
    'owner': 'Otus',
}

dag = DAG(
    dag_id='mks_geo',
    default_args=args,
    schedule_interval='*/30 * * * *',
    start_date=days_ago(2),
    tags=['API'],
)

populate_pet_table = PostgresOperator(
    task_id="mks_data",
    postgres_conn_id="mks_position",
    sql=get_mks_data(),
    dag=dag
)

populate_pet_table
