import os
import shutil
import hashlib
import fnmatch
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class UpstreamSyncResult:
    files_synced_to_library: List[str]
    agents_updated: List[str]
    has_library_changes: bool

class SyncEngine:
    """Xử lý đồng bộ 3 Nguồn: Agent Folders <-> Central Skills Library <-> Git Remote."""

    @staticmethod
    def is_ignored(rel_path: str, ignore_patterns: List[str]) -> bool:
        """Kiểm tra đường dẫn tương đối có nằm trong danh sách ignore hay không (đặc biệt là .system)."""
        rel_str = rel_path.replace("\\", "/")
        parts = rel_str.split("/")
        
        # Bắt buộc loại trừ folder .system của Codex
        if ".system" in parts:
            return True

        for pattern in ignore_patterns:
            clean_pat = pattern.replace("\\", "/")
            if fnmatch.fnmatch(rel_str, clean_pat) or any(fnmatch.fnmatch(p, clean_pat.strip("*/")) for p in parts):
                return True
        return False

    @staticmethod
    def get_file_hash(filepath: Path) -> str:
        """Tính mã hash MD5 của file để so sánh sự thay đổi nội dung."""
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

    def scan_and_sync_upstream(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        selected_agents: List[str],
        ignore_patterns: List[str]
    ) -> UpstreamSyncResult:
        """
        [Upstream Sync]: Quét các Agent Folders active.
        Nếu thấy file ở Agent mới/khác so với Library (và không thuộc .system),
        copy file đó ngược về Central Library và phân bổ sang các Agent còn lại.
        """
        library_skills_dir = library_path / "skills"
        library_skills_dir.mkdir(parents=True, exist_ok=True)

        synced_files = []
        agents_affected = set()
        has_changes = False

        for agent_name in selected_agents:
            agent_dir_str = agent_paths.get(agent_name, "")
            if not agent_dir_str:
                continue

            agent_dir = Path(agent_dir_str)
            # Đối với Claude Code, nếu path là root ~/.claude thì subfolder skills là ~/.claude/skills
            agent_skills_dir = agent_dir / "skills" if (agent_dir / "skills").exists() or agent_name == "claude" else agent_dir
            if not agent_skills_dir.exists():
                continue

            for root, dirs, files in os.walk(agent_skills_dir):
                # Bỏ qua thư mục .system khi os.walk
                if ".system" in dirs:
                    dirs.remove(".system")

                for file_name in files:
                    agent_file = Path(root) / file_name
                    try:
                        rel_path = agent_file.relative_to(agent_skills_dir)
                    except ValueError:
                        continue

                    rel_str = str(rel_path)
                    if self.is_ignored(rel_str, ignore_patterns):
                        continue

                    library_file = library_skills_dir / rel_path

                    # So sánh nội dung & thời gian sửa đổi
                    agent_hash = self.get_file_hash(agent_file)
                    lib_hash = self.get_file_hash(library_file)

                    if agent_hash and agent_hash != lib_hash:
                        agent_mtime = agent_file.stat().st_mtime
                        lib_mtime = library_file.stat().st_mtime if library_file.exists() else 0

                        # Nếu file bên Agent mới hơn Library
                        if agent_mtime > lib_mtime:
                            library_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(agent_file, library_file)
                            synced_files.append(f"{agent_name}: {rel_str}")
                            agents_affected.add(agent_name)
                            has_changes = True

        return UpstreamSyncResult(
            files_synced_to_library=synced_files,
            agents_updated=list(agents_affected),
            has_library_changes=has_changes
        )

    def deploy_skills_to_agents(
        self,
        library_path: Path,
        agent_paths: Dict[str, str],
        selected_agents: List[str],
        ignore_patterns: List[str]
    ) -> List[str]:
        """
        [Downstream Sync]: Đồng bộ danh mục skills/ từ Central Library sang tất cả Agent active,
        tuyệt đối GIỮ NGUYÊN thư mục nội bộ .system trong Codex.
        """
        library_skills_dir = library_path / "skills"
        if not library_skills_dir.exists():
            return []

        deployed_agents = []

        for agent_name in selected_agents:
            agent_dir_str = agent_paths.get(agent_name, "")
            if not agent_dir_str:
                continue

            agent_dir = Path(agent_dir_str)
            target_skills_dir = agent_dir / "skills" if (agent_dir / "skills").exists() or agent_name == "claude" else agent_dir
            target_skills_dir.mkdir(parents=True, exist_ok=True)

            for root, dirs, files in os.walk(library_skills_dir):
                if ".system" in dirs:
                    dirs.remove(".system")

                for file_name in files:
                    src_file = Path(root) / file_name
                    try:
                        rel_path = src_file.relative_to(library_skills_dir)
                    except ValueError:
                        continue

                    rel_str = str(rel_path)
                    if self.is_ignored(rel_str, ignore_patterns):
                        continue

                    dest_file = target_skills_dir / rel_path
                    dest_file.parent.mkdir(parents=True, exist_ok=True)

                    src_hash = self.get_file_hash(src_file)
                    dest_hash = self.get_file_hash(dest_file)

                    if src_hash != dest_hash:
                        shutil.copy2(src_file, dest_file)

            deployed_agents.append(agent_name)

        return deployed_agents
