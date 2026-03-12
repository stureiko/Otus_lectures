from datetime import datetime

from pydantic import BaseModel


class ProgressItem(BaseModel):
    task_id: int
    task_title: str
    solved: bool
    attempts_count: int
    first_solved_at: datetime | None

    model_config = {"from_attributes": True}


class LeaderboardItem(BaseModel):
    user_id: int
    user_name: str
    solved_count: int
    total_attempts: int
