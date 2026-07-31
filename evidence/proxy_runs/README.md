# T4 QLoRA Proxy Evidence

This directory contains public-safe summaries from the completed M0 and M1 screening runs and their preregistered comparison.

## Conditions

- **M0:** 72% General / 14% Hindi / 14% Hinglish
- **M1:** 60% General / 20% Hindi / 20% Hinglish
- Both conditions used 7,995,392 model tokens, 976 optimizer steps, seed 42, the same pinned Qwen2.5-1.5B revision, and the same fixed validation split.

## Decision

M1 passes four of five preregistered acceptance checks but misses the Hindi ≥2% improvement threshold. It is therefore promising directional evidence, not an accepted winner.

See [`comparisons/M0_vs_M1.md`](comparisons/M0_vs_M1.md) for the complete finding.
