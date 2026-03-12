from pydantic import BaseModel


class ExecuteRequest(BaseModel):
    task_id: int
    sql: str


class QueryResult(BaseModel):
    columns: list[str]
    rows: list[list]
    row_count: int


class ExecuteResponse(BaseModel):
    success: bool
    result: QueryResult | None = None
    error: str | None = None


class ValidateRequest(BaseModel):
    task_id: int
    sql: str


class DiffRow(BaseModel):
    row: list
    status: str  # "missing" | "extra"


class ValidateResponse(BaseModel):
    is_correct: bool
    student_result: QueryResult | None = None
    error: str | None = None
    diff: list[DiffRow] = []
    message: str = ""
