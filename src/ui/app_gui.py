import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Dict

from src.config_manager import ConfigManager
from src.sync_engine import SyncEngine
from src.adapter_engine import AdapterEngine
from src.git_engine import GitEngine, GitStatusResult

class AppGUI(tk.Tk):
    """Giao diện Desktop mỏng nhẹ, chạy mượt mà trên macOS và Windows."""

    def __init__(self):
        super().__init__()

        self.title("⚡ Skills Auto Sync Tool")
        self.geometry("780x620")
        self.minsize(720, 560)

        # Config & Engines
        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.config
        self.sync_engine = SyncEngine()
        self.adapter_engine = AdapterEngine()
        self.git_engine = GitEngine()

        # UI Variables
        self.library_path_var = tk.StringVar(value=self.config.library_path)
        self.agent_vars: Dict[str, tk.BooleanVar] = {
            "antigravity": tk.BooleanVar(value="antigravity" in self.config.selected_agents),
            "codex": tk.BooleanVar(value="codex" in self.config.selected_agents),
            "claude": tk.BooleanVar(value="claude" in self.config.selected_agents),
        }
        self.path_vars: Dict[str, tk.StringVar] = {
            agent: tk.StringVar(value=self.config.agent_paths.get(agent, ""))
            for agent in ["antigravity", "codex", "claude"]
        }

        self._setup_styles()
        self._build_ui()
        self.refresh_git_status_async()

    def _setup_styles(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("TFrame", background="#f7fafc")
        style.configure("TLabel", background="#f7fafc", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), foreground="#2d3748")
        style.configure("Status.TLabel", font=("Segoe UI", 10, "bold"), foreground="#2b6cb0")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), foreground="#ffffff", background="#2b6cb0")

    def _build_ui(self):
        main_container = ttk.Frame(self, padding="16 16 16 16")
        main_container.pack(fill=tk.BOTH, expand=True)

        # --- SECTION 1: Central Library Path ---
        sec1 = ttk.LabelFrame(main_container, text=" 📌 1. THƯ VIỆN SKILLS TRUNG TÂM (LOCAL LIBRARY) ", padding="10 10 10 10")
        sec1.pack(fill=tk.X, pady=(0, 12))

        f1 = ttk.Frame(sec1)
        f1.pack(fill=tk.X, pady=2)
        ttk.Label(f1, text="Library Path:").pack(side=tk.LEFT, padx=(0, 8))
        ttk.Entry(f1, textvariable=self.library_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(f1, text="Browse...", command=self.browse_library_path).pack(side=tk.LEFT)

        # Status Line
        f_status = ttk.Frame(sec1)
        f_status.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(f_status, text="Git Status:").pack(side=tk.LEFT, padx=(0, 6))
        self.lbl_git_status = ttk.Label(f_status, text="Checking...", style="Status.TLabel")
        self.lbl_git_status.pack(side=tk.LEFT)

        # --- SECTION 2: Active Agents Configuration ---
        sec2 = ttk.LabelFrame(main_container, text=" 🤖 2. CHỌN AGENTS ĐỒNG BỘ TRÊN MÁY NÀY ", padding="10 10 10 10")
        sec2.pack(fill=tk.X, pady=(0, 12))

        agents_info = [
            ("antigravity", "Antigravity Agent", "~/.gemini/config/skills"),
            ("codex", "Codex Agent (Giữ nguyên .system)", "~/.codex/skills"),
            ("claude", "Claude Code Agent", "~/.claude"),
        ]

        for key, label_text, default_hint in agents_info:
            row = ttk.Frame(sec2)
            row.pack(fill=tk.X, pady=4)

            ttk.Checkbutton(row, text=label_text, variable=self.agent_vars[key], width=32).pack(side=tk.LEFT)
            ttk.Entry(row, textvariable=self.path_vars[key]).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
            ttk.Button(row, text="Browse", command=lambda k=key: self.browse_agent_path(k)).pack(side=tk.LEFT, padx=(0, 4))
            ttk.Button(row, text="Auto Detect", command=lambda k=key: self.auto_detect_path(k)).pack(side=tk.LEFT)

        # --- SECTION 3: Action Buttons Bar ---
        sec3 = ttk.Frame(main_container)
        sec3.pack(fill=tk.X, pady=(0, 12))

        btn_sync = tk.Button(
            sec3, text="🚀 SMART SYNC NOW", font=("Segoe UI", 11, "bold"),
            bg="#2b6cb0", fg="white", activebackground="#3182ce", activeforeground="white",
            padx=16, pady=8, command=self.run_smart_sync
        )
        btn_sync.pack(side=tk.RIGHT, padx=(8, 0))

        btn_preview = ttk.Button(sec3, text="🔍 Preview Changes", command=self.preview_changes)
        btn_preview.pack(side=tk.RIGHT, padx=(8, 0))

        btn_save = ttk.Button(sec3, text="⚙️ Save Config", command=self.save_current_config)
        btn_save.pack(side=tk.RIGHT)

        # --- SECTION 4: Log Output Console ---
        sec4 = ttk.LabelFrame(main_container, text=" 💡 LOG BÁO CÁO TIẾN TRÌNH ", padding="8 8 8 8")
        sec4.pack(fill=tk.BOTH, expand=True)

        self.txt_log = tk.Text(sec4, font=("Consolas", 9), height=10, bg="#1a202c", fg="#e2e8f0")
        self.txt_log.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(sec4, orient=tk.VERTICAL, command=self.txt_log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.configure(yscrollcommand=scrollbar.set)

        self.log("[System] Đã sẵn sàng. Bấm 'Smart Sync' để tự động đồng bộ 3 nguồn.")

    def log(self, message: str):
        """Ghi log vào khung console."""
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)

    def browse_library_path(self):
        d = filedialog.askdirectory(title="Chọn Thư viện Skills Trung tâm")
        if d:
            self.library_path_var.set(d)
            self.refresh_git_status_async()

    def browse_agent_path(self, agent_key: str):
        d = filedialog.askdirectory(title=f"Chọn đường dẫn folder của {agent_key}")
        if d:
            self.path_vars[agent_key].set(d)

    def auto_detect_path(self, agent_key: str):
        defaults = self.config_mgr.get_default_agent_paths()
        detected = defaults.get(agent_key, "")
        self.path_vars[agent_key].set(detected)
        self.log(f"[Auto-Detect] {agent_key} -> {detected}")

    def save_current_config(self):
        """Cập nhật và lưu cấu hình vào config.json."""
        self.config.library_path = self.library_path_var.get().strip()
        self.config.selected_agents = [k for k, v in self.agent_vars.items() if v.get()]
        for k, v in self.path_vars.items():
            self.config.agent_paths[k] = v.get().strip()

        self.config_mgr.save_config()
        self.log("[Config] Đã lưu cấu hình thành công vào config.json.")

    def refresh_git_status_async(self):
        lib_str = self.library_path_var.get().strip()
        if not lib_str or not Path(lib_str).exists():
            self.lbl_git_status.configure(text="🔴 Chưa chọn/Không thấy đường dẫn Library", foreground="#c53030")
            return

        res = self.git_engine.get_git_status(Path(lib_str))
        if res.status == "UP_TO_DATE":
            self.lbl_git_status.configure(text="🟢 Up-to-date (Git synchronized)", foreground="#2f855a")
        elif res.status == "AHEAD":
            self.lbl_git_status.configure(text=f"🔵 Local Ahead ({res.ahead_count} commits / dirty)", foreground="#2b6cb0")
        elif res.status == "BEHIND":
            self.lbl_git_status.configure(text=f"🟧 Remote Ahead ({res.behind_count} commits pending)", foreground="#dd6b20")
        elif res.status == "DIVERGED":
            self.lbl_git_status.configure(text=f"🔴 Conflict (Diverged: +{res.ahead_count}/-{res.behind_count})", foreground="#c53030")
        elif res.status == "OFFLINE":
            self.lbl_git_status.configure(text="⚠️ Offline Mode (Offline sync enabled)", foreground="#d69e2e")
        else:
            self.lbl_git_status.configure(text=f"ℹ️ {res.error_message}", foreground="#718096")

    def preview_changes(self):
        """Xem trước các file sẽ được đồng bộ."""
        lib_str = self.library_path_var.get().strip()
        if not lib_str or not Path(lib_str).exists():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn Thư viện Skills Trung tâm hợp lệ trước.")
            return

        self.save_current_config()
        lib_path = Path(lib_str)

        self.log("--- 🔍 PREVIEW SUMMARY ---")
        res = self.sync_engine.scan_and_sync_upstream(
            lib_path, self.config.agent_paths, self.config.selected_agents, self.config.ignore_patterns
        )

        if res.files_synced_to_library:
            self.log(f"Phát hiện {len(res.files_synced_to_library)} file sửa mới ở Agent (sẽ gom về Library):")
            for f in res.files_synced_to_library:
                self.log(f"  • {f}")
        else:
            self.log("Không có file sửa mới ở Agent. Library đã cập nhật.")

        self.refresh_git_status_async()

    def run_smart_sync(self):
        """Thực thi toàn bộ tiến trình 1-Click Smart Sync (Upstream Sync -> Git Sync -> Deploy Adapters)."""
        lib_str = self.library_path_var.get().strip()
        if not lib_str or not Path(lib_str).exists():
            messagebox.showerror("Lỗi", "Đường dẫn Thư viện Skills Trung tâm không tồn tại.")
            return

        self.save_current_config()
        lib_path = Path(lib_str)

        self.log("\n🚀 === KHỞI ĐỘNG SMART SYNC ===")

        # BƯỚC 1: UPSTREAM SYNC (Gom file sửa từ Agent về Library)
        self.log("[Step 1/3] Quét thay đổi từ Agent Folders (bỏ qua .system)...")
        up_res = self.sync_engine.scan_and_sync_upstream(
            lib_path, self.config.agent_paths, self.config.selected_agents, self.config.ignore_patterns
        )

        if up_res.has_library_changes:
            self.log(f"  ✓ Đã gom {len(up_res.files_synced_to_library)} file sửa đổi mới từ Agent về Library.")

        # BƯỚC 2: GIT SMART SYNC
        self.log("[Step 2/3] Kiểm tra và đồng bộ Git Remote...")
        git_res = self.git_engine.get_git_status(lib_path)

        if git_res.status == "BEHIND":
            self.log(f"  ➜ Pulling {git_res.behind_count} commits từ Git...")
            ok, msg = self.git_engine.execute_smart_sync(lib_path, "AUTO_PULL")
            self.log(f"  {'✓' if ok else '❌'} {msg}")

        elif git_res.status == "AHEAD" or up_res.has_library_changes:
            self.log("  ➜ Committing & Pushing thay đổi mới lên Git...")
            ok, msg = self.git_engine.execute_smart_sync(lib_path, "AUTO_PUSH")
            self.log(f"  {'✓' if ok else '❌'} {msg}")

        elif git_res.status == "DIVERGED":
            ans = messagebox.askyesno(
                "Xung đột Git Remote",
                f"Phát hiện xung đột Git Remote (+{git_res.ahead_count}/-{git_res.behind_count}).\n\n"
                "Bạn có muốn FORCE PUSH bản Local hiện tại đè lên Git Remote không?\n"
                "(Chọn 'No' để Force Pull bản Remote về)."
            )
            mode = "FORCE_PUSH" if ans else "FORCE_PULL"
            ok, msg = self.git_engine.execute_smart_sync(lib_path, mode)
            self.log(f"  {'✓' if ok else '❌'} {msg}")

        elif git_res.status == "OFFLINE":
            self.log("  ⚠️ Offline Mode: Bỏ qua Git sync, tiếp tục đồng bộ cục bộ.")

        # BƯỚC 3: DEPLOY ADAPTERS & DOWNSTREAM SYNC
        self.log("[Step 3/3] Triển khai Adapters (AGENTS.md, CLAUDE.md) & Phân bổ Skills...")
        adapters_deployed = self.adapter_engine.deploy_adapters(
            lib_path, self.config.agent_paths, self.config.selected_agents
        )
        for adp in adapters_deployed:
            self.log(f"  ✓ Deployed rule: {adp}")

        skills_deployed = self.sync_engine.deploy_skills_to_agents(
            lib_path, self.config.agent_paths, self.config.selected_agents, self.config.ignore_patterns
        )
        self.log(f"  ✓ Đã cập nhật skills tới: {', '.join(skills_deployed)}")

        self.refresh_git_status_async()
        self.log("🎉 === SMART SYNC HOÀN TẤT THÀNH CÔNG ===\n")
