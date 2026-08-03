# Contributing

Contributions that improve reproducibility, validation, documentation or
evaluation are welcome.

## Before opening a pull request

1. Create a focused branch.
2. Do not add raw corpora, gated examples, model weights, checkpoints, tokens
   or private paths.
3. Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_evidence.py --repo-root .
```

4. Regenerate the dashboard when comparison evidence changes:

```bash
python3 scripts/generate_dashboard.py \
  --comparison evidence/proxy_runs/comparisons/M0_vs_M1.json \
  --output docs/index.html
```

5. Explain whether the change affects frozen experimental assumptions,
   acceptance gates or interpretation.

## Experiment proposals

New experiments should specify:

- hypothesis;
- baseline and treatment;
- exact model revision;
- data revisions or hashes;
- token and step budgets;
- seeds;
- evaluation files;
- acceptance rules;
- stopping criteria;
- public-safe evidence outputs.

Acceptance thresholds must be registered before observing treatment results.

## Data and artifact policy

Never commit:

- `*.jsonl`, `*.parquet`, `*.arrow`;
- raw or cleaned private datasets;
- gated dataset examples;
- `checkpoint-*`;
- `*.safetensors`, `*.bin`, `*.pt`, `*.pth`;
- optimizer states;
- credentials or personal Drive paths;
- ZIP archives containing restricted artifacts.

## Style

The release tooling deliberately uses only the Python standard library. Keep
new core analysis utilities dependency-free unless a strong technical reason
is documented.
