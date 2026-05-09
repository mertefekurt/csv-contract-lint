from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation


TYPE_ORDER = ("integer", "decimal", "datetime", "boolean", "string")
NULL_MARKERS = {"", "null", "none", "na", "n/a", "nan"}


@dataclass(frozen=True)
class ParsedValue:
    kind: str
    normalized: object


def is_nullish(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in NULL_MARKERS


def parse_value(value: str) -> ParsedValue:
    text = value.strip()
    lowered = text.lower()

    if lowered in {"true", "false", "yes", "no"}:
        return ParsedValue("boolean", lowered in {"true", "yes"})

    try:
        integer = int(text)
    except ValueError:
        pass
    else:
        return ParsedValue("integer", integer)

    try:
        decimal = Decimal(text)
    except InvalidOperation:
        pass
    else:
        return ParsedValue("decimal", str(decimal))

    for parser in (_parse_iso_datetime, _parse_common_date):
        parsed = parser(text)
        if parsed is not None:
            return ParsedValue("datetime", parsed.isoformat())

    return ParsedValue("string", text)


def compatible_type(expected: str, actual: str) -> bool:
    if expected == actual:
        return True
    return expected == "decimal" and actual == "integer"


def resolve_column_type(types: set[str]) -> str:
    if not types:
        return "string"
    for candidate in TYPE_ORDER:
        if all(compatible_type(candidate, item) for item in types):
            return candidate
    return "string"


def _parse_iso_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _parse_common_date(value: str) -> datetime | None:
    for pattern in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue
    return None
