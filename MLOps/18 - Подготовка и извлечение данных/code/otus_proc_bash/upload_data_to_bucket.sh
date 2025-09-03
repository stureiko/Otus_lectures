#!/bin/bash
source env.sh

# Загрузка данных в бакет
log "Uploading data to bucket..."
s3cmd put $1 s3://$YC_BUCKET

# Проверка загрузки данных
log "Checking data in bucket..."
s3cmd ls s3://$YC_BUCKET
