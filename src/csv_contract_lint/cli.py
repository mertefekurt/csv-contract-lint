"""Core utilities for this package."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .contract import infer_contract
from .io import read_json, write_json
from .validator import validate_csv


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser and subcommands."""
    parser = argparse.ArgumentParser(
        prog="csv-contract-lint",
        description="infer and validate lightweight csv data contracts",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    infer = subparsers.add_parser("infer", help="create a contract from a known-good csv")
    infer.add_argument("csv", type=Path)
    infer.add_argument("-o", "--output", type=Path, required=True)
    infer.add_argument("--sample-size", type=int)
    infer.add_argument("--enum-limit", type=int, default=12)

    check = subparsers.add_parser("check", help="validate a csv against a saved contract")
    check.add_argument("csv", type=Path)
    check.add_argument("-c", "--contract", type=Path, required=True)
    check.add_argument("--null-drift", type=float, default=0.15)
    check.add_argument("--allow-extra-columns", action="store_true")

    inspect = subparsers.add_parser("inspect", help="print a compact contract summary")
    inspect.add_argument("contract", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the main workflow."""
    args = build_parser().parse_args(argv)

    if args.command == "infer":
        contract = infer_contract(args.csv, sample_size=args.sample_size, enum_limit=args.enum_limit)
        write_json(args.output, contract)
        print(f"wrote contract with {len(contract['columns'])} columns to {args.output}")
        return 0

    if args.command == "check":
        result = validate_csv(
            args.csv,
            read_json(args.contract),
            null_drift=args.null_drift,
            allow_extra_columns=args.allow_extra_columns,
        )
        for warning in result.warnings:
            print(f"warning: {warning}", file=sys.stderr)
        for error in result.errors:
            print(f"error: {error}", file=sys.stderr)
        print("csv matches contract" if result.ok else "csv failed contract")
        return 0 if result.ok else 1

    if args.command == "inspect":
        contract = read_json(args.contract)
        print(json.dumps(_summary(contract), indent=2))
        return 0

    return 2


def _summary(contract: dict[str, Any]) -> dict[str, Any]:
    """Return a compact, stable representation for the inspect command."""
    return {
        "source": contract.get("source"),
        "row_count": contract.get("row_count"),
        "columns": [
            {
                "name": column["name"],
                "type": column["type"],
                "nullable": column["nullable"],
            }
            for column in contract.get("columns", [])
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())
