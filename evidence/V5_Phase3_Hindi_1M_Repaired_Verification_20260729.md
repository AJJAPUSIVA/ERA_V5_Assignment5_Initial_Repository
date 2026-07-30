# V5 Phase 3 — Hindi 1M Repaired Evidence Verification

**Date:** 2026-07-29  
**Result:** **PASSED**

## Repair applied

- Final records inspected: **2,421**
- Stale top-level `content_sha256` values repaired: **2,262**
- Top-level values already correct: **159**
- Valid top-level content hashes after repair: **2,421 of 2,421**
- Valid nested `cleaning.content_sha256` values: **2,421 of 2,421**
- Text, record IDs, record order, and provisional token counts were preserved.
- The stale partial `reports/source_selection_state.json` checkpoint was removed.
- A machine-readable repair report was added at `reports/content_hash_repair.json`.

## Corpus identity

- Old final JSONL SHA-256: `ea85acb3f37b907deda87512c75b823ba6d1aca033cc8e536f428acdd43e3b14`
- Repaired final JSONL SHA-256: `2e06bf4be2a03f73e53f64f3b6dc77e7beda7fdd1203ac92ab40372f96d8f9e9`
- Text-and-ID identity SHA-256: `d0262289ab471839a07ecf2da51ed38dd9872ade524086701e0059e1288fdb0e`
- Final documents: **2,421**
- Provisional Unicode-word tokens: **1,000,032**

The final file SHA changed only because record metadata changed. The Hindi text and its order did not change.

## Evidence integrity

- Repaired ZIP SHA-256: `0262da2e9073fa7de03bbc163e04fea5cf0fb9a13de321289778895b0298dd96`
- ZIP corruption test: **passed**
- ZIP entries: **33**
- Internally checksummed artifacts: **32**
- Internal artifact checksum verification: **32 of 32 passed**
- Private benchmark, raw, rejected, reserve, native-review, and private-checkpoint files: **not present**

## Updated dependent evidence

The following were regenerated or updated:

- `final/hindi.1m.decontaminated.jsonl`
- `reports/content_hash_repair.json`
- `reports/final_validation.json`
- `reports/final_trim.json`
- `manifests/hindi.1m.decontaminated.manifest.json`
- `reports/phase3_status.json`
- `reports/artifact_checksums.json`
- `reports/SAFE_EVIDENCE_README.txt`

## Final determination

**Phase 3 is now fully verified at the pilot-data level.**

The production-data gate remains closed because the target-aware mixed-language tokenizer has not been trained or frozen, the Kronecker input architecture has not yet passed controlled comparisons, and corpus token totals have not been recounted with the frozen tokenizer.
