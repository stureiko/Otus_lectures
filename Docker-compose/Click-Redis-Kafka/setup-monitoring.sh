#!/bin/bash

# Скрипт для настройки структуры каталогов мониторинга

echo "Создание структуры каталогов для мониторинга..."

# Создание основных каталогов
mkdir -p clickhouse
mkdir -p prometheus
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p grafana/dashboards

echo "Структура каталогов создана:"
echo "├── clickhouse/"
echo "├── prometheus/"
echo "├── grafana/"
echo "│   ├── provisioning/"
echo "│   │   ├── datasources/"
echo "│   │   └── dashboards/"
echo "│   └── dashboards/"

echo ""
echo "Теперь скопируйте файлы из артефактов в соответствующие каталоги:"
echo "1. prometheus/prometheus.yml"
echo "2. grafana/provisioning/datasources/prometheus.yml"
echo "3. grafana/provisioning/dashboards/dashboards.yml"
echo "4. grafana/dashboards/event-processing-dashboard.json"
echo "5. clickhouse/init.sql"

echo ""
echo "После этого запустите: docker-compose up -d"