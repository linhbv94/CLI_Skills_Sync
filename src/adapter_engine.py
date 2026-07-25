import os
from pathlib import Path
from typing import List, Dict

CLAUDE_HEADER_METADATA = """# Claude Code Project & Global Instructions

> **Source:** Synchronized automatically by Skills Auto Sync Tool from shared_rules/agents.md
> **Note:** Follow these global rules and guidelines strictly.

"""

class AdapterEngine:
    """Chịu trách nhiệm chuyển đổi quy tắc chung shared_rules/agents.md sang AGENTS.md và CLAUDE.md."""

    def deploy_adapters(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        selected_agents: List[str]
    ) -> List[str]:
        """Đọc quy tắc chung và render/deploy file instruction cho từng Agent."""
        shared_rules_dir = library_path / "shared_rules"
        source_agents_md = shared_rules_dir / "agents.md"

        if not source_agents_md.exists():
            # Fallback nếu nằm trực tiếp ở root library
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
                # Codex và Antigravity sử dụng file tên AGENTS.md
                # Nếu agent_dir kết thúc bằng /skills thì đặt AGENTS.md ở parent hoặc trực tiếp
                target_agents_file = agent_dir / "AGENTS.md"
                if agent_dir.name == "skills":
                    target_agents_file = agent_dir.parent / "AGENTS.md"

                try:
                    with open(target_agents_file, "w", encoding="utf-8") as f:
                        f.write(rules_content)
                    deployed_list.append(f"{agent_name} -> {target_agents_file.name}")
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy AGENTS.md cho {agent_name}: {e}")

            elif agent_name == "claude":
                # Claude Code sử dụng CLAUDE.md
                target_claude_file = agent_dir / "CLAUDE.md"
                try:
                    claude_content = CLAUDE_HEADER_METADATA + rules_content
                    with open(target_claude_file, "w", encoding="utf-8") as f:
                        f.write(claude_content)
                    deployed_list.append(f"claude -> {target_claude_file.name}")
                except Exception as e:
                    print(f"[AdapterEngine] Lỗi deploy CLAUDE.md: {e}")

        return deployed_list
