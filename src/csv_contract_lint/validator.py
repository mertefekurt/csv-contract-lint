from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .types import compatible_type, is_nullish, parse_value


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_csv(
    csv_path: str | Path,
    contract: dict[str, Any],
    *,
    null_drift: float = 0.15,
    allow_extra_columns: bool = False,
) -> ValidationResult:
    result = ValidationResult()
    expected_columns = {column["name"]: column for column in contract.get("columns", [])}
    observed_nulls = {name: 0 for name in expected_columns}
    observed_rows = 0

    with Path(csv_path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        _validate_headers(headers, expected_columns, allow_extra_columns, result)

        for row_number, row in enumerate(reader, start=2):
            observed_rows += 1
            _validate_row(row_number, row, expected_columns, observed_nulls, result)

    _validate_null_drift(observed_rows, observed_nulls, expected_columns, null_drift, result)
    return result


def _validate_headers(
    headers: list[str],
    expected_columns: dict[str, dict[str, Any]],
    allow_extra_columns: bool,
    result: ValidationResult,
) -> None:
    observed = set(headers)
    expected = set(expected_columns)

    for name in sorted(expected - observed):
        result.errors.append(f"missing column: {name}")

    if not allow_extra_columns:
        for name in sorted(observed - expected):
            result.warnings.append(f"extra column: {name}")


def _validate_row(
    row_number: int,
    row: dict[str, str],
    expected_columns: dict[str, dict[str, Any]],
    observed_nulls: dict[str, int],
    result: ValidationResult,
) -> None:
    for name, column in expected_columns.items():
        value = row.get(name)
        if is_nullish(value):
            observed_nulls[name] += 1
            if not column.get("nullable", False):
                result.errors.append(f"row {row_number}: {name} is null but contract marks it required")
            continue

        parsed = parse_value(value or "")
        if not compatible_type(column["type"], parsed.kind):
            result.errors.append(f"row {row_number}: {name} expected {column['type']}, got {parsed.kind}")

        allowed = column.get("allowed_values")
        if allowed is not None and str(parsed.normalized) not in allowed:
            result.errors.append(f"row {row_number}: {name} value {parsed.normalized!r} is outside allowed values")


def _validate_null_drift(
    observed_rows: int,
    observed_nulls: dict[str, int],
    expected_columns: dict[str, dict[str, Any]],
    null_drift: float,
    result: ValidationResult,
) -> None:
    if observed_rows == 0:
        return

    for name, null_count in observed_nulls.items():
        expected_rate = float(expected_columns[name].get("null_rate", 0))
        observed_rate = null_count / observed_rows
        if observed_rate - expected_rate > null_drift:
            result.warnings.append(
                f"{name} null rate drifted from {expected_rate:.1%} to {observed_rate:.1%}"
            )
