# CSV Contract Lint

> infer and validate lightweight contracts for csv files

## Snapshot

<img src="assets/readme-cover.svg" alt="CSV Contract Lint cover" width="100%" />

| Part | Notes |
| --- | --- |
| Area | data and privacy |
| Entry | `csv-contract-lint` |
| Main files | src/, tests/, .gitignore, pyproject.toml |

## Use

```bash
git clone https://github.com/mertefekurt/csv-contract-lint.git
cd csv-contract-lint
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
csv-contract-lint --help
```

## Notes

This project stays useful when the output is easy to read and the setup is easy to throw away after a quick check.
