from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_branding import scan
from scripts.rebrand_repository import rebrand


class BrandingTests(unittest.TestCase):
    def test_clean_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(
                "# IndicMix Lab\n",
                encoding="utf-8",
            )
            self.assertEqual(scan(root), [])

    def test_legacy_brand_is_detected_and_rebranded(self) -> None:
        legacy = "ERA" + " V5"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            readme = root / "README.md"
            readme.write_text(
                f"# {legacy} research\n",
                encoding="utf-8",
            )
            self.assertEqual(len(scan(root)), 1)
            changed = rebrand(root, apply=True)
            self.assertEqual(changed, [readme])
            self.assertEqual(scan(root), [])
            self.assertIn(
                "IndicMix Lab",
                readme.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
