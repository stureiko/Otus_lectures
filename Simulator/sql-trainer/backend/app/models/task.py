import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty))
    topic: Mapped[str] = mapped_column(String(100))       # "SELECT", "JOIN", "GROUP BY", ...
    order_num: Mapped[int] = mapped_column(Integer, default=0)

    # Эталонное решение
    reference_sql: Mapped[str] = mapped_column(Text)

    # SQL для инициализации sandbox-базы данных
    db_schema_sql: Mapped[str] = mapped_column(Text)     # CREATE TABLE ...
    db_seed_sql: Mapped[str] = mapped_column(Text)       # INSERT INTO ...

    # Параметры сравнения
    order_matters: Mapped[bool] = mapped_column(Boolean, default=False)

    hints: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON-массив подсказок
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    submissions: Mapped[list["Submission"]] = relationship(back_populates="task")
    progress: Mapped[list["Progress"]] = relationship(back_populates="task")
