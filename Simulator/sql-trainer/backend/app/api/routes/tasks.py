import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_teacher
from app.core.schema_parser import parse_schema
from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TableColumn, TableSchema, TaskCreate, TaskDetail, TaskListItem, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskListItem])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Task).order_by(Task.order_num, Task.id))
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskDetail)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено.")

    # Парсим схему из DDL
    parsed = parse_schema(task.db_schema_sql)
    schema = [
        TableSchema(
            name=t.name,
            columns=[TableColumn(name=c.name, type=c.type) for c in t.columns],
        )
        for t in parsed
    ]

    return TaskDetail(
        id=task.id,
        title=task.title,
        description=task.description,
        difficulty=task.difficulty,
        topic=task.topic,
        order_num=task.order_num,
        hints=task.hints,
        order_matters=task.order_matters,
        db_schema=schema,
    )


@router.post("", response_model=TaskDetail, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    teacher: User = Depends(require_teacher),
):
    task = Task(
        title=data.title,
        description=data.description,
        difficulty=data.difficulty,
        topic=data.topic,
        order_num=data.order_num,
        reference_sql=data.reference_sql,
        db_schema_sql=data.db_schema_sql,
        db_seed_sql=data.db_seed_sql,
        order_matters=data.order_matters,
        hints=json.dumps(data.hints, ensure_ascii=False),
        created_by=teacher.id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return await get_task(task.id, db, teacher)


@router.put("/{task_id}", response_model=TaskDetail)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    teacher: User = Depends(require_teacher),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено.")

    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "hints":
            setattr(task, field, json.dumps(value, ensure_ascii=False))
        else:
            setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return await get_task(task.id, db, teacher)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    _teacher: User = Depends(require_teacher),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено.")
    await db.delete(task)
    await db.commit()
