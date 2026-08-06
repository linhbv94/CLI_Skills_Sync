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
            if agent_dir.name == "skills":
                files.append(agent_dir.parent / "AGENTS.md")
            else:
                files.append(agent_dir / "AGENTS.md")
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
        bản trong Central Library (AGENTS.md), tự động gom về Library.
        """
        lib_root_file = library_path / "AGENTS.md"

        lib_mtime = lib_root_file.stat().st_mtime if lib_root_file.exists() else 0
        lib_hash = self.get_file_hash(lib_root_file)

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
                with open(newer_agent_rules, "r", encoding="utf-8") as f:
                    content = f.read()

                # Nếu là CLAUDE.md, bỏ phần header metadata tự sinh nếu có
                if newer_agent_rules.name == "CLAUDE.md" and CLAUDE_HEADER_METADATA.strip() in content:
                    content = content.replace(CLAUDE_HEADER_METADATA, "").strip()

                with open(lib_root_file, "w", encoding="utf-8") as f:
                    f.write(content)

                # Đồng bộ timestamp mtime để giữ tính nhất quán
                import os
                agent_mtime = newer_agent_rules.stat().st_mtime
                os.utime(lib_root_file, (agent_mtime, agent_mtime))

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
        source_agents_md = library_path / "AGENTS.md"

        if not source_agents_md.exists():
            return []

        try:
            lib_mtime = source_agents_md.stat().st_mtime
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
                if agent_dir.name == "skills":
                    target_file = agent_dir.parent / "AGENTS.md"
                else:
                    target_file = agent_dir / "AGENTS.md"

                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(rules_content)
                    import os
                    os.utime(target_file, (lib_mtime, lib_mtime))
                    deployed_list.append(f"{agent_name} -> {target_file.name}")
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy AGENTS.md: {e}")

            elif agent_name == "claude":
                target_claude_file = agent_dir / "CLAUDE.md"
                try:
                    claude_content = CLAUDE_HEADER_METADATA + rules_content
                    with open(target_claude_file, "w", encoding="utf-8") as f:
                        f.write(claude_content)
                    import os
                    os.utime(target_claude_file, (lib_mtime, lib_mtime))
                    deployed_list.append(f"claude -> CLAUDE.md")
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy CLAUDE.md: {e}")

        return deployed_list
