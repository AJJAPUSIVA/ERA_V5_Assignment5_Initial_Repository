#!/usr/bin/env python3
"""Replace exact legacy public-facing names without changing experiment IDs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

LEGACY_BRAND = "ERA" + " V5"
LEGACY_REPOSITORY = "ERA_" + "V5_Assignment5_Initial_Repository"
LEGACY_URL = "https://github.com/AJJAPUSIVA/" + LEGACY_REPOSITORY

REPLACEMENTS = (
    (LEGACY_URL, "https://github.com/AJJAPUSIVA/indicmix-lab"),
    (LEGACY_REPOSITORY, "indicmix-lab"),
    (LEGACY_BRAND + " Assignment 5", "IndicMix Lab"),
    (LEGACY_BRAND + " Assignment5", "IndicMix Lab"),
    (LEGACY_BRAND + " Session 5", "IndicMix Lab"),
    (LEGACY_BRAND, "IndicMix Lab"),
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


def rebrand(root: Path, *, apply: bool) -> list[Path]:
    changed: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if not is_text(path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = content
        for old, new in REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != content:
            changed.append(path)
            if apply:
                path.write_text(updated, encoding="utf-8")
    return changed


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebrand exact public-facing project names."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes. Without this flag, only list affected files.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.repo_root.resolve()
    changed = rebrand(root, apply=args.apply)
    mode = "Updated" if args.apply else "Would update"
    for path in changed:
        print(f"{mode}: {path.relative_to(root)}")
    print(f"{mode} {len(changed)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
