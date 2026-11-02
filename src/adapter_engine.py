from src import safe_sync_io
import os
from pathlib import Path
from typing import List, Dict, Tuple

CLAUDE_HEADER_METADATA = """# Claude Code Project & Global Instructions

> **Source:** Synchronized automatically by Skills Auto Sync Tool from shared_rules/agents.md
> **Note:** Follow these global rules and guidelines strictly.

"""

ADAPTER_LOCALIZED = {
    "en": {
        "dry_run_msg": "Will collect modified rules from {} to Central Library.",
        "sync_ok_msg": "Successfully collected AGENTS.md/CLAUDE.md from {} to Central Library."
    },
    "vi": {
        "dry_run_msg": "Sẽ gom rules sửa đổi từ {} về Central Library.",
        "sync_ok_msg": "Đã gom AGENTS.md/CLAUDE.md sửa đổi từ {} về Central Library."
    }
}

class AdapterEngine:
    """Chịu trách nhiệm chuyển đổi quy tắc chung shared_rules/agents.md <-> AGENTS.md / CLAUDE.md 2 chiều."""

    @staticmethod
    def get_file_hash(filepath: Path) -> str:
        return safe_sync_io.file_hash(filepath.parent, filepath.name)


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
        lang: str = "en"
    ) -> Tuple[bool, str]:
        """
        [Upstream Rules Sync]: Phát hiện nếu AGENTS.md hoặc CLAUDE.md ở bất kỳ Agent nào mới hơn
        bản trong Central Library (AGENTS.md), tự động gom về Library.
        """
        l = ADAPTER_LOCALIZED.get(lang, ADAPTER_LOCALIZED["en"])
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
                return True, l["dry_run_msg"].format(source_info)
            try:
                content = safe_sync_io.read_text(newer_agent_rules.parent, newer_agent_rules.name)

                # Nếu là CLAUDE.md, bỏ phần header metadata tự sinh nếu có
                if newer_agent_rules.name == "CLAUDE.md" and CLAUDE_HEADER_METADATA.strip() in content:
                    content = content.replace(CLAUDE_HEADER_METADATA, "").strip()

                agent_mtime = newer_agent_rules.stat().st_mtime
                safe_sync_io.write_text(lib_root_file.parent, lib_root_file.name, content, mtime=agent_mtime)

                return True, l["sync_ok_msg"].format(source_info)
            except ValueError:
                raise
            except Exception as e:
                print(f"[AdapterEngine] Lỗi gom upstream rules: {e}")

        return False, ""

    def deploy_adapters(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        selected_agents: List[str],
        lang: str = "en"
    ) -> List[str]:
        """Đọc quy tắc chung và render/deploy file instruction cho tất cả Agent active."""
        # 1. Gom Upstream trước nếu có thay đổi từ Agent
        self.sync_rules_upstream(library_path, agent_paths, selected_agents, lang=lang)

        # 2. Tìm nguồn rules file chuẩn trong Library
        source_agents_md = library_path / "AGENTS.md"

        if not source_agents_md.exists():
            return []

        try:
            lib_mtime = source_agents_md.stat().st_mtime
            rules_content = safe_sync_io.read_text(source_agents_md.parent, source_agents_md.name)
        except ValueError:
            raise
        except Exception as e:
            print(f"[AdapterEngine] Không thể đọc {source_agents_md}: {e}")
            return []

        deployed_list = []

        for agent_name in selected_agents:
            agent_dir_str = agent_paths.get(agent_name, "")
            if not agent_dir_str:
                continue

            agent_dir = Path(agent_dir_str)
            safe_sync_io.ensure_directory(agent_dir)

            if agent_name in ["antigravity", "codex"]:
                if agent_dir.name == "skills":
                    target_file = agent_dir.parent / "AGENTS.md"
                else:
                    target_file = agent_dir / "AGENTS.md"

                try:
                    safe_sync_io.ensure_directory(target_file.parent)
                    safe_sync_io.write_text(target_file.parent, target_file.name, rules_content, mtime=lib_mtime)
                    deployed_list.append(f"{agent_name} -> {target_file.name}")
                except ValueError:
                    raise
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy AGENTS.md: {e}")

            elif agent_name == "claude":
                target_claude_file = agent_dir / "CLAUDE.md"
                try:
                    claude_content = CLAUDE_HEADER_METADATA + rules_content
                    safe_sync_io.write_text(target_claude_file.parent, target_claude_file.name, claude_content, mtime=lib_mtime)
                    deployed_list.append(f"claude -> CLAUDE.md")
                except ValueError:
                    raise
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy CLAUDE.md: {e}")

        return deployed_list

    def is_downstream_rules_pending(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        agent_name: str
    ) -> bool:
        """Kiểm tra xem file rules (AGENTS.md / CLAUDE.md) của Agent có cần cập nhật từ Central Library không."""
        lib_root_file = library_path / "AGENTS.md"
        if not lib_root_file.exists():
            return False

        agent_dir_str = agent_paths.get(agent_name, "")
        if not agent_dir_str:
            return False

        agent_dir = Path(agent_dir_str)
        if agent_name in ["antigravity", "codex"]:
            target_file = agent_dir.parent / "AGENTS.md" if agent_dir.name == "skills" else agent_dir / "AGENTS.md"
        elif agent_name == "claude":
            target_file = agent_dir / "CLAUDE.md"
        else:
            return False

        if not target_file.exists():
            return True

        return self.get_file_hash(lib_root_file) != self.get_file_hash(target_file)

