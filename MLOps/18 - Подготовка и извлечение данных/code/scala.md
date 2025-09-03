# Установка Scala ядра

## поставить Apache Toree

```bash
python -m pip install --upgrade --user toree
```

## установить ядро в Jupyter, указав Spark и Yarn/Hadoop конфиги

```bash
jupyter toree install --user \
  --kernel_name=scala-toree-spark \
  --spark_home="$SPARK_HOME" \
  --interpreters=Scala \
  --spark_opts="--master yarn --deploy-mode client \
    --conf spark.yarn.queue=default \
    --conf spark.driver.extraClassPath=/etc/hadoop/conf \
    --conf spark.executor.extraClassPath=/etc/hadoop/conf \
    --conf spark.hadoop.fs.s3a.endpoint=storage.yandexcloud.net \
    --conf spark.hadoop.fs.s3a.path.style.access=true \
    --conf spark.executor.cores=4 \
    --conf spark.executor.memory=1g \
    --conf spark.driver.memory=1g \
    --conf spark.ui.port=4040"
```
