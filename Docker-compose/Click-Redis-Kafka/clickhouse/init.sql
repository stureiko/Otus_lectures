-- Создание базы данных (если нужно)
CREATE DATABASE IF NOT EXISTS default;

-- Создание таблицы для событий
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
PARTITION BY toYYYYMM(timestamp);

-- Создание материализованного представления для агрегации по часам
CREATE MATERIALIZED VIEW IF NOT EXISTS events_hourly
ENGINE = SummingMergeTree()
ORDER BY (event_type, hour, user_id)
AS SELECT
    event_type,
    toStartOfHour(timestamp) as hour,
    user_id,
    count() as event_count,
    sum(value) as total_value
FROM events
GROUP BY event_type, hour, user_id;

-- Создание материализованного представления для агрегации по дням
CREATE MATERIALIZED VIEW IF NOT EXISTS events_daily
ENGINE = SummingMergeTree()
ORDER BY (event_type, day, country)
AS SELECT
    event_type,
    toDate(timestamp) as day,
    country,
    count() as event_count,
    sum(value) as total_value,
    uniq(user_id) as unique_users
FROM events
GROUP BY event_type, day, country;