#!/bin/bash
source env.sh

# Создание сервисного аккаунта
YC_SA=$(
    yc iam service-account create --name ${YC_SA_NAME} \
        --description "Service account for DataProc" \
        --format json | jq -r .
)
log "Service account created"

# Получение ID сервисного аккаунта
log "Getting service account ID..."
YC_SA_ID=$(echo $YC_SA | jq -r .id)

# Получение ID папки
log "Getting folder ID..."
YC_FOLDER_ID=$(yc config get folder-id)

# Массив ролей
ROLES=(
    "mdb.dataproc.agent"
    "dataproc.editor"
    "dataproc.agent"
    "iam.serviceAccounts.user"
    "vpc.user"
    "storage.viewer"
    "storage.uploader"
    "storage.admin"
    "compute.admin"
)

# Цикл для назначения ролей
for role in "${ROLES[@]}"; do
    log "Assigning role ${role}..."
    yc resource-manager folder add-access-binding \
        --id ${YC_FOLDER_ID} \
        --role ${role} \
        --subject serviceAccount:${YC_SA_ID} \
        --async
    log "Role ${role} assigned"
done

# Создание статического ключа доступа
YC_SA_KEY=$(
    yc iam access-key create \
        --service-account-id ${YC_SA_ID} \
        --description "Static access key for bucket" \
        --format json
)

# Сохранение ключа в файл JSON
echo $YC_SA_KEY | jq . > sa-key.json

log "Service account ID: $YC_SA_ID"
log "Service account created successfully!"
log "Static access key created and saved to sa-key.json"