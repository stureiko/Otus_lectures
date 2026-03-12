import re

FORBIDDEN_KEYWORDS = {
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER",
    "TRUNCATE", "CREATE", "GRANT", "REVOKE", "ATTACH",
    "DETACH", "PRAGMA", "VACUUM", "REINDEX",
}


class QueryValidationError(Exception):
    pass


def validate_query(sql: str) -> None:
    """
    Проверяет, что запрос не содержит запрещённых операций.
    Разрешены только SELECT-запросы (и WITH ... SELECT).
    """
    cleaned = sql.strip()
    if not cleaned:
        raise QueryValidationError("Запрос не может быть пустым.")

    # Убираем строковые литералы и комментарии перед анализом
    normalized = _strip_literals_and_comments(cleaned).upper()

    # Проверяем запрещённые ключевые слова
    tokens = re.findall(r"\b[A-Z_]+\b", normalized)
    for token in tokens:
        if token in FORBIDDEN_KEYWORDS:
            raise QueryValidationError(
                f"Операция '{token}' запрещена. Допустимы только SELECT-запросы."
            )

    # Запрос должен начинаться с SELECT или WITH (CTE)
    first_token = tokens[0] if tokens else ""
    if first_token not in ("SELECT", "WITH"):
        raise QueryValidationError(
            "Запрос должен начинаться с SELECT (или WITH для CTE)."
        )


def _strip_literals_and_comments(sql: str) -> str:
    """Убирает строковые литералы и SQL-комментарии."""
    # Однострочные комментарии
    result = re.sub(r"--[^\n]*", " ", sql)
    # Многострочные комментарии
    result = re.sub(r"/\*.*?\*/", " ", result, flags=re.DOTALL)
    # Строковые литералы в кавычках
    result = re.sub(r"'[^']*'", "''", result)
    result = re.sub(r'"[^"]*"', '""', result)
    return result
