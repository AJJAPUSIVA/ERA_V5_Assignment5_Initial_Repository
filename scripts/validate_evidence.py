#!/usr/bin/env python3
"""Validate the public-safe IndicMix Lab evidence and open-source release files."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

try:
    from scripts.compare_runs import (
        ComparisonError,
        build_comparison,
        extract_losses,
        load_json,
    )
except ModuleNotFoundError:
    from compare_runs import (  # type: ignore
        ComparisonError,
        build_comparison,
        extract_losses,
        load_json,
    )

REQUIRED_RELEASE_FILES = (
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "THIRD_PARTY_NOTICES.md",
    ".github/workflows/ci.yml",
    "scripts/compare_runs.py",
    "scripts/generate_dashboard.py",
    "scripts/validate_evidence.py",
    "scripts/check_branding.py",
    "scripts/rebrand_repository.py",
    "tests/test_compare_runs.py",
    "tests/test_dashboard.py",
    "tests/test_branding.py",
    "docs/EXPERIMENT_CARD.md",
    "docs/PORTFOLIO_CASE_STUDY.md",
    "docs/REPOSITORY_RENAME_GUIDE.md",
    "docs/index.html",
)

BASELINE_PATH = "evidence/proxy_runs/M0/m0_validation_metrics.json"
TREATMENT_PATH = "evidence/proxy_runs/M1/m1_validation_metrics.json"
COMPARISON_PATH = "evidence/proxy_runs/comparisons/M0_vs_M1.json"

FORBIDDEN_SUFFIXES = (
    ".jsonl",
    ".parquet",
    ".arrow",
    ".safetensors",
    ".pt",
    ".pth",
    ".bin",
    ".zip",
)


def close(left: float, right: float, *, tolerance: float = 1e-12) -> bool:
    return math.isclose(
        float(left),
        float(right),
        rel_tol=tolerance,
        abs_tol=tolerance,
    )


def check_required_files(root: Path, errors: list[str]) -> None:
    for relative in REQUIRED_RELEASE_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required release file: {relative}")

    for relative in (BASELINE_PATH, TREATMENT_PATH, COMPARISON_PATH):
        if not (root / relative).is_file():
            errors.append(f"Missing required evidence file: {relative}")


def check_forbidden_artifacts(root: Path, errors: list[str]) -> None:
    skipped_parts = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "build",
        "dist",
    }
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in skipped_parts for part in relative.parts):
            continue
        if path.name.startswith("checkpoint-"):
            errors.append(f"Checkpoint file must not be public: {relative}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"Forbidden public artifact: {relative}")


def check_comparison(root: Path, errors: list[str]) -> None:
    try:
        baseline = extract_losses(load_json(root / BASELINE_PATH))
        treatment = extract_losses(load_json(root / TREATMENT_PATH))
        committed: dict[str, Any] = load_json(root / COMPARISON_PATH)
        recomputed = build_comparison(baseline, treatment)
    except (ComparisonError, TypeError, ValueError) as exc:
        errors.append(f"Comparison could not be validated: {exc}")
        return

    exact_fields = (
        "status",
        "baseline",
        "treatment",
        "decision",
        "all_acceptance_gates_pass",
        "frozen_model_tokens",
        "optimizer_steps_per_condition",
    )
    for field in exact_fields:
        if committed.get(field) != recomputed.get(field):
            errors.append(
                f"Comparison mismatch for {field}: "
                f"committed={committed.get(field)!r}, "
                f"recomputed={recomputed.get(field)!r}"
            )

    if committed.get("acceptance_checks") != recomputed.get("acceptance_checks"):
        errors.append("Committed acceptance checks do not match recomputation")

    for lane, expected in recomputed["validation"].items():
        actual = committed.get("validation", {}).get(lane)
        if not isinstance(actual, dict):
            errors.append(f"Missing committed validation lane: {lane}")
            continue
        for key in (
            "m0_loss",
            "m1_loss",
            "relative_change",
            "relative_change_percent",
        ):
            if key not in actual or not close(actual[key], expected[key]):
                errors.append(f"Mismatch in validation.{lane}.{key}")

    for section in ("combined_hinglish", "equal_weight_overall"):
        actual = committed.get(section)
        expected = recomputed[section]
        if not isinstance(actual, dict):
            errors.append(f"Missing comparison section: {section}")
            continue
        for key in (
            "m0_loss",
            "m1_loss",
            "relative_change",
            "relative_change_percent",
        ):
            if key not in actual or not close(actual[key], expected[key]):
                errors.append(f"Mismatch in {section}.{key}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    check_required_files(root, errors)
    check_forbidden_artifacts(root, errors)
    if not errors:
        check_comparison(root, errors)
    return errors


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate IndicMix Lab public evidence and release structure."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.repo_root.resolve()
    errors = validate(root)

    if errors:
        print("Evidence validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    comparison = json.loads(
        (root / COMPARISON_PATH).read_text(encoding="utf-8")
    )
    passed = sum(
        bool(value)
        for value in comparison["acceptance_checks"].values()
    )
    total = len(comparison["acceptance_checks"])

    print("Evidence validation passed.")
    print(f"Acceptance checks: {passed}/{total}")
    print(f"Decision: {comparison['decision']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
