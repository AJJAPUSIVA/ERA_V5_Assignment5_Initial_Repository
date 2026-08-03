#!/usr/bin/env python3
"""Generate a deterministic, dependency-free HTML results dashboard."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

DEFAULT_REPOSITORY_URL = (
    "https://github.com/AJJAPUSIVA/"
    "ERA_V5_Assignment5_Initial_Repository"
)


def load_comparison(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("Comparison JSON must contain an object")
    return value


def _format_change(value: float) -> str:
    return f"{float(value):+.2f}%"


def build_dashboard(
    comparison: Mapping[str, Any],
    *,
    repository_url: str = DEFAULT_REPOSITORY_URL,
) -> str:
    baseline = html.escape(str(comparison["baseline"]))
    treatment = html.escape(str(comparison["treatment"]))
    decision = html.escape(str(comparison["decision"]))
    validation = comparison["validation"]

    metrics = [
        (
            "General",
            float(validation["general"]["relative_change_percent"]),
        ),
        (
            "Hindi",
            float(validation["hindi"]["relative_change_percent"]),
        ),
        (
            "Hinglish native",
            float(validation["hinglish_native"]["relative_change_percent"]),
        ),
        (
            "Hinglish romanized",
            float(
                validation["hinglish_romanized"]["relative_change_percent"]
            ),
        ),
        (
            "Combined Hinglish",
            float(
                comparison["combined_hinglish"]["relative_change_percent"]
            ),
        ),
        (
            "Equal-weight overall",
            float(
                comparison["equal_weight_overall"]["relative_change_percent"]
            ),
        ),
    ]
    max_abs = max(abs(value) for _, value in metrics) or 1.0

    metric_rows = []
    for name, value in metrics:
        width = max(2.0, abs(value) / max_abs * 100)
        category = "improvement" if value < 0 else "regression"
        label = "improvement" if value < 0 else "regression"
        metric_rows.append(
            "<div class=\"metric\">"
            f"<div class=\"metric-label\"><span>{html.escape(name)}</span>"
            f"<strong>{_format_change(value)}</strong></div>"
            "<div class=\"track\">"
            f"<div class=\"bar {category}\" style=\"width:{width:.2f}%\" "
            f"role=\"img\" aria-label=\"{html.escape(name)} "
            f"{abs(value):.2f} percent {label}\"></div>"
            "</div></div>"
        )

    gate_rows = []
    for name, passed in comparison["acceptance_checks"].items():
        status = "PASS" if passed else "FAIL"
        css = "pass" if passed else "fail"
        gate_rows.append(
            "<tr>"
            f"<td>{html.escape(str(name))}</td>"
            f"<td><span class=\"pill {css}\">{status}</span></td>"
            "</tr>"
        )

    passed_count = sum(
        bool(value)
        for value in comparison["acceptance_checks"].values()
    )
    gate_total = len(comparison["acceptance_checks"])
    decision_class = (
        "accepted"
        if comparison["all_acceptance_gates_pass"]
        else "not-accepted"
    )
    source_url = (
        repository_url.rstrip("/")
        + "/blob/master/evidence/proxy_runs/comparisons/M0_vs_M1.json"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="ERA V5 M0 versus M1 Hindi and Hinglish data-mixture results.">
<title>ERA V5 — M0 vs M1 Results</title>
<style>
:root {{
  color-scheme: light dark;
  --bg: #0b1020;
  --panel: #121a2d;
  --panel-2: #19233a;
  --text: #eef3ff;
  --muted: #aab6d3;
  --border: #2b3859;
  --good: #42d392;
  --warn: #ffb454;
  --bad: #ff6b7a;
  --accent: #7aa2ff;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  background:
    radial-gradient(circle at 10% 0%, #1b2a54 0, transparent 35rem),
    var(--bg);
  color: var(--text);
  line-height: 1.55;
}}
main {{ max-width: 1080px; margin: 0 auto; padding: 48px 20px 72px; }}
a {{ color: #a8c1ff; }}
.eyebrow {{
  color: var(--accent); font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; font-size: .78rem;
}}
h1 {{ font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; margin: .4rem 0 1rem; }}
.lead {{ max-width: 760px; color: var(--muted); font-size: 1.15rem; }}
.grid {{
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
  margin: 30px 0;
}}
.card, section {{
  border: 1px solid var(--border); border-radius: 18px;
  background: linear-gradient(180deg, rgba(255,255,255,.035), transparent), var(--panel);
  padding: 22px;
  box-shadow: 0 18px 50px rgba(0,0,0,.18);
}}
.card .value {{ font-size: 2rem; font-weight: 800; }}
.card .label {{ color: var(--muted); }}
section {{ margin-top: 18px; }}
.decision {{ border-left: 6px solid var(--bad); }}
.decision.accepted {{ border-left-color: var(--good); }}
.decision h2 {{ margin-top: 0; }}
.metric {{ margin: 18px 0; }}
.metric-label {{ display: flex; justify-content: space-between; gap: 12px; }}
.track {{
  height: 12px; border-radius: 99px; overflow: hidden;
  background: var(--panel-2); margin-top: 7px;
}}
.bar {{ height: 100%; border-radius: inherit; }}
.improvement {{ background: linear-gradient(90deg, #23a96e, var(--good)); }}
.regression {{ background: linear-gradient(90deg, #d68b2e, var(--warn)); }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 12px 10px; border-bottom: 1px solid var(--border); text-align: left; }}
th {{ color: var(--muted); font-size: .82rem; text-transform: uppercase; letter-spacing: .05em; }}
.pill {{
  display: inline-block; padding: 3px 10px; border-radius: 999px;
  font-size: .76rem; font-weight: 800;
}}
.pass {{ color: #07180f; background: var(--good); }}
.fail {{ color: #20070b; background: var(--bad); }}
.note {{ color: var(--muted); font-size: .92rem; }}
footer {{ color: var(--muted); margin-top: 34px; font-size: .9rem; }}
@media (max-width: 760px) {{
  .grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<main>
  <div class="eyebrow">ERA V5 · release v1.0.0</div>
  <h1>Hindi/Hinglish mixture screening</h1>
  <p class="lead">
    A controlled comparison of {baseline} and {treatment} using the same
    Qwen2.5-1.5B revision, frozen token budget, optimizer steps, seed and
    validation files.
  </p>

  <div class="grid">
    <div class="card">
      <div class="value">{passed_count}/{gate_total}</div>
      <div class="label">acceptance gates passed</div>
    </div>
    <div class="card">
      <div class="value">{_format_change(comparison['combined_hinglish']['relative_change_percent'])}</div>
      <div class="label">combined Hinglish loss</div>
    </div>
    <div class="card">
      <div class="value">{_format_change(comparison['equal_weight_overall']['relative_change_percent'])}</div>
      <div class="label">equal-weight overall loss</div>
    </div>
  </div>

  <section class="decision {decision_class}">
    <h2>Decision</h2>
    <p><strong>{decision}</strong></p>
    <p class="note">
      M1 improved both Hinglish lanes and overall loss, while General
      regression remained negligible. Hindi improved by 1.20%, below the
      preregistered 2% minimum, so the treatment was not accepted.
    </p>
  </section>

  <section>
    <h2>Relative loss change</h2>
    <p class="note">Negative values indicate improvement; positive values indicate regression.</p>
    {''.join(metric_rows)}
  </section>

  <section>
    <h2>Frozen acceptance checks</h2>
    <table>
      <thead><tr><th>Check</th><th>Result</th></tr></thead>
      <tbody>{''.join(gate_rows)}</tbody>
    </table>
  </section>

  <section>
    <h2>Interpretation boundary</h2>
    <p>
      This is one-seed directional evidence from a resource-constrained T4
      QLoRA experiment. It is not equivalent to full-parameter BF16 continued
      pretraining and does not demonstrate transfer to a 3B model.
    </p>
    <p><a href="{html.escape(source_url)}">Inspect the machine-readable source evidence</a></p>
  </section>

  <footer>
    Generated deterministically by <code>scripts/generate_dashboard.py</code>.
    No external JavaScript or charting library is used.
  </footer>
</main>
</body>
</html>
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the ERA V5 static results dashboard."
    )
    parser.add_argument("--comparison", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--repository-url",
        default=DEFAULT_REPOSITORY_URL,
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    comparison = load_comparison(args.comparison)
    output = build_dashboard(
        comparison,
        repository_url=args.repository_url,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Created: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
