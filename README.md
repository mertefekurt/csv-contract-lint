![Project Banner](https://socialify.git.ci/mertefekurt/csv-contract-lint?font=Inter&theme=Dark&pattern=Circuit+Board)

# csv-contract-lint

`csv-contract-lint` is a tiny Python CLI for teams that move data through CSV files and still want a clear contract around shape, types, required fields, and small controlled vocabularies.

It is built for the practical mess: finance exports, ops reports, vendor drops, analytics handoffs, and batch jobs where a changed column can quietly break the next step.

![Terminal Output](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=400&size=14&duration=4000&pause=1000&center=false&vCenter=false&multiline=true&width=600&height=200&lines=%24+csv-contract-lint+infer+orders.csv+-o+orders.contract.json;wrote+contract+with+5+columns+to+orders.contract.json;%24+csv-contract-lint+check+new-orders.csv+-c+orders.contract.json;error:+row+14:+total+expected+decimal,+got+string;csv+failed+contract)

## Why it exists 🧾

CSV is simple until it becomes someone else's interface. A supplier renames `customer_id`, an export starts sending `pending_review`, or a date column turns into free text. This tool catches those changes before they land in a dashboard, import job, or notebook.

## What it checks 🔎

- column presence and unexpected columns
- inferred scalar types: `integer`, `decimal`, `datetime`, `boolean`, `string`
- required vs nullable fields
- low-cardinality allowed values for status-like columns
- null-rate drift between a trusted sample and a new file

## Install

```bash
python -m pip install .
```

## Usage

Create a contract from a known-good CSV:

```bash
csv-contract-lint infer data/orders.csv -o contracts/orders.contract.json
```

Check a fresh file against that contract:

```bash
csv-contract-lint check incoming/orders.csv -c contracts/orders.contract.json
```

Print a compact summary:

```bash
csv-contract-lint inspect contracts/orders.contract.json
```

## Example contract

```json
{
  "version": 1,
  "source": "orders.csv",
  "row_count": 2000,
  "columns": [
    {
      "name": "status",
      "type": "string",
      "nullable": false,
      "null_rate": 0,
      "unique_ratio": 0.003,
      "allowed_values": ["failed", "paid", "refunded"]
    }
  ]
}
```

## Design notes 🛠️

The project keeps the core small on purpose:

- `src/csv_contract_lint/contract.py` infers contracts from trusted files
- `src/csv_contract_lint/validator.py` validates candidate files
- `src/csv_contract_lint/types.py` owns parsing and type compatibility
- `src/csv_contract_lint/cli.py` exposes the workflow as a CLI

No service, no database, no hidden state. Contracts are plain JSON so they can be reviewed, versioned, and used in CI.

## Test

```bash
python -m pytest
```

## Roadmap 🗺️

- optional strict column ordering
- junit output for CI systems
- richer numeric bounds for amount-like columns
- profile comparison between two CSV files without writing a contract first

## License

MIT
