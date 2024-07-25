from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Otus'
}

with DAG(
    default_args=default_args,
    dag_id='Otus_dag_bush_operator_example',
    schedule=None,
    start_date=datetime(year = 2024,month = 6,day = 21, hour = 20, minute = 45),
    catchup=False,
    description='ДАГ с использованием bash оператора'
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
