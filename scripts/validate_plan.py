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
proxy = load_yaml("proxy_experiments.yaml")

errors = []

main_total = sum(mixture["main_curriculum_percent"].values())
if not math.isclose(main_total, 92.0, abs_tol=1e-9):
    errors.append(f"Main mixture sums to {main_total}, expected 92.")

reserve_total = float(mixture["anneal_reserve_percent"])
if not math.isclose(reserve_total, 8.0, abs_tol=1e-9):
    errors.append(f"Reserve is {reserve_total}, expected 8.")

effective_total = sum(mixture["final_effective_exposure_percent"].values())
if not math.isclose(effective_total, 100.0, abs_tol=1e-9):
    errors.append(f"Final effective exposure sums to {effective_total}, expected 100.")

indic_total = sum(mixture["indic_final_split_percent_of_total_budget"].values())
if not math.isclose(indic_total, mixture["final_effective_exposure_percent"]["indic"], abs_tol=1e-9):
    errors.append(
        f"Indic split sums to {indic_total}, expected "
        f'{mixture["final_effective_exposure_percent"]["indic"]}.'
    )

for stage in curriculum["stages"]:
    if stage.get("exclusive_reserve"):
        reserve_stage_total = sum(stage["reserve_percent_of_total_budget"].values())
        if not math.isclose(reserve_stage_total, 8.0, abs_tol=1e-9):
            errors.append(
                f'Anneal stage reserve sums to {reserve_stage_total}, expected 8.'
            )
    else:
        stage_total = sum(stage["mixture_percent"].values())
        if not math.isclose(stage_total, 100.0, abs_tol=1e-9):
            errors.append(
                f'Stage {stage["name"]} mixture sums to {stage_total}, expected 100.'
            )

for run_name in ["M0", "M1"]:
    run_total = sum(proxy["runs"][run_name].values())
    if not math.isclose(run_total, 100.0, abs_tol=1e-9):
        errors.append(f"Proxy {run_name} sums to {run_total}, expected 100.")

for stage in proxy["runs"]["M2"]["stages"]:
    stage_total = stage["general"] + stage["hindi"] + stage["hinglish"]
    if not math.isclose(stage_total, 100.0, abs_tol=1e-9):
        errors.append(f"M2 stage sums to {stage_total}, expected 100.")

if errors:
    print("PLAN VALIDATION: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("PLAN VALIDATION: PASS")
print(f"Main curriculum: {main_total:.1f}%")
print(f"Anneal reserve: {reserve_total:.1f}%")
print(f"Final exposure: {effective_total:.1f}%")
print(f"Final Indic allocation: {indic_total:.1f}%")
print(f"Supply rows: {len(supply['supply_rows'])}")
