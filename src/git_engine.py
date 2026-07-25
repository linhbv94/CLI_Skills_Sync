import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class GitStatusResult:
    status: str  # "UP_TO_DATE", "BEHIND", "AHEAD", "DIVERGED", "DIRTY", "OFFLINE", "NO_GIT"
    ahead_count: int = 0
    behind_count: int = 0
    dirty_files: List[str] = None
    error_message: str = ""

class GitEngine:
    """Gọi các lệnh Shell Git để quản lý tự động pull, push, fetch và kiểm tra xung đột."""

    @staticmethod
    def is_git_available() -> bool:
        return shutil.which("git") is not None

    def run_cmd(self, args: List[str], cwd: Path, timeout: int = 15) -> Tuple[int, str, str]:
        """Chạy lệnh git subprocess an toàn."""
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def fetch_remote(self, repo_path: Path) -> bool:
        """Thực hiện git fetch origin."""
        if not (repo_path / ".git").exists():
            return False
        code, out, err = self.run_cmd(["fetch", "origin"], cwd=repo_path, timeout=10)
        return code == 0

    def get_git_status(self, repo_path: Path) -> GitStatusResult:
        """Đánh giá chi tiết trạng thái Git của Local Library vs Remote Repo."""
        if not self.is_git_available():
            return GitStatusResult(status="NO_GIT", error_message="Git CLI chưa được cài đặt.")

        if not (repo_path / ".git").exists():
            return GitStatusResult(status="NO_GIT", error_message="Thư mục thư viện gốc chưa phải là Git repo.")

        # Thử fetch remote
        is_online = self.fetch_remote(repo_path)

        # Kiểm tra Working Tree có bị sửa đổi chưa commit hay không
        code, status_out, _ = self.run_cmd(["status", "--porcelain"], cwd=repo_path)
        dirty_files = [line for line in status_out.splitlines() if line.strip()]

        if not is_online:
            return GitStatusResult(
                status="OFFLINE",
                dirty_files=dirty_files,
                error_message="Không thể kết nối Internet/Git Remote (Offline Mode)."
            )

        # So sánh HEAD với origin/main (hoặc origin/HEAD)
        code, rev_out, _ = self.run_cmd(["rev-list", "--left-right", "--count", "HEAD...origin/main"], cwd=repo_path)
        
        ahead = 0
        behind = 0
        if code == 0 and rev_out:
            parts = rev_out.split()
            if len(parts) >= 2:
                ahead = int(parts[0])
                behind = int(parts[1])

        if ahead > 0 and behind > 0:
            status_str = "DIVERGED"
        elif behind > 0:
            status_str = "BEHIND"
        elif ahead > 0 or len(dirty_files) > 0:
            status_str = "AHEAD"
        else:
            status_str = "UP_TO_DATE"

        return GitStatusResult(
            status=status_str,
            ahead_count=ahead,
            behind_count=behind,
            dirty_files=dirty_files
        )

    def execute_smart_sync(self, repo_path: Path, mode: str) -> Tuple[bool, str]:
        """
        Thực thi hành động Git theo mode:
        - AUTO_PULL: git pull --ff-only origin main
        - AUTO_PUSH: git add . && git commit && git push origin main
        - FORCE_PULL: git reset --hard origin/main
        - FORCE_PUSH: git push --force-with-lease origin main
        """
        if not (repo_path / ".git").exists():
            return False, "Không phải thư mục Git repo."

        if mode == "AUTO_PULL":
            code, out, err = self.run_cmd(["pull", "--ff-only", "origin", "main"], cwd=repo_path)
            if code == 0:
                return True, "Đã pull dữ liệu mới từ Git thành công."
            return False, f"Không thể auto pull fast-forward: {err}"

        elif mode == "AUTO_PUSH":
            self.run_cmd(["add", "."], cwd=repo_path)
            self.run_cmd(["commit", "-m", "auto sync: skills library update"], cwd=repo_path)
            code, out, err = self.run_cmd(["push", "origin", "main"], cwd=repo_path)
            if code == 0:
                return True, "Đã push dữ liệu mới lên Git Remote thành công."
            return False, f"Không thể push lên Remote: {err}"

        elif mode == "FORCE_PULL":
            code, out, err = self.run_cmd(["reset", "--hard", "origin/main"], cwd=repo_path)
            if code == 0:
                return True, "Đã khôi phục dữ liệu theo bản Remote thành công."
            return False, f"Lỗi Force Pull: {err}"

        elif mode == "FORCE_PUSH":
            code, out, err = self.run_cmd(["push", "--force-with-lease", "origin", "main"], cwd=repo_path)
            if code == 0:
                return True, "Đã ghi đè bản Local lên Remote thành công."
            return False, f"Lỗi Force Push: {err}"

        return False, f"Mode không hợp lệ: {mode}"
