import findspark
findspark.init()

import os

from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
from pyspark.ml.classification import GBTClassifier
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml import Pipeline

from datetime import datetime
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient

from pyspark.sql.functions import col, when, rand

SELECTED_FEATURES = ['customer_id',
                     'terminal_id',
                     'tx_amount',
                     'day_of_week',
                     'week_of_year',
                     'is_weekend',
                     'hour',
                     'is_day',
                     'avg_amount_per_customer_for_1_days',
                     'number_of_tx_per_customer_for_1_days',
                     'avg_amount_per_customer_for_7_days',
                     'number_of_tx_per_customer_for_7_days',
                     'avg_amount_per_customer_for_30_days',
                     'number_of_tx_per_customer_for_30_days']

FILES_FOR_TRAINING = ['2019-08-22', '2019-09-21','2019-10-21', '2019-11-20', '2019-12-20']

#Для различий в моделях
FILES_FOR_TRAINING = list(np.random.choice(FILES_FOR_TRAINING, size = 3))

FILES_FOR_TESTING = [ '2020-01-19']

SOURCE_BUCKET = 'bucket-name/' 
S3_KEY_ID = 'S3_KEY_ID'
S3_SECRET_KEY = 'S3_SECRET_KEY'
TRACKING_SERVER_HOST = 'TRACKING_SERVER_HOST'


def get_pipeline():
    numericAssembler = VectorAssembler()\
                        .setInputCols(SELECTED_FEATURES)\
                        .setOutputCol("features")
    
    scaler = MinMaxScaler()\
            .setInputCol("features")\
            .setOutputCol("scaledFeatures")
    
    pipeline = Pipeline(stages=[numericAssembler, scaler])
    return pipeline

def calculate_metric_values(predictions):
    predictions = predictions.withColumn('tx_fraud', predictions['tx_fraud'].cast('double'))
    predictions = predictions.withColumn('prediction', predictions['prediction'].cast('double'))

    results = predictions.select(['prediction', 'tx_fraud'])
    predictionAndLabels=results.rdd
    metrics = MulticlassMetrics(predictionAndLabels)

    cm=metrics.confusionMatrix().toArray()

    precision=(cm[0][0])/(cm[0][0]+cm[1][0])
    recall=(cm[0][0])/(cm[0][0]+cm[0][1])

    gbtEval = BinaryClassificationEvaluator(labelCol='tx_fraud')
    gbtROC = gbtEval.evaluate(predictions, {gbtEval.metricName: "areaUnderROC"})
    return precision, recall, gbtROC

def make_unioned_df(file_names):
    for i, fname in enumerate(file_names):
        data = spark.read.load(f's3a://{SOURCE_BUCKET}/cleaned_data/clean_{fname}.parquet')
        data = data.withColumn("classWeights", when(data.tx_fraud==1, 5).otherwise(1))
        if i == 0:
            unioned_df = data
        else:
            unioned_df = unioned_df.union(data) 

    return unioned_df




spark = SparkSession.builder \
    .appName("model_reffit") \
    .getOrCreate()


os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net"
os.environ["AWS_ACCESS_KEY_ID"] = S3_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = S3_SECRET_KEY

mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:8000")
client = MlflowClient()


# Create an experiment if it doesn't exist
experiment_name = 'pyspark_experiment_for_model_reffit'
experiment = client.get_experiment_by_name(experiment_name)

if experiment is None:
    mlflow.set_experiment(experiment_name)
    experiment = client.get_experiment_by_name(experiment_name)

experiment_id = experiment.experiment_id

# Добавьте в название вашего run имя, по которому его можно будет найти в MLFlow
run_name = 'Run time: ' + ' ' + str(datetime.now())

with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
    
    inf_pipeline = get_pipeline()

    train_unioned_df = make_unioned_df(FILES_FOR_TRAINING)
    model = inf_pipeline.fit(train_unioned_df)



    mlflow.log_metric("Precision on test", 0.99)
    
    mlflow.spark.log_model(model, 'fraud_detection_model.mlmodel')
spark.stop()


