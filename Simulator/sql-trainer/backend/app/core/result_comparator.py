from dataclasses import dataclass

from app.core.sql_executor import QueryResult


@dataclass
class DiffRow:
    row: list
    status: str  # "missing" | "extra"


@dataclass
class CompareResult:
    is_correct: bool
    diff: list[DiffRow]
    message: str


class ResultComparator:
    """
    Сравнивает результат студента с эталонным результатом.

    Поддерживает два режима:
      - order_matters=True  — строки должны совпадать по порядку
      - order_matters=False — порядок строк не важен (сравнение как множеств)
    """

    def compare(
        self,
        student: QueryResult,
        reference: QueryResult,
        order_matters: bool = False,
    ) -> CompareResult:
        # Проверяем структуру (количество колонок)
        if len(student.columns) != len(reference.columns):
            return CompareResult(
                is_correct=False,
                diff=[],
                message=(
                    f"Неверное количество столбцов: "
                    f"ожидается {len(reference.columns)}, "
                    f"получено {len(student.columns)}."
                ),
            )

        if order_matters:
            return self._compare_ordered(student, reference)
        return self._compare_unordered(student, reference)

    def _compare_ordered(
        self, student: QueryResult, reference: QueryResult
    ) -> CompareResult:
        diff = []
        max_len = max(len(student.rows), len(reference.rows))

        for i in range(max_len):
            if i >= len(reference.rows):
                diff.append(DiffRow(row=student.rows[i], status="extra"))
            elif i >= len(student.rows):
                diff.append(DiffRow(row=reference.rows[i], status="missing"))
            elif self._rows_equal(student.rows[i], reference.rows[i]):
                continue
            else:
                diff.append(DiffRow(row=reference.rows[i], status="missing"))
                diff.append(DiffRow(row=student.rows[i], status="extra"))

        is_correct = len(diff) == 0
        message = "Верно!" if is_correct else self._build_message(student, reference, diff)
        return CompareResult(is_correct=is_correct, diff=diff, message=message)

    def _compare_unordered(
        self, student: QueryResult, reference: QueryResult
    ) -> CompareResult:
        # Преобразуем строки в tuple для хранения в multiset
        ref_multiset: dict[tuple, int] = {}
        for row in reference.rows:
            key = tuple(str(v) for v in row)
            ref_multiset[key] = ref_multiset.get(key, 0) + 1

        stu_multiset: dict[tuple, int] = {}
        for row in student.rows:
            key = tuple(str(v) for v in row)
            stu_multiset[key] = stu_multiset.get(key, 0) + 1

        diff = []

        # Строки которых не хватает у студента
        for key, count in ref_multiset.items():
            stu_count = stu_multiset.get(key, 0)
            for _ in range(max(0, count - stu_count)):
                diff.append(DiffRow(row=list(key), status="missing"))

        # Лишние строки у студента
        for key, count in stu_multiset.items():
            ref_count = ref_multiset.get(key, 0)
            for _ in range(max(0, count - ref_count)):
                diff.append(DiffRow(row=list(key), status="extra"))

        is_correct = len(diff) == 0
        message = "Верно!" if is_correct else self._build_message(student, reference, diff)
        return CompareResult(is_correct=is_correct, diff=diff, message=message)

    @staticmethod
    def _rows_equal(row_a: list, row_b: list) -> bool:
        return all(str(a) == str(b) for a, b in zip(row_a, row_b))

    @staticmethod
    def _build_message(
        student: QueryResult, reference: QueryResult, diff: list[DiffRow]
    ) -> str:
        missing = sum(1 for d in diff if d.status == "missing")
        extra = sum(1 for d in diff if d.status == "extra")
        parts = []
        if len(student.rows) != len(reference.rows):
            parts.append(
                f"Ожидается {len(reference.rows)} строк, получено {len(student.rows)}."
            )
        if missing:
            parts.append(f"Не хватает {missing} строк.")
        if extra:
            parts.append(f"Лишних строк: {extra}.")
        return " ".join(parts) if parts else "Результат не совпадает с эталоном."
