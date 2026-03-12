import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.result_comparator import ResultComparator
from app.core.sql_executor import ExecutionError, ExecutionTimeoutError, QueryResult, SQLExecutor
from app.db.session import get_db
from app.models.progress import Progress
from app.models.submission import Submission
from app.models.task import Task
from app.models.user import User
from app.schemas.execution import (
    DiffRow,
    ExecuteRequest,
    ExecuteResponse,
    QueryResult as QueryResultSchema,
    ValidateRequest,
    ValidateResponse,
)

router = APIRouter(tags=["execution"])

executor = SQLExecutor()
comparator = ResultComparator()


def _to_schema(result: QueryResult) -> QueryResultSchema:
    return QueryResultSchema(
        columns=result.columns,
        rows=result.rows,
        row_count=result.row_count,
    )


async def _get_task_or_404(task_id: int, db: AsyncSession) -> Task:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено.")
    return task


async def _update_progress(
    db: AsyncSession, user_id: int, task_id: int, is_correct: bool
) -> None:
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user_id, Progress.task_id == task_id
        )
    )
    progress = result.scalar_one_or_none()
    if progress is None:
        progress = Progress(user_id=user_id, task_id=task_id, attempts_count=0, solved=False)
        db.add(progress)

    progress.attempts_count = (progress.attempts_count or 0) + 1
    if is_correct and not (progress.solved or False):
        from datetime import datetime, timezone
        progress.solved = True
        progress.first_solved_at = datetime.now(timezone.utc)

    await db.commit()


@router.post("/execute", response_model=ExecuteResponse)
async def execute_sql(
    data: ExecuteRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Выполняет SQL-запрос студента и возвращает результат без проверки."""
    task = await _get_task_or_404(data.task_id, db)

    try:
        result = executor.execute(data.sql, task.db_schema_sql, task.db_seed_sql)
    except ExecutionTimeoutError as e:
        # Сохраняем попытку
        db.add(Submission(user_id=user.id, task_id=task.id,
                          sql_query=data.sql, error_message=str(e)))
        await db.commit()
        return ExecuteResponse(success=False, error=str(e))
    except ExecutionError as e:
        db.add(Submission(user_id=user.id, task_id=task.id,
                          sql_query=data.sql, error_message=str(e)))
        await db.commit()
        return ExecuteResponse(success=False, error=str(e))

    # Сохраняем попытку
    db.add(Submission(
        user_id=user.id,
        task_id=task.id,
        sql_query=data.sql,
        result_json=json.dumps({"columns": result.columns, "rows": result.rows}),
    ))
    await db.commit()

    return ExecuteResponse(success=True, result=_to_schema(result))


@router.post("/validate", response_model=ValidateResponse)
async def validate_sql(
    data: ValidateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Выполняет SQL студента, сравнивает с эталоном и возвращает результат проверки."""
    task = await _get_task_or_404(data.task_id, db)

    # Выполняем запрос студента
    try:
        student_result = executor.execute(data.sql, task.db_schema_sql, task.db_seed_sql)
    except (ExecutionError, ExecutionTimeoutError) as e:
        db.add(Submission(user_id=user.id, task_id=task.id,
                          sql_query=data.sql, is_correct=False, error_message=str(e)))
        await _update_progress(db, user.id, task.id, is_correct=False)
        return ValidateResponse(is_correct=False, error=str(e),
                                message="Ошибка выполнения запроса.")

    # Выполняем эталонный запрос
    try:
        reference_result = executor.execute(
            task.reference_sql, task.db_schema_sql, task.db_seed_sql, validate=False
        )
    except (ExecutionError, ExecutionTimeoutError) as e:
        return ValidateResponse(
            is_correct=False,
            error=f"Ошибка в эталонном запросе задачи: {e}",
            message="Ошибка конфигурации задания. Обратитесь к преподавателю.",
        )

    # Сравниваем
    compare = comparator.compare(student_result, reference_result, task.order_matters)

    # Сохраняем попытку
    db.add(Submission(
        user_id=user.id,
        task_id=task.id,
        sql_query=data.sql,
        result_json=json.dumps({"columns": student_result.columns, "rows": student_result.rows}),
        is_correct=compare.is_correct,
    ))
    await _update_progress(db, user.id, task.id, is_correct=compare.is_correct)

    return ValidateResponse(
        is_correct=compare.is_correct,
        student_result=_to_schema(student_result),
        diff=[DiffRow(row=d.row, status=d.status) for d in compare.diff],
        message=compare.message,
    )
