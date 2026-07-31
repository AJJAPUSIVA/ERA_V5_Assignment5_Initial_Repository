# M0 T4 QLoRA Proxy Report

## Status

Complete.

## Condition

- Model: `Qwen/Qwen2.5-1.5B`
- Model revision: `8faed761d45a263340a0528343f099c05c9a4323`
- Repository basis: `80b2b453403a3c73ce463e730b7b1f322c3b91cf`
- Seed: 42
- Mixture: 72% General / 14% Hindi / 14% Hinglish
- Actual sampled mixture: 72.0031% / 13.9985% / 13.9985%
- Frozen model-token budget: 7,995,392
- Optimizer steps: 976
- Runtime: 3.10 hours
- Training method: 4-bit NF4 QLoRA, LoRA adapters only, FP16 compute

## Validation results

| Lane | Loss | Perplexity |
|---|---:|---:|
| General | 2.421526 | 11.263 |
| Hindi | 1.321622 | 3.749 |
| Hinglish native | 1.505295 | 4.505 |
| Hinglish romanized | 3.607619 | 36.878 |

## Interpretation

M0 is the preregistered baseline for the controlled M1 mixture comparison. It completed the exact frozen budget and is valid for directional comparison.

This is a resource-constrained, one-seed T4 QLoRA proxy. It is not equivalent to full-parameter BF16 continued pretraining.
