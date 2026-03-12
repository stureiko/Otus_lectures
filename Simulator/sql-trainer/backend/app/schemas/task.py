import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.models.task import Difficulty


class TaskListItem(BaseModel):
    id: int
    title: str
    difficulty: Difficulty
    topic: str
    order_num: int

    model_config = {"from_attributes": True}


class TableColumn(BaseModel):
    name: str
    type: str


class TableSchema(BaseModel):
    name: str
    columns: list[TableColumn]


class TaskDetail(BaseModel):
    id: int
    title: str
    description: str
    difficulty: Difficulty
    topic: str
    order_num: int
    hints: list[str]
    order_matters: bool
    # Алиас "schema" в JSON, Python-атрибут db_schema (избегаем конфликта с Pydantic)
    db_schema: list[TableSchema] = Field(default=[], alias="schema", serialization_alias="schema")

    model_config = {"from_attributes": True, "populate_by_name": True}

    @field_validator("hints", mode="before")
    @classmethod
    def parse_hints(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v or []


class TaskCreate(BaseModel):
    title: str
    description: str
    difficulty: Difficulty
    topic: str
    order_num: int = 0
    reference_sql: str
    db_schema_sql: str
    db_seed_sql: str
    order_matters: bool = False
    hints: list[str] = []


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    difficulty: Difficulty | None = None
    topic: str | None = None
    order_num: int | None = None
    reference_sql: str | None = None
    db_schema_sql: str | None = None
    db_seed_sql: str | None = None
    order_matters: bool | None = None
    hints: list[str] | None = None
