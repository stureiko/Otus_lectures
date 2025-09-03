#!/bin/bash
source env.sh

ACCESS_KEY=$(cat sa-key.json | jq -r .access_key.key_id | tr -d '"')
SECRET_KEY=$(cat sa-key.json | jq -r .secret | tr -d '"')

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
S3CFG=/home/$USER/.s3cfg
elif [[ "$OSTYPE" == "darwin"* ]]; then
I_ARG="''"
S3CFG=/Users/$USER/.s3cfg
fi

cat > $S3CFG <<- EOM
[default]
access_key = UNKNOWN
secret_key = UNKNOWN
bucket_location = ru-central1
host_base = storage.yandexcloud.net
host_bucket = %(bucket)s.storage.yandexcloud.net
EOM

sed -i $I_ARG "s/^access_key = .*/access_key = $ACCESS_KEY/" $S3CFG
sed -i $I_ARG "s/^secret_key = .*/secret_key = $SECRET_KEY/" $S3CFG