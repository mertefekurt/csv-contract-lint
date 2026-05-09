from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .types import is_nullish, parse_value, resolve_column_type


def infer_contract(
    csv_path: str | Path,
    *,
    sample_size: int | None = None,
    enum_limit: int = 12,
) -> dict[str, Any]:
    path = Path(csv_path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("csv file does not include a header row")

        stats = _new_stats(reader.fieldnames)
        row_count = 0
        for row in reader:
            row_count += 1
            _capture_row(stats, row)
            if sample_size is not None and row_count >= sample_size:
                break

    return {
        "version": 1,
        "source": path.name,
        "row_count": row_count,
        "columns": [_build_column(name, stats[name], row_count, enum_limit) for name in reader.fieldnames],
    }


def _new_stats(fieldnames: list[str]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "nulls": 0,
            "types": set(),
            "values": Counter(),
            "non_null_count": 0,
        }
        for name in fieldnames
    }


def _capture_row(stats: dict[str, dict[str, Any]], row: dict[str, str]) -> None:
    for name, value in row.items():
        column = stats[name]
        if is_nullish(value):
            column["nulls"] += 1
            continue
        parsed = parse_value(value)
        column["types"].add(parsed.kind)
        column["values"][str(parsed.normalized)] += 1
        column["non_null_count"] += 1


def _build_column(name: str, stats: dict[str, Any], row_count: int, enum_limit: int) -> dict[str, Any]:
    observed_values = stats["values"]
    non_null_count = stats["non_null_count"]
    null_rate = stats["nulls"] / row_count if row_count else 0
    column = {
        "name": name,
        "type": resolve_column_type(stats["types"]),
        "nullable": stats["nulls"] > 0,
        "null_rate": round(null_rate, 4),
        "unique_ratio": round(len(observed_values) / non_null_count, 4) if non_null_count else 0,
    }

    if 0 < len(observed_values) <= enum_limit:
        column["allowed_values"] = sorted(observed_values)

    return column
