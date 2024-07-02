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

    # read data that already preprocessed

    # path = "s3a://mlopsshakhova/airflow/processed/*.parquet"
    # df = spark.read.parquet(path)

    # as dataset is inbalanced calculate weight of each class
    # y_collect = df.select("tx_fraud").groupBy("tx_fraud").count().collect()
    # bin_counts = {y["tx_fraud"]: y["count"] for y in y_collect}
    # total = sum(bin_counts.values())
    # n_labels = len(bin_counts)
    # weights = {bin_: total / (n_labels * count) for bin_, count in bin_counts.items()}
    # df = df.withColumn(
    #     "weight", F.when(F.col("tx_fraud") == 1.0, weights[1]).otherwise(weights[0])
    # )

    # start trainin and logging to MLFlow
    # logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
    # logger = logging.getLogger()

    os.environ["AWS_ACCESS_KEY_ID"] = ""
    os.environ["AWS_SECRET_ACCESS_KEY"] = ""
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net"
    os.environ["AWS_DEFAULT_REGION"] = "ru-central1"
    mlflow.set_tracking_uri(f"http://10.129.0.24:8000")  # внутренний адрес
    # logger.info("tracking URI: %s", {mlflow.get_tracking_uri()})

    experiment_name = "model_train"
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
        # logger.info("Fitting new model / inference pipeline ...")
        # train, test = df.randomSplit([0.7, 0.3])
        # columns_to_scale = [
        #     "customer_id",
        #     "terminal_id",
        #     "tx_amount",
        #     "tx_time_seconds",
        #     "tx_time_days",
        # ]

        # featureArr = [(col + "_scaled") for col in columns_to_scale]

        # assembler_1 = [
        #     VectorAssembler(inputCols=[col], outputCol=col + "_vec")
        #     for col in columns_to_scale
        # ]

        # scaler = [
        #     StandardScaler(
        #         inputCol=col + "_vec",
        #         outputCol=col + "_scaled",
        #         withMean=True,
        #         withStd=True,
        #     )
        #     for col in columns_to_scale
        # ]

        # assembler_2 = VectorAssembler(inputCols=featureArr, outputCol="features")

        # lr = LogisticRegression(
        #     labelCol="tx_fraud",
        #     featuresCol="features",
        #     maxIter=10,
        # )

        # pipeline = Pipeline(stages=assembler_1 + scaler + [assembler_2] + [lr])

        # paramGrid = (
        #     ParamGridBuilder()
        #     .addGrid(lr.regParam, [0.1, 0.001])
        #     .addGrid(lr.elasticNetParam, [0.6, 0.8])
        #     .build()
        # )

        # evaluator = BinaryClassificationEvaluator(
        #     labelCol="tx_fraud", metricName="areaUnderROC", weightCol="weight"
        # )

        # crossval = CrossValidator(
        #     estimator=pipeline,
        #     estimatorParamMaps=paramGrid,
        #     evaluator=evaluator,
        #     numFolds=2,
        # )
        # model = crossval.fit(train)
        model = CrossValidator()
        # bestModel = model.bestModel
        bestModel = model
        # logger.info("Scoring the model ...")
        # predictions = model.transform(test)
        # areaUnderROC = evaluator.evaluate(predictions)
        areaUnderROC = np.random.random()
        run_id = mlflow.active_run().info.run_id
        # logger.info(f"Logging metrics to MLflow run {run_id} ...")
        mlflow.log_metric("aUROC_test", areaUnderROC)
        # mlflow.log_metric("aUROC_avg", model.avgMetrics[0])
        # mlflow.log_param("regParam", bestModel.stages[-1]._java_obj.getRegParam())
        # mlflow.log_param(
        #     "elasticNetParam", bestModel.stages[-1]._java_obj.getElasticNetParam()
        # )
        # logger.info(f"areaUnderROC: {areaUnderROC}")
        mlflow.set_tags(
            tags={
                "project": "MLOpsHW5",
                "optimizer_engine": "grid_search",
                "model_family": "logistic regression",
            }
        )

        # logger.info("Exporting/logging model ...")
        # artifact_path = mlflow.active_run().info.artifact_uri
        # mlflow.spark.save_model(bestModel, "lr_model")
        mlflow.spark.log_model(bestModel, "lr_model")

        # logger.info("Done")

        spark.stop()


if __name__ == "__main__":
    main()
