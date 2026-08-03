#!/usr/bin/env python3
"""Fail when tracked text contains legacy public-facing project branding."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

LEGACY_BRAND = "ERA" + " V5"
LEGACY_REPOSITORY = "ERA_" + "V5_Assignment5_Initial_Repository"

FORBIDDEN = (
    LEGACY_BRAND,
    LEGACY_REPOSITORY,
    LEGACY_BRAND + " Assignment 5",
    LEGACY_BRAND + " Assignment5",
)

TEXT_SUFFIXES = {
    "",
    ".md",
    ".txt",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".cff",
    ".html",
    ".css",
    ".toml",
    ".ipynb",
}

SKIP_PARTS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
}


def is_text(path: Path) -> bool:
    return path.is_file() and (
        path.suffix.lower() in TEXT_SUFFIXES
        or path.name in {"LICENSE", "VERSION"}
    )


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in root.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if not is_text(path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            for forbidden in FORBIDDEN:
                if forbidden in line:
                    findings.append(
                        f"{path.relative_to(root)}:{line_number}: "
                        f"contains legacy branding"
                    )
                    break
    return findings


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check tracked text for legacy project branding."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    findings = scan(args.repo_root.resolve())
    if findings:
        print("Legacy branding check failed:", file=sys.stderr)
        for finding in findings:
            print(f" - {finding}", file=sys.stderr)
        return 1
    print("Legacy branding check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
