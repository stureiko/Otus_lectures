from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text

from app.api.routes import auth, execute, progress, tasks, teacher
from app.config import settings
from app.db.session import AsyncSessionLocal, Base, engine
from app.models import Task, User
from app.models.user import UserRole
from app.core.security import hash_password


async def _seed_initial_data() -> None:
    """Заполняет базу начальными данными если она пустая."""
    from app.db.seed.tasks import TASKS
    from app.models.task import Difficulty

    async with AsyncSessionLocal() as db:
        # Создаём учётную запись преподавателя по умолчанию
        result = await db.execute(select(User).where(User.email == "teacher@example.com"))
        teacher = result.scalar_one_or_none()
        if not teacher:
            teacher = User(
                email="teacher@example.com",
                name="Преподаватель",
                hashed_password=hash_password("teacher123"),
                role=UserRole.teacher,
            )
            db.add(teacher)
            await db.flush()

        # Добавляем задания если их нет
        result = await db.execute(select(Task))
        if not result.scalars().first():
            for t in TASKS:
                task = Task(
                    title=t["title"],
                    description=t["description"],
                    difficulty=Difficulty(t["difficulty"]),
                    topic=t["topic"],
                    order_num=t["order_num"],
                    reference_sql=t["reference_sql"],
                    db_schema_sql=t["db_schema_sql"],
                    db_seed_sql=t["db_seed_sql"],
                    order_matters=t["order_matters"],
                    hints=t["hints"],
                    created_by=teacher.id,
                )
                db.add(task)

        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы и заполняем начальными данными
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await _seed_initial_data()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(execute.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
