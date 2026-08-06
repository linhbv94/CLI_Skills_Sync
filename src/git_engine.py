import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List

GIT_LOCALIZED = {
    "en": {
        "no_git_cli": "Git CLI is not installed.",
        "no_remote_url": "Git Remote URL is not provided.",
        "clone_ok": "Successfully cloned from {}",
        "clone_err": "Clone repo error: {}",
        "init_ok": "Initialized Git and linked remote origin -> {}",
        "link_err": "Link remote error: {}",
        "update_ok": "Successfully updated Git Remote origin -> {}",
        "url_ok": "Git Repo is linked correctly.",
        "no_repo": "Not a Git repository.",
        "no_git_init": "Git is not initialized.",
        "auth_err": "Git Remote Auth Error (Check Token or SSH key): {}",
        "offline": "No internet connection (Offline).",
        "not_found": "Remote Repository not found (Incorrect link): {}",
        "not_git_repo_dir": "Central Library folder is not a Git repo.",
        "offline_mode_msg": "Cannot connect to Internet/Git Remote (Offline Mode).",
        "pull_ok": "Successfully pulled new data from Git.",
        "pull_ff_err": "Cannot auto pull fast-forward: {}",
        "push_ok": "Successfully pushed new data to Git Remote.",
        "push_err": "Cannot push to Remote: {}",
        "merge_ok": "Successfully merged and pushed to Git Remote.",
        "merge_err": "Auto merge failed (manual resolution required): {}",
        "force_pull_ok": "Successfully restored data to Remote version.",
        "force_pull_err": "Force Pull Error: {}",
        "force_push_ok": "Successfully overwrote Remote version with Local version.",
        "force_push_err": "Force Push Error: {}",
        "invalid_mode": "Invalid mode: {}"
    },
    "vi": {
        "no_git_cli": "Git CLI chưa được cài đặt.",
        "no_remote_url": "Chưa nhập Git Remote URL.",
        "clone_ok": "Đã clone thành công từ {}",
        "clone_err": "Lỗi clone repo: {}",
        "init_ok": "Đã khởi tạo Git và liên kết remote origin -> {}",
        "link_err": "Lỗi liên kết remote: {}",
        "update_ok": "Đã cập nhật Git Remote origin -> {}",
        "url_ok": "Git Repo đã được liên kết chính xác.",
        "no_repo": "Không phải thư mục Git repo.",
        "no_git_init": "Chưa khởi tạo Git.",
        "auth_err": "Lỗi xác thực Git Remote (Chưa cấu hình Token hoặc SSH key): {}",
        "offline": "Không có kết nối mạng (Offline).",
        "not_found": "Không tìm thấy Repository trên Remote (Sai link): {}",
        "not_git_repo_dir": "Thư mục thư viện gốc chưa phải là Git repo.",
        "offline_mode_msg": "Không thể kết nối Internet/Git Remote (Offline Mode).",
        "pull_ok": "Đã pull dữ liệu mới từ Git thành công.",
        "pull_ff_err": "Không thể auto pull fast-forward: {}",
        "push_ok": "Đã push dữ liệu mới lên Git Remote thành công.",
        "push_err": "Không thể push lên Remote: {}",
        "merge_ok": "Đã tự động hợp nhất (Merge) và đẩy lên Git Remote thành công.",
        "merge_err": "Hợp nhất tự động thất bại (cần giải quyết bằng tay): {}",
        "force_pull_ok": "Đã khôi phục dữ liệu theo bản Remote thành công.",
        "force_pull_err": "Lỗi Force Pull: {}",
        "force_push_ok": "Đã ghi đè bản Local lên Remote thành công.",
        "force_push_err": "Lỗi Force Push: {}",
        "invalid_mode": "Mode không hợp lệ: {}"
    }
}

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

    def ensure_git_repo_linked(self, repo_path: Path, remote_url: str, lang: str = "en") -> Tuple[bool, str]:
        """
        Đảm bảo thư mục library_path đã được khởi tạo Git và liên kết với remote_url.
        """
        l = GIT_LOCALIZED.get(lang, GIT_LOCALIZED["en"])
        if not self.is_git_available():
            return False, l["no_git_cli"]

        if not remote_url:
            return False, l["no_remote_url"]

        # Case 1: Thư mục chưa tồn tại -> Clone từ Remote
        if not repo_path.exists():
            repo_path.parent.mkdir(parents=True, exist_ok=True)
            code, out, err = self.run_cmd(["clone", remote_url, str(repo_path)], cwd=repo_path.parent)
            if code == 0:
                return True, l["clone_ok"].format(remote_url)
            return False, l["clone_err"].format(err)

        # Case 2: Thư mục tồn tại nhưng chưa có .git
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            self.run_cmd(["init"], cwd=repo_path)
            self.run_cmd(["branch", "-M", "main"], cwd=repo_path)
            code, out, err = self.run_cmd(["remote", "add", "origin", remote_url], cwd=repo_path)
            if code == 0:
                return True, l["init_ok"].format(remote_url)
            return False, l["link_err"].format(err)

        # Case 3: Đã là Git repo -> Cập nhật remote origin
        code, current_url, _ = self.run_cmd(["remote", "get-url", "origin"], cwd=repo_path)
        if current_url != remote_url:
            if code == 0:
                self.run_cmd(["remote", "set-url", "origin", remote_url], cwd=repo_path)
            else:
                self.run_cmd(["remote", "add", "origin", remote_url], cwd=repo_path)
            return True, l["update_ok"].format(remote_url)

        return True, l["url_ok"]

    def fetch_remote(self, repo_path: Path, lang: str = "en") -> Tuple[bool, str, str]:
        """Thực hiện git fetch origin. Trả về (success, error_type, error_msg)."""
        l = GIT_LOCALIZED.get(lang, GIT_LOCALIZED["en"])
        if not (repo_path / ".git").exists():
            return False, "NO_REPO", l["no_git_init"]
        
        code, out, err = self.run_cmd(["fetch", "origin"], cwd=repo_path, timeout=10)
        if code == 0:
            return True, "", ""
            
        # Phân tích nguyên nhân lỗi dựa trên thông báo stderr
        err_lower = err.lower()
        if any(x in err_lower for x in ["auth", "permission denied", "could not read username", "terminal prompts disabled"]):
            return False, "AUTH", l["auth_err"].format(err)
        elif any(x in err_lower for x in ["could not resolve host", "network is unreachable", "timed out", "connection reset"]):
            return False, "OFFLINE", l["offline"]
        elif "not found" in err_lower:
            return False, "NOT_FOUND", l["not_found"].format(err)
        
        return False, "ERROR", err

    def get_git_status(self, repo_path: Path, lang: str = "en") -> GitStatusResult:
        """Đánh giá chi tiết trạng thái Git của Local Library vs Remote Repo."""
        l = GIT_LOCALIZED.get(lang, GIT_LOCALIZED["en"])
        if not self.is_git_available():
            return GitStatusResult(status="NO_GIT", error_message=l["no_git_cli"])
        
        if not (repo_path / ".git").exists():
            return GitStatusResult(status="NO_GIT", error_message=l["not_git_repo_dir"])

        # Thử fetch remote
        success, err_type, err_msg = self.fetch_remote(repo_path, lang)

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
                    error_message=l["offline_mode_msg"]
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

    def execute_smart_sync(self, repo_path: Path, mode: str, lang: str = "en") -> Tuple[bool, str]:
        """
        Thực thi hành động Git theo mode.
        """
        l = GIT_LOCALIZED.get(lang, GIT_LOCALIZED["en"])
        if not (repo_path / ".git").exists():
            return False, l["no_repo"]

        if mode == "AUTO_PULL":
            code, out, err = self.run_cmd(["pull", "--ff-only", "origin", "main"], cwd=repo_path)
            if code == 0:
                return True, l["pull_ok"]
            return False, l["pull_ff_err"].format(err)

        elif mode == "AUTO_PUSH":
            self.run_cmd(["add", "."], cwd=repo_path)
            self.run_cmd(["commit", "-m", "auto sync: skills library update"], cwd=repo_path)
            code, out, err = self.run_cmd(["push", "origin", "main"], cwd=repo_path)
            if code == 0:
                return True, l["push_ok"]
            return False, l["push_err"].format(err)

        elif mode == "AUTO_MERGE":
            self.run_cmd(["add", "."], cwd=repo_path)
            self.run_cmd(["commit", "-m", "auto sync: local changes before merge"], cwd=repo_path)
            code, out, err = self.run_cmd(["pull", "origin", "main", "--no-rebase"], cwd=repo_path)
            if code == 0:
                self.run_cmd(["push", "origin", "main"], cwd=repo_path)
                return True, l["merge_ok"]
            return False, l["merge_err"].format(err)

        elif mode == "FORCE_PULL":
            code, out, err = self.run_cmd(["reset", "--hard", "origin/main"], cwd=repo_path)
            if code == 0:
                return True, l["force_pull_ok"]
            return False, l["force_pull_err"].format(err)

        elif mode == "FORCE_PUSH":
            code, out, err = self.run_cmd(["push", "--force-with-lease", "origin", "main"], cwd=repo_path)
            if code == 0:
                return True, l["force_push_ok"]
            return False, l["force_push_err"].format(err)

        return False, l["invalid_mode"].format(mode)
