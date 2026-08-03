from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.compare_runs import (
    CHECK_ANY_LANE,
    CHECK_GENERAL,
    CHECK_HINDI,
    CHECK_HINGLISH,
    CHECK_OVERALL,
    ComparisonError,
    build_comparison,
    extract_losses,
)

BASELINE = {
    "general": {"loss": 2.4215264804661274},
    "hindi": {"loss": 1.3216221360489726},
    "hinglish_native": {"loss": 1.5052946617728786},
    "hinglish_romanized": {"loss": 3.6076190769672394},
}

TREATMENT = {
    "general": {"loss": 2.422442192211747},
    "hindi": {"loss": 1.305719105526805},
    "hinglish_native": {"loss": 1.4741369548596834},
    "hinglish_romanized": {"loss": 3.521340847015381},
}


class ComparisonTests(unittest.TestCase):
    def test_current_result_and_frozen_gates(self) -> None:
        comparison = build_comparison(
            extract_losses(BASELINE),
            extract_losses(TREATMENT),
        )

        self.assertAlmostEqual(
            comparison["combined_hinglish"]["relative_change_percent"],
            -2.2968495630045793,
            places=12,
        )
        self.assertAlmostEqual(
            comparison["equal_weight_overall"]["relative_change_percent"],
            -1.495283686242577,
            places=12,
        )
        self.assertFalse(comparison["all_acceptance_gates_pass"])
        self.assertFalse(comparison["acceptance_checks"][CHECK_HINDI])
        self.assertTrue(comparison["acceptance_checks"][CHECK_HINGLISH])
        self.assertTrue(comparison["acceptance_checks"][CHECK_GENERAL])
        self.assertTrue(comparison["acceptance_checks"][CHECK_ANY_LANE])
        self.assertTrue(comparison["acceptance_checks"][CHECK_OVERALL])
        self.assertEqual(
            comparison["decision"],
            "M1 DOES NOT PASS ALL PREDECLARED ACCEPTANCE GATES",
        )

    def test_nested_metric_payload_is_supported(self) -> None:
        nested = {"result": {"validation": BASELINE}}
        losses = extract_losses(nested)
        self.assertAlmostEqual(losses["hindi"], 1.3216221360489726)

    def test_missing_lane_is_rejected(self) -> None:
        malformed = dict(BASELINE)
        malformed.pop("hindi")
        with self.assertRaises(ComparisonError):
            extract_losses(malformed)

    def test_non_positive_loss_is_rejected(self) -> None:
        malformed = dict(BASELINE)
        malformed["general"] = {"loss": 0}
        with self.assertRaises(ComparisonError):
            extract_losses(malformed)

    def test_cli_writes_json_and_markdown(self) -> None:
        root = Path(__file__).resolve().parents[1]
        script = root / "scripts" / "compare_runs.py"

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            baseline_path = directory / "baseline.json"
            treatment_path = directory / "treatment.json"
            output_dir = directory / "out"

            baseline_path.write_text(
                json.dumps(BASELINE),
                encoding="utf-8",
            )
            treatment_path.write_text(
                json.dumps(TREATMENT),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--baseline",
                    str(baseline_path),
                    "--treatment",
                    str(treatment_path),
                    "--output-dir",
                    str(output_dir),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_dir / "M0_vs_M1.json").is_file())
            self.assertTrue((output_dir / "M0_vs_M1.md").is_file())

            payload = json.loads(
                (output_dir / "M0_vs_M1.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertFalse(payload["all_acceptance_gates_pass"])


if __name__ == "__main__":
    unittest.main()
