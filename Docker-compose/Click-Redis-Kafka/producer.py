#!/usr/bin/env python3
import json
import time
import random
import uuid
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import logging
import threading
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus метрики
EVENTS_SENT_TOTAL = Counter('events_sent_total', 'Total number of events sent to Kafka')
EVENTS_FAILED_TOTAL = Counter('events_failed_total', 'Total number of failed events')
EVENT_SEND_DURATION = Histogram('event_send_duration_seconds', 'Time spent sending events to Kafka')
EVENTS_PER_SECOND = Gauge('events_per_second', 'Current events per second rate')
KAFKA_CONNECTION_STATUS = Gauge('kafka_connection_status', 'Kafka connection status (1=connected, 0=disconnected)')

class EventProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = 'events'
        self.producer = None
        self.metrics_port = 8000
        
        # Запуск HTTP сервера для метрик
        start_http_server(self.metrics_port)
        logger.info(f"Metrics server started on port {self.metrics_port}")
        
        self.connect_to_kafka()
    
    def connect_to_kafka(self):
        """Подключение к Kafka с повторными попытками"""
        max_retries = 30
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: str(k).encode('utf-8') if k else None,
                    batch_size=16384,
                    linger_ms=10,
                    retries=3
                )
                logger.info(f"Успешное подключение к Kafka: {self.bootstrap_servers}")
                KAFKA_CONNECTION_STATUS.set(1)
                return
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к Kafka не удалась: {e}")
                KAFKA_CONNECTION_STATUS.set(0)
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
    
    def generate_event(self):
        """Генерация события"""
        event_types = ['click', 'view', 'purchase', 'login', 'logout', 'search']
        users = [f'user_{i}' for i in range(1, 1001)]
        
        event = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'event_type': random.choice(event_types),
            'user_id': random.choice(users),
            'session_id': str(uuid.uuid4()),
            'page': f'/page_{random.randint(1, 100)}',
            'value': round(random.uniform(1, 1000), 2),
            'metadata': {
                'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                'os': random.choice(['Windows', 'MacOS', 'Linux', 'iOS', 'Android']),
                'country': random.choice(['US', 'UK', 'DE', 'FR', 'RU', 'CN', 'JP'])
            }
        }
        return event
    
    def send_event(self, event):
        """Отправка события в Kafka"""
        try:
            with EVENT_SEND_DURATION.time():
                future = self.producer.send(
                    self.topic,
                    key=event['user_id'],
                    value=event
                )
                # Не ждем результата для увеличения производительности
                EVENTS_SENT_TOTAL.inc()
                return True
        except KafkaError as e:
            logger.error(f"Ошибка отправки события: {e}")
            EVENTS_FAILED_TOTAL.inc()
            KAFKA_CONNECTION_STATUS.set(0)
            return False
    
    def run(self):
        """Основной цикл генерации событий"""
        logger.info("Начинаю генерацию событий со скоростью 100 событий/сек")
        
        events_sent = 0
        start_time = time.time()
        
        try:
            while True:
                batch_start = time.time()
                batch_events = 0
                
                # Отправляем 100 событий
                for i in range(100):
                    event = self.generate_event()
                    if self.send_event(event):
                        events_sent += 1
                        batch_events += 1
                    
                    # Небольшая задержка между событиями (0.01 сек = 10мс)
                    time.sleep(0.01)
                
                # Обновляем метрику events per second
                EVENTS_PER_SECOND.set(batch_events)
                
                # Вычисляем время выполнения батча
                batch_time = time.time() - batch_start
                
                # Логируем статистику каждые 10 секунд
                if events_sent % 1000 == 0:
                    elapsed = time.time() - start_time
                    rate = events_sent / elapsed
                    logger.info(f"Отправлено событий: {events_sent}, Скорость: {rate:.2f} событий/сек")
                
                # Если батч выполнился быстрее секунды, ждем
                if batch_time < 1.0:
                    time.sleep(1.0 - batch_time)
                    
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
        finally:
            KAFKA_CONNECTION_STATUS.set(0)
            if self.producer:
                self.producer.close()
                logger.info("Продюсер закрыт")

if __name__ == "__main__":
    producer = EventProducer()
    producer.run()