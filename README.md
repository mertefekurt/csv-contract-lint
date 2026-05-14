<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=250&section=header&text=csv-contract-lint&fontSize=60&fontAlignY=35&desc=Stop%20fragile%20CSV%20handoffs%20before%20they%20break%20imports%2C%20dashboards%2C%20or%20nightly%20jobs.%20Infer%20a%20versionable%20data%20contract%20from%20one%20trusted%20file%2C%20then%20catch%20schema%20drift%2C%20type%20surprises%2C%20enum%20changes%2C%20and%20null-rate%20regressions%20from%20a%20fast%20Python%20CLI.&descAlignY=55&descSize=20)

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CSV](https://img.shields.io/badge/Data-CSV%20Contracts-16A34A?style=for-the-badge&logo=files&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-Terminal-111827?style=for-the-badge&logo=gnometerminal&logoColor=white)
![Tests](https://img.shields.io/badge/Quality-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

</div>

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=33C9FF&width=650&height=40&lines=Data+Contracts+For+The+CSV+Reality)

`csv-contract-lint` turns a known-good CSV into a compact JSON contract and validates every future file against it. It is built for teams that still rely on CSV boundaries but need CI-friendly protection against renamed columns, silent null spikes, unexpected value sets, and type drift.

<table>
  <tr>
    <td width="50%" valign="top">

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=FF4ECD&width=500&height=40&lines=Core+Features)

- 🧬 Infers a contract from a trusted baseline CSV
- 🧱 Detects missing columns, extra columns, and required-field breaks
- 🔎 Validates scalar types such as numbers, booleans, dates, and strings
- 🏷️ Locks small enum-like columns to observed values
- 📉 Warns when null rates drift beyond the configured threshold
- ⚙️ Ships as a clean Python CLI with focused pytest coverage

  </td>
  <td width="50%" valign="top">

![Code Snapshot](assets/code-snapshot.png)

  </td>
  </tr>
</table>

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=9DFF57&width=650&height=40&lines=Blazing+Fast+CLI+Demo)

![Demo](https://readme-typing-svg.demolab.com/?font=Fira+Code&duration=1500&pause=500&multiline=true&width=950&height=150&color=F8F8F2&background=282A3600&lines=%24+csv-contract-lint+infer+data%2Forders.csv+-o+contracts%2Forders.json;%3E+wrote+contract+with+12+columns;%24+csv-contract-lint+check+incoming%2Forders.csv+-c+contracts%2Forders.json;%3E+csv+matches+contract)

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=FFB86C&width=650&height=40&lines=Validation+Pipeline)

```mermaid
flowchart TD
    A[Trusted CSV Baseline] --> B[Infer Contract]
    B --> C[Persist JSON Contract]
    C --> D[New CSV Arrives]
    D --> E[Header Checks]
    D --> F[Row Type Checks]
    D --> G[Enum Guardrails]
    D --> H[Null Drift Analysis]
    E --> I{Contract Result}
    F --> I
    G --> I
    H --> I
    I -->|Pass| J[Ship Data Forward]
    I -->|Warn or Fail| K[Fix Feed Before Import]
    classDef source fill:#33C9FF,stroke:#0F172A,color:#0F172A,stroke-width:2px
    classDef contract fill:#9DFF57,stroke:#17320E,color:#0F172A,stroke-width:2px
    classDef checks fill:#FF4ECD,stroke:#2A0A1F,color:#FFFFFF,stroke-width:2px
    classDef result fill:#FFB86C,stroke:#4A2500,color:#0F172A,stroke-width:2px
    classDef stop fill:#EF4444,stroke:#450A0A,color:#FFFFFF,stroke-width:2px
    class A,D source
    class B,C contract
    class E,F,G,H checks
    class I,J result
    class K stop
```

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=33C9FF&width=650&height=40&lines=Quick+Start)

```bash
git clone https://github.com/mertefekurt/csv-contract-lint.git
cd csv-contract-lint
python -m pip install .
csv-contract-lint infer data/orders.csv -o contracts/orders.contract.json
csv-contract-lint check incoming/orders.csv -c contracts/orders.contract.json
```

<details>
<summary>🛠️ View CLI Reference / Advanced Config</summary>

| Command | Purpose |
| --- | --- |
| `csv-contract-lint infer <csv> -o <contract>` | Create a contract from a known-good CSV file |
| `csv-contract-lint check <csv> -c <contract>` | Validate a CSV against a saved contract |
| `csv-contract-lint inspect <contract>` | Print a compact contract summary |

| Option | Command | Default | Purpose |
| --- | --- | --- | --- |
| `--sample-size` | `infer` | all rows | Limit the baseline rows used for inference |
| `--enum-limit` | `infer` | `12` | Capture allowed values for low-cardinality columns |
| `--null-drift` | `check` | `0.15` | Warn when observed null rate exceeds baseline by this amount |
| `--allow-extra-columns` | `check` | disabled | Ignore additional columns in incoming files |

| Check | Signal |
| --- | --- |
| Missing columns | A required field disappeared from the incoming CSV |
| Extra columns | A new field arrived without a contract update |
| Type compatibility | A column changed from its inferred scalar type |
| Required values | A non-null baseline column now contains empty cells |
| Allowed values | A controlled vocabulary gained an unexpected value |
| Null drift | A field is losing data at a materially higher rate |

</details>

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=FF4ECD&width=650&height=40&lines=Project+Map)

```text
csv-contract-lint/
├── src/csv_contract_lint/
│   ├── cli.py          # argparse commands and exit behavior
│   ├── contract.py     # baseline inference and contract shape
│   ├── validator.py    # validation errors, warnings, and drift checks
│   ├── types.py        # scalar parsing and compatibility rules
│   └── io.py           # JSON persistence helpers
├── tests/              # contract and validator coverage
└── assets/
    └── code-snapshot.png
```

![Header](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=26&color=9DFF57&width=650&height=40&lines=License)

MIT
