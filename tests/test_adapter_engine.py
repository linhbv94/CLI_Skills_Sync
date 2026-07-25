import os
import tempfile
import unittest
from pathlib import Path

from src.adapter_engine import AdapterEngine


class AdapterEngineTests(unittest.TestCase):
    def test_preview_does_not_create_or_update_library_rules(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            library = root / "library"
            agent = root / "agent"
            library.mkdir()
            agent.mkdir()

            agent_rules = agent / "AGENTS.md"
            agent_rules.write_text("new rules", encoding="utf-8")
            os.utime(agent_rules, (200, 200))

            changed, message = AdapterEngine().sync_rules_upstream(
                library,
                {"codex": str(agent)},
                ["codex"],
                dry_run=True,
            )

            self.assertTrue(changed)
            self.assertIn("Sẽ gom", message)
            self.assertFalse((library / "shared_rules").exists())
            self.assertFalse((library / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
