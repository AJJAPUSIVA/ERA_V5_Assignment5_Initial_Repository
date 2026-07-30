# V5 Phase 2 — General 5M Evidence Verification

**Evidence ZIP:** `general_5m_deterministic_20260729T105823Z_evidence.zip`  
**Verification date:** 2026-07-29  
**Overall result:** **PASSED**

## 1. Package integrity

- External SHA-256 expected: `ea3e8285d6985b0cd0e8636809d05cc643e0c1fa8fb4b189a400cdf6975bb74e`
- External SHA-256 calculated: `ea3e8285d6985b0cd0e8636809d05cc643e0c1fa8fb4b189a400cdf6975bb74e`
- Match: **Yes**
- ZIP corruption test: **Passed**
- ZIP entries: **38**
- Internal artifact checksums: **30 of 30 passed**
- The only unlisted file is `reports/artifact_checksums.json` itself, which is expected to avoid self-referential hashing.

## 2. Input provenance

The recorded input hashes were independently compared with the supplied reference artifacts:

- URL-calibrated pipeline ZIP SHA-256:  
  `a18bc39fdf393a31cade27e18652ed889723c86076a713bb35261f02347826e0`
- Verified Phase 1 evidence ZIP SHA-256:  
  `55864d2143add4c2b512f2c2ddf0b5e7b58d5940cdce2e677d1accb598fb6f59`
- FineWeb-Edu revision recorded for every final record:  
  `87f09149ef4734204d70ed1d046ddc9ca3f2b8f9`
- Dataset/config: `HuggingFaceFW/fineweb-edu`, `sample-10BT`

The Phase 1 scanner source copied into Phase 2 has SHA-256  
`2bb9c6dba18336bc6e8a70006bbe7bcdf725e3540e830638a3275f9067864943`, matching the scanner in the verified Phase 1 package.

## 3. Deterministic source collection and cleaning

Four new raw shards were reported:

| Shard | Raw documents | Raw provisional tokens | Accepted documents | Accepted provisional tokens | Rejected |
|---|---:|---:|---:|---:|---:|
| shard_01 | 949 | 1,051,563 | 948 | 1,051,499 | 1 |
| shard_02 | 1,047 | 1,055,478 | 1,046 | 1,054,540 | 1 |
| shard_03 | 985 | 1,050,945 | 980 | 1,023,353 | 5 |
| shard_04 | 1,068 | 1,050,485 | 1,065 | 1,047,197 | 3 |
| **Total** | **4,049** | **4,208,471** | **4,039** | **4,176,589** | **10** |

Reported rejection reasons:

- High URL density: 6
- Too short: 2
- Repeated lines: 1
- Low lexical diversity: 1

Reported PII masking across the four new shards:

- Emails: 194
- IP addresses: 14
- Phone matches: 264

The safe evidence package does not contain the four raw source shards or rejected records, so their source-selection hashes and rejection decisions cannot be recomputed solely from this package. Their reported totals do reconcile with the accepted final supply.

## 4. Merge and final corpus

The verified Phase 1 seed and four accepted shards reconcile as follows:

| Component | Documents | Provisional tokens |
|---|---:|---:|
| Phase 1 seed | 1,013 | 998,830 |
| shard_01 | 948 | 1,051,499 |
| shard_02 | 1,046 | 1,054,540 |
| shard_03 | 980 | 1,023,353 |
| shard_04 | 1,065 | 1,047,197 |
| **Final** | **5,052** | **5,175,419** |

Independent checks on `final/general.5m.decontaminated.jsonl`:

- Valid JSONL records: **5,052**
- Unique public IDs: **5,052**
- Unique source record IDs: **5,052**
- Merge positions: exactly `0` through `5051`
- Text/content SHA-256 fields correct: **5,052 of 5,052**
- Language: `en` for all records
- Lane: `general` for all records
- Source: `HuggingFaceFW/fineweb-edu` for all records
- Licence: `ODC-By-1.0` for all records
- Source revision consistent across all records
- Characters: **23,869,269**
- Final content SHA-256:  
  `81aeb4800f2d6eb271ef6c5bc6eae3467afe55509dd7295cef11be377e356d80`

The final and pre-decontamination files are byte-for-byte identical because no benchmark-contaminated document was removed.

## 5. Global deduplication

Packaged report:

- Documents seen: 5,052
- Kept: 5,052
- Exact duplicates: 0
- Near duplicates: 0
- Threshold: 0.82
- MinHash: 128 permutations, 5-word shingles, 16 bands, seed 42

The packaged global deduplicator was independently rerun on the final corpus:

- Reproduced exact duplicates: **0**
- Reproduced near duplicates: **0**
- Reproduced kept records: **5,052**
- Reproduced output SHA-256:  
  `81aeb4800f2d6eb271ef6c5bc6eae3467afe55509dd7295cef11be377e356d80`
- Byte-for-byte match with supplied final corpus: **Yes**

The synthetic global-dedup smoke test also passed, removing one exact and one near duplicate from four synthetic records.

## 6. Benchmark decontamination

The evidence records all six benchmark families:

- MMLU-Pro: 12,102
- ARC-Challenge: 2,590
- WinoGrande Debiased: 12,282
- BIG-Bench Hard: 6,511
- GSM8K: 8,792
- GPQA Main: 448

Total normalized benchmark examples: **42,725**  
Unique scan variants: **69,736**

Phase 2 scan result:

- Documents scanned: 5,052
- Kept: 5,052
- Removed: 0
- GPQA matches: 0

The synthetic scanner smoke test passed, removing one embedded synthetic benchmark example and retaining one clean record.

Because the safe package intentionally excludes normalized benchmark text and scan variants, the full benchmark scan cannot be independently rerun from this package alone. Its result is supported by the scanner provenance, benchmark inventory/validation snapshots, smoke test, reconciliation reports, and empty contamination audit.

## 7. Privacy and restricted benchmark review

The ZIP contains no:

- `benchmarks_private` directory
- Normalized benchmark JSONL files
- Benchmark scan JSONL files
- Consolidated scan-variant file
- Redistributed GPQA text

The package includes benchmark metadata and hashes only, which are appropriate for evidence verification.

## 8. Manifest and completion gate

- Manifest status: **ready**
- Phase 2 status: **completed**
- Final records: **5,052**
- Final provisional tokens: **5,175,419**
- Global duplicates removed: **0**
- Benchmark-contaminated records removed: **0**
- Production data gate: **false**, correctly retained

Remaining blockers recorded by the package:

1. Freeze the V5 tokenizer.
2. Recount the corpus with the frozen tokenizer.
3. Build production-scale multi-lane supply.
4. Perform cross-lane/global production deduplication.

## 9. Minor observations

- The inherited cleaning configuration is named `general_205m.yaml`; this is a naming/provenance detail, not a failed check.
- Manifest `pipeline_config_records` contains both an absolute Colab path and a relative path for the same configuration, reflecting new shards versus the Phase 1 seed. Normalizing this field in future manifests would make reporting cleaner.
- The 5,175,419 token count remains provisional, as explicitly declared.

## Final determination

**V5 Phase 2 — Deterministic General 5M pilot is verified as completed.**

The evidence package is internally consistent, its checksums pass, its final corpus reconciles exactly, the packaged global deduplicator reproduces the claimed zero-duplicate result, and no private benchmark files were included.

The production-data gate should remain closed until tokenizer freezing, exact token recounting, multi-lane expansion, and cross-lane production deduplication are complete.
