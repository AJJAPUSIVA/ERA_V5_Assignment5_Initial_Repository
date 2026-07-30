# ERA V5 Session 5 — Mixture and Curriculum Specification

**Status:** Initial assignment submission plan  
**Executed data gate:** General, verified Hindi, and Hindi–English mixed-language pilots  
**Planning convention:** 100B tokens is used only as a transparent reference budget for supply arithmetic. It is **not** a claim that the cohort budget has been fixed at 100B.

## 1. Executive hypothesis

V5 should not maximize a single benchmark family at the expense of broad language competence. My hypothesis is that the best mixture uses a broad General-language base, a large but quality-tiered Indic allocation, explicit Reasoning, Code, Mathematics, Agentic, and Long-context lanes, and a protected high-quality reserve for the final cooldown.

The numbers below are hypotheses to be tested through cheap proxy runs before full-scale adoption. The present project has independently verified pilot supply for General, Hindi, and Hinglish. Other capability lanes remain **starved** until their inventory datasets pass the same data gate.

## 2. Data-gating evidence

| Pilot lane | Final supply | Gate status | Evidence |
|---|---:|---|---|
| General | 5,175,419 provisional tokens | Verified | [Phase 2 report](evidence/V5_Phase2_General_5M_Evidence_Verification_20260729.md) |
| Hindi Devanagari | 1,000,032 provisional tokens | Verified after hash repair | [Phase 3 repaired report](evidence/V5_Phase3_Hindi_1M_Repaired_Verification_20260729.md) |
| Hinglish mixed-language | 1,000,016 provisional tokens | Automated gate passed; bilingual review pending | [Phase 4 report](evidence/V5_Phase4_Hinglish_1M_Evidence_Verification_20260729.md) |
| **Total documented pilot supply** | **7,175,467 provisional tokens** | Pilot scale | [Data-gate summary](evidence/data_gate_summary.md) |

Important limitation: these counts are provisional Unicode-word counts. They are not final tokenizer-token counts.

## 3. Full budget allocation

The first 92% is the main curriculum. The final 8% is an exclusive anneal reserve held out from earlier stages.

| Capability lane | Main curriculum | Anneal contribution | Final effective exposure | Why it exists |
|---|---:|---:|---:|---|
| General language | 27.5% | 2.0% | **29.5%** | Broad language modelling, knowledge, discourse, and regression protection |
| Indic | 23.5% | 2.5% | **26.0%** | Native-language, translation, instruction-following, and code-switch competence |
| Reasoning | 12.0% | 1.5% | **13.5%** | Multi-step correctness and transferable problem solving |
| Code | 8.0% | 0.5% | **8.5%** | Program synthesis, structured generation, and execution-aware tasks |
| Mathematics/science | 5.5% | 0.5% | **6.0%** | Quantitative reasoning and scientific notation |
| Agentic | 5.5% | 0.5% | **6.0%** | Tool selection, action planning, observation handling, and recovery |
| Long-context | 5.5% | 0.5% | **6.0%** | Retrieval, dependency tracking, and synthesis across long inputs |
| Non-Indic multilingual | 4.5% | 0.0% | **4.5%** | Cross-lingual transfer and protection against bilingual over-specialization |
| **Total** | **92.0%** | **8.0%** | **100.0%** | |

### Why these numbers are defensible hypotheses

- General remains the largest lane because every specialist capability depends on stable language modelling.
- Indic is the second-largest lane because V5 explicitly targets Indic competence, but it is quality-tiered rather than treated as one undifferentiated bucket.
- Reasoning receives more exposure than any specialist lane because it transfers across mathematics, code, agentic work, and factual tasks.
- Code, Mathematics, Agentic, and Long-context are large enough to be explicit capabilities, but not large enough to crowd out language coverage before proxy evidence supports doing so.
- The 8% anneal reserve is large enough to affect the final training phase while leaving 92% for broad curriculum learning.

## 4. Indic tier allocation

The Indic share is split explicitly across quality tiers.

| Indic tier | Main share | Anneal share | Final total-budget share | Share of final Indic allocation |
|---|---:|---:|---:|---:|
| Verified | 10.0% | 2.5% | **12.5%** | **48.1%** |
| Unverified | 6.0% | 0.0% | **6.0%** | **23.1%** |
| Translated | 4.0% | 0.0% | **4.0%** | **15.4%** |
| Synthetic | 3.5% | 0.0% | **3.5%** | **13.5%** |
| **Total Indic** | **23.5%** | **2.5%** | **26.0%** | **100.0%** |

### Tier policy

- **Verified:** passed source, licence, language/script, quality, deduplication, cross-lane, decontamination, and human-review gates where required.
- **Unverified:** useful Indic text that passes automated cleaning but lacks full source or human verification.
- **Translated:** machine- or human-translated data with source-language provenance and translation-quality checks.
- **Synthetic:** generated or transformed examples whose prompts, generators, and filtering rules are documented.

The synthetic share is capped at 3.5% of the total budget. This is motivated by the Hinglish pilot, where limited authentic supply caused the final pilot to become 55.61% synthetic. That corpus passed automated data-quality checks, but the result demonstrates why synthetic supply should not silently dominate the full mixture.

## 5. Supply and repetition accounting

The following table uses a **100B-token reference budget** only to make the supply gap visible. It shows why the current pilots support a data gate and proxy experiment, but cannot populate a production mixture through repetition.

| Lane/tier | Final share | Required at 100B | Current unique pilot supply | Naive repeat factor | Status |
|---|---:|---:|---:|---:|---|
| General Language | 29.5% | 29.50B | 5.175M | 5,700.0× | Severely starved |
| Indic Verified | 12.5% | 12.50B | 1.000M | 12,499.6× | Severely starved |
| Indic Unverified | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Indic Translated | 4.0% | 4.00B | 0 | Unavailable | No gated supply |
| Indic Synthetic | 3.5% | 3.50B | 556,100 | 6,293.8× | Severely starved |
| Reasoning | 13.5% | 13.50B | 0 | Unavailable | No gated supply |
| Code | 8.5% | 8.50B | 0 | Unavailable | No gated supply |
| Mathematics Science | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Agentic | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Long Context | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Non Indic Multilingual | 4.5% | 4.50B | 0 | Unavailable | No gated supply |

Additional current supply:

- Authentic Hinglish pending bilingual review: **443,916 provisional tokens**. It is not counted as verified Indic until review is completed.
- Total Hinglish synthetic supply: **556,100 provisional tokens**.
- No project-local data-gated supply currently exists for Reasoning, Code, Mathematics/science, Agentic, Long-context, Non-Indic multilingual, Indic unverified, or Indic translated lanes.

### Repeat policy

The selector must not use high repetition to hide a supply gap.

- Preferred: no repetition before the unique pool is exhausted.
- Soft warning: more than 2× exposure.
- Hard review: more than 4× exposure.
- Prohibited for production planning: repeat factors in the hundreds or thousands.

Therefore, the current pilot supply is evidence for cleaning quality and small proxies—not evidence that the final percentages are already supplied.

## 6. Dataset and benchmark mapping

Rows marked **pending inventory confirmation** are proposed capability mappings. They must be replaced with the exact Session 5 inventory entries before the mixture is accepted for cohort training.

| Lane | Current project data | Planned inventory fill | Primary evaluation |
|---|---|---|---|
| General | Verified General 5M pilot | General-language sources from course inventory | MMLU-Pro, ARC-Challenge, WinoGrande, validation loss |
| Indic verified | Verified Hindi 1M; authentic Hinglish pending review | Verified Indic sources from course inventory | MILU Hindi, IndicQA Hindi, IndicIFEval |
| Indic unverified | None | Pending inventory confirmation | Indic language modelling and downstream composite |
| Indic translated | None | Pending inventory confirmation | FLORES/IN22-style translation evaluation |
| Indic synthetic | IndicCMix-derived Hinglish subset | Synthetic Indic sources with generator provenance | Indic composite plus human-quality audit |
| Reasoning | None | Pending inventory confirmation | GSM8K, BBH, GPQA, MMLU-Pro |
| Code | None | Pending inventory confirmation | HumanEval/MBPP-style execution metrics |
| Mathematics/science | None | Pending inventory confirmation | GSM8K and MATH-style quantitative evaluation |
| Agentic | None | Pending inventory confirmation | Tool success, completion rate, invalid-action rate |
| Long-context | None | Pending inventory confirmation | RULER/LongBench-style retrieval and synthesis |
| Non-Indic multilingual | None | Pending inventory confirmation | Cross-lingual validation and multilingual composite |

### Benchmark contamination rule

All benchmark inputs, answer choices, prompts, and visible task text used for evaluation must remain private and must be excluded from training through the same decontamination pipeline used in Phases 1–4.

## 7. Protected always-on floors

The selector enforces floors over every rolling **100,000 model-token window** during the main curriculum.

| Protected lane | Minimum floor | Reason |
|---|---:|---|
| General language | 20% | Prevent specialist narrowing and broad-language regression |
| Verified Indic | 6% | Prevent late-stage loss of native-script competence |
| Reasoning | 4% | Preserve multi-step capability throughout training |
| Code | 3% | Preserve structured generation and execution-oriented syntax |
| Agentic | 2% | Prevent tool-use exposure from becoming a one-time phase |
| Long-context | 2% | Maintain exposure to long dependency chains |

Rules:

1. Floors apply to rolling windows, not only cumulative totals.
2. A floor becomes executable only after that lane passes the data gate.
3. If clean supply cannot satisfy a floor without violating the repetition policy, training must pause or the floor must be revised through an explicit review.
4. Synthetic data cannot satisfy the verified-Indic floor.

## 8. Anneal reserve

Exactly **8% of total training tokens** is held out from the first 92%.

Reserve composition:

| Reserve component | Total-budget share |
|---|---:|
| General, high-quality | 2.0% |
| Verified Indic | 2.5% |
| Reasoning | 1.5% |
| Code | 0.5% |
| Mathematics/science | 0.5% |
| Agentic | 0.5% |
| Long-context | 0.5% |
| **Total reserve** | **8.0%** |

Eligibility:

- Data-gated and licence-cleared
- Excluded from all earlier stages
- No benchmark contamination
- No duplicate exposure
- Highest source-quality tier available
- Human-reviewed where synthetic, translated, or mixed-language quality is material

The reserve is not a second copy of earlier data. It is a genuinely held-back pool used during the cooldown.

## 9. Curriculum schedule

| Stage | Budget interval | Main emphasis |
|---|---:|---|
| Foundation | 0–35% | Broad language, verified data, easy/medium tasks |
| Capability expansion | 35–67% | Indic, code, mathematics, medium reasoning, initial tools and long context |
| Reasoning intensification | 67–92% | Hard reasoning, agentic trajectories, long context, protected language floors |
| Anneal/cooldown | 92–100% | Exclusive high-quality reserve |

Detailed stage weights are stored in [`configs/curriculum.yaml`](configs/curriculum.yaml).

## 10. Difficulty and reasoning-length bands

Difficulty and reasoning length are separate controls.

### Difficulty

| Band | Operational definition | Example |
|---|---|---|
| D1 | Retrieval, classification, or one operation | Identify the language of a sentence |
| D2 | Two or three dependent operations | Compare two paragraphs and justify one difference |
| D3 | Multi-step constrained reasoning | Solve a quantitative problem with several dependencies |
| D4 | Branching, tool-assisted, or long-horizon work | Use tools, evaluate results, and revise a plan |

### Reasoning length

| Band | Operational definition | Example |
|---|---|---|
| R0 | No intermediate reasoning required | Sentiment classification |
| R1 | One or two linked steps | Simple arithmetic word problem |
| R2 | Three to five linked steps | Constraint-based scheduling |
| R3 | Six or more linked steps, branching, or tool calls | Multi-source research and synthesis |

## 11. Low-budget proxy experiment

The executed proxy isolates one testable hypothesis using only the currently data-gated lanes.

**Model candidate:** `Qwen/Qwen2.5-1.5B`  
**Method:** continued pretraining from the same base checkpoint  
**Budget ceiling:** 1,000 SEK  
**Mandatory runs:** M0 and M1  
**Optional run:** M2 only after M0 and M1 complete

| Run | General | Hindi | Hinglish | Purpose |
|---|---:|---:|---:|---|
| M0 | 72% | 14% | 14% | Supply-proportional baseline |
| M1 | 60% | 20% | 20% | Protected Indic treatment |
| M2 | Same cumulative 60/20/20 | Curriculum schedule | Test timing separately from cumulative mixture |

Training details and fixed decision rules are in [`configs/proxy_experiments.yaml`](configs/proxy_experiments.yaml).

Acceptance rule:

- Hindi validation loss improves by at least 2%.
- Combined native and Romanized Hinglish loss improves by at least 2%.
- General validation loss worsens by no more than 1%.
- No lane worsens by more than 2%.
- Weighted overall loss does not worsen.

With one seed, results are directional evidence. A proposed 3B confirmation repeats the baseline and winning treatment with at least two seeds.

## 12. Starved-lane cleaning order

Cleaning follows the mixture gaps rather than convenience.

1. Reasoning
2. Agentic
3. Long-context
4. Code
5. Mathematics/science
6. Indic translated
7. Indic unverified
8. Non-Indic multilingual
9. Additional verified Indic and authentic Romanized Hinglish

The ordering can change after the exact course inventory is inserted and required-token gaps are recomputed.

## 13. Reproducibility and privacy

Public repository contents:

- Mixture and curriculum specifications
- Validation scripts
- Text-free manifests and checksums
- Aggregated experiment metrics
- Data-gate verification reports

Never publish:

- Raw or rejected records
- Gated dataset contents
- Private benchmark text
- Human-review samples
- Model credentials or API tokens
- Paid-training checkpoints unless separately licensed and intentionally released

## 14. Assignment completion checklist

| Requirement | Status |
|---|---|
| Share for every capability lane | Complete as hypothesis |
| Indic verified/unverified/translated/synthetic split | Complete |
| Agentic, Reasoning, and Long-context named | Complete |
| Inventory dataset mapping | Pending exact course inventory for starved lanes |
| Real supply and repeat accounting | Complete for current project supply |
| Protected floors | Complete |
| Anneal reserve | Complete |
| Curriculum stages | Complete |
| Difficulty bands with examples | Complete |
| Reasoning-length bands with examples | Complete |
| 1B-scale proxy plan | Complete; 1.5B candidate selected |
| 3B confirmation plan | Specified, not executed |
| Data gate | General and Hindi verified; Hinglish automated gate passed |
| Public GitHub link | Pending push and incognito test |

## 15. Decision statement

This plan is intentionally falsifiable. The mixture is accepted only when cheap proxy runs show capability gains within predefined regression limits. Until then, every percentage remains a design hypothesis rather than a production truth.
