"""
Эндпоинты для преподавателей:
  POST /api/teacher/sandbox      — протестировать SQL против произвольной схемы/данных
  GET  /api/teacher/tasks/{id}   — получить полные данные задачи (включая SQL-поля)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_teacher
from app.core.sql_executor import ExecutionError, ExecutionTimeoutError, SQLExecutor
from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.execution import ExecuteResponse, QueryResult as QueryResultSchema
from app.schemas.task import TaskCreate

router = APIRouter(prefix="/teacher", tags=["teacher"])
executor = SQLExecutor()


@router.get("/tasks/{task_id}", response_model=TaskCreate)
async def get_task_full(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    _teacher: User = Depends(require_teacher),
):
    """Возвращает полные данные задачи включая SQL-поля (только для преподавателей)."""
    import json
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено.")
    hints = json.loads(task.hints) if isinstance(task.hints, str) else (task.hints or [])
    return TaskCreate(
        title=task.title,
        description=task.description,
        difficulty=task.difficulty,
        topic=task.topic,
        order_num=task.order_num,
        reference_sql=task.reference_sql,
        db_schema_sql=task.db_schema_sql,
        db_seed_sql=task.db_seed_sql,
        order_matters=task.order_matters,
        hints=hints,
    )


class SandboxRequest(BaseModel):
    schema_sql: str
    seed_sql: str
    sql: str
    validate_safety: bool = True   # False — разрешить DDL для проверки схемы/seed


@router.post("/sandbox", response_model=ExecuteResponse)
async def run_sandbox(
    data: SandboxRequest,
    _teacher: User = Depends(require_teacher),
):
    """
    Выполняет произвольный SQL в in-memory SQLite с заданной схемой и данными.
    Используется в форме создания задачи для проверки reference_sql.
    """
    try:
        result = executor.execute(
            data.sql,
            data.schema_sql,
            data.seed_sql,
            validate=data.validate_safety,
        )
    except ExecutionTimeoutError as e:
        return ExecuteResponse(success=False, error=str(e))
    except ExecutionError as e:
        return ExecuteResponse(success=False, error=str(e))

    return ExecuteResponse(
        success=True,
        result=QueryResultSchema(
            columns=result.columns,
            rows=result.rows,
            row_count=result.row_count,
        ),
    )
