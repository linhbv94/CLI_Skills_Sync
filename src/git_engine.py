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
        import os
        try:
            env = os.environ.copy()
            env["GIT_TERMINAL_PROMPT"] = "0"  # Tắt prompt hỏi Username/Password
            env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"  # Tắt prompt hỏi SSH key passphrase
            res = subprocess.run(
                ["git"] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=timeout
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def ensure_git_repo_linked(self, repo_path: Path, remote_url: str) -> Tuple[bool, str]:
        """
        Đảm bảo thư mục library_path đã được khởi tạo Git và liên kết với remote_url:
        - Nếu thư mục chưa tồn tại & có remote_url: clone về.
        - Nếu thư mục chưa có .git: git init, git branch -M main, git remote add origin <url>.
        - Nếu đã có .git: cập nhật remote URL nếu bị lệch.
        """
        if not self.is_git_available():
            return False, "Git CLI chưa được cài đặt."

        if not remote_url:
            return False, "Chưa nhập Git Remote URL."

        # Case 1: Thư mục chưa tồn tại -> Clone từ Remote
        if not repo_path.exists():
            repo_path.parent.mkdir(parents=True, exist_ok=True)
            code, out, err = self.run_cmd(["clone", remote_url, str(repo_path)], cwd=repo_path.parent)
            if code == 0:
                return True, f"Đã clone thành công từ {remote_url}"
            return False, f"Lỗi clone repo: {err}"

        # Case 2: Thư mục tồn tại nhưng chưa có .git
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            self.run_cmd(["init"], cwd=repo_path)
            self.run_cmd(["branch", "-M", "main"], cwd=repo_path)
            code, out, err = self.run_cmd(["remote", "add", "origin", remote_url], cwd=repo_path)
            if code == 0:
                return True, f"Đã khởi tạo Git và liên kết remote origin -> {remote_url}"
            return False, f"Lỗi liên kết remote: {err}"

        # Case 3: Đã là Git repo -> Cập nhật remote origin
        code, current_url, _ = self.run_cmd(["remote", "get-url", "origin"], cwd=repo_path)
        if current_url != remote_url:
            if code == 0:
                self.run_cmd(["remote", "set-url", "origin", remote_url], cwd=repo_path)
            else:
                self.run_cmd(["remote", "add", "origin", remote_url], cwd=repo_path)
            return True, f"Đã cập nhật Git Remote origin -> {remote_url}"

        return True, "Git Repo đã được liên kết chính xác."

    def fetch_remote(self, repo_path: Path) -> Tuple[bool, str, str]:
        """Thực hiện git fetch origin. Trả về (success, error_type, error_msg)."""
        if not (repo_path / ".git").exists():
            return False, "NO_REPO", "Chưa khởi tạo Git."
        
        code, out, err = self.run_cmd(["fetch", "origin"], cwd=repo_path, timeout=10)
        if code == 0:
            return True, "", ""
            
        # Phân tích nguyên nhân lỗi dựa trên thông báo stderr
        err_lower = err.lower()
        if any(x in err_lower for x in ["auth", "permission denied", "could not read username", "terminal prompts disabled"]):
            return False, "AUTH", f"Lỗi xác thực Git Remote (Chưa cấu hình Token hoặc SSH key): {err}"
        elif any(x in err_lower for x in ["could not resolve host", "network is unreachable", "timed out", "connection reset"]):
            return False, "OFFLINE", "Không có kết nối mạng (Offline)."
        elif "not found" in err_lower:
            return False, "NOT_FOUND", f"Không tìm thấy Repository trên Remote (Sai link): {err}"
        
        return False, "ERROR", err

    def get_git_status(self, repo_path: Path) -> GitStatusResult:
        """Đánh giá chi tiết trạng thái Git của Local Library vs Remote Repo."""
        if not self.is_git_available():
            return GitStatusResult(status="NO_GIT", error_message="Git CLI chưa được cài đặt.")
        
        if not (repo_path / ".git").exists():
            return GitStatusResult(status="NO_GIT", error_message="Thư mục thư viện gốc chưa phải là Git repo.")

        # Thử fetch remote
        success, err_type, err_msg = self.fetch_remote(repo_path)

        # Kiểm tra Working Tree có bị sửa đổi chưa commit hay không
        code, status_out, _ = self.run_cmd(["status", "--porcelain"], cwd=repo_path)
        dirty_files = [line for line in status_out.splitlines() if line.strip()]

        if not success:
            if err_type == "AUTH":
                return GitStatusResult(
                    status="AUTH_ERROR",
                    dirty_files=dirty_files,
                    error_message=err_msg
                )
            elif err_type == "NOT_FOUND":
                return GitStatusResult(
                    status="NOT_FOUND_ERROR",
                    dirty_files=dirty_files,
                    error_message=err_msg
                )
            else:
                return GitStatusResult(
                    status="OFFLINE",
                    dirty_files=dirty_files,
                    error_message="Không thể kết nối Internet/Git Remote (Offline Mode)."
                )

        # So sánh HEAD với origin/main
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

        elif mode == "AUTO_MERGE":
            self.run_cmd(["add", "."], cwd=repo_path)
            self.run_cmd(["commit", "-m", "auto sync: local changes before merge"], cwd=repo_path)
            code, out, err = self.run_cmd(["pull", "origin", "main", "--no-rebase"], cwd=repo_path)
            if code == 0:
                self.run_cmd(["push", "origin", "main"], cwd=repo_path)
                return True, "Đã tự động hợp nhất (Merge) và đẩy lên Git Remote thành công."
            return False, f"Hợp nhất tự động thất bại (cần giải quyết bằng tay): {err}"

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
