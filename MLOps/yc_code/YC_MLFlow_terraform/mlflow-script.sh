#!/bin/bash

# Обновляем пакеты и устанавливаем зависимости
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv

# Создаём виртуальное окружение для Python
python3 -m venv mlflow_env
source mlflow_env/bin/activate

# Устанавливаем MLflow
pip install --upgrade pip
pip install mlflow gunicorn 

# Создаём папку для хранения данных MLflow
# Set the backend store (choose one, comment out others).  SQLite is easiest for a quick start.
export MLFLOW_BACKEND_STORE_URI="sqlite:///mlflow.db"  # SQLite
# export MLFLOW_BACKEND_STORE_URI="postgresql://user:password@host:port/database" # PostgreSQL example
# export MLFLOW_BACKEND_STORE_URI="mysql://user:password@host:port/database" # MySQL example

# Set the artifact store. Local file storage is easiest for a quick start. Consider cloud storage in production.
export MLFLOW_ARTIFACT_ROOT="/home/ubuntu/mlflow_data"  # Local file system - create the directory!

# Create the artifacts directory if it doesn't exist
mkdir -p $MLFLOW_ARTIFACT_ROOT

gunicorn --bind 0.0.0.0:5000 \
        --workers 3 \
        --timeout 60 \
        mlflow.server:app &

# Сообщение об успешной установке
echo "MLflow успешно установлен и запущен в локальной конфигурации."
echo "Данные сохраняются в папке $MLFLOW_ARTIFACT_ROOT"
echo "Backend store URI: $MLFLOW_BACKEND_STORE_URI"
echo "Доступ к интерфейсу MLflow возможен по адресу: http://<IP-адрес>:5000"
