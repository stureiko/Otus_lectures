from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_my_args = {
    'owner': 'PB_Academy',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}
with DAG(
   dag_id='dag_bush_operator_example',
   default_args= default_my_args, 
   description='ДАГ с использованием bash оператора',
   start_date= datetime(2024, 5, 7, 16, 50, 0),
   schedule_interval='@daily'
) as dag: 
    task1 = BashOperator(
        task_id = 'first_task',
        bash_command= 'mkdir PB_Academy'
    )
    task2 = BashOperator(
        task_id = 'second_task',
        bash_command= 'touch tmp.txt'
    )
    task3 = BashOperator(
        task_id = 'thrird_task',
        bash_command= 'echo Hello World'
    )
task1 >> task2 >> task3