import sqlite3
import threading
from dataclasses import dataclass

from app.config import settings
from app.core.query_validator import QueryValidationError, validate_query


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[list]

    @property
    def row_count(self) -> int:
        return len(self.rows)


class ExecutionError(Exception):
    pass


class ExecutionTimeoutError(ExecutionError):
    pass


class SQLExecutor:
    """
    Выполняет SQL-запросы студента в изолированной in-memory SQLite базе.
    Для каждого запроса создаётся и уничтожается отдельное соединение.
    """

    def __init__(self):
        self.timeout = settings.SANDBOX_TIMEOUT_SEC
        self.max_rows = settings.SANDBOX_MAX_ROWS

    def execute(
        self,
        sql: str,
        db_schema_sql: str,
        db_seed_sql: str,
        validate: bool = True,
    ) -> QueryResult:
        """
        Инициализирует sandbox-базу, выполняет запрос и возвращает результат.
        """
        if validate:
            try:
                validate_query(sql)
            except QueryValidationError as e:
                raise ExecutionError(str(e))

        result: QueryResult | None = None
        exception: Exception | None = None

        def _run():
            nonlocal result, exception
            try:
                conn = sqlite3.connect(":memory:", check_same_thread=False)
                conn.row_factory = sqlite3.Row
                try:
                    # Инициализируем схему и данные задачи
                    conn.executescript(db_schema_sql)
                    conn.executescript(db_seed_sql)

                    cursor = conn.execute(sql)
                    columns = [desc[0] for desc in cursor.description or []]
                    rows = [list(row) for row in cursor.fetchmany(self.max_rows)]
                    result = QueryResult(columns=columns, rows=rows)
                finally:
                    conn.close()
            except Exception as e:
                exception = e

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=self.timeout)

        if thread.is_alive():
            raise ExecutionTimeoutError(
                f"Запрос выполняется дольше {self.timeout} секунд. "
                "Проверьте запрос на наличие бесконечных циклов или тяжёлых операций."
            )

        if exception:
            # Оборачиваем sqlite-ошибки в понятное сообщение
            raise ExecutionError(str(exception))

        return result
