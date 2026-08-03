# Changelog

All notable public changes are documented here.

## [1.0.0] — 2026-08-03

### Added

- Reproducible standard-library M0-versus-M1 comparison CLI
- Repository evidence validator
- Deterministic visual dashboard generator
- Unit tests for metrics, acceptance gates, CLI behavior and dashboard output
- GitHub Actions CI across Python 3.10, 3.11 and 3.12
- Comment-only `requirements.txt` documenting zero third-party dependencies
- Experiment card and portfolio case study
- Static results dashboard suitable for GitHub Pages
- MIT license, citation metadata and contribution guidance
- Release notes and third-party notices

### Evidence carried into the release

- Completed M0 and M1 T4 QLoRA runs
- Exact frozen token and optimizer-step controls
- Human-readable and machine-readable comparison
- Transparent finding that M1 passed four of five gates but did not qualify

### Not included

- Raw corpora
- Restricted or gated dataset examples
- Checkpoints, adapters or optimizer states
- Claims of multi-seed, 3B or full-parameter BF16 confirmation
