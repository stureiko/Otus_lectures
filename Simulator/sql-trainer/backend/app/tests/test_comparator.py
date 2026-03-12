import pytest

from app.core.result_comparator import ResultComparator
from app.core.sql_executor import QueryResult

comparator = ResultComparator()


def make_result(columns, rows):
    return QueryResult(columns=columns, rows=rows)


class TestResultComparator:
    def test_exact_match_ordered(self):
        student = make_result(["id", "name"], [[1, "Alice"], [2, "Bob"]])
        reference = make_result(["id", "name"], [[1, "Alice"], [2, "Bob"]])
        result = comparator.compare(student, reference, order_matters=True)
        assert result.is_correct

    def test_wrong_order_strict(self):
        student = make_result(["id", "name"], [[2, "Bob"], [1, "Alice"]])
        reference = make_result(["id", "name"], [[1, "Alice"], [2, "Bob"]])
        result = comparator.compare(student, reference, order_matters=True)
        assert not result.is_correct

    def test_wrong_order_relaxed(self):
        student = make_result(["id", "name"], [[2, "Bob"], [1, "Alice"]])
        reference = make_result(["id", "name"], [[1, "Alice"], [2, "Bob"]])
        result = comparator.compare(student, reference, order_matters=False)
        assert result.is_correct

    def test_missing_row(self):
        student = make_result(["id"], [[1]])
        reference = make_result(["id"], [[1], [2]])
        result = comparator.compare(student, reference, order_matters=False)
        assert not result.is_correct
        assert any(d.status == "missing" for d in result.diff)

    def test_extra_row(self):
        student = make_result(["id"], [[1], [2], [3]])
        reference = make_result(["id"], [[1], [2]])
        result = comparator.compare(student, reference, order_matters=False)
        assert not result.is_correct
        assert any(d.status == "extra" for d in result.diff)

    def test_column_count_mismatch(self):
        student = make_result(["id"], [[1]])
        reference = make_result(["id", "name"], [[1, "Alice"]])
        result = comparator.compare(student, reference, order_matters=False)
        assert not result.is_correct
        assert "столбц" in result.message

    def test_duplicate_rows(self):
        student = make_result(["id"], [[1], [1]])
        reference = make_result(["id"], [[1], [1]])
        result = comparator.compare(student, reference, order_matters=False)
        assert result.is_correct
