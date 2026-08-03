# Portfolio Case Study — Hindi/Hinglish Data-Mixture Optimization

## Challenge

Increase Hindi and Hinglish exposure in a 1.5B language-model training mixture
without causing unacceptable regression in General-language performance.

## Constraints

- Single Colab T4 GPU
- Limited compute budget
- Approximately eight million model tokens per condition
- Public repository could not include raw corpora or model artifacts
- Initial result limited to one seed
- Required transparent acceptance and rejection criteria

## Approach

I designed a controlled M0/M1 comparison:

- M0: 72% General / 14% Hindi / 14% Hinglish
- M1: 60% General / 20% Hindi / 20% Hinglish

Both conditions used the same:

- Qwen2.5-1.5B model revision
- validation split and files
- sequence length
- token budget
- optimizer steps
- QLoRA configuration
- seed
- evaluation logic

I preregistered five acceptance gates and required every gate to pass before
promoting the treatment.

## Engineering work

- Created frozen experiment configurations and evidence schemas
- Built QLoRA calibration and controlled training runs
- Recorded exact model revisions, token budgets and environments
- Produced machine-readable and human-readable result reports
- Implemented a dependency-free comparison CLI
- Added automated evidence validation and unit tests
- Added CI across multiple Python versions
- Built a deterministic visual dashboard
- Kept raw corpora and restricted artifacts out of Git history

## Result

| Outcome | Relative change |
|---|---:|
| General loss | +0.04% |
| Hindi loss | -1.20% |
| Hinglish native loss | -2.07% |
| Hinglish romanized loss | -2.39% |
| Combined Hinglish loss | -2.30% |
| Equal-weight overall loss | -1.50% |

M1 passed four of five gates. It improved both Hinglish lanes and overall loss,
but Hindi improved by 1.20%, below the required 2%.

## Decision

I did not declare M1 the winner. It was classified as promising but
non-qualifying, and M0 remained the preregistered baseline.

This decision demonstrates that experiment quality is not defined only by a
positive result. Reliable ML work also requires frozen criteria, reproducible
evidence and willingness to reject an attractive treatment when it misses a
declared threshold.

## Skills demonstrated

- Experimental design
- LLM data-mixture reasoning
- QLoRA training
- Reproducible ML engineering
- Python command-line tooling
- Unit testing and CI
- Data governance and publication safety
- Technical writing
- Negative-result interpretation
- Open-source release preparation

## Next technical milestones

- Multi-seed 1.5B replication
- Bilingual Hinglish human evaluation
- Public downstream benchmark integration
- Matched 3B baseline/treatment confirmation
- Full-parameter BF16 study only after positive 3B QLoRA evidence

## Résumé bullet

Designed and executed a preregistered T4 QLoRA mixture study on
Qwen2.5-1.5B, building hash-oriented data controls, matched M0/M1 experiments,
automated acceptance gates and reproducible public evidence; measured 2.30%
combined Hinglish and 1.50% overall loss improvements while transparently
rejecting the treatment after one frozen gate missed its threshold.
