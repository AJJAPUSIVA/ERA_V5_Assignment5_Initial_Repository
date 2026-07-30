# ERA V5 Session 5 — Mixture and Curriculum Specification

**Status:** Session-aligned written plan; low-budget proxy planned but not yet executed

**Public repository:** published; incognito-access confirmation still must be recorded before submission

**Data gate:** General and Hindi verified; Hinglish automated gate passed with bilingual review pending

**Planning convention:** a 100B-token reference is used only for transparent supply arithmetic. It is not a claim that the cohort budget is fixed at 100B.

## 1. Design target and falsifiable hypothesis

Session 5 defines V5 around three differentiators: strong coding and agentic work, controllable reasoning depth, and native Indic competence. This plan works backward from those capabilities and treats every allocation as a hypothesis rather than a production truth.

> A broad General-language base, a protected and quality-tiered Indic lane, explicit Code, Reasoning, Agentic and Long-context capacity, and a held-back high-quality anneal reserve will outperform a web-heavy baseline without unacceptable regression in broad language competence.

The mixture is not trusted at full scale until it survives approximately 1B-parameter screening and 3B-parameter confirmation.

## 2. Data-gating evidence

| Pilot lane | Final supply | Gate status | Evidence |
|---|---:|---|---|
| General | 5,175,419 provisional tokens | Verified | [Phase 2 report](evidence/V5_Phase2_General_5M_Evidence_Verification_20260729.md) |
| Hindi Devanagari | 1,000,032 provisional tokens | Verified after hash repair | [Phase 3 report](evidence/V5_Phase3_Hindi_1M_Repaired_Verification_20260729.md) |
| Hinglish mixed-language | 1,000,016 provisional tokens | Automated gate passed; bilingual review pending | [Phase 4 report](evidence/V5_Phase4_Hinglish_1M_Evidence_Verification_20260729.md) |
| **Total documented pilot supply** | **7,175,467 provisional tokens** | Pilot scale | [Data-gate summary](evidence/data_gate_summary.md) |

These are provisional Unicode-word counts, not final tokenizer-token counts.

## 3. Main-pretraining and anneal presets

The first **92%** is the main curriculum. The final **8%** is a genuinely held-back anneal reserve.

### 3.1 Contribution to the total training budget

| Capability lane | Main contribution | Anneal contribution | Final effective exposure |
|---|---:|---:|---:|
| General language | 27.5% | 2.0% | **29.5%** |
| Indic | 23.5% | 2.5% verified | **26.0%** |
| Reasoning | 12.0% | 1.5% | **13.5%** |
| Code | 8.0% | 0.5% | **8.5%** |
| Mathematics/science | 5.5% | 0.5% | **6.0%** |
| Agentic | 5.5% | 0.5% | **6.0%** |
| Long-context | 5.5% | 0.5% | **6.0%** |
| Non-Indic multilingual | 4.5% | 0.0% | **4.5%** |
| **Total** | **92.0%** | **8.0%** | **100.0%** |

### 3.2 Normalized main-pretraining preset

| Lane | Share within main pretraining |
|---|---:|
| General Language | 29.89% |
| Indic | 25.54% |
| Reasoning | 13.04% |
| Code | 8.70% |
| Mathematics Science | 5.98% |
| Agentic | 5.98% |
| Long Context | 5.98% |
| Non Indic Multilingual | 4.89% |

### 3.3 Normalized anneal preset

| Anneal component | Share within reserve |
|---|---:|
| General Language | 25.00% |
| Indic Verified | 31.25% |
| Reasoning | 18.75% |
| Code | 6.25% |
| Mathematics Science | 6.25% |
| Agentic | 6.25% |
| Long Context | 6.25% |

The reserve is excluded from the first 92%; it is not a repeated copy of earlier data.

## 4. Indic tier split

| Indic tier | Final total-budget share | Share of final Indic allocation |
|---|---:|---:|
| Verified | **12.5%** | **48.1%** |
| Unverified | **6.0%** | **23.1%** |
| Translated | **4.0%** | **15.4%** |
| Synthetic | **3.5%** | **13.5%** |
| **Total Indic** | **26.0%** | **100.0%** |

Synthetic Indic cannot satisfy the verified floor and is capped at 3.5% of the total budget. The Phase 4 pilot ended at 55.61% synthetic because authentic supply was insufficient; that result supports an explicit cap.

## 5. Supply and repetition accounting

The 100B reference exposes the gap between desired shares and currently gated supply.

| Lane/tier | Final share | Required at 100B | Current unique pilot supply | Naive repeat factor | Status |
|---|---:|---:|---:|---:|---|
| General language | 29.5% | 29.50B | 5.175M | 5,700.0× | Severely starved |
| Indic verified | 12.5% | 12.50B | 1.000M | 12,499.6× | Severely starved |
| Indic unverified | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Indic translated | 4.0% | 4.00B | 0 | Unavailable | No gated supply |
| Indic synthetic | 3.5% | 3.50B | 556,100 | 6,293.8× | Severely starved |
| Reasoning | 13.5% | 13.50B | 0 | Unavailable | No gated supply |
| Code | 8.5% | 8.50B | 0 | Unavailable | No gated supply |
| Mathematics/science | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Agentic | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Long-context | 6.0% | 6.00B | 0 | Unavailable | No gated supply |
| Non-Indic multilingual | 4.5% | 4.50B | 0 | Unavailable | No gated supply |

Authentic Hinglish contributes another 443,916 provisional tokens but remains outside the verified tier until bilingual review is complete.

Repeat policy:

- prefer unique data before repetition;
- warn above 2× exposure;
- require explicit review above 4×;
- never use hundreds or thousands of repetitions to claim that a production lane is supplied.

The complete accounting is in [`configs/supply_accounting.yaml`](configs/supply_accounting.yaml).

## 6. Inventory, benchmarks and training shape

The canonical inventory schema is:

`capability`, `dataset`, `published_samples`, `published_tokens_or_size`, `license`, `access_status`, `project_provenance_tier`, `data_gate_status`, `training_stage`, `loss_shape`, `benchmark`, and `source_citation`.

| Capability | Dataset | Published samples | Published tokens or size | License | Access status | Project provenance tier | Data gate status | Training stage | Loss shape | Benchmark | Source citation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| General | Verified General pilot | 5,052 | 5,175,419 | Mixed sources in Phase 2 manifest | Project pilot available | Project verified | Verified | Pretraining; high-quality anneal subset | Next-token loss | MMLU-Pro, ARC-Challenge, WinoGrande | [Phase 2 report](evidence/V5_Phase2_General_5M_Evidence_Verification_20260729.md) |
| Indic verified | Sangraha verified Hindi | 2,421 | 1,000,032 | CC-BY-4.0 | Project pilot available | Verified | Verified after hash repair | Pretraining; verified anneal subset | Next-token loss | MILU Hindi, IndicQA Hindi, IndicIFEval | [Phase 3 report](evidence/V5_Phase3_Hindi_1M_Repaired_Verification_20260729.md) |
| Indic authentic pending | COMI-LINGUA + PHINC | 24,759 | 443,916 | CC-BY-4.0 | Project pilot available | Authentic; human review pending | Automated gate passed; bilingual review pending | Pretraining; anneal after review | Next-token loss | Hinglish validation loss, Indic code-switch composite | [Phase 4 report](evidence/V5_Phase4_Hinglish_1M_Evidence_Verification_20260729.md) |
| Indic synthetic | IndicCMix subset | 26,874 | 556,100 | MIT | Project pilot available | Synthetic | Automated gate passed | Limited pretraining; excluded from verified floor | Next-token loss | Indic composite, human-quality audit | [Phase 4 report](evidence/V5_Phase4_Hinglish_1M_Evidence_Verification_20260729.md) |
| Indic unverified | ai4bharat/sangraha — unverified subset | Not published | 24,307.7M unverified tokens | CC-BY-4.0 | Public | Public unverified candidate | Public candidate; not yet project-gated | Pretraining | Next-token loss | Indic language modelling, Indic downstream composite | [Dataset card](https://huggingface.co/datasets/ai4bharat/sangraha) |
| Indic translated | ai4bharat/BPCC | ~230M bitext pairs | 109 GB | CC0 / CC-BY-4.0 by component | Public; acknowledgement required | Public parallel-corpus candidate | Public candidate; not yet project-gated | Pretraining; anneal only if high quality | Next-token loss on parallel text | IN22-Gen, IN22-Conv, FLORES-200 | [Dataset card](https://huggingface.co/datasets/ai4bharat/BPCC) |
| Reasoning | open-r1/OpenR1-Math-220k | 220,000 problems | 12.6 GB; 2–4 traces/problem | Apache-2.0 | Public | Public synthetic verified-reasoning candidate | Public candidate; not yet project-gated | Reasoning SFT; RL candidate | Supervised reasoning-trace loss | GSM8K, BBH, GPQA, MMLU-Pro | [Dataset card](https://huggingface.co/datasets/open-r1/OpenR1-Math-220k) |
| Code | bigcode/the-stack-v2 | 3.28B unique files | 67.5 TB; ~900B train tokens | Source-specific SPDX; permissive-only filter required | Public gated; bulk agreement required | Public source-code candidate | Public candidate; not yet project-gated | Pretraining; filtered anneal subset | Next-token loss on code | HumanEval, MBPP | [Dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
| Mathematics/science | AI-MO/NuminaMath-1.5 | 896,215 problems | Token count not published | Apache-2.0 | Public | Public math post-training candidate | Public candidate; not yet project-gated | Reasoning SFT; RL candidate | Supervised solution-trace loss | GSM8K, MATH-500, AIME-style evaluation | [Dataset card](https://huggingface.co/datasets/AI-MO/NuminaMath-1.5) |
| Agentic | Salesforce/xlam-function-calling-60k | 60,000 | Token count not published | CC-BY-4.0 | Public; acknowledgement required | Public synthetic agentic candidate | Public candidate; not yet project-gated | Agentic SFT; high-quality anneal trajectories | Response-only masked loss | Tool success, task completion, invalid-action rate | [Dataset card](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) |
| Long-context | zai-org/LongCite-45k | 44,600 | 5.73 GB; up to 128K words | Apache-2.0 | Public | Public long-context SFT candidate | Public candidate; not yet project-gated | Late-pretraining support; long-context SFT; anneal subset | Response-and-citation loss | RULER, LongBench | [Dataset card](https://huggingface.co/datasets/zai-org/LongCite-45k) |
| Non-Indic multilingual | HuggingFaceFW/fineweb-2 | 4,484,929,995 documents | 20.2 TB; 1,000+ languages | ODC-By-1.0; Common Crawl terms also apply | Public | Public multilingual-web candidate | Public candidate; not yet project-gated | Pretraining | Next-token loss | Cross-lingual validation, multilingual composite | [Dataset card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) |

The eight previously starved lanes now map to named public datasets. These mappings complete the inventory-selection requirement, but they do **not** claim that the datasets have passed this project's licence review, deduplication, contamination, quality, privacy or sampling gates. Their `data_gate_status` therefore remains `public_candidate_not_yet_project_gated` until those checks are executed.

See [`configs/benchmark_mapping.yaml`](configs/benchmark_mapping.yaml).

## 7. Training lifecycle: do not flatten every capability into pretraining

### Pretraining

Reasoning exposure means problem statements, textbook explanations, proofs, concise worked solutions and short visible derivations. It does **not** mean filling base pretraining with every long reasoning trace.

Early Agentic exposure means tool documentation, API schemas, planning text and basic function calls. The scarcest full trajectories are protected.

### Annealing or reasoning SFT

Use supervised short, medium and long reasoning traces, self-checks and corrections. Use the highest-quality multi-step Agentic trajectories, including failures and recovery.

### Reasoning RL

Use verifiable problems and environment or final-answer rewards. This is a later stage and does not require a token-level target for every reasoning step.

## 8. Agentic loss mask

| Segment | Training loss |
|---|---:|
| User request | 0 |
| System/tool documentation context | 0 |
| Tool observation | 0 |
| Assistant plan | 1 |
| Assistant tool call and arguments | 1 |
| Assistant final answer | 1 |

Tool observations are ground-truth context. Training the model to reproduce them would teach it to invent tool outputs instead of calling tools.

## 9. OPUS and protected always-on floors

Every rolling **100,000 model-token window** is filled in this order:

1. Insert protected Verified-Indic, Reasoning and Agentic tokens.
2. Lock those tokens outside OPUS or any global selector.
3. Run the selector only on the remaining capacity.
4. Fill the remaining window with selected candidates.

| OPUS-bypass lane | Minimum |
|---|---:|
| Verified Indic | 6% |
| Reasoning | 4% |
| Agentic | 2% |

General language has a separate 15% stability guardrail. Synthetic data cannot satisfy the Verified-Indic floor. A floor activates only after its lane passes the data gate.

## 10. Curriculum and stable transitions

| Stage | Budget interval | Main role |
|---|---:|---|
| Foundation | 0–35% | Broad language, verified data, moderate context, reasoning support |
| Capability expansion | 35–67% | More Code, Math, Indic, medium reasoning and initial longer contexts |
| Reasoning intensification | 67–92% | Harder reasoning support, Agentic work and true long-context dependencies |
| Anneal/cooldown | 92–100% | Exclusive high-quality reserve |

The stage mixtures exactly reproduce the declared 92% main allocation:

| Lane | Foundation | Expansion | Intensification |
|---|---:|---:|---:|
| General | 40.00% | 28.00% | 18.16% |
| Indic | 25.00% | 27.00% | 24.44% |
| Reasoning | 8.00% | 12.00% | 21.44% |
| Code | 8.00% | 10.00% | 8.00% |
| Mathematics/science | 5.00% | 7.00% | 6.04% |
| Agentic | 3.00% | 6.00% | 10.12% |
| Long-context | 4.00% | 6.00% | 8.72% |
| Non-Indic multilingual | 7.00% | 4.00% | 3.08% |

Foundation's 4% Long-context share means moderate-context preparation, not true very-long-context training.

Mixture boundaries are blended rather than switched abruptly:

| Boundary | Blend width |
|---|---:|
| Foundation → Expansion | 1.0% of total tokens |
| Expansion → Intensification | 1.0% |
| Intensification → Anneal | 0.75% |

During transitions, weights are linearly interpolated and loss, validation loss, gradient norm and throughput are monitored. Pause and roll back if gradient norm exceeds 4× its trailing baseline. Do not change architecture or parameter-freezing policy at the same boundary.

## 11. Difficulty and controllable reasoning effort

### Difficulty

| Band | Operational definition | Example |
|---|---|---|
| D1 | Retrieval, classification or one operation | Identify a sentence's language |
| D2 | Two or three dependent operations | Compare two passages and justify one difference |
| D3 | Multi-step constrained reasoning | Solve a quantitative problem with dependencies |
| D4 | Branching, tool-assisted or long-horizon work | Use tools, recover from failure and revise a plan |

### Course reasoning-effort dial

| Effort | Proxy trace-length hypothesis | Example |
|---|---:|---|
| Low | 0–128 tokens | Direct answer or one short derivation |
| Medium | 129–512 | Three-to-five-step constrained solution |
| High | 513–2,048 | Proof or debugging plan with verification |
| Ultra | >2,048 or branching/tool-assisted | Multi-source research with failures and recovery |

These boundaries are testable hypotheses.

## 12. Planned proxy experiments

The current 1,000 SEK proxy tests one narrow question using only data-gated General, Hindi and Hinglish lanes. It does not claim to validate the complete V5 mixture.

### Approximately 1B-scale screening

**Candidate:** `Qwen/Qwen2.5-1.5B`, continued from the same base checkpoint.

| Run | General | Hindi | Hinglish | Purpose |
|---|---:|---:|---:|---|
| M0 | 72% | 14% | 14% | Supply-aligned baseline |
| M1 | 60% | 20% | 20% | Protected Indic treatment |
| M2 | Same cumulative 60/20/20 | Curriculum schedule | Optional timing ablation |

M0 and M1 are mandatory. M2 runs only after both and their evaluations finish.

Acceptance requires:

- Hindi validation loss improves by at least 2%;
- combined Hinglish loss improves by at least 2%;
- General loss worsens by no more than 1%;
- no lane worsens by more than 2%;
- weighted overall loss does not worsen.

One seed is directional evidence only.

### 3B confirmation

**Candidate:** `Qwen/Qwen2.5-3B`.

Compare the baseline with the best 1.5B treatment using at least two seeds per condition, identical token budgets, tokenizer, optimizer, schedule and evaluation files. Refute the treatment if the gain disappears, reverses or violates a regression guardrail.

See [`configs/proxy_experiments.yaml`](configs/proxy_experiments.yaml).

## 13. Starved-lane cleaning priority

1. Reasoning inventory supply
2. Agentic trajectories
3. Long-context documents and dependencies
4. Code
5. Mathematics/science
6. Indic translated
7. Indic unverified
8. Non-Indic multilingual
9. Additional Verified Indic and authentic Romanized Hinglish

This order should be recalculated after the mapped public candidates pass project data gates and local token counts are measured.

## 14. Reproducibility, privacy and submission status

Public:

- written specifications and configs;
- text-free manifests and checksums;
- aggregated metrics and cost summaries;
- verification reports.

Private:

- raw/rejected data;
- benchmark text;
- human-review samples;
- gated dataset contents;
- credentials and paid checkpoints unless intentionally released.

| Assignment requirement | Status |
|---|---|
| Capability shares sum to 100% | Complete |
| Four-tier Indic split | Complete |
| Explicit Agentic, Reasoning and Long-context lanes | Complete |
| Exact course-inventory mapping for starved lanes | Complete — public candidates mapped; project data gates pending |
| Published inventory schema with access, provenance, gate and citations | Complete |
| Supply and repetition accounting | Complete for project-backed lanes |
| OPUS-bypass protected floors | Complete |
| Separate anneal reserve and preset | Complete |
| Curriculum and transition safeguards | Complete |
| Difficulty and effort bands with examples | Complete |
| 1B-scale screening plan | Complete; not executed |
| 3B-scale confirmation plan | Complete; not executed |
| Data gate | General/Hindi verified; Hinglish review pending |
| Public GitHub README | Published |
| Incognito public-access test | **Pending user confirmation** |

## 15. Session 5 alignment summary

The Session 5 alignment decisions are incorporated directly into this README and the linked configuration files:

1. The 92% main-pretraining preset is separated from the exclusive 8% anneal reserve.
2. Proxy experiments are described as planned, not executed.
3. Reasoning-support pretraining is separated from later reasoning SFT and RL.
4. Agentic training uses response-only loss masking and excludes tool observations from loss.
5. Verified Indic, Reasoning and Agentic floors bypass OPUS.
6. Mixture transitions use gradual blend bands with gradient-norm safeguards.
7. Reasoning effort is mapped to low, medium, high and ultra bands.
8. Stage mixtures are corrected so their weighted totals reproduce the headline 92% allocation exactly.
9. The inventory uses the canonical published-data, access, provenance, gate, stage, loss, benchmark and citation schema, with named public candidates for every previously starved lane.
10. GitHub publication status is recorded separately from the pending incognito-access test.

## 16. Decision statement

No percentage becomes trusted because it appears in this document. The mixture survives only if cheap proxies improve the targeted capability within predeclared regression limits and the result persists at the larger confirmation scale.
