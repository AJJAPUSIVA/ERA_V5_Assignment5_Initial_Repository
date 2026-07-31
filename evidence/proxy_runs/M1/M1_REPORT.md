# M1 T4 QLoRA Proxy Report

## Status

Complete.

## Condition

- Model: `Qwen/Qwen2.5-1.5B`
- Model revision: `8faed761d45a263340a0528343f099c05c9a4323`
- Repository basis: `80b2b453403a3c73ce463e730b7b1f322c3b91cf`
- Seed: 42
- Mixture: 60% General / 20% Hindi / 20% Hinglish
- Actual sampled mixture: 60.0026% / 19.9923% / 20.0051%
- Frozen model-token budget: 7,995,392
- Optimizer steps: 976
- Runtime: 3.24 hours
- Training method: 4-bit NF4 QLoRA, LoRA adapters only, FP16 compute

## Validation results

| Lane | Loss | Perplexity |
|---|---:|---:|
| General | 2.422442 | 11.273 |
| Hindi | 1.305719 | 3.690 |
| Hinglish native | 1.474137 | 4.367 |
| Hinglish romanized | 3.521341 | 33.830 |

## Interpretation

M1 improves Hindi and both Hinglish validation losses relative to M0 while producing only a negligible General-language regression. However, its Hindi improvement is 1.20%, below the preregistered 2% acceptance threshold. M1 therefore does not pass every frozen acceptance gate.

This is a resource-constrained, one-seed T4 QLoRA proxy. It is not equivalent to full-parameter BF16 continued pretraining.
