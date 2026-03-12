import re
from dataclasses import dataclass


@dataclass
class TableColumn:
    name: str
    type: str


@dataclass
class TableSchema:
    name: str
    columns: list[TableColumn]


def parse_schema(db_schema_sql: str) -> list[TableSchema]:
    """
    Парсит DDL-скрипт и возвращает список таблиц с их колонками.
    Используется для отображения схемы БД во фронтенде.
    """
    tables = []
    # Ищем CREATE TABLE блоки
    pattern = re.compile(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"']?(\w+)[`\"']?\s*\(([^;]+)\)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(db_schema_sql):
        table_name = match.group(1)
        body = match.group(2)
        columns = _parse_columns(body)
        tables.append(TableSchema(name=table_name, columns=columns))
    return tables


def _parse_columns(body: str) -> list[TableColumn]:
    columns = []
    for line in body.split(","):
        line = line.strip()
        if not line:
            continue
        # Пропускаем constraint-строки
        upper = line.upper()
        if any(upper.startswith(kw) for kw in ("PRIMARY", "FOREIGN", "UNIQUE", "CHECK", "CONSTRAINT")):
            continue
        # Извлекаем имя и тип
        parts = line.split()
        if len(parts) >= 2:
            col_name = parts[0].strip('`"\'')
            col_type = parts[1].strip('`"\',()')
            columns.append(TableColumn(name=col_name, type=col_type))
    return columns
