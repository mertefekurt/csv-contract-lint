from __future__ import annotations

import csv

from csv_contract_lint.contract import infer_contract
from csv_contract_lint.validator import validate_csv


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def test_validate_csv_reports_type_and_enum_errors(tmp_path):
    baseline = tmp_path / "baseline.csv"
    candidate = tmp_path / "candidate.csv"
    write_csv(
        baseline,
        [
            {"id": "1", "status": "paid", "total": "12.50"},
            {"id": "2", "status": "failed", "total": "7.25"},
        ],
    )
    write_csv(
        candidate,
        [
            {"id": "not-a-number", "status": "paid", "total": "12.50"},
            {"id": "2", "status": "pending", "total": "7.25"},
        ],
    )

    result = validate_csv(candidate, infer_contract(baseline))

    assert not result.ok
    assert any("id expected integer" in error for error in result.errors)
    assert any("status value 'pending'" in error for error in result.errors)


def test_validate_csv_warns_on_null_rate_drift(tmp_path):
    baseline = tmp_path / "baseline.csv"
    candidate = tmp_path / "candidate.csv"
    write_csv(
        baseline,
        [
            {"id": "1", "email": "a@example.com"},
            {"id": "2", "email": "b@example.com"},
        ],
    )
    write_csv(
        candidate,
        [
            {"id": "1", "email": ""},
            {"id": "2", "email": ""},
        ],
    )

    result = validate_csv(candidate, infer_contract(baseline), null_drift=0.20)

    assert not result.ok
    assert any("email is null" in error for error in result.errors)
    assert any("email null rate drifted" in warning for warning in result.warnings)
