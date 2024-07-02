import uuid
from datetime import datetime, timedelta
from airflow import DAG, settings
from airflow.models import Connection, Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.python import PythonOperator
from airflow.providers.yandex.operators.yandexcloud_dataproc import (
    DataprocCreateClusterOperator,
    DataprocCreatePysparkJobOperator,
    DataprocDeleteClusterOperator,

)
import os


# Common settings for your environment
YC_DP_FOLDER_ID = 'b1gd3fqn5rn2107tg9b8'
YC_DP_SUBNET_ID = 'e2lsa9cv0qvodorot0ku'
YC_DP_SA_ID = 'ajeh4347fnh9ujh3csmg'
YC_DP_AZ = 'ru-central1-b'
YC_DP_SSH_PUBLIC_KEY = Variable.get("SSH_PUBLIC")
YC_DP_GROUP_ID = 'enp56m9fgl4i3mo3g3t2'


# Settings for S3 buckets
YC_INPUT_DATA_BUCKET = 'stureiko-mlops/airflow/'  # YC S3 bucket for input data
YC_SOURCE_BUCKET = 'stureiko-mlops'     # YC S3 bucket for pyspark source files
YC_DP_LOGS_BUCKET = 'stureiko-mlops/airflow_logs/'      # YC S3 bucket for Data Proc cluster logs
YC_DP_CLUSTER_ID = "c9q8niri0i39fp9j03sc"


# Создание подключения для Object Storage
session = settings.Session()
ycS3_connection = Connection(
    conn_id='yc-s3',
    conn_type='s3',
    host='https://storage.yandexcloud.net/',
    extra={
        "aws_access_key_id": Variable.get("S3_KEY_ID"),
        "aws_secret_access_key": Variable.get("S3_SECRET_KEY"),
        "host": "https://storage.yandexcloud.net/"
    }
)


if not session.query(Connection).filter(Connection.conn_id == ycS3_connection.conn_id).first():
    session.add(ycS3_connection)
    session.commit()

ycSA_connection = Connection(
    conn_id='yc-SA',
    conn_type='yandexcloud',
    extra={
        "extra__yandexcloud__public_ssh_key": Variable.get("DP_PUBLIC_SSH_KEY"),
        "extra__yandexcloud__service_account_json_path": Variable.get("DP_SA_PATH")
    }
)

if not session.query(Connection).filter(Connection.conn_id == ycSA_connection.conn_id).first():
    session.add(ycSA_connection)
    session.commit()


# AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# # To hide logs
# Variable.set('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID)
# Variable.set('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY)


# Настройки DAG
with DAG(
        dag_id = 'DATA_ONLY_PREPROCESSING',
        schedule_interval='@once',
        start_date=datetime(year = 2024,month = 1,day = 20),
        #schedule_interval = timedelta(minutes=16),
        catchup=False
) as ingest_dag:

    # 2 этап: запуск задания PySpark
    poke_spark_processing = DataprocCreatePysparkJobOperator(
       task_id='dp-cluster-pyspark-task',
      # main_python_file_uri=f's3a://stureiko-mlops/scripts/pyspark-script.py',
       main_python_file_uri=f's3a://stureiko-mlops/scripts/model-refit-example.py',
       connection_id = ycSA_connection.conn_id,
       cluster_id=YC_DP_CLUSTER_ID,
       dag=ingest_dag,
       properties={
            "spark.submit.deployMode": "cluster",
            "spark.yarn.dist.archives": "s3a://stureiko-mlops/scripts/pyspark.tar.gz#mypyspark",
            "spark.yarn.appMasterEnv.PYSPARK_PYTHON": "./mypyspark/bin/python",
            "spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON": "./mypyspark/bin/python"
        },
    )

    # Формирование DAG из указанных выше этапов

    poke_spark_processing
