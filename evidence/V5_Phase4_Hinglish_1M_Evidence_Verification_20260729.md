# V5 Phase 4 — Hinglish Mixed-Language 1M Evidence Verification

**Evidence ZIP:** `hinglish_mixed_1m_20260729T140153Z_evidence.zip`  
**Verification date:** 2026-07-29  
**Overall determination:** **Automated data-quality gate passed. Mixture-composition gate requires adjustment before tokenizer-mixture freezing.**

## 1. Package integrity

- External SHA-256 expected: `2a94d5b76cc01281d4515edc19831d16f2362d50e1b601b9dacb25a367c4d750`
- External SHA-256 calculated: `2a94d5b76cc01281d4515edc19831d16f2362d50e1b601b9dacb25a367c4d750`
- Match: **Yes**
- ZIP corruption test: **Passed**
- ZIP entries: **29**
- Internal artifact checksums: **22 of 22 passed**
- `reports/artifact_checksums.json` is intentionally not self-hashed.

## 2. Input provenance

The package records the expected verified inputs:

- URL-calibrated V5 pipeline ZIP:  
  `a18bc39fdf393a31cade27e18652ed889723c86076a713bb35261f02347826e0`
- Verified General 5M evidence ZIP:  
  `ea3e8285d6985b0cd0e8636809d05cc643e0c1fa8fb4b189a400cdf6975bb74e`
- Repaired Hindi 1M evidence ZIP:  
  `0262da2e9073fa7de03bbc163e04fea5cf0fb9a13de321289778895b0298dd96`
- General 5M corpus:  
  `81aeb4800f2d6eb271ef6c5bc6eae3467afe55509dd7295cef11be377e356d80`
- Repaired Hindi 1M corpus:  
  `2e06bf4be2a03f73e53f64f3b6dc77e7beda7fdd1203ac92ab40372f96d8f9e9`

Pinned source revisions:

- COMI-LINGUA: `0214cb358e59e36da60e01d3d59ddd24df897749`
- PHINC: `44b5471df75e508b9d6fcdbcc93df04bb1e84056`
- IndicCMix: `2ead5962df60aed39c510db24f3368c037ab3522`
- HinGE: `e25a10382d9adb77f3a4f03b721fbd0a43c0de4c`

## 3. Source collection and cleaning

### Raw supply

- Authentic records: **44,225**
- Authentic provisional tokens: **743,950**
- Synthetic top-up records: **34,397**
- Synthetic top-up provisional tokens: **706,075**
- Total raw records: **78,622**

### Cleaning

- Accepted: **62,742**
- Rejected: **15,880**
- Accepted provisional tokens: **1,227,879**
- PII masks:
  - Emails: 17
  - Phone-like values: 60
  - URLs: 1,244

Primary rejection counts:

- Missing Devanagari: 7,908
- Insufficient Romanized-Hindi markers: 4,140
- Missing Latin text: 2,670
- Too short: 1,136
- Other script/mixedness/repetition checks: 26

The final corpus was independently scanned for obvious unmasked email and URL patterns; none were found.

## 4. Internal deduplication

Reported removal:

- Documents seen: **62,742**
- Exact duplicates removed: **33**
- MinHash near duplicates removed: **74**
- Kept: **62,635**
- Near-duplicate threshold: 0.88
- MinHash configuration: 128 permutations, 5-word shingles, 16 bands

The text-free duplicate audit contains exactly **107** rows, matching 33 exact plus 74 near duplicates.

The packaged V5 deduplicator was independently rerun on the final corpus using the same settings:

- Records seen: **51,633**
- Exact duplicates remaining: **0**
- Near duplicates remaining: **0**
- Records retained: **51,633**

The rerun preserved the original ID and text sequence for all 51,633 records.

## 5. Cross-lane exclusion

Reported comparison against the verified General and Hindi lanes:

- Reference documents: **7,473**
- Candidate documents: **62,635**
- Exact matches removed: **0**
- Near matches removed: **0**
- Kept: **62,635**
- Threshold: 0.90
- MinHash: 128 permutations, 7-word shingles, 16 bands

An independent exact-text comparison between the final Phase 4 corpus and all 7,473 supplied General/Hindi reference documents found **zero exact overlaps**.

The complete cross-lane MinHash scan cannot be reproduced from the safe package alone because its private index and pre-trim candidate file are excluded. Its report, input hashes, and empty safe removal audit are internally consistent.

## 6. Benchmark decontamination

Private benchmark inventory:

- 111,958 unique scan variants
- English benchmarks: MMLU-Pro, ARC-Challenge, WinoGrande Debiased, BBH, GSM8K, GPQA Main
- Hindi benchmarks: MILU Hindi, IndicQA Hindi, IndicIFEval Hindi
- Hinglish references: COMI-LINGUA LID test and HinGE human text
- Gold answers included: **No**
- Rationales included: **No**
- Private benchmark text included in safe evidence: **No**

Decontamination result:

- Documents scanned: **62,635**
- Removed: **3,988**
- Kept before final trim: **58,647**

Matches removed:

- COMI-LINGUA LID test: **3,987 documents**
- IndicQA Hindi: **1 document**

Primary methods:

- Exact document: 3,867
- Exact embedded span: 6
- High word-ngram overlap: 115

The large COMI-LINGUA removal demonstrates substantial overlap between the selected source split and the held-out test references. The pipeline correctly removed those documents before final selection.

The safe audit contains exactly **3,988 text-free rows**. The synthetic benchmark-scanner smoke test passed.

The complete benchmark scan cannot be independently rerun from the safe ZIP because benchmark text is intentionally private.

## 7. Final corpus validation

Independent checks on `final/hinglish.mixed.1m.decontaminated.jsonl`:

- Valid JSONL records: **51,633**
- Unique IDs: **51,633**
- Unique source/style keys: **51,633**
- Unique exact text hashes: **51,633**
- Valid top-level `content_sha256`: **51,633 of 51,633**
- Valid per-record provisional token counts: **51,633 of 51,633**
- Sequential final positions: **0 through 51,632**
- Characters: **5,834,833**
- Provisional Unicode-word tokens: **1,000,016**
- Language: `hi-en` for every record
- Lane: `mixed_language` for every record
- Final file SHA-256:  
  `22dd2553b26ab8b3b3ff3c85045f56bc93ae2389ad439f08a2e2be1567c69668`

Every final record also satisfies the style-specific script and mixedness constraints recorded in the notebook.

## 8. Final source and style mixture

### By source

| Source | Documents | Provisional tokens |
|---|---:|---:|
| COMI-LINGUA | 15,928 | 324,073 |
| PHINC | 8,831 | 119,843 |
| IndicCMix | 26,874 | 556,100 |
| **Total** | **51,633** | **1,000,016** |

### By style

| Style | Documents | Provisional tokens | Token share |
|---|---:|---:|---:|
| Authentic native-script code-mixed | 15,928 | 324,073 | 32.41% |
| Authentic Romanized Hinglish | 8,831 | 119,843 | 11.98% |
| Synthetic native-script code-mixed | 13,380 | 278,974 | 27.90% |
| Synthetic Romanized Hinglish | 13,494 | 277,126 | 27.71% |

Aggregated token shares:

- Authentic: **443,916 tokens — 44.39%**
- Synthetic: **556,100 tokens — 55.61%**
- Native-script mixed: **603,047 tokens — 60.30%**
- Romanized mixed: **396,969 tokens — 39.70%**

## 9. Mixture-composition issue

The notebook intended the following 1M-token quotas:

- Authentic native-script: 35%
- Authentic Romanized: 25%
- Synthetic native-script: 20%
- Synthetic Romanized: 20%

The final supply did not meet those quotas because the cleaned and decontaminated authentic pool was too small, especially for PHINC Romanized Hinglish. The deterministic fallback filled the shortfall with synthetic IndicCMix records.

Compared with the intended quotas, the final corpus is short by:

- Authentic native-script: **25,927 tokens**
- Authentic Romanized: **130,157 tokens**

It contains excess synthetic supply of approximately:

- Synthetic native-script: **78,974 tokens**
- Synthetic Romanized: **77,126 tokens**

Therefore, approximately **156,084 additional authentic tokens** are needed to produce the intended 60% authentic / 40% synthetic 1M-token mixture while replacing an equivalent amount of synthetic text.

This does not invalidate the cleaned corpus. It means the corpus should not be treated as the frozen target tokenizer mixture until either:

1. the original quotas are restored with more authentic supply; or
2. the mixture specification is explicitly revised and approved to 44.39% authentic / 55.61% synthetic.

## 10. Kronecker readiness diagnostics

The package correctly labels these as pre-tokenizer word-surface proxies.

| Position dimension | Surfaces over limit | Proxy truncation rate |
|---:|---:|---:|
| 16 | 75,808 | 7.5807% |
| 24 | 13,249 | 1.3249% |
| 32 | 3,742 | 0.3742% |
| 48 | 58 | 0.0058% |

UTF-8 byte lengths:

- Median: 6 bytes
- 90th percentile: 15 bytes
- 99th percentile: 27 bytes
- Maximum: 74 bytes

The Kronecker feature smoke test produced distinct deterministic features for Latin, Devanagari, abbreviated, and Romanized sample surfaces.

For this pre-tokenizer corpus, position dimension 48 has substantially lower proxy truncation than 32. The final choice must be recomputed over the actual token surfaces of each trained 64K, 96K, and 128K tokenizer candidate.

## 11. Privacy review

The ZIP contains no:

- Raw source files
- Cleaned pre-dedup files
- Rejected text
- Reserve text
- Human-review sample
- Private checkpoints
- Private benchmark JSONL
- Consolidated benchmark scan text
- General/Hindi cross-lane reference index

All three public audit CSVs are text-free.

`phase4_benchmark_inventory.json` contains absolute private Drive paths as provenance metadata, but no benchmark text. Future evidence packages should prefer relative or redacted private-path identifiers.

## 12. Completion status

The package reports Phase 4 as `completed` while correctly retaining:

- Production data gate: **false**
- Tokenizer frozen: **false**
- Kronecker model implemented: **false**

The private bilingual human review also remains pending.

## Final determination

**Phase 4 passes the automated cleaning, masking, script/mixedness, internal deduplication, cross-lane exact-overlap, benchmark decontamination, record-integrity, manifest, checksum, and privacy gates.**

It should be considered a verified **mixed-language pilot corpus**, not yet the frozen tokenizer-training mixture.

Before tokenizer candidate training is treated as final:

1. add approximately **156,084 authentic tokens**, primarily Romanized Hinglish; or formally approve the synthetic-majority mixture;
2. complete the private bilingual human review;
3. train the actual 64K, 96K, and 128K tokenizer candidates;
4. recompute fertility and Kronecker truncation using their real token surfaces.
