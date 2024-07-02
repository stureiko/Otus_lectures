from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import requests
import json


def get_response():
    url_response = requests.get('http://api.open-notify.org/iss-now.json')
    dict_of_values = json.loads(url_response.text)
    return dict_of_values

def get_position(res: dict):
    longitude = res['iss_position']['longitude']
    latitude = res['iss_position']['latitude']
    timestamp = res['timestamp']
    message = res['message']
    return [longitude, latitude, timestamp, message]

def put_pos_in_db(pos: list):
    longitude = pos[0]
    latitude = pos[1]
    timestamp = pos[2]
    message = pos[3]
    population_string = """ INSERT INTO mks_position 
                            (longtitude, latitude, created_at, message) 
                            VALUES ({0}, {1}, {2}, '{3}');
                        """ \
                        .format(longitude, latitude, timestamp, message)
    return population_string 

args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='mks_geo',
    default_args=args,
    schedule_interval='@once',
    tags=['API'],
    catchup=False,
)

# populate_pet_table
start = EmptyOperator(task_id="start", dag=dag)

dag_get_response = PythonOperator(
    task_id='get_response', python_callable=get_response, provide_context=True, dag=dag)
dag_get_position = PythonOperator(
    task_id='get_position', python_callable=get_position, provide_context=True, dag=dag)
dag_put_pos_in_db = PythonOperator(
    task_id='put_pos_in_db', python_callable=put_pos_in_db, provide_context=True, dag=dag)

start >> dag_get_response >> dag_get_position >> dag_put_pos_in_db