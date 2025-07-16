# ClickHouse с кеширующим сервером

конфигурация:

1. контейнер с ClickHouse
2. Кеширующая БД например Redis
3. контейнер Kafka
4. Скрипт Python который генерирует поток сообщений в Kafka 100 событий в секунду который собирается в Redis и затем оттуда раз в секунду собирается в ClickHouse

# Система обработки событий с Kafka, Redis и ClickHouse + Мониторинг

Этот проект реализует систему обработки событий в реальном времени с использованием:
- **Kafka** - для потоковой передачи сообщений
- **Redis** - для кеширования и буферизации
- **ClickHouse** - для хранения и аналитики данных
- **Prometheus** - для сбора метрик
- **Grafana** - для визуализации метрик

## Архитектура

```
Producer (100 событий/сек) → Kafka → Consumer → Redis → ClickHouse
                ↓                ↓        ↓        ↓
            Prometheus ← Exporters ← Metrics ← Applications
                ↓
            Grafana Dashboard
```

## Мониторинг

### Компоненты мониторинга

1. **Prometheus** - сбор метрик с эндпоинтов
2. **Grafana** - визуализация метрик
3. **Exporters** - экспорт метрик из сервисов:
   - Redis Exporter
   - Kafka Exporter
   - ClickHouse Exporter
4. **Custom Metrics** - метрики из Python приложений

### Веб-интерфейсы

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

### Эндпоинты метрик

- **Producer**: http://localhost:8000/metrics
- **Consumer**: http://localhost:8001/metrics
- **Redis Exporter**: http://localhost:9121/metrics
- **Kafka Exporter**: http://localhost:9308/metrics
- **ClickHouse Exporter**: http://localhost:9116/metrics

## Быстрый старт

### Требования
- Docker и Docker Compose
- Make (опционально)

### Запуск

1. Клонируйте репозиторий и перейдите в папку проекта

2. Создайте структуру каталогов:
```bash
chmod +x setup-monitoring.sh
./setup-monitoring.sh
```

3. Создайте файлы из артефактов в соответствующие каталоги:
   - `prometheus/prometheus.yml`
   - `grafana/provisioning/datasources/prometheus.yml`
   - `grafana/provisioning/dashboards/dashboards.yml`
   - `grafana/dashboards/event-processing-dashboard.json`
   - `clickhouse/init.sql`

4. Запустите систему:
```bash
make up
```

Или без Make:
```bash
docker-compose up -d
```

5. Откройте мониторинг:
```bash
make monitoring
```

## Метрики

### Producer метрики

- `events_sent_total` - общее количество отправленных событий
- `events_failed_total` - количество неудачных отправок
- `event_send_duration_seconds` - время отправки события
- `events_per_second` - текущая скорость отправки
- `kafka_connection_status` - статус подключения к Kafka

### Consumer метрики

- `events_consumed_total` - общее количество полученных событий
- `events_cached_total` - количество событий в кеше Redis
- `events_written_total` - количество событий записанных в ClickHouse
- `kafka_consume_duration_seconds` - время чтения из Kafka
- `redis_write_duration_seconds` - время записи в Redis
- `clickhouse_write_duration_seconds` - время записи в ClickHouse
- `redis_queue_size` - размер очереди в Redis
- `events_in_batch` - количество событий в текущем батче

### Infrastructure метрики

- **Kafka**: consumer lag, throughput, partition metrics
- **Redis**: memory usage, connections, commands
- **ClickHouse**: query performance, table sizes, merges

## Дашборд Grafana

Дашборд включает следующие панели:

1. **Event Processing Rate** - скорость обработки событий
2. **Service Connection Status** - статус подключений к сервисам
3. **Queue and Batch Metrics** - метрики очередей и батчей
4. **Latency Metrics** - задержки операций
5. **Cumulative Event Counts** - общее количество событий
6. **Error Rate** - частота ошибок
7. **Kafka Consumer Lag** - задержка консьюмера
8. **Redis Memory Usage** - использование памяти Redis
9. **ClickHouse Query Statistics** - статистика запросов ClickHouse

## Алерты и уведомления

Для настройки алертов можно добавить правила в Prometheus:

```yaml
# prometheus/alerts.yml
groups:
  - name: event-processing
    rules:
      - alert: HighErrorRate
        expr: rate(events_failed_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} events per second"
      
      - alert: KafkaConsumerLag
        expr: kafka_consumer_lag_sum > 1000
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Kafka consumer lag is high"
          description: "Consumer lag is {{ $value }} messages"
```

## Производительность и масштабирование

### Мониторинг производительности

```bash
# Проверка текущей производительности
curl -s http://localhost:8000/metrics | grep events_per_second
curl -s http://localhost:8001/metrics | grep events_written_total

# Мониторинг ресурсов
docker stats

# Размер очереди Redis
docker exec -it redis redis-cli llen events_queue
```

### Оптимизация по метрикам

1. **Если высокая задержка записи в ClickHouse**:
   - Увеличьте размер батча
   - Добавьте больше consumer'ов

2. **Если растет размер очереди Redis**:
   - Уменьшите интервал батчевой обработки
   - Оптимизируйте запросы к ClickHouse

3. **Если высокий consumer lag в Kafka**:
   - Добавьте больше партиций
   - Увеличьте количество consumer'ов

## Структура проекта

```
.
├── docker-compose.yml              # Конфигурация всех сервисов
├── Dockerfile                      # Dockerfile для Python приложений
├── requirements.txt               # Python зависимости
├── producer.py                    # Генератор событий с метриками
├── consumer.py                    # Обработчик событий с метриками
├── setup-monitoring.sh            # Скрипт создания структуры каталогов
├── clickhouse/
│   └── init.sql                   # Инициализация ClickHouse
├── prometheus/
│   └── prometheus.yml             # Конфигурация Prometheus
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml     # Автоматическое подключение Prometheus
│   │   └── dashboards/
│   │       └── dashboards.yml     # Автоматическая загрузка дашбордов
│   └── dashboards/
│       └── event-processing-dashboard.json  # Основной дашборд
├── Makefile                       # Команды для управления
└── README.md                      # Документация
```

## Команды для мониторинга

```bash
# Запуск всех сервисов включая мониторинг
make up

# Открытие веб-интерфейсов мониторинга
make monitoring

# Просмотр логов
make logs

# Статус всех сервисов
make status

# Просмотр метрик напрямую
curl http://localhost:8000/metrics  # Producer
curl http://localhost:8001/metrics  # Consumer

# Проверка Prometheus targets
curl http://localhost:9090/api/v1/targets
```

## Troubleshooting мониторинга

### Grafana не показывает данные

1. Проверьте подключение к Prometheus:
   ```bash
   curl http://localhost:9090/api/v1/query?query=up
   ```

2. Проверьте targets в Prometheus:
   ```
   http://localhost:9090/targets
   ```

3. Проверьте логи Grafana:
   ```bash
   docker-compose logs grafana
   ```

### Prometheus не собирает метрики

1. Проверьте endpoints:
   ```bash
   curl http://localhost:8000/metrics
   curl http://localhost:8001/metrics
   ```

2. Проверьте конфигурацию:
   ```bash
   docker exec -it prometheus cat /etc/prometheus/prometheus.yml
   ```

### Экспортеры не работают

1. Проверьте подключения к сервисам:
   ```bash
   # Redis
   docker exec -it redis redis-cli ping
   
   # Kafka
   docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
   
   # ClickHouse
   docker exec -it clickhouse clickhouse-client --query "SELECT 1"
   ```

## Дополнительные возможности

### Добавление custom метрик

```python
from prometheus_client import Counter, Histogram, Gauge

# Создание метрик
CUSTOM_METRIC = Counter('custom_events_total', 'Custom events counter')

# Использование
CUSTOM_METRIC.inc()
```

### Экспорт в другие системы

Prometheus поддерживает экспорт в:
- **Grafana Cloud**
- **New Relic**
- **Datadog**
- **AWS CloudWatch**

### Горизонтальное масштабирование

```bash
# Запуск нескольких consumer'ов
docker-compose up -d --scale consumer=3

# Мониторинг нагрузки
docker-compose logs -f consumer
```

## Примеры запросов PromQL

```promql
# Средняя скорость обработки за последние 5 минут
rate(events_processed_total[5m])

# 95-й перцентиль времени записи в ClickHouse
histogram_quantile(0.95, rate(clickhouse_write_duration_seconds_bucket[5m]))

# Отношение успешных к общему количеству событий
rate(events_sent_total[1m]) / (rate(events_sent_total[1m]) + rate(events_failed_total[1m]))

# Прогнозирование заполнения очереди
predict_linear(redis_queue_size[1h], 3600)
```
# Просмотр топиков Kafka
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Просмотр сообщений в Kafka
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic events --from-beginning

# Статистика производителя
docker exec -it kafka kafka-run-class kafka.tools.JmxTool --object-name kafka.producer:type=producer-metrics,client-id=* --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi

# Информация о Redis
docker exec -it redis redis-cli info stats

# Статистика ClickHouse
docker exec -it clickhouse clickhouse-client --query "SELECT * FROM system.parts WHERE table = 'events'"
```

## Остановка и очистка

```bash
# Остановка всех сервисов
make down

# Полная очистка (включая volumes)
make clean
```

## Производительность

### Ожидаемые показатели

- **Производительность Producer**: 100 событий/секунду
- **Пропускная способность Kafka**: до 10K сообщений/секунду
- **Латентность Redis**: < 1мс
- **Пропускная способность ClickHouse**: до 1M записей/секунду

### Мониторинг производительности

```sql
-- Статистика событий по минутам
SELECT 
    toStartOfMinute(timestamp) as minute,
    count() as events_per_minute
FROM events 
WHERE timestamp > now() - INTERVAL 1 HOUR
GROUP BY minute 
ORDER BY minute DESC;

-- Топ активных пользователей
SELECT 
    user_id,
    count() as event_count,
    sum(value) as total_value
FROM events 
WHERE timestamp > now() - INTERVAL 1 HOUR
GROUP BY user_id 
ORDER BY event_count DESC 
LIMIT 10;

-- Распределение событий по типам
SELECT 
    event_type,
    count() as count,
    avg(value) as avg_value
FROM events 
GROUP BY event_type 
ORDER BY count DESC;
```

## Troubleshooting

### Проблемы с подключением

1. **Kafka недоступен**:
   - Проверьте логи: `docker-compose logs kafka`
   - Убедитесь, что Zookeeper запущен: `docker-compose logs zookeeper`

2. **Redis недоступен**:
   - Проверьте логи: `docker-compose logs redis`
   - Проверьте подключение: `docker exec -it redis redis-cli ping`

3. **ClickHouse недоступен**:
   - Проверьте логи: `docker-compose logs clickhouse`
   - Проверьте подключение: `docker exec -it clickhouse clickhouse-client --query "SELECT 1"`

### Проблемы с производительностью

1. **Низкая скорость обработки**:
   - Увеличьте `batch_size` в consumer.py
   - Добавьте больше партиций в Kafka
   - Запустите несколько экземпляров consumer

2. **Высокое потребление памяти**:
   - Уменьшите TTL в Redis
   - Настройте retention policy для Kafka
   - Оптимизируйте размер батчей

3. **Потеря данных**:
   - Проверьте логи consumer
   - Убедитесь в правильности конфигурации Kafka (replication factor)
   - Проверьте доступность всех сервисов

## Дополнительные возможности

### Добавление метрик

Для добавления метрик Prometheus можно расширить docker-compose.yml:

```yaml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Horizontal scaling

Для масштабирования можно использовать Kubernetes или Docker Swarm:

```bash
# Docker Swarm
docker stack deploy -c docker-compose.yml event-processing

# Kubernetes
kubectl apply -f k8s/
```

## Лицензия

MIT License

## Контакты

Если у вас есть вопросы или предложения, создайте issue в репозитории.
