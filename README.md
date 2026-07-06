<img src="assets/readme-cover.svg" alt="CSV Contract Lint cover" width="100%" />

# CSV Contract Lint

infer and validate lightweight contracts for csv files.

![stack](https://img.shields.io/badge/stack-Python-0891b2?style=flat-square) ![python](https://img.shields.io/badge/python-3.9-b45309?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-be185d?style=flat-square) ![tests](https://img.shields.io/badge/tests-pytest-4b5563?style=flat-square)

| Question | Answer |
| --- | --- |
| What is it? | A focused Python utility for contract checks. |
| How does it run? | `csv-contract-lint` |
| Why keep it small? | Easier review, easier tests, fewer moving parts. |

## Command

```bash
python -m pip install -e ".[dev]"
csv-contract-lint --help
python -m csv_contract_lint --help
```

## Verify

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m csv_contract_lint --help
```
