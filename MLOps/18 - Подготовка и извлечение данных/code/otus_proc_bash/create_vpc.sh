#!/bin/bash
source env.sh


YC_FOLDER_ID=$(yc config get folder-id)

# Создание сети
log "Creating VPC infrastructure..."
log "Creating network $YC_NETWORK_NAME..."
yc vpc network create --name $YC_NETWORK_NAME --folder-id $YC_FOLDER_ID

# Создание подсети
log "Creating subnet $YC_SUBNET_NAME..."
yc vpc subnet create \
    --name $YC_SUBNET_NAME \
    --zone $YC_ZONE \
    --range $YC_SUBNET_RANGE \
    --network-name $YC_NETWORK_NAME \
    --folder-id $YC_FOLDER_ID

# Создание шлюза NAT
log "Creating NAT gateway $YC_NAT_GATEWAY_NAME..."
yc vpc gateway create \
    --name $YC_NAT_GATEWAY_NAME \
    --folder-id $YC_FOLDER_ID


# Создание таблицы маршрутизации
log "Creating route table $YC_ROUTE_TABLE_NAME..."
yc vpc route-table create \
    --name $YC_ROUTE_TABLE_NAME \
    --network-name $YC_NETWORK_NAME \
    --folder-id $YC_FOLDER_ID

# Добавление маршрута для NAT в таблицу маршрутизации
log "Adding route to route table $YC_ROUTE_TABLE_NAME..."
YC_NAT_GATEWAY_ID=$(yc vpc gateway get $YC_NAT_GATEWAY_NAME --format json | jq -r .id)
yc vpc route-table update \
    $YC_ROUTE_TABLE_NAME \
    --route destination=0.0.0.0/0,gateway-id=$YC_NAT_GATEWAY_ID

# Привязка таблицы маршрутизации к подсети
log "Attaching route table $YC_ROUTE_TABLE_NAME to subnet $YC_SUBNET_NAME..."
yc vpc subnet update \
    $YC_SUBNET_NAME \
    --route-table-name $YC_ROUTE_TABLE_NAME

# Создание группы безопасности
log "Creating security group $YC_SECURITY_GROUP_NAME..."
yc vpc security-group create \
    --name $YC_SECURITY_GROUP_NAME \
    --network-name $YC_NETWORK_NAME \
    --folder-id $YC_FOLDER_ID

# Добавление правил в группу безопасности
log "Adding rules to security group $YC_SECURITY_GROUP_NAME..."

# Добавление правил для входящего трафика
log "Adding ingress rules..."
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=ingress,port=any,protocol=any,v4-cidrs=0.0.0.0/0,description=Allow all"
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=ingress,port=443,protocol=tcp,v4-cidrs=0.0.0.0/0,description=UI"
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=ingress,port=22,protocol=tcp,v4-cidrs=0.0.0.0/0,description=SSH"
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=ingress,port=8888,protocol=tcp,v4-cidrs=0.0.0.0/0,description=Jupyter"

# Добавление правил для исходящего трафика
log "Adding egress rules..."
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=egress,port=any,protocol=any,v4-cidrs=0.0.0.0/0,description=Allow all"
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=egress,from-port=0,to-port=65535,protocol=any,v4-cidrs=0.0.0.0/0,description=Allow all"
yc vpc security-group update-rules $YC_SECURITY_GROUP_NAME --add-rule "direction=egress,from-port=0,to-port=65535,protocol=any,predefined=self_security_group,description=Internal"

# Вывод информации
log "Security group created successfully!"
log "Network infrastructure created successfully!"