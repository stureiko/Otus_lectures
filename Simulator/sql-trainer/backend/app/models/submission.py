from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    sql_query: Mapped[str] = mapped_column(Text)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)   # JSON: columns + rows
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True) # None = только выполнен
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="submissions")
    task: Mapped["Task"] = relationship(back_populates="submissions")
