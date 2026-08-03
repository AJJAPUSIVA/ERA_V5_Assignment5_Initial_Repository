# Experiment Card — IndicMix Lab M0/M1 T4 QLoRA Mixture Screen

## 1. Summary

This experiment tests whether increasing Hindi and Hinglish exposure improves
target-language validation losses without unacceptable General-language
regression.

The comparison is a resource-constrained, one-seed directional proxy using
QLoRA adapters. It is not a full-parameter BF16 continued-pretraining study.

## 2. Research question

Does changing the training mixture from:

- M0: 72% General / 14% Hindi / 14% Hinglish

to:

- M1: 60% General / 20% Hindi / 20% Hinglish

produce at least 2% Hindi and combined Hinglish improvements while respecting
the frozen General and per-lane regression guardrails?

## 3. Hypothesis and decision rule

M1 qualifies only when **all** of the following hold:

1. Hindi relative loss improvement is at least 2%.
2. Combined Hinglish relative loss improvement is at least 2%.
3. General relative loss regression is no greater than 1%.
4. No individual validation lane regresses by more than 2%.
5. Equal-weight overall loss does not worsen.

Relative change is:

```text
(treatment_loss - baseline_loss) / baseline_loss
```

Negative change indicates improvement.

## 4. Model and method

| Field | Value |
|---|---|
| Model | `Qwen/Qwen2.5-1.5B` |
| Revision | `8faed761d45a263340a0528343f099c05c9a4323` |
| Sequence length | 1,024 |
| Base-weight storage | 4-bit NF4 with double quantization |
| Trainable parameters | LoRA adapters only |
| Compute dtype | FP16 |
| Optimizer | paged AdamW 8-bit |
| Learning rate | 2e-4 |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Seed | 42 |
| Hardware | Colab T4 |

## 5. Frozen execution controls

| Control | M0 | M1 |
|---|---:|---:|
| Model tokens | 7,995,392 | 7,995,392 |
| Optimizer steps | 976 | 976 |
| Seed | 42 | 42 |
| Runtime | 3.10 hours | 3.24 hours |
| Validation files | Identical | Identical |

The tokenizer, model revision, optimizer family, schedule, evaluation files
and validation split were held fixed.

## 6. Data scope

The proxy uses only the project’s General, Hindi and Hinglish pilot lanes.

| Lane | Documented pilot supply | Gate status |
|---|---:|---|
| General | 5,175,419 provisional tokens | Verified |
| Hindi | 1,000,032 provisional tokens | Verified after hash repair |
| Hinglish | 1,000,016 provisional tokens | Automated gate passed; bilingual review pending |

These supply counts are documented provisional counts and should not be
confused with the exact frozen model-token budget consumed by each run.

Raw corpora are intentionally excluded from the public repository.

## 7. Validation results

| Validation lane | M0 loss | M1 loss | Relative change |
|---|---:|---:|---:|
| General | 2.421526 | 2.422442 | +0.04% |
| Hindi | 1.321622 | 1.305719 | -1.20% |
| Hinglish native | 1.505295 | 1.474137 | -2.07% |
| Hinglish romanized | 3.607619 | 3.521341 | -2.39% |
| Combined Hinglish | 2.556457 | 2.497739 | -2.30% |
| Equal-weight overall | 2.214016 | 2.180910 | -1.50% |

## 8. Acceptance results

| Gate | Result |
|---|---|
| Hindi improves by at least 2% | **FAIL** |
| Combined Hinglish improves by at least 2% | **PASS** |
| General regression is no greater than 1% | **PASS** |
| No lane regresses by more than 2% | **PASS** |
| Equal-weight overall does not worsen | **PASS** |

## 9. Conclusion

M1 passed four of five gates and produced useful directional improvements,
especially on both Hinglish lanes. However, Hindi improved by 1.20%, below the
frozen 2% requirement.

M1 is therefore classified as **promising but non-qualifying**. M0 remains the
preregistered baseline. The acceptance threshold was not changed after
observing the result.

## 10. Reproducibility

Recompute the comparison:

```bash
python3 scripts/compare_runs.py \
  --baseline evidence/proxy_runs/M0/m0_validation_metrics.json \
  --treatment evidence/proxy_runs/M1/m1_validation_metrics.json \
  --output-dir build/comparison
```

Validate committed evidence:

```bash
python3 scripts/validate_evidence.py --repo-root .
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## 11. Evidence files

- `evidence/proxy_runs/M0/M0_REPORT.md`
- `evidence/proxy_runs/M0/m0_validation_metrics.json`
- `evidence/proxy_runs/M1/M1_REPORT.md`
- `evidence/proxy_runs/M1/m1_validation_metrics.json`
- `evidence/proxy_runs/comparisons/M0_vs_M1.md`
- `evidence/proxy_runs/comparisons/M0_vs_M1.json`
- `configs/proxy_experiments_t4_qlora.yaml`
- `configs/m0_m1_comparison.yaml`

## 12. Limitations

- One seed
- Small proxy token budget
- Adapter-only QLoRA rather than full-parameter training
- No matched 3B confirmation
- No downstream benchmark suite
- No statistical interval from repeated runs
- Hinglish bilingual review remains pending
- Internal loss improvements do not by themselves prove deployment quality

## 13. Ethical and publication considerations

The public repository does not contain raw corpora, gated samples, model
weights, checkpoints, optimizer states, credentials or private paths.

Language-mixture conclusions should not be interpreted as evidence that all
Hindi or Hinglish varieties, registers or communities are represented
adequately.

## 14. Recommended follow-up

1. Repeat M0 and M1 with additional seeds.
2. Report mean, variability and direction consistency.
3. Complete bilingual Hinglish review.
4. Add downstream Hindi and code-switching evaluation.
5. Test a preregistered M2 only if the multi-seed evidence justifies it.
6. Run matched 3B baseline and treatment confirmation.
