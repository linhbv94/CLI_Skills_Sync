import os
import tempfile
import unittest
from pathlib import Path

from src.sync_engine import SyncEngine


class SyncEngineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.library = self.root / "library"
        self.agent_a = self.root / "agent_a"
        self.agent_b = self.root / "agent_b"
        self.engine = SyncEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write(self, path: Path, content: str, mtime: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        os.utime(path, (mtime, mtime))

    def test_preview_reports_changes_without_writing(self):
        agent_file = self.agent_a / "demo_skill" / "SKILL.md"
        self._write(agent_file, "agent version", 200)

        result = self.engine.scan_and_sync_upstream(
            self.library,
            {"antigravity": str(self.agent_a)},
            ["antigravity"],
            [],
            dry_run=True,
        )

        self.assertTrue(result.has_library_changes)
        self.assertEqual(
            result.files_synced_to_library,
            ["antigravity: demo_skill/SKILL.md"],
        )
        self.assertFalse((self.library / "skills").exists())

    def test_newest_agent_version_wins_regardless_of_agent_order(self):
        relative_path = Path("demo_skill") / "SKILL.md"
        self._write(self.library / "skills" / relative_path, "library", 100)
        self._write(self.agent_a / relative_path, "older agent", 200)
        self._write(self.agent_b / relative_path, "newest agent", 300)

        result = self.engine.scan_and_sync_upstream(
            self.library,
            {
                "antigravity": str(self.agent_a),
                "codex": str(self.agent_b),
            },
            ["codex", "antigravity"],
            [],
        )

        self.assertEqual(
            (self.library / "skills" / relative_path).read_text(encoding="utf-8"),
            "newest agent",
        )
        self.assertEqual(
            result.files_synced_to_library,
            ["codex: demo_skill/SKILL.md"],
        )

    def test_system_directory_is_always_ignored(self):
        system_file = self.agent_a / ".system" / "internal" / "SKILL.md"
        self._write(system_file, "secret", 200)

        result = self.engine.scan_and_sync_upstream(
            self.library,
            {"codex": str(self.agent_a)},
            ["codex"],
            [],
        )

        self.assertFalse(result.has_library_changes)
        self.assertFalse((self.library / "skills" / ".system").exists())


if __name__ == "__main__":
    unittest.main()
