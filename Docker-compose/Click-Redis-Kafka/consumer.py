#!/usr/bin/env python3
import json
import time
import threading
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import redis
from clickhouse_driver import Client
import os
import logging
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus метрики
EVENTS_CONSUMED_TOTAL = Counter('events_consumed_total', 'Total number of events consumed from Kafka')
EVENTS_CACHED_TOTAL = Counter('events_cached_total', 'Total number of events cached in Redis')
EVENTS_WRITTEN_TOTAL = Counter('events_written_total', 'Total number of events written to ClickHouse')
EVENTS_FAILED_TOTAL = Counter('events_failed_total', 'Total number of failed events')

KAFKA_CONSUME_DURATION = Histogram('kafka_consume_duration_seconds', 'Time spent consuming from Kafka')
REDIS_WRITE_DURATION = Histogram('redis_write_duration_seconds', 'Time spent writing to Redis')
CLICKHOUSE_WRITE_DURATION = Histogram('clickhouse_write_duration_seconds', 'Time spent writing to ClickHouse')

KAFKA_CONNECTION_STATUS = Gauge('kafka_connection_status', 'Kafka connection status (1=connected, 0=disconnected)')
REDIS_CONNECTION_STATUS = Gauge('redis_connection_status', 'Redis connection status (1=connected, 0=disconnected)')
CLICKHOUSE_CONNECTION_STATUS = Gauge('clickhouse_connection_status', 'ClickHouse connection status (1=connected, 0=disconnected)')

REDIS_QUEUE_SIZE = Gauge('redis_queue_size', 'Current size of Redis events queue')
EVENTS_IN_BATCH = Gauge('events_in_batch', 'Number of events in current batch')

class EventConsumer:
    def __init__(self):
        # Kafka настройки
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = 'events'
        self.consumer = None
        
        # Redis настройки
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.redis_client = None
        
        # ClickHouse настройки
        self.clickhouse_host = os.getenv('CLICKHOUSE_HOST', 'localhost')
        self.clickhouse_port = int(os.getenv('CLICKHOUSE_PORT', '8123'))
        self.clickhouse_client = None
        
        # Флаг для остановки потоков
        self.stop_event = threading.Event()
        
        # Запуск HTTP сервера для метрик
        self.metrics_port = 8001
        start_http_server(self.metrics_port)
        logger.info(f"Metrics server started on port {self.metrics_port}")
        
        self.connect_to_services()
        self.setup_clickhouse()
    
    def connect_to_services(self):
        """Подключение ко всем сервисам"""
        max_retries = 30
        retry_delay = 2
        
        # Подключение к Redis
        for attempt in range(max_retries):
            try:
                self.redis_client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    decode_responses=True
                )
                self.redis_client.ping()
                logger.info(f"Успешное подключение к Redis: {self.redis_host}:{self.redis_port}")
                REDIS_CONNECTION_STATUS.set(1)
                break
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к Redis не удалась: {e}")
                REDIS_CONNECTION_STATUS.set(0)
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
        
        # Подключение к ClickHouse
        for attempt in range(max_retries):
            try:
                self.clickhouse_client = Client(
                    host=self.clickhouse_host,
                    port=9000,
                    user='default',
                    password='',
                    database='default'
                )
                self.clickhouse_client.execute('SELECT 1')
                logger.info(f"Успешное подключение к ClickHouse: {self.clickhouse_host}:9000")
                CLICKHOUSE_CONNECTION_STATUS.set(1)
                break
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к ClickHouse не удалась: {e}")
                CLICKHOUSE_CONNECTION_STATUS.set(0)
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
        
        # Подключение к Kafka
        for attempt in range(max_retries):
            try:
                self.consumer = KafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.bootstrap_servers,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    key_deserializer=lambda k: k.decode('utf-8') if k else None,
                    group_id='event_consumer_group',
                    auto_offset_reset='latest',
                    enable_auto_commit=True,
                    auto_commit_interval_ms=1000,
                    consumer_timeout_ms=1000
                )
                logger.info(f"Успешное подключение к Kafka: {self.bootstrap_servers}")
                KAFKA_CONNECTION_STATUS.set(1)
                break
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к Kafka не удалась: {e}")
                KAFKA_CONNECTION_STATUS.set(0)
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
    
    def setup_clickhouse(self):
        """Создание таблицы в ClickHouse"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS events (
            id String,
            timestamp DateTime,
            event_type String,
            user_id String,
            session_id String,
            page String,
            value Float64,
            browser String,
            os String,
            country String,
            ingestion_time DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp, user_id)
        """
        
        try:
            self.clickhouse_client.execute(create_table_query)
            logger.info("Таблица events создана или уже существует в ClickHouse")
        except Exception as e:
            logger.error(f"Ошибка создания таблицы: {e}")
            raise
    
    def kafka_to_redis_worker(self):
        """Поток для чтения из Kafka и записи в Redis"""
        logger.info("Запущен поток Kafka -> Redis")
        events_processed = 0
        
        try:
            while not self.stop_event.is_set():
                try:
                    # Получаем сообщения из Kafka
                    with KAFKA_CONSUME_DURATION.time():
                        msg_pack = self.consumer.poll(timeout_ms=1000)
                    
                    for tp, messages in msg_pack.items():
                        for message in messages:
                            try:
                                event = message.value
                                EVENTS_CONSUMED_TOTAL.inc()
                                
                                # Сохраняем в Redis с TTL (время жизни 3600 сек = 1 час)
                                with REDIS_WRITE_DURATION.time():
                                    redis_key = f"event:{event['id']}"
                                    self.redis_client.setex(
                                        redis_key, 
                                        3600, 
                                        json.dumps(event)
                                    )
                                    
                                    # Добавляем в список для батчевой обработки
                                    self.redis_client.lpush('events_queue', json.dumps(event))
                                    EVENTS_CACHED_TOTAL.inc()
                                
                                events_processed += 1
                                
                                # Обновляем размер очереди
                                queue_size = self.redis_client.llen('events_queue')
                                REDIS_QUEUE_SIZE.set(queue_size)
                                
                                if events_processed % 1000 == 0:
                                    logger.info(f"Обработано событий Kafka->Redis: {events_processed}")
                                    
                            except Exception as e:
                                logger.error(f"Ошибка обработки сообщения: {e}")
                                EVENTS_FAILED_TOTAL.inc()
                                
                except Exception as e:
                    logger.error(f"Ошибка чтения из Kafka: {e}")
                    KAFKA_CONNECTION_STATUS.set(0)
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"Критическая ошибка в потоке Kafka->Redis: {e}")
    
    def redis_to_clickhouse_worker(self):
        """Поток для чтения из Redis и записи в ClickHouse"""
        logger.info("Запущен поток Redis -> ClickHouse")
        batch_size = 1000
        
        try:
            while not self.stop_event.is_set():
                try:
                    # Получаем батч событий из Redis
                    batch = []
                    for _ in range(batch_size):
                        event_data = self.redis_client.rpop('events_queue')
                        if event_data:
                            batch.append(json.loads(event_data))
                        else:
                            break
                    
                    if batch:
                        EVENTS_IN_BATCH.set(0)
                    
                    # Спим 1 секунду перед следующим батчем
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Ошибка записи в ClickHouse: {e}")
                    CLICKHOUSE_CONNECTION_STATUS.set(0)
                    EVENTS_FAILED_TOTAL.inc()
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"Критическая ошибка в потоке Redis->ClickHouse: {e}")
    
    def run(self):
        """Запуск всех потоков"""
        logger.info("Запуск консьюмера событий")
        
        # Создаем и запускаем потоки
        kafka_thread = threading.Thread(target=self.kafka_to_redis_worker)
        clickhouse_thread = threading.Thread(target=self.redis_to_clickhouse_worker)
        
        kafka_thread.start()
        clickhouse_thread.start()
        
        try:
            # Ждем завершения потоков
            kafka_thread.join()
            clickhouse_thread.join()
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
        finally:
            self.stop_event.set()
            KAFKA_CONNECTION_STATUS.set(0)
            REDIS_CONNECTION_STATUS.set(0)
            CLICKHOUSE_CONNECTION_STATUS.set(0)
            if self.consumer:
                self.consumer.close()
            if self.redis_client:
                self.redis_client.close()
            if self.clickhouse_client:
                self.clickhouse_client.disconnect()
            logger.info("Консьюмер остановлен")

if __name__ == "__main__":
    consumer = EventConsumer()
    consumer.run().set(len(batch))
                        
                        # Подготавливаем данные для ClickHouse
                        clickhouse_data = []
                        for event in batch:
                            clickhouse_data.append([
                                event['id'],
                                datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00')),
                                event['event_type'],
                                event['user_id'],
                                event['session_id'],
                                event['page'],
                                event['value'],
                                event['metadata']['browser'],
                                event['metadata']['os'],
                                event['metadata']['country']
                            ])
                        
                        # Вставляем данные в ClickHouse
                        with CLICKHOUSE_WRITE_DURATION.time():
                            self.clickhouse_client.execute(
                                """
                                INSERT INTO events 
                                (id, timestamp, event_type, user_id, session_id, page, value, browser, os, country)
                                VALUES
                                """,
                                clickhouse_data
                            )
                        
                        EVENTS_WRITTEN_TOTAL.inc(len(batch))
                        logger.info(f"Записано {len(batch)} событий в ClickHouse")
                        
                        # Обновляем размер очереди
                        queue_size = self.redis_client.llen('events_queue')
                        REDIS_QUEUE_SIZE.set(queue_size)
                    else:
                        EVENTS_IN_BATCH#!/usr/bin/env python3
import json
import time
import threading
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import redis
from clickhouse_driver import Client
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EventConsumer:
    def __init__(self):
        # Kafka настройки
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = 'events'
        self.consumer = None
        
        # Redis настройки
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.redis_client = None
        
        # ClickHouse настройки
        self.clickhouse_host = os.getenv('CLICKHOUSE_HOST', 'localhost')
        self.clickhouse_port = int(os.getenv('CLICKHOUSE_PORT', '8123'))
        self.clickhouse_client = None
        
        # Флаг для остановки потоков
        self.stop_event = threading.Event()
        
        self.connect_to_services()
        self.setup_clickhouse()
    
    def connect_to_services(self):
        """Подключение ко всем сервисам"""
        max_retries = 30
        retry_delay = 2
        
        # Подключение к Redis
        for attempt in range(max_retries):
            try:
                self.redis_client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    decode_responses=True
                )
                self.redis_client.ping()
                logger.info(f"Успешное подключение к Redis: {self.redis_host}:{self.redis_port}")
                break
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к Redis не удалась: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
        
        # Подключение к ClickHouse
        for attempt in range(max_retries):
            try:
                self.clickhouse_client = Client(
                    host=self.clickhouse_host,
                    port=9000,
                    user='default',
                    password='',
                    database='default'
                )
                self.clickhouse_client.execute('SELECT 1')
                logger.info(f"Успешное подключение к ClickHouse: {self.clickhouse_host}:9000")
                break
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к ClickHouse не удалась: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
        
        # Подключение к Kafka
        for attempt in range(max_retries):
            try:
                self.consumer = KafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.bootstrap_servers,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    key_deserializer=lambda k: k.decode('utf-8') if k else None,
                    group_id='event_consumer_group',
                    auto_offset_reset='latest',
                    enable_auto_commit=True,
                    auto_commit_interval_ms=1000,
                    consumer_timeout_ms=1000
                )
                logger.info(f"Успешное подключение к Kafka: {self.bootstrap_servers}")
                break
            except Exception as e:
                logger.error(f"Попытка {attempt + 1}/{max_retries} подключения к Kafka не удалась: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise
    
    def setup_clickhouse(self):
        """Создание таблицы в ClickHouse"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS events (
            id String,
            timestamp DateTime,
            event_type String,
            user_id String,
            session_id String,
            page String,
            value Float64,
            browser String,
            os String,
            country String,
            ingestion_time DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp, user_id)
        """
        
        try:
            self.clickhouse_client.execute(create_table_query)
            logger.info("Таблица events создана или уже существует в ClickHouse")
        except Exception as e:
            logger.error(f"Ошибка создания таблицы: {e}")
            raise
    
    def kafka_to_redis_worker(self):
        """Поток для чтения из Kafka и записи в Redis"""
        logger.info("Запущен поток Kafka -> Redis")
        events_processed = 0
        
        try:
            while not self.stop_event.is_set():
                try:
                    # Получаем сообщения из Kafka
                    msg_pack = self.consumer.poll(timeout_ms=1000)
                    
                    for tp, messages in msg_pack.items():
                        for message in messages:
                            try:
                                event = message.value
                                
                                # Сохраняем в Redis с TTL (время жизни 3600 сек = 1 час)
                                redis_key = f"event:{event['id']}"
                                self.redis_client.setex(
                                    redis_key, 
                                    3600, 
                                    json.dumps(event)
                                )
                                
                                # Добавляем в список для батчевой обработки
                                self.redis_client.lpush('events_queue', json.dumps(event))
                                
                                events_processed += 1
                                
                                if events_processed % 1000 == 0:
                                    logger.info(f"Обработано событий Kafka->Redis: {events_processed}")
                                    
                            except Exception as e:
                                logger.error(f"Ошибка обработки сообщения: {e}")
                                
                except Exception as e:
                    logger.error(f"Ошибка чтения из Kafka: {e}")
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"Критическая ошибка в потоке Kafka->Redis: {e}")
    
    def redis_to_clickhouse_worker(self):
        """Поток для чтения из Redis и записи в ClickHouse"""
        logger.info("Запущен поток Redis -> ClickHouse")
        batch_size = 1000
        
        try:
            while not self.stop_event.is_set():
                try:
                    # Получаем батч событий из Redis
                    batch = []
                    for _ in range(batch_size):
                        event_data = self.redis_client.rpop('events_queue')
                        if event_data:
                            batch.append(json.loads(event_data))
                        else:
                            break
                    
                    if batch:
                        # Подготавливаем данные для ClickHouse
                        clickhouse_data = []
                        for event in batch:
                            clickhouse_data.append([
                                event['id'],
                                datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00')),
                                event['event_type'],
                                event['user_id'],
                                event['session_id'],
                                event['page'],
                                event['value'],
                                event['metadata']['browser'],
                                event['metadata']['os'],
                                event['metadata']['country']
                            ])
                        
                        # Вставляем данные в ClickHouse
                        self.clickhouse_client.execute(
                            """
                            INSERT INTO events 
                            (id, timestamp, event_type, user_id, session_id, page, value, browser, os, country)
                            VALUES
                            """,
                            clickhouse_data
                        )
                        
                        logger.info(f"Записано {len(batch)} событий в ClickHouse")
                    
                    # Спим 1 секунду перед следующим батчем
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Ошибка записи в ClickHouse: {e}")
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"Критическая ошибка в потоке Redis->ClickHouse: {e}")
    
    def run(self):
        """Запуск всех потоков"""
        logger.info("Запуск консьюмера событий")
        
        # Создаем и запускаем потоки
        kafka_thread = threading.Thread(target=self.kafka_to_redis_worker)
        clickhouse_thread = threading.Thread(target=self.redis_to_clickhouse_worker)
        
        kafka_thread.start()
        clickhouse_thread.start()
        
        try:
            # Ждем завершения потоков
            kafka_thread.join()
            clickhouse_thread.join()
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
        finally:
            self.stop_event.set()
            if self.consumer:
                self.consumer.close()
            if self.redis_client:
                self.redis_client.close()
            if self.clickhouse_client:
                self.clickhouse_client.disconnect()
            logger.info("Консьюмер остановлен")

if __name__ == "__main__":
    consumer = EventConsumer()
    consumer.run()