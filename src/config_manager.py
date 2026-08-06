import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict

DEFAULT_IGNORE_PATTERNS = [
    "**/.system/**",
    "**/.git/**",
    "**/.DS_Store",
    "**/desktop.ini",
    "**/*.tmp",
    "**/*.bak*"
]

@dataclass
class AppConfig:
    version: str = "2.3.0"
    lang: str = "en"
    agents: Dict[str, int] = field(default_factory=lambda: {"anti": 1, "codex": 1, "claude": 0})
    skills_lib: str = ""
    git_repo: str = ""
    ignore_patterns: List[str] = field(default_factory=lambda: list(DEFAULT_IGNORE_PATTERNS))

class ConfigManager:
    """Quản lý nạp, ghi cấu hình config.json tại thư mục hệ thống chuẩn."""

    def __init__(self, config_dir: Path = None):
        if config_dir is None:
            # Xác định thư mục hệ thống Application Support (macOS) hoặc AppData (Windows)
            home = Path.home()
            if sys.platform == "win32":
                app_data = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
                self.config_dir = app_data / "Skills_Sync"
            else:
                self.config_dir = home / "Library" / "Application Support" / "Skills_Sync"
        else:
            self.config_dir = Path(config_dir)

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.config = AppConfig()
        self.load_config()

    def get_default_agent_paths(self) -> Dict[str, str]:
        """Tự động phát hiện đường dẫn mặc định của các Agent theo HĐH."""
        home = Path.home()
        if sys.platform == "win32":
            user_profile = Path(os.environ.get("USERPROFILE", home))
            return {
                "anti": str(user_profile / ".gemini" / "config"),
                "codex": str(user_profile / ".codex"),
                "claude": str(user_profile / ".claude")
            }
        else:
            return {
                "anti": str(home / ".gemini" / "config"),
                "codex": str(home / ".codex"),
                "claude": str(home / ".claude")
            }

    def load_config(self) -> AppConfig:
        """Nạp cấu hình từ file json cục bộ."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.config.version = data.get("version", "2.2.0")
                self.config.lang = data.get("lang", "en")
                self.config.skills_lib = data.get("skills_lib", "")
                git_repo = data.get("git_repo", "")
                if git_repo.startswith("/http"):
                    git_repo = git_repo.lstrip("/")
                self.config.git_repo = git_repo
                
                # Nạp agents config
                agents_data = data.get("agents", {})
                self.config.agents = {
                    "anti": agents_data.get("anti", 1),
                    "codex": agents_data.get("codex", 1),
                    "claude": agents_data.get("claude", 0)
                }
                
                self.config.ignore_patterns = data.get("ignore_patterns", DEFAULT_IGNORE_PATTERNS)
            except Exception as e:
                print(f"[ConfigManager] Lỗi nạp config.json ({e}), sử dụng mặc định.")
                self.save_config()
        else:
            self.save_config()

        return self.config

    def save_config(self):
        """Lưu cấu hình hiện tại vào config.json."""
        data = {
            "version": self.config.version,
            "lang": self.config.lang,
            "agents": self.config.agents,
            "skills_lib": self.config.skills_lib,
            "git_repo": self.config.git_repo,
            "ignore_patterns": self.config.ignore_patterns
        }

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ConfigManager] Lỗi ghi config.json: {e}")
