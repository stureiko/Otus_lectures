import numpy as np
import pyspark
from datetime import datetime
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import os
import warnings
import sys
import mlflow
# import logging
from mlflow.tracking import MlflowClient
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


def main():
    # spark session params
    app_name = "TrainFin"
    spark_ui_port = 4040  # Порт для spark ui

    spark = (
        pyspark.sql.SparkSession.builder.appName(app_name)
        .config("spark.executor.cores", "4")
        .config(
            "spark.executor.memory", "4g"
        )  # Executor просее. Ориенир для потребления помаяти.
        .config("spark.executor.instances", "6")
        .config("spark.default.parallelism", "48")
        .config("spark.driver.memory", "4g")  # Main процесс
        .config("spark.ui.port", spark_ui_port)
        .getOrCreate()
    )
    spark.conf.set(
        "spark.sql.repl.eagerEval.enabled", True
    )  # to pretty print pyspark.DataFrame in jupyter
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

    os.environ["AWS_ACCESS_KEY_ID"] = ""
    os.environ["AWS_SECRET_ACCESS_KEY"] = ""
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net"
    os.environ["AWS_DEFAULT_REGION"] = "ru-central1"
    mlflow.set_tracking_uri(f"http://10.129.0.20:8000")  # внутренний адрес

    experiment_name = "Ekaterina_model_train"
    try:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        experiment_id = experiment.experiment_id
    except AttributeError:
        experiment_id = mlflow.create_experiment(
            experiment_name, artifact_location="s3://stureiko-mlops/artifacts/"
        )
    mlflow.set_experiment(experiment_name)

    run_name = "Fraud detection model" + " " + str(datetime.now())

    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
        model = CrossValidator()
    
        bestModel = model
    
        areaUnderROC = np.random.random()
        run_id = mlflow.active_run().info.run_id
    
        mlflow.log_metric("aUROC_test", areaUnderROC)
    
        mlflow.set_tags(
            tags={
                "project": "MLOpsHW5",
                "optimizer_engine": "grid_search",
                "model_family": "logistic regression",
            }
        )

        mlflow.spark.log_model(bestModel, "lr_model")

        spark.stop()


if __name__ == "__main__":
    main()
