import pytest

from app.core.query_validator import QueryValidationError, validate_query
from app.core.sql_executor import ExecutionError, SQLExecutor

SCHEMA = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);
"""

SEED = """
INSERT INTO users VALUES (1, 'Алиса', 25);
INSERT INTO users VALUES (2, 'Боб', 30);
INSERT INTO users VALUES (3, 'Карл', 22);
"""

executor = SQLExecutor()


class TestQueryValidator:
    def test_valid_select(self):
        validate_query("SELECT * FROM users")

    def test_valid_with_cte(self):
        validate_query("WITH t AS (SELECT id FROM users) SELECT * FROM t")

    def test_forbidden_drop(self):
        with pytest.raises(QueryValidationError, match="DROP"):
            validate_query("DROP TABLE users")

    def test_forbidden_delete(self):
        with pytest.raises(QueryValidationError, match="DELETE"):
            validate_query("DELETE FROM users")

    def test_forbidden_insert(self):
        with pytest.raises(QueryValidationError, match="INSERT"):
            validate_query("INSERT INTO users VALUES (4, 'test', 20)")

    def test_empty_query(self):
        with pytest.raises(QueryValidationError):
            validate_query("  ")

    def test_must_start_with_select(self):
        with pytest.raises(QueryValidationError):
            validate_query("EXPLAIN SELECT * FROM users")


class TestSQLExecutor:
    def test_basic_select(self):
        result = executor.execute("SELECT * FROM users", SCHEMA, SEED)
        assert result.row_count == 3
        assert "id" in result.columns

    def test_where_filter(self):
        result = executor.execute("SELECT name FROM users WHERE age > 24", SCHEMA, SEED)
        assert result.row_count == 2

    def test_syntax_error(self):
        with pytest.raises(ExecutionError):
            executor.execute("SELECT FROM", SCHEMA, SEED)

    def test_unknown_table(self):
        with pytest.raises(ExecutionError):
            executor.execute("SELECT * FROM nonexistent", SCHEMA, SEED)

    def test_forbidden_query_raises(self):
        with pytest.raises(ExecutionError):
            executor.execute("DROP TABLE users", SCHEMA, SEED)
