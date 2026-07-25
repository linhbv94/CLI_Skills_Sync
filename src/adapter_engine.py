import hashlib
from pathlib import Path
from typing import List, Dict, Tuple

CLAUDE_HEADER_METADATA = """# Claude Code Project & Global Instructions

> **Source:** Synchronized automatically by Skills Auto Sync Tool from shared_rules/agents.md
> **Note:** Follow these global rules and guidelines strictly.

"""

class AdapterEngine:
    """Chịu trách nhiệm chuyển đổi quy tắc chung shared_rules/agents.md <-> AGENTS.md / CLAUDE.md 2 chiều."""

    @staticmethod
    def get_file_hash(filepath: Path) -> str:
        if not filepath.exists() or not filepath.is_file():
            return ""
        hasher = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    def get_agent_rules_files(self, agent_name: str, agent_dir_str: str) -> List[Path]:
        """Lấy danh sách các file rules tiềm năng của agent."""
        if not agent_dir_str:
            return []
        agent_dir = Path(agent_dir_str)
        files = []

        if agent_name in ["antigravity", "codex"]:
            # Check cả ở agent_dir và parent nếu agent_dir là subfolder skills
            files.append(agent_dir / "AGENTS.md")
            if agent_dir.name == "skills":
                files.append(agent_dir.parent / "AGENTS.md")
        elif agent_name == "claude":
            files.append(agent_dir / "CLAUDE.md")

        return [f for f in files if f.exists()]

    def sync_rules_upstream(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        selected_agents: List[str],
        dry_run: bool = False,
    ) -> Tuple[bool, str]:
        """
        [Upstream Rules Sync]: Phát hiện nếu AGENTS.md hoặc CLAUDE.md ở bất kỳ Agent nào mới hơn
        bản trong Central Library (shared_rules/agents.md hoặc AGENTS.md), tự động gom về Library.
        """
        shared_rules_dir = library_path / "shared_rules"
        lib_rules_file = shared_rules_dir / "agents.md"
        lib_root_file = library_path / "AGENTS.md"

        lib_mtime = max(
            lib_rules_file.stat().st_mtime if lib_rules_file.exists() else 0,
            lib_root_file.stat().st_mtime if lib_root_file.exists() else 0
        )
        lib_hash = self.get_file_hash(lib_rules_file) or self.get_file_hash(lib_root_file)

        newer_agent_rules = None
        source_info = ""

        for agent_name in selected_agents:
            agent_dir_str = agent_paths.get(agent_name, "")
            rules_files = self.get_agent_rules_files(agent_name, agent_dir_str)

            for rf in rules_files:
                rf_hash = self.get_file_hash(rf)
                if rf_hash and rf_hash != lib_hash:
                    rf_mtime = rf.stat().st_mtime
                    if rf_mtime > lib_mtime:
                        newer_agent_rules = rf
                        source_info = f"{agent_name} ({rf.name})"
                        lib_mtime = rf_mtime

        if newer_agent_rules and newer_agent_rules.exists():
            if dry_run:
                return True, f"Sẽ gom rules sửa đổi từ {source_info} về Central Library."
            try:
                shared_rules_dir.mkdir(parents=True, exist_ok=True)
                with open(newer_agent_rules, "r", encoding="utf-8") as f:
                    content = f.read()

                # Nếu là CLAUDE.md, bỏ phần header metadata tự sinh nếu có
                if newer_agent_rules.name == "CLAUDE.md" and CLAUDE_HEADER_METADATA.strip() in content:
                    content = content.replace(CLAUDE_HEADER_METADATA, "").strip()

                with open(lib_rules_file, "w", encoding="utf-8") as f:
                    f.write(content)
                with open(lib_root_file, "w", encoding="utf-8") as f:
                    f.write(content)

                return True, f"Đã gom AGENTS.md/CLAUDE.md sửa đổi từ {source_info} về Central Library."
            except Exception as e:
                print(f"[AdapterEngine] Lỗi gom upstream rules: {e}")

        return False, ""

    def deploy_adapters(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        selected_agents: List[str]
    ) -> List[str]:
        """Đọc quy tắc chung và render/deploy file instruction cho tất cả Agent active."""
        # 1. Gom Upstream trước nếu có thay đổi từ Agent
        self.sync_rules_upstream(library_path, agent_paths, selected_agents)

        # 2. Tìm nguồn rules file chuẩn trong Library
        shared_rules_dir = library_path / "shared_rules"
        source_agents_md = shared_rules_dir / "agents.md"

        if not source_agents_md.exists():
            root_agents_md = library_path / "AGENTS.md"
            if root_agents_md.exists():
                source_agents_md = root_agents_md
            else:
                return []

        try:
            with open(source_agents_md, "r", encoding="utf-8") as f:
                rules_content = f.read()
        except Exception as e:
            print(f"[AdapterEngine] Không thể đọc {source_agents_md}: {e}")
            return []

        deployed_list = []

        for agent_name in selected_agents:
            agent_dir_str = agent_paths.get(agent_name, "")
            if not agent_dir_str:
                continue

            agent_dir = Path(agent_dir_str)
            agent_dir.mkdir(parents=True, exist_ok=True)

            if agent_name in ["antigravity", "codex"]:
                targets = [agent_dir / "AGENTS.md"]
                if agent_dir.name == "skills":
                    targets.append(agent_dir.parent / "AGENTS.md")

                for t in targets:
                    try:
                        t.parent.mkdir(parents=True, exist_ok=True)
                        with open(t, "w", encoding="utf-8") as f:
                            f.write(rules_content)
                        deployed_list.append(f"{agent_name} -> {t.name}")
                    except Exception as e:
                        print(f"[AdapterEngine] Lỗi deploy AGENTS.md: {e}")

            elif agent_name == "claude":
                target_claude_file = agent_dir / "CLAUDE.md"
                try:
                    claude_content = CLAUDE_HEADER_METADATA + rules_content
                    with open(target_claude_file, "w", encoding="utf-8") as f:
                        f.write(claude_content)
                    deployed_list.append(f"claude -> CLAUDE.md")
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy CLAUDE.md: {e}")

        return deployed_list
