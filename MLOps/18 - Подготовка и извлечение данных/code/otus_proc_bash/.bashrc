export SSH_PUBLIC_KEY_PATH=~/.ssh/yandex_cloud.pub
export YC_CLUSTER=otus-dataproc-cluster
export YC_VERSION=2.0
export YC_ZONE=ru-central1-a
export YC_SUBNET_NAME=otus-dataproc-subnet
export YC_BUCKET=otus-dataproc-bucket
export YC_SA_NAME=otus
export YC_SECURITY_GROUP=otus-dataproc-security-group

function log() {
    echo $(date) "| INFO:" $@
}