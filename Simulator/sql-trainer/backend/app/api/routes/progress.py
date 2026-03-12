from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.progress import Progress
from app.models.task import Task
from app.models.user import User
from app.schemas.progress import LeaderboardItem, ProgressItem

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=list[ProgressItem])
async def get_my_progress(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Progress)
        .options(selectinload(Progress.task))
        .where(Progress.user_id == user.id)
        .order_by(Progress.task_id)
    )
    items = result.scalars().all()
    return [
        ProgressItem(
            task_id=p.task_id,
            task_title=p.task.title,
            solved=p.solved,
            attempts_count=p.attempts_count,
            first_solved_at=p.first_solved_at,
        )
        for p in items
    ]


@router.get("/leaderboard", response_model=list[LeaderboardItem])
async def get_leaderboard(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(
            User.id,
            User.name,
            func.count(Progress.id).filter(Progress.solved == True).label("solved_count"),
            func.sum(Progress.attempts_count).label("total_attempts"),
        )
        .join(Progress, Progress.user_id == User.id, isouter=True)
        .group_by(User.id, User.name)
        .order_by(func.count(Progress.id).filter(Progress.solved == True).desc())
        .limit(50)
    )
    rows = result.all()
    return [
        LeaderboardItem(
            user_id=row.id,
            user_name=row.name,
            solved_count=row.solved_count or 0,
            total_attempts=int(row.total_attempts or 0),
        )
        for row in rows
    ]
