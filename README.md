# ERA V5 — Reproducible Hindi/Hinglish Data-Mixture Experiments

[![CI](https://github.com/AJJAPUSIVA/ERA_V5_Assignment5_Initial_Repository/actions/workflows/ci.yml/badge.svg)](https://github.com/AJJAPUSIVA/ERA_V5_Assignment5_Initial_Repository/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: standard library](https://img.shields.io/badge/Python-standard%20library-blue.svg)](scripts/compare_runs.py)
[![Release](https://img.shields.io/badge/release-v1.0.0-brightgreen.svg)](docs/RELEASE_NOTES_v1.0.0.md)

A controlled 1.5B-parameter QLoRA study testing whether increased Hindi and
Hinglish allocation improves multilingual validation performance without
unacceptable General-language regression.

This repository emphasizes **preregistered decision rules, exact experiment
controls, machine-readable evidence, reproducible analysis, and candid
reporting of a non-qualifying treatment**.

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
> improved by 1.20% rather than the required 2%. M1 is therefore a promising
> but non-qualifying treatment. M0 remains the preregistered baseline.

[Open the visual results dashboard](docs/index.html) ·
[Read the experiment card](docs/EXPERIMENT_CARD.md) ·
[Read the full comparison](evidence/proxy_runs/comparisons/M0_vs_M1.md)

## What this project demonstrates

- Hash- and revision-oriented experiment provenance
- Controlled M0/M1 data-mixture comparison
- Resource-constrained 4-bit QLoRA training on a T4 GPU
- Frozen token, step, seed, model and evaluation controls
- Automated acceptance-gate calculations
- Machine-readable and human-readable evidence
- Standard-library command-line tooling
- Comment-only `requirements.txt` documenting zero third-party dependencies
- Unit tests and GitHub Actions CI
- Transparent limitations and negative-result reporting

## Experiment controls

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
| M0 mixture | 72% General / 14% Hindi / 14% Hinglish |
| M1 mixture | 60% General / 20% Hindi / 20% Hinglish |

The completed run is a one-seed, resource-constrained directional proxy. It is
not equivalent to full-parameter BF16 continued pretraining, and it does not
establish transfer to a 3B model.

## Quick start

No third-party package installation is required. The release tooling uses only
the Python standard library. `requirements.txt` is included as a documented,
comment-only dependency manifest.

### Recompute the comparison

```bash
python3 scripts/compare_runs.py \
  --baseline evidence/proxy_runs/M0/m0_validation_metrics.json \
  --treatment evidence/proxy_runs/M1/m1_validation_metrics.json \
  --baseline-name M0 \
  --treatment-name M1 \
  --output-dir build/comparison
```

### Validate the repository evidence

```bash
python3 scripts/validate_evidence.py --repo-root .
```

### Regenerate the visual dashboard

```bash
python3 scripts/generate_dashboard.py \
  --comparison evidence/proxy_runs/comparisons/M0_vs_M1.json \
  --output docs/index.html
```

### Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Repository map

```text
.
├── configs/                         # Frozen plans and executed configurations
├── evidence/proxy_runs/             # Public-safe M0/M1 evidence
├── scripts/
│   ├── compare_runs.py              # Reproducible comparison CLI
│   ├── generate_dashboard.py        # Deterministic HTML generator
│   └── validate_evidence.py         # Repository and result validation
├── tests/                           # Standard-library unit tests
├── docs/
│   ├── ASSIGNMENT_SPEC.md           # Original assignment README
│   ├── EXPERIMENT_CARD.md
│   ├── PORTFOLIO_CASE_STUDY.md
│   ├── RELEASE_NOTES_v1.0.0.md
│   └── index.html                   # Static visual results dashboard
└── .github/workflows/ci.yml         # Python 3.10–3.12 CI
```

## Acceptance gates

All five rules were required:

1. Hindi loss improves by at least 2%.
2. Combined Hinglish loss improves by at least 2%.
3. General loss worsens by no more than 1%.
4. No individual validation lane worsens by more than 2%.
5. Equal-weight overall loss does not worsen.

The implementation of these rules is tested in
[`tests/test_compare_runs.py`](tests/test_compare_runs.py).

## Evidence

- [M0 report](evidence/proxy_runs/M0/M0_REPORT.md)
- [M1 report](evidence/proxy_runs/M1/M1_REPORT.md)
- [M0 validation metrics](evidence/proxy_runs/M0/m0_validation_metrics.json)
- [M1 validation metrics](evidence/proxy_runs/M1/m1_validation_metrics.json)
- [Human-readable comparison](evidence/proxy_runs/comparisons/M0_vs_M1.md)
- [Machine-readable comparison](evidence/proxy_runs/comparisons/M0_vs_M1.json)
- [Original assignment specification](docs/ASSIGNMENT_SPEC.md)

## Limitations

- One seed per condition
- Approximately eight million model tokens per condition
- Internal validation losses rather than broad downstream benchmarks
- QLoRA adapter training rather than full-parameter BF16 continued pretraining
- No demonstrated 1.5B-to-3B transfer
- Hinglish bilingual review remains pending
- Raw corpora and restricted artifacts are intentionally excluded

## Roadmap

- Replicate M0 and M1 with additional seeds
- Report means, variability and direction consistency
- Complete bilingual Hinglish review
- Add public downstream Hindi/Hinglish benchmarks
- Preregister and test M2 only if justified
- Run matched two-seed 3B baseline and treatment confirmation
- Consider full-parameter BF16 only after positive 3B QLoRA evidence

## Open-source boundaries

The MIT license covers code and original documentation in this repository.
Models and datasets retain their upstream licenses and access conditions. Raw
corpora, gated examples, checkpoints, adapters, optimizer states and private
paths are not included. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Citation

Use [`CITATION.cff`](CITATION.cff), or cite the repository as:

> AJJAPUSIVA. *ERA V5: Reproducible Hindi/Hinglish Data-Mixture Experiments*,
> version 1.0.0, 2026.
