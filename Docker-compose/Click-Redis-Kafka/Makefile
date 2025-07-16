.PHONY: help build up down logs clean status test-kafka test-redis test-clickhouse monitoring

help:
	@echo "Доступные команды:"
	@echo "  build      - Сборка Docker образов"
	@echo "  up         - Запуск всех сервисов"
	@echo "  down       - Остановка всех сервисов"
	@echo "  logs       - Просмотр логов"
	@echo "  clean      - Очистка volumes и образов"
	@echo "  status     - Статус сервисов"
	@echo "  test-kafka - Тест подключения к Kafka"
	@echo "  test-redis - Тест подключения к Redis"
	@echo "  test-clickhouse - Тест подключения к ClickHouse"
	@echo "  monitoring - Открыть веб-интерфейсы мониторинга"

build:
	@echo "Сборка Docker образов..."
	mkdir -p clickhouse prometheus grafana/provisioning/datasources grafana/provisioning/dashboards grafana/dashboards
	docker-compose build

up:
	@echo "Запуск всех сервисов..."
	mkdir -p clickhouse prometheus grafana/provisioning/datasources grafana/provisioning/dashboards grafana/dashboards
	docker-compose up -d
	@echo "Ожидание запуска сервисов..."
	sleep 30
	@echo "Проверка статуса сервисов..."
	docker-compose ps

down:
	@echo "Остановка всех сервисов..."
	docker-compose down

logs:
	@echo "Просмотр логов всех сервисов..."
	docker-compose logs -f

clean:
	@echo "Остановка и очистка..."
	docker-compose down -v
	docker system prune -f

status:
	@echo "Статус сервисов:"
	docker-compose ps

test-kafka:
	@echo "Тест подключения к Kafka..."
	docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
	docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic events --partitions 3 --replication-factor 1 --if-not-exists

test-redis:
	@echo "Тест подключения к Redis..."
	docker exec -it redis redis-cli ping

test-clickhouse:
	@echo "Тест подключения к ClickHouse..."
	docker exec -it clickhouse clickhouse-client --query "SELECT version()"
	docker exec -it clickhouse clickhouse-client --query "SHOW TABLES"

monitoring:
	@echo "Открываем веб-интерфейсы мониторинга:"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Metrics endpoints:"
	@echo "  Producer: http://localhost:8000/metrics"
	@echo "  Consumer: http://localhost:8001/metrics"
	@echo "  Redis Exporter: http://localhost:9121/metrics"
	@echo "  Kafka Exporter: http://localhost:9308/metrics"
	@echo "  ClickHouse Exporter: http://localhost:9116/metrics"
	@if command -v xdg-open > /dev/null; then \
		xdg-open http://localhost:3000; \
	elif command -v open > /dev/null; then \
		open http://localhost:3000; \
	else \
		echo "Откройте http://localhost:3000 в браузере"; \
	fi clickhouse-client --query "SHOW TABLES"