from __future__ import annotations

import csv

from csv_contract_lint.contract import infer_contract


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def test_infer_contract_detects_types_and_allowed_values(tmp_path):
    source = tmp_path / "orders.csv"
    write_csv(
        source,
        [
            {"id": "1", "status": "paid", "total": "12.50", "created_at": "2026-05-01"},
            {"id": "2", "status": "refunded", "total": "9.00", "created_at": "2026-05-02"},
        ],
    )

    contract = infer_contract(source)

    columns = {column["name"]: column for column in contract["columns"]}
    assert columns["id"]["type"] == "integer"
    assert columns["status"]["allowed_values"] == ["paid", "refunded"]
    assert columns["total"]["type"] == "decimal"
    assert columns["created_at"]["type"] == "datetime"
