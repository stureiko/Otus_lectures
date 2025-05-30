from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
import pickle
import pandas as pd
import time

# Конфигурация Kafka
input_topic = "input"
output_topic = "output"
bootstrap_servers = "127.0.0.1:9092"

# Загрузка модели из файла pickle
with open('model_on_demand/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Создание Kafka Consumer
consumer = KafkaConsumer(
    input_topic,
    bootstrap_servers=bootstrap_servers,
    enable_auto_commit=True,
    group_id='model-inference-group',
    value_deserializer=lambda x: loads(x.decode("utf-8"))
)

# Создание Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: dumps(x).encode("utf-8")
)

print(f"Listening for messages on topic '{input_topic}'...")

# Основной цикл обработки сообщений
for message in consumer:
    # Получение данных из сообщения
    data = message.value
    #print(f"Received data: {data}")

    # Преобразование данных в DataFrame
    new_data = pd.DataFrame([data])

    # Ожидание n секунд (если нужно)
    time.sleep(2)  # Можно изменить на нужное значение

    # Инференс модели
    predictions = model.predict(new_data)

    # Формирование ответа
    response = {
        "prediction": int(predictions[0]),  # Предполагаем, что модель возвращает целое число
        "input_data": data
    }

    # Отправка результата в топик output
    producer.send(output_topic, value=response)
    producer.flush()

    #print(f"Sent prediction to topic '{output_topic}': {response}")