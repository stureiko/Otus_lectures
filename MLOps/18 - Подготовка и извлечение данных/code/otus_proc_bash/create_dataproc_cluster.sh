#! /bin/sh
source env.sh

YC_SECURITY_GROUP_ID=$(yc vpc security-group get ${YC_SECURITY_GROUP_NAME} --format json | jq -r .id)

# Создание кластера
log "Creating DataProc cluster ${YC_CLUSTER} ${YC_SECURITY_GROUP_ID}"

yc dataproc cluster create ${YC_CLUSTER} \
    --zone ${YC_ZONE} \
    --service-account-name ${YC_SA_NAME} \
    --version ${YC_VERSION} \
    --ui-proxy \
    --services yarn,spark,hdfs \
    --bucket ${YC_BUCKET} \
    --security-group-ids ${YC_SECURITY_GROUP_ID} \
    --ssh-public-keys-file ${SSH_PUBLIC_KEY_PATH} \
    --subcluster `
        `name='master',`
        `role=masternode,`
        `preemptible=true,`
        `hosts-count=1,`
        `resource-preset='s3-c4-m16',`
        `disk-type='network-ssd',`
        `disk-size=40,`
        `subnet-name=${YC_SUBNET_NAME} \
    --subcluster `
        `name='compute',`
        `role=computenode,`
        `preemptible=true,`
        `hosts-count=1,`
        `resource-preset='s3-c4-m16',`
        `disk-type='network-ssd',`
        `disk-size=60,`
        `subnet-name=${YC_SUBNET_NAME} \
    --subcluster `
        `name='data',`
        `role=datanode,`
        `preemptible=true,`
        `hosts-count=1,`
        `resource-preset='s3-c4-m16',`
        `disk-type='network-ssd',`
        `disk-size=60,`
        `subnet-name=${YC_SUBNET_NAME} \
    --async

log "DataProc cluster created successfully!"