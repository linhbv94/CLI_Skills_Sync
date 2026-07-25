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
    version: str = "1.1.0"
    library_path: str = ""
    selected_agents: List[str] = field(default_factory=lambda: ["antigravity", "codex", "claude"])
    agent_paths: Dict[str, str] = field(default_factory=dict)
    ignore_patterns: List[str] = field(default_factory=lambda: list(DEFAULT_IGNORE_PATTERNS))
    git_settings: Dict[str, bool] = field(default_factory=lambda: {"auto_fetch": True, "auto_push": True})

class ConfigManager:
    """Quản lý nạp, ghi cấu hình config.json và tự động dò đường dẫn Agent theo HĐH."""

    def __init__(self, config_dir: Path = None):
        if config_dir is None:
            home = Path.home()
            if sys.platform == "win32":
                self.config_dir = Path(os.environ.get("APPDATA", home)) / "skills_auto_sync"
            else:
                self.config_dir = home / ".config" / "skills_auto_sync"
        else:
            self.config_dir = Path(config_dir)

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.config = AppConfig()
        self.load_config()

    def get_default_agent_paths(self) -> Dict[str, str]:
        """Tự động phát hiện đường dẫn mặc định của Antigravity, Codex và Claude Code theo HĐH."""
        home = Path.home()
        paths = {
            "antigravity": str(home / ".gemini" / "config" / "skills"),
            "codex": str(home / ".codex" / "skills"),
            "claude": str(home / ".claude")
        }
        return paths

    def load_config(self) -> AppConfig:
        """Nạp cấu hình từ file json, tự động điền đường dẫn nếu chưa có."""
        defaults = self.get_default_agent_paths()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.config.version = data.get("version", "1.1.0")
                self.config.library_path = data.get("library_path", "")
                self.config.selected_agents = data.get("selected_agents", ["antigravity", "codex", "claude"])
                
                agent_paths = data.get("agent_paths", {})
                for agent_key, default_p in defaults.items():
                    if agent_key not in agent_paths or not agent_paths[agent_key]:
                        agent_paths[agent_key] = default_p
                self.config.agent_paths = agent_paths
                self.config.ignore_patterns = data.get("ignore_patterns", DEFAULT_IGNORE_PATTERNS)
                self.config.git_settings = data.get("git_settings", {"auto_fetch": True, "auto_push": True})
            except Exception as e:
                print(f"[ConfigManager] Lỗi nạp config ({e}), sử dụng mặc định.")
                self.config.agent_paths = defaults
        else:
            self.config.agent_paths = defaults
            self.save_config()

        return self.config

    def save_config(self):
        """Lưu trạng thái cấu hình hiện tại vào config.json."""
        data = {
            "version": self.config.version,
            "library_path": self.config.library_path,
            "selected_agents": self.config.selected_agents,
            "agent_paths": self.config.agent_paths,
            "ignore_patterns": self.config.ignore_patterns,
            "git_settings": self.config.git_settings
        }
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ConfigManager] Lỗi ghi config.json: {e}")
