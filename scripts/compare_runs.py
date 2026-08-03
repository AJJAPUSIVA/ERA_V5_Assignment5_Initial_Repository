#!/usr/bin/env python3
"""Recompute a controlled M0-versus-treatment validation comparison.

This module intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

LANES: tuple[str, ...] = (
    "general",
    "hindi",
    "hinglish_native",
    "hinglish_romanized",
)

CHECK_HINDI = "Hindi loss improves by at least 2%"
CHECK_HINGLISH = "Combined Hinglish improves by at least 2%"
CHECK_GENERAL = "General regression is no greater than 1%"
CHECK_ANY_LANE = "No individual lane regresses by more than 2%"
CHECK_OVERALL = "Equal-weight overall loss does not worsen"


class ComparisonError(ValueError):
    """Raised when comparison inputs are malformed or unsafe to evaluate."""


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ComparisonError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ComparisonError(f"Invalid JSON in {path}: {exc}") from exc


def _find_lane_mapping(value: Any) -> Mapping[str, Any] | None:
    if isinstance(value, Mapping):
        if all(lane in value for lane in LANES):
            return value
        for nested in value.values():
            result = _find_lane_mapping(nested)
            if result is not None:
                return result
    elif isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for nested in value:
            result = _find_lane_mapping(nested)
            if result is not None:
                return result
    return None


def _extract_loss(value: Any, lane: str) -> float:
    if isinstance(value, bool):
        raise ComparisonError(f"{lane}: boolean is not a valid loss")

    if isinstance(value, (int, float)):
        loss = float(value)
    elif isinstance(value, Mapping):
        loss = None
        for key in ("loss", "eval_loss", "validation_loss"):
            candidate = value.get(key)
            if isinstance(candidate, bool):
                continue
            if isinstance(candidate, (int, float)):
                loss = float(candidate)
                break
        if loss is None:
            raise ComparisonError(
                f"{lane}: expected a numeric loss or one of "
                "'loss', 'eval_loss', 'validation_loss'"
            )
    else:
        raise ComparisonError(f"{lane}: unsupported metric value {type(value)!r}")

    if not math.isfinite(loss) or loss <= 0:
        raise ComparisonError(f"{lane}: loss must be finite and positive")
    return loss


def extract_losses(payload: Any) -> dict[str, float]:
    lane_mapping = _find_lane_mapping(payload)
    if lane_mapping is None:
        raise ComparisonError(
            "Could not locate all required validation lanes: "
            + ", ".join(LANES)
        )
    return {
        lane: _extract_loss(lane_mapping[lane], lane)
        for lane in LANES
    }


def relative_change(baseline: float, treatment: float) -> float:
    if baseline <= 0 or not math.isfinite(baseline):
        raise ComparisonError("Baseline loss must be finite and positive")
    if treatment <= 0 or not math.isfinite(treatment):
        raise ComparisonError("Treatment loss must be finite and positive")
    return (treatment - baseline) / baseline


def build_comparison(
    baseline_losses: Mapping[str, float],
    treatment_losses: Mapping[str, float],
    *,
    baseline_name: str = "M0",
    treatment_name: str = "M1",
    model_tokens: int = 7_995_392,
    optimizer_steps: int = 976,
) -> dict[str, Any]:
    for lane in LANES:
        if lane not in baseline_losses or lane not in treatment_losses:
            raise ComparisonError(f"Missing lane: {lane}")

    lane_changes = {
        lane: relative_change(
            float(baseline_losses[lane]),
            float(treatment_losses[lane]),
        )
        for lane in LANES
    }

    baseline_hinglish = (
        float(baseline_losses["hinglish_native"])
        + float(baseline_losses["hinglish_romanized"])
    ) / 2
    treatment_hinglish = (
        float(treatment_losses["hinglish_native"])
        + float(treatment_losses["hinglish_romanized"])
    ) / 2
    hinglish_change = relative_change(
        baseline_hinglish,
        treatment_hinglish,
    )

    baseline_overall = sum(float(baseline_losses[lane]) for lane in LANES) / 4
    treatment_overall = sum(float(treatment_losses[lane]) for lane in LANES) / 4
    overall_change = relative_change(baseline_overall, treatment_overall)

    checks = {
        CHECK_HINGLISH: hinglish_change <= -0.02,
        CHECK_OVERALL: overall_change <= 0,
        CHECK_GENERAL: lane_changes["general"] <= 0.01,
        CHECK_HINDI: lane_changes["hindi"] <= -0.02,
        CHECK_ANY_LANE: all(change <= 0.02 for change in lane_changes.values()),
    }
    all_pass = all(checks.values())

    decision = (
        f"{treatment_name} PASSES ALL PREDECLARED ACCEPTANCE GATES"
        if all_pass
        else f"{treatment_name} DOES NOT PASS ALL PREDECLARED ACCEPTANCE GATES"
    )

    return {
        "acceptance_checks": checks,
        "all_acceptance_gates_pass": all_pass,
        "baseline": baseline_name,
        "combined_hinglish": {
            f"{baseline_name.lower()}_loss": baseline_hinglish,
            f"{treatment_name.lower()}_loss": treatment_hinglish,
            "relative_change": hinglish_change,
            "relative_change_percent": hinglish_change * 100,
        },
        "decision": decision,
        "equal_weight_overall": {
            f"{baseline_name.lower()}_loss": baseline_overall,
            f"{treatment_name.lower()}_loss": treatment_overall,
            "relative_change": overall_change,
            "relative_change_percent": overall_change * 100,
        },
        "frozen_model_tokens": int(model_tokens),
        "interpretation": "One-seed directional T4 QLoRA proxy evidence only.",
        "optimizer_steps_per_condition": int(optimizer_steps),
        "schema_version": "v5-m0-m1-comparison-result-1",
        "status": "complete",
        "treatment": treatment_name,
        "validation": {
            lane: {
                f"{baseline_name.lower()}_loss": float(baseline_losses[lane]),
                f"{treatment_name.lower()}_loss": float(treatment_losses[lane]),
                f"{treatment_name.lower()}_perplexity":
                    math.exp(float(treatment_losses[lane])),
                "relative_change": lane_changes[lane],
                "relative_change_percent": lane_changes[lane] * 100,
            }
            for lane in LANES
        },
    }


def render_markdown(comparison: Mapping[str, Any]) -> str:
    baseline = str(comparison["baseline"])
    treatment = str(comparison["treatment"])
    validation = comparison["validation"]

    def label(lane: str) -> str:
        return lane.replace("_", " ").title()

    rows = []
    for lane in LANES:
        item = validation[lane]
        rows.append(
            f"| {label(lane)} "
            f"| {item[f'{baseline.lower()}_loss']:.6f} "
            f"| {item[f'{treatment.lower()}_loss']:.6f} "
            f"| {item['relative_change_percent']:+.2f}% |"
        )

    aggregate_rows = [
        (
            "Combined Hinglish",
            comparison["combined_hinglish"],
        ),
        (
            "Equal-weight overall",
            comparison["equal_weight_overall"],
        ),
    ]
    aggregate_lines = []
    for title, item in aggregate_rows:
        aggregate_lines.append(
            f"| {title} "
            f"| {item[f'{baseline.lower()}_loss']:.6f} "
            f"| {item[f'{treatment.lower()}_loss']:.6f} "
            f"| {item['relative_change_percent']:+.2f}% |"
        )

    check_lines = [
        f"| {name} | {'PASS' if passed else 'FAIL'} |"
        for name, passed in comparison["acceptance_checks"].items()
    ]

    passed = sum(bool(value) for value in comparison["acceptance_checks"].values())
    total = len(comparison["acceptance_checks"])

    return (
        f"# {baseline}-versus-{treatment} T4 QLoRA Comparison\n\n"
        "## Status\n\nComplete.\n\n"
        "## Validation comparison\n\n"
        f"| Validation lane | {baseline} loss | {treatment} loss "
        "| Relative change |\n"
        "|---|---:|---:|---:|\n"
        + "\n".join(rows)
        + "\n\nNegative relative change indicates improvement.\n\n"
        "## Aggregate comparison\n\n"
        f"| Metric | {baseline} | {treatment} | Relative change |\n"
        "|---|---:|---:|---:|\n"
        + "\n".join(aggregate_lines)
        + "\n\n## Predeclared acceptance checks\n\n"
        "| Check | Result |\n|---|---|\n"
        + "\n".join(check_lines)
        + "\n\n## Decision\n\n"
        f"**{comparison['decision']}**\n\n"
        f"{passed} of {total} frozen acceptance checks passed.\n\n"
        "This comparison is one-seed directional evidence from a "
        "resource-constrained T4 QLoRA experiment. It is not equivalent "
        "to full-parameter BF16 continued pretraining.\n"
    )


def write_outputs(
    comparison: Mapping[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{comparison['baseline']}_vs_{comparison['treatment']}"
    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"

    json_path.write_text(
        json.dumps(comparison, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_markdown(comparison),
        encoding="utf-8",
    )
    return json_path, markdown_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recompute a frozen M0-versus-treatment comparison."
    )
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--treatment", required=True, type=Path)
    parser.add_argument("--baseline-name", default="M0")
    parser.add_argument("--treatment-name", default="M1")
    parser.add_argument("--model-tokens", type=int, default=7_995_392)
    parser.add_argument("--optimizer-steps", type=int, default=976)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
        help="Return exit code 3 when any acceptance gate fails.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        baseline = extract_losses(load_json(args.baseline))
        treatment = extract_losses(load_json(args.treatment))
        comparison = build_comparison(
            baseline,
            treatment,
            baseline_name=args.baseline_name,
            treatment_name=args.treatment_name,
            model_tokens=args.model_tokens,
            optimizer_steps=args.optimizer_steps,
        )
        json_path, markdown_path = write_outputs(
            comparison,
            args.output_dir,
        )
    except ComparisonError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"Created: {json_path}")
    print(f"Created: {markdown_path}")
    print(f"Decision: {comparison['decision']}")

    if args.fail_on_gate_failure and not comparison["all_acceptance_gates_pass"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
