from __future__ import annotations

import unittest

from scripts.compare_runs import build_comparison
from scripts.generate_dashboard import build_dashboard


class DashboardTests(unittest.TestCase):
    def test_dashboard_contains_decision_and_no_external_scripts(self) -> None:
        baseline = {
            "general": 2.4215264804661274,
            "hindi": 1.3216221360489726,
            "hinglish_native": 1.5052946617728786,
            "hinglish_romanized": 3.6076190769672394,
        }
        treatment = {
            "general": 2.422442192211747,
            "hindi": 1.305719105526805,
            "hinglish_native": 1.4741369548596834,
            "hinglish_romanized": 3.521340847015381,
        }
        comparison = build_comparison(baseline, treatment)
        output = build_dashboard(comparison)

        self.assertIn(
            "M1 DOES NOT PASS ALL PREDECLARED ACCEPTANCE GATES",
            output,
        )
        self.assertIn("Combined Hinglish", output)
        self.assertIn("-2.30%", output)
        self.assertNotIn("<script src=", output)
        self.assertNotIn("cdn.", output)


if __name__ == "__main__":
    unittest.main()
