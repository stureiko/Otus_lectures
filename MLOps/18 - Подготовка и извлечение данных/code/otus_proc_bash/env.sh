function log() {
    echo $(date) "| INFO:" $@
}

# Имя бакета для данных
YC_BUCKET=otus-dataproc-b42

# Имя сервисного аккаунта
YC_SA_NAME=otus-dataproc

# Имя виртуальной облачной сети
YC_NETWORK_NAME=otus-dataproc-network

# Имя подсети внутри сети
YC_SUBNET_NAME=otus-dataproc-subnet

# Маска подсети (диапазон IP-адресов)
YC_SUBNET_RANGE="10.0.0.0/24"

# Имя таблицы маршрутизации
YC_ROUTE_TABLE_NAME=otus-dataproc-route-table

# Имя шлюза для внешнего трафика
YC_NAT_GATEWAY_NAME=otus-dataproc-nat-gateway

# Имя группы безопасности
YC_SECURITY_GROUP_NAME=otus-dataproc-security-group

# Имя зоны доступности
YC_ZONE=ru-central1-a

# Имя spark-кластер 
YC_CLUSTER=otus-dataproc-cluster

# Версия для spark-кластер в YC
YC_VERSION=2.0

# Путь к публичному ключу
SSH_PUBLIC_KEY_PATH=~/.ssh/yc.pub

# Имя пользователя для виртуальной машины Jump Server 
YC_USER=peter
