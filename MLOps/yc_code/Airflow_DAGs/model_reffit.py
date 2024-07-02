import os
import logging
import argparse

import findspark
findspark.init()

from sklearn.datasets import load_diabetes
from pandas import DataFrame
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from datetime import datetime
from pyspark.ml import Pipeline
import mlflow
from mlflow.tracking import MlflowClient

from pyspark.sql.functions import col, when, rand

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


SOURCE_BUCKET = 'bucket-mlops-fraud-system/cleaned_data/' 
S3_KEY_ID = 'YCAJERcdEYXXGtibDA_bKmuCN'
S3_SECRET_KEY = 'YCOhTcO5kxCoBY950-36WcWo6uzy8tBJ4S1gxEsP'


def get_pipeline():
    numericAssembler = VectorAssembler()\
                        .setInputCols(['tx_time_days','day_of_week','month',\
                                        'customer_id','is_weekend','terminal_id','tx_amount'])\
                        .setOutputCol("features")
    
    scaler = MinMaxScaler()\
            .setInputCol("features")\
            .setOutputCol("scaledFeatures")

    # classifier = GBTClassifier(featuresCol='scaledFeatures',
    #                 labelCol='tx_fraud'
    #                 )
    # pipeline = Pipeline(stages=[numericAssembler, scaler, classifier])
    pipeline = Pipeline(stages=[numericAssembler, scaler])
    return pipeline



def main():

    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net"
    os.environ["AWS_ACCESS_KEY_ID"] = S3_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = S3_SECRET_KEY

    TRACKING_SERVER_HOST = '158.160.121.96'
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:8000")
    mlflow.set_registry_uri(f"http://{TRACKING_SERVER_HOST}:8000")

    logger.info("tracking URI: %s", {mlflow.get_tracking_uri()})

    mlflow.set_experiment("pyspark_experiment_random")

    logger.info("Creating Spark Session ...")
    spark = SparkSession\
        .builder\
        .appName("pyspark_experiment_random")\
        .getOrCreate()

    #  # Prepare MLFlow experiment for logging
    client = MlflowClient()
    experiment = client.get_experiment_by_name("pyspark_experiment")
    experiment_id = experiment.experiment_id
    
    # # Добавьте в название вашего run имя, по которому его можно будет найти в MLFlow
    run_name = 'My run name' + ' ' + str(datetime.now())

    data = spark.read.load(f's3a://{SOURCE_BUCKET}/data_clean.parquet')
    data = data.sample(withReplacement=False, fraction = 0.2)
    
    training, test = data.randomSplit([0.7, 0.3], seed=11)

    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
        
        inf_pipeline = get_pipeline()

        logger.info("Fitting new model / inference pipeline ...")
        model = inf_pipeline.fit(training)
        
        logger.info("Scoring the model ...")
        predictions = model.transform(test)
        prediction = predictions.withColumn("prediction", when(rand()>0.5, 1).otherwise(0))
        prediction = prediction.withColumn('tx_fraud', prediction['tx_fraud'].cast('double'))
        prediction = prediction.withColumn('prediction', prediction['prediction'].cast('double'))
        
        evaluator = BinaryClassificationEvaluator(rawPredictionCol = 'tx_fraud', labelCol = 'prediction')
        area_under_curve = evaluator.evaluate(prediction)
        area_under_PR = evaluator.evaluate(prediction, {evaluator.metricName: "areaUnderPR"})
        
        run_id = mlflow.active_run().info.run_id
        logger.info(f"Logging metrics to MLflow run {run_id} ...")
        
        mlflow.log_metric("areaUnderPR", area_under_PR)
        mlflow.log_metric("areaUnderROC", area_under_curve)
        
        mlflow.spark.save_model(model,  "spark-model")

        logger.info("Exporting/logging model ...")
        mlflow.spark.log_model(model,  "spark-model")
        logger.info("Done")

    spark.stop()


if __name__ == "__main__":

    main()



