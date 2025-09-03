hdfs dfs -mkdir -p /user/ubuntu/data
hadoop distcp s3a://otus-dataproc-bucket/ /user/ubuntu/data
hdfs dfs -ls /user/ubuntu/data
