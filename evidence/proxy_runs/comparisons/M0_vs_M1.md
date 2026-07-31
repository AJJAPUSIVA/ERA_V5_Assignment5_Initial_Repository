# M0-versus-M1 T4 QLoRA Comparison

## Status

Complete.

## Experimental controls

- Model-token budget per condition: 7,995,392
- Optimizer steps per condition: 976
- Model: `Qwen/Qwen2.5-1.5B`
- Model revision: `8faed761d45a263340a0528343f099c05c9a4323`
- Repository basis: `80b2b453403a3c73ce463e730b7b1f322c3b91cf`
- Seed: 42
- M0 mixture: 72% General / 14% Hindi / 14% Hinglish
- M1 mixture: 60% General / 20% Hindi / 20% Hinglish
- Interpretation: one-seed directional T4 QLoRA proxy evidence only

## Validation comparison

| Validation lane | M0 loss | M1 loss | Relative change | Gate implication |
|---|---:|---:|---:|---|
| General | 2.421526 | 2.422442 | +0.04% | Passes ≤1% regression guardrail |
| Hindi | 1.321622 | 1.305719 | -1.20% | Improves, but misses ≥2% target |
| Hinglish native | 1.505295 | 1.474137 | -2.07% | Improves |
| Hinglish romanized | 3.607619 | 3.521341 | -2.39% | Improves |

Negative relative change indicates improvement.

## Aggregate comparison

| Metric | M0 | M1 | Relative change |
|---|---:|---:|---:|
| Combined Hinglish | 2.556457 | 2.497739 | -2.30% |
| Equal-weight overall | 2.214016 | 2.180910 | -1.50% |

## Predeclared acceptance checks

| Check | Result |
|---|---|
| Hindi loss improves by at least 2% | **FAIL** |
| Combined Hinglish improves by at least 2% | **PASS** |
| General regression is no greater than 1% | **PASS** |
| No individual lane regresses by more than 2% | **PASS** |
| Equal-weight overall loss does not worsen | **PASS** |

## Conclusion

**M1 does not pass all preregistered acceptance gates.** Four of five checks pass. The increased Indic allocation produces useful directional gains: native Hinglish improves by 2.07%, romanized Hinglish by 2.39%, combined Hinglish by 2.30%, and the equal-weight overall loss by 1.50%. General loss changes by only +0.04%, remaining safely inside the 1% guardrail. Hindi improves by 1.20%, but this is below the frozen 2% minimum and is the sole failed gate.

Under the strict decision rule, M1 must not be declared the accepted winner. M0 remains the preregistered baseline, while M1 should be described as a promising but non-qualifying treatment. A later M2 curriculum or multi-seed confirmation may test whether the Hinglish gains can be retained while crossing the Hindi threshold. M2 was not started for this submission.

These findings are one-seed directional evidence from a resource-constrained T4 QLoRA experiment and are not equivalent to a full-parameter BF16 continued-pretraining result.
