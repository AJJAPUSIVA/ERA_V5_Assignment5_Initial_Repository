# ERA V5 v1.0.0

## Release summary

Version 1.0.0 turns the completed assignment into a reproducible open-source
ML experiment repository.

The release preserves the central scientific finding:

- M1 improved combined Hinglish loss by 2.30%.
- M1 improved equal-weight overall loss by 1.50%.
- General loss regressed by only 0.04%.
- Hindi improved by 1.20%, below the required 2%.
- Four of five acceptance gates passed.
- M1 was not promoted as the accepted mixture.

## Added in v1.0.0

- Dependency-free comparison CLI
- Evidence validator
- Deterministic static dashboard
- Unit tests
- Python 3.10–3.12 GitHub Actions CI
- Job-facing README
- Experiment card
- Portfolio case study
- MIT license
- Citation metadata
- Contribution, conduct, security and third-party notices

## Reproducibility commands

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_evidence.py --repo-root .
python3 scripts/compare_runs.py \
  --baseline evidence/proxy_runs/M0/m0_validation_metrics.json \
  --treatment evidence/proxy_runs/M1/m1_validation_metrics.json \
  --output-dir build/comparison
```

## Scope boundary

This release does not claim:

- statistical confirmation across seeds;
- downstream benchmark leadership;
- 1.5B-to-3B transfer;
- equivalence to full-parameter BF16 continued pretraining;
- release of a standalone competitive model.

## Suggested Git tag

```text
v1.0.0
```
