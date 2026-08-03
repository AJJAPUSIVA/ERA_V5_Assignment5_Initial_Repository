# IndicMix Lab — Reproducible Hindi/Hinglish Data-Mixture Research

[![CI](https://github.com/AJJAPUSIVA/indicmix-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/AJJAPUSIVA/indicmix-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: standard library](https://img.shields.io/badge/Python-standard%20library-blue.svg)](scripts/compare_runs.py)
[![Release](https://img.shields.io/badge/release-v1.0.0-brightgreen.svg)](docs/RELEASE_NOTES_v1.0.0.md)

**IndicMix Lab** is a reproducible machine-learning research project testing
whether increased Hindi and Hinglish allocation improves multilingual
language-model validation performance without unacceptable General-language
regression.

The project emphasizes preregistered decision rules, matched controls,
machine-readable evidence, dependency-free analysis tooling, and candid
reporting of a non-qualifying treatment.

## Key result

| Metric | M0 | M1 | Relative change |
|---|---:|---:|---:|
| General loss | 2.421526 | 2.422442 | +0.04% |
| Hindi loss | 1.321622 | 1.305719 | -1.20% |
| Hinglish native loss | 1.505295 | 1.474137 | -2.07% |
| Hinglish romanized loss | 3.607619 | 3.521341 | -2.39% |
| Combined Hinglish loss | 2.556457 | 2.497739 | -2.30% |
| Equal-weight overall loss | 2.214016 | 2.180910 | -1.50% |

Negative change means lower validation loss and therefore improvement.

> **Decision:** M1 passed four of five frozen acceptance gates, but Hindi
> improved by 1.20% rather than the required 2%. M1 is therefore promising
> but non-qualifying. M0 remains the preregistered baseline.

[Visual results dashboard](docs/index.html) ·
[Experiment card](docs/EXPERIMENT_CARD.md) ·
[Full comparison](evidence/proxy_runs/comparisons/M0_vs_M1.md)

## Research question

Does increasing the Hindi/Hinglish share from M0 to M1 improve target-language
validation losses while retaining General-language stability?

| Condition | General | Hindi | Hinglish |
|---|---:|---:|---:|
| M0 baseline | 72% | 14% | 14% |
| M1 treatment | 60% | 20% | 20% |

## Frozen controls

| Control | Value |
|---|---|
| Base model | `Qwen/Qwen2.5-1.5B` |
| Model revision | `8faed761d45a263340a0528343f099c05c9a4323` |
| Method | 4-bit NF4 QLoRA, LoRA adapters only |
| Compute dtype | FP16 |
| Sequence length | 1,024 |
| Model-token budget per condition | 7,995,392 |
| Optimizer steps per condition | 976 |
| Seed | 42 |

This is a one-seed, resource-constrained directional proxy. It is not
equivalent to full-parameter BF16 continued pretraining and does not establish
transfer to a 3B model.

## What the project demonstrates

- Controlled multilingual data-mixture experimentation
- Exact model, token, step, seed and evaluation controls
- Resource-constrained QLoRA training
- Automated acceptance-gate calculations
- Machine-readable and human-readable evidence
- Dependency-free Python command-line tooling
- Unit tests and GitHub Actions CI
- Deterministic static results visualization
- Transparent limitations and negative-result reporting
- Public-safe research artifact management

## Quick start

No third-party installation is required. The tooling uses only the Python
standard library. `requirements.txt` is a comment-only dependency manifest.

### Rebrand existing tracked text

Run this once after copying the release overlay into the existing repository:

```bash
python3 scripts/rebrand_repository.py --repo-root . --apply
```

This changes only exact public-facing project names and repository URLs. It
does not rename evidence files, model revisions, hashes, M0/M1 identifiers or
schema versions.

### Recompute the comparison

```bash
python3 scripts/compare_runs.py \
  --baseline evidence/proxy_runs/M0/m0_validation_metrics.json \
  --treatment evidence/proxy_runs/M1/m1_validation_metrics.json \
  --baseline-name M0 \
  --treatment-name M1 \
  --output-dir build/comparison
```

### Validate evidence and branding

```bash
python3 scripts/validate_evidence.py --repo-root .
python3 scripts/check_branding.py --repo-root .
```

### Regenerate the dashboard

```bash
python3 scripts/generate_dashboard.py \
  --comparison evidence/proxy_runs/comparisons/M0_vs_M1.json \
  --output docs/index.html
```

### Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Repository map

```text
.
├── configs/                         # Frozen plans and configurations
├── evidence/proxy_runs/             # Public-safe M0/M1 evidence
├── scripts/
│   ├── compare_runs.py
│   ├── generate_dashboard.py
│   ├── validate_evidence.py
│   ├── rebrand_repository.py
│   └── check_branding.py
├── tests/
├── docs/
│   ├── EXPERIMENT_CARD.md
│   ├── PORTFOLIO_CASE_STUDY.md
│   ├── REPOSITORY_RENAME_GUIDE.md
│   ├── RELEASE_NOTES_v1.0.0.md
│   └── index.html
└── .github/workflows/ci.yml
```

## Acceptance gates

All five rules were required:

1. Hindi loss improves by at least 2%.
2. Combined Hinglish loss improves by at least 2%.
3. General loss worsens by no more than 1%.
4. No individual validation lane worsens by more than 2%.
5. Equal-weight overall loss does not worsen.

## Evidence

- [M0 report](evidence/proxy_runs/M0/M0_REPORT.md)
- [M1 report](evidence/proxy_runs/M1/M1_REPORT.md)
- [M0 validation metrics](evidence/proxy_runs/M0/m0_validation_metrics.json)
- [M1 validation metrics](evidence/proxy_runs/M1/m1_validation_metrics.json)
- [Human-readable comparison](evidence/proxy_runs/comparisons/M0_vs_M1.md)
- [Machine-readable comparison](evidence/proxy_runs/comparisons/M0_vs_M1.json)

## Limitations

- One seed per condition
- Approximately eight million model tokens per condition
- Internal validation losses rather than broad downstream benchmarks
- QLoRA adapter training rather than full-parameter BF16 training
- No demonstrated 1.5B-to-3B transfer
- Hinglish bilingual review remains pending
- Raw corpora and restricted artifacts are intentionally excluded

## Roadmap

- Replicate M0 and M1 with additional seeds
- Report means, variability and direction consistency
- Complete bilingual Hinglish review
- Add public downstream Hindi/Hinglish benchmarks
- Test a preregistered M2 only when justified
- Run matched two-seed 3B confirmation
- Consider full-parameter BF16 after positive 3B QLoRA evidence

## Open-source boundaries

The MIT license covers original code and documentation. Models and datasets
retain upstream licenses and access conditions. Raw corpora, gated examples,
checkpoints, adapters, optimizer states and private paths are not included.

## Citation

Use [`CITATION.cff`](CITATION.cff), or cite:

> AJJAPUSIVA. *IndicMix Lab: Reproducible Hindi/Hinglish Data-Mixture
> Research*, version 1.0.0, 2026.
