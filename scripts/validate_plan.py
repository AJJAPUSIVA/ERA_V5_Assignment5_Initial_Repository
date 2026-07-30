from pathlib import Path
import math
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(name):
    with (ROOT / "configs" / name).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


mixture = load_yaml("full_mixture.yaml")
curriculum = load_yaml("curriculum.yaml")
supply = load_yaml("supply_accounting.yaml")
inventory = load_yaml("benchmark_mapping.yaml")
proxy = load_yaml("proxy_experiments.yaml")

errors = []
tol = 1e-6

budget = mixture["budget_accounting"]
if not math.isclose(
    budget["main_curriculum_percent_of_total"]
    + budget["exclusive_anneal_reserve_percent_of_total"],
    budget["total_percent"],
    abs_tol=tol,
):
    errors.append("Main curriculum plus anneal reserve does not equal total budget.")

main = mixture["main_curriculum_contribution_percent_of_total"]
if not math.isclose(sum(main.values()), 92.0, abs_tol=tol):
    errors.append(f"Main contribution sums to {sum(main.values())}, expected 92.")

main_preset = mixture["main_pretraining_preset_percent_within_main_92"]
if not math.isclose(sum(main_preset.values()), 100.0, abs_tol=1e-5):
    errors.append(f"Normalized main preset sums to {sum(main_preset.values())}, expected 100.")

reserve = mixture["anneal_contribution_percent_of_total"]
if not math.isclose(sum(reserve.values()), 8.0, abs_tol=tol):
    errors.append(f"Reserve contribution sums to {sum(reserve.values())}, expected 8.")

anneal_preset = mixture["anneal_preset_percent_within_reserve_8"]
if not math.isclose(sum(anneal_preset.values()), 100.0, abs_tol=1e-5):
    errors.append(f"Normalized anneal preset sums to {sum(anneal_preset.values())}, expected 100.")

effective = mixture["final_effective_exposure_percent"]
if not math.isclose(sum(effective.values()), 100.0, abs_tol=tol):
    errors.append(f"Final effective exposure sums to {sum(effective.values())}, expected 100.")

indic_total = sum(mixture["indic_final_split_percent_of_total_budget"].values())
if not math.isclose(indic_total, effective["indic"], abs_tol=tol):
    errors.append(f"Indic split sums to {indic_total}, expected {effective['indic']}.")

main_stages = [stage for stage in curriculum["stages"] if not stage.get("exclusive_reserve")]
weighted = {lane: 0.0 for lane in main}

previous_end = 0.0
for stage in main_stages:
    start = float(stage["start_percent"])
    end = float(stage["end_percent"])
    if not math.isclose(start, previous_end, abs_tol=tol):
        errors.append(f"Stage {stage['name']} starts at {start}, previous stage ended at {previous_end}.")
    previous_end = end

    stage_mix = stage["mixture_percent_within_stage"]
    if not math.isclose(sum(stage_mix.values()), 100.0, abs_tol=tol):
        errors.append(f"Stage {stage['name']} mixture does not sum to 100.")

    duration = end - start
    for lane in weighted:
        weighted[lane] += duration * float(stage_mix[lane]) / 100.0

if not math.isclose(previous_end, 92.0, abs_tol=tol):
    errors.append(f"Main stages end at {previous_end}, expected 92.")

for lane, expected in main.items():
    if not math.isclose(weighted[lane], expected, abs_tol=1e-5):
        errors.append(
            f"Stage-weighted {lane} contribution is {weighted[lane]:.8f}, expected {expected:.8f}."
        )

anneal_stage = [stage for stage in curriculum["stages"] if stage.get("exclusive_reserve")]
if len(anneal_stage) != 1:
    errors.append("Expected exactly one exclusive anneal stage.")
else:
    anneal_stage = anneal_stage[0]
    if not math.isclose(float(anneal_stage["start_percent"]), 92.0, abs_tol=tol):
        errors.append("Anneal stage must begin at 92%.")
    if not math.isclose(float(anneal_stage["end_percent"]), 100.0, abs_tol=tol):
        errors.append("Anneal stage must end at 100%.")
    if not math.isclose(
        sum(anneal_stage["normalized_anneal_preset_percent"].values()),
        100.0,
        abs_tol=1e-5,
    ):
        errors.append("Anneal stage normalized preset does not sum to 100%.")

selector = curriculum["selector_policy"]
protected = selector["opus_bypass_protected_floors_percent"]
required_protected = {"indic_verified", "reasoning", "agentic"}
if not required_protected.issubset(protected):
    errors.append("OPUS-bypass floors must include Verified Indic, Reasoning and Agentic.")

if selector.get("synthetic_data_cannot_satisfy_verified_floor") is not True:
    errors.append("Synthetic data must not satisfy the Verified-Indic floor.")

for transition in curriculum.get("transition_blends", []):
    if float(transition["blend_width_percent_of_total_tokens"]) <= 0:
        errors.append("Every transition blend must have positive width.")
    if transition["schedule"] != "linear_interpolation":
        errors.append("Transition schedule must be explicitly defined as linear interpolation.")

effort = curriculum["reasoning_effort_bands"]
if set(effort) < {"low", "medium", "high", "ultra"}:
    errors.append("Reasoning effort bands must include low, medium, high and ultra.")

mask = curriculum["agentic_loss_mask"]
if mask["tool_observation"] != 0 or mask["assistant_tool_call"] != 1:
    errors.append("Agentic mask must exclude tool observations and train assistant tool calls.")

required_columns = set(inventory["required_inventory_columns"])
for row in inventory["inventory_rows"] + inventory["starved_lane_templates"]:
    missing = required_columns - set(row)
    if missing:
        errors.append(f"Inventory row {row.get('capability')} is missing columns: {sorted(missing)}")

if proxy.get("status") != "planned_not_executed":
    errors.append("Proxy status must remain planned_not_executed until result files exist.")

screening = proxy["one_b_scale_screening"]
for run_name in ["M0", "M1"]:
    run_total = sum(screening["runs"][run_name].values())
    if not math.isclose(run_total, 100.0, abs_tol=tol):
        errors.append(f"Proxy {run_name} sums to {run_total}, expected 100.")

m2 = screening["runs"]["M2_optional"]
for stage in m2["stages"]:
    total = stage["general"] + stage["hindi"] + stage["hinglish"]
    if not math.isclose(total, 100.0, abs_tol=tol):
        errors.append(f"M2 stage sums to {total}, expected 100.")

three_b = proxy["three_b_scale_confirmation"]
if three_b["minimum_seeds_per_condition"] < 2:
    errors.append("3B confirmation requires at least two seeds per condition.")
if not three_b["same_model_token_budget_between_conditions"]:
    errors.append("3B confirmation conditions must use equal model-token budgets.")

if errors:
    print("PLAN VALIDATION: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("PLAN VALIDATION: PASS")
print(f"Main contribution: {sum(main.values()):.1f}%")
print(f"Anneal reserve: {sum(reserve.values()):.1f}%")
print(f"Final exposure: {sum(effective.values()):.1f}%")
print(f"Final Indic allocation: {indic_total:.1f}%")
print("Stage-weighted headline mixture: exact")
print("Separate main and anneal presets: valid")
print("OPUS-bypass floors: Verified Indic, Reasoning, Agentic")
print("Reasoning lifecycle and Agentic mask: valid")
print(f"Inventory rows checked: {len(inventory['inventory_rows']) + len(inventory['starved_lane_templates'])}")
print(f"Supply rows: {len(supply['supply_rows'])}")
