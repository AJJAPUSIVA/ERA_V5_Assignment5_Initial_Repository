# Session 5 alignment patch

This patch:

1. Separates the 92% main-pretraining preset from the 8% anneal preset.
2. Changes proxy wording from executed to planned.
3. Splits reasoning-support pretraining from later reasoning SFT and RL.
4. Adds Agentic response-only loss masking and excludes tool observations from loss.
5. Makes Verified Indic, Reasoning and Agentic floors bypass OPUS.
6. Adds gradual mixture-transition bands and gradient-norm safeguards.
7. Maps the internal reasoning bands to low, medium, high and ultra effort.
8. Corrects stage mixtures so their weighted totals exactly reproduce the headline 92% allocation.
9. Adds samples, tokens, licence, provenance, stage, loss-shape and benchmark fields to the inventory schema.
10. Records GitHub publication separately from the pending incognito test.
