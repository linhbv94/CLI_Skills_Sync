import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import List, Dict

from src.config_manager import ConfigManager
from src.sync_engine import SyncEngine
from src.adapter_engine import AdapterEngine
from src.git_engine import GitEngine, GitStatusResult

# Palette màu Dark Theme tương thích cao trên macOS & Windows
BG_DARK = "#1e1e2e"
CARD_BG = "#2a2b3d"
TEXT_COLOR = "#e2e8f0"
TEXT_MUTED = "#a0aec0"
BORDER_COLOR = "#4a5568"
ACCENT_PRIMARY = "#3182ce"
ACCENT_HOVER = "#4299e1"
SUCCESS_COLOR = "#38a169"
WARNING_COLOR = "#dd6b20"
DANGER_COLOR = "#e53e3e"

class AppGUI(tk.Tk):
    """Giao diện Desktop mỏng nhẹ, thiết kế chuẩn Dark Mode chạy hoàn hảo trên Mac & Windows."""

    def __init__(self):
        super().__init__()

        self.title("⚡ Skills Auto Sync Tool")
        self.geometry("820x680")
        self.minsize(760, 600)
        self.configure(bg=BG_DARK)

        # Config & Engines
        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.config
        self.sync_engine = SyncEngine()
        self.adapter_engine = AdapterEngine()
        self.git_engine = GitEngine()

        # UI Variables
        self.library_path_var = tk.StringVar(value=self.config.library_path)
        self.git_remote_url_var = tk.StringVar(value=self.config.git_remote_url)
        self.agent_vars: Dict[str, tk.BooleanVar] = {
            "antigravity": tk.BooleanVar(value="antigravity" in self.config.selected_agents),
            "codex": tk.BooleanVar(value="codex" in self.config.selected_agents),
            "claude": tk.BooleanVar(value="claude" in self.config.selected_agents),
        }
        self.path_vars: Dict[str, tk.StringVar] = {
            agent: tk.StringVar(value=self.config.agent_paths.get(agent, ""))
            for agent in ["antigravity", "codex", "claude"]
        }

        self._build_ui()
        self.refresh_git_status()

    def _build_ui(self):
        main_frame = tk.Frame(self, bg=BG_DARK, padx=16, pady=16)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- HEADER TITLE ---
        lbl_title = tk.Label(
            main_frame, text="⚡ Skills Auto Sync Tool",
            font=("Segoe UI", 16, "bold"), fg="#63b3ed", bg=BG_DARK
        )
        lbl_title.pack(anchor="w", pady=(0, 12))

        # --- SECTION 1: CENTRAL SKILLS LIBRARY & GIT REMOTE REPO ---
        sec1 = tk.LabelFrame(
            main_frame, text=" 📌 1. THƯ VIỆN GỐC & GIT REMOTE REPO ",
            font=("Segoe UI", 11, "bold"), fg="#9f7aea", bg=CARD_BG,
            bd=1, relief="solid", padx=12, pady=12
        )
        sec1.pack(fill=tk.X, pady=(0, 12))

        # Row 1.1: Local Library Path
        r1 = tk.Frame(sec1, bg=CARD_BG)
        r1.pack(fill=tk.X, pady=4)
        tk.Label(r1, text="Skills Lib Path:", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg=CARD_BG, width=15, anchor="w").pack(side=tk.LEFT)
        e_lib = tk.Entry(r1, textvariable=self.library_path_var, font=("Segoe UI", 10), bg="#1a202c", fg="#e2e8f0", insertbackground="white", bd=1, relief="solid")
        e_lib.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        tk.Button(r1, text="Browse...", font=("Segoe UI", 9), bg="#4a5568", fg="white", activebackground="#718096", activeforeground="white", command=self.browse_library_path).pack(side=tk.LEFT)

        # Row 1.2: Git Remote URL
        r2 = tk.Frame(sec1, bg=CARD_BG)
        r2.pack(fill=tk.X, pady=4)
        tk.Label(r2, text="Git Remote URL:", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg=CARD_BG, width=15, anchor="w").pack(side=tk.LEFT)
        e_url = tk.Entry(r2, textvariable=self.git_remote_url_var, font=("Segoe UI", 10), bg="#1a202c", fg="#e2e8f0", insertbackground="white", bd=1, relief="solid")
        e_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        tk.Button(r2, text="🔗 Link/Clone Repo", font=("Segoe UI", 9, "bold"), bg="#805ad5", fg="white", activebackground="#9f7aea", activeforeground="white", command=self.link_git_repo).pack(side=tk.LEFT)

        # Row 1.3: Git Status Badge Line
        r3 = tk.Frame(sec1, bg=CARD_BG)
        r3.pack(fill=tk.X, pady=(6, 0))
        tk.Label(r3, text="Git Status:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(side=tk.LEFT, padx=(0, 8))
        self.lbl_git_status = tk.Label(r3, text="Checking...", font=("Segoe UI", 10, "bold"), fg="#63b3ed", bg=CARD_BG)
        self.lbl_git_status.pack(side=tk.LEFT)

        # --- SECTION 2: ACTIVE AGENTS ---
        sec2 = tk.LabelFrame(
            main_frame, text=" 🤖 2. CẤU HÌNH AGENTS TRÊN MÁY NÀY ",
            font=("Segoe UI", 11, "bold"), fg="#38b2ac", bg=CARD_BG,
            bd=1, relief="solid", padx=12, pady=12
        )
        sec2.pack(fill=tk.X, pady=(0, 12))

        agents_info = [
            ("antigravity", "Antigravity Agent", "~/.gemini/config/skills"),
            ("codex", "Codex Agent (Giữ .system)", "~/.codex/skills"),
            ("claude", "Claude Code Agent", "~/.claude"),
        ]

        for key, label_text, default_hint in agents_info:
            row = tk.Frame(sec2, bg=CARD_BG)
            row.pack(fill=tk.X, pady=4)

            chk = tk.Checkbutton(
                row, text=label_text, variable=self.agent_vars[key],
                font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg=CARD_BG,
                activebackground=CARD_BG, activeforeground=TEXT_COLOR, selectcolor="#2d3748"
            )
            chk.pack(side=tk.LEFT, width=24, anchor="w")

            ent = tk.Entry(row, textvariable=self.path_vars[key], font=("Segoe UI", 10), bg="#1a202c", fg="#e2e8f0", insertbackground="white", bd=1, relief="solid")
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

            tk.Button(row, text="Browse", font=("Segoe UI", 9), bg="#4a5568", fg="white", activebackground="#718096", activeforeground="white", command=lambda k=key: self.browse_agent_path(k)).pack(side=tk.LEFT, padx=(0, 4))
            tk.Button(row, text="Auto Detect", font=("Segoe UI", 9), bg="#2d3748", fg="white", activebackground="#4a5568", activeforeground="white", command=lambda k=key: self.auto_detect_path(k)).pack(side=tk.LEFT)

        # --- SECTION 3: ACTION BAR ---
        sec3 = tk.Frame(main_container_frame:=main_frame, bg=BG_DARK)
        sec3.pack(fill=tk.X, pady=(0, 12))

        btn_sync = tk.Button(
            sec3, text="🚀 SMART SYNC NOW", font=("Segoe UI", 11, "bold"),
            bg=ACCENT_PRIMARY, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            bd=0, padx=18, pady=8, cursor="hand2", command=self.run_smart_sync
        )
        btn_sync.pack(side=tk.RIGHT, padx=(8, 0))

        btn_preview = tk.Button(
            sec3, text="🔍 Preview Changes", font=("Segoe UI", 10),
            bg="#4a5568", fg="white", activebackground="#718096", activeforeground="white",
            bd=0, padx=12, pady=6, cursor="hand2", command=self.preview_changes
        )
        btn_preview.pack(side=tk.RIGHT, padx=(8, 0))

        btn_save = tk.Button(
            sec3, text="⚙️ Save Config", font=("Segoe UI", 10),
            bg="#2d3748", fg="white", activebackground="#4a5568", activeforeground="white",
            bd=0, padx=12, pady=6, cursor="hand2", command=self.save_current_config
        )
        btn_save.pack(side=tk.RIGHT)

        # --- SECTION 4: LOG CONSOLE ---
        sec4 = tk.LabelFrame(
            main_frame, text=" 💡 LOG BÁO CÁO TIẾN TRÌNH ",
            font=("Segoe UI", 10, "bold"), fg=TEXT_MUTED, bg=CARD_BG,
            bd=1, relief="solid", padx=8, pady=8
        )
        sec4.pack(fill=tk.BOTH, expand=True)

        self.txt_log = tk.Text(
            sec4, font=("Menlo" if sys.platform == "darwin" else "Consolas", 10),
            bg="#0f172a", fg="#38bdf8", insertbackground="white", bd=0, wrap="word"
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = tk.Scrollbar(sec4, orient=tk.VERTICAL, command=self.txt_log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.configure(yscrollcommand=scrollbar.set)

        self.log("[System] Đã sẵn sàng. Điền đường dẫn Library + Git Remote URL rồi bấm Smart Sync!")

    def log(self, message: str):
        """Ghi log vào console window."""
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)

    def browse_library_path(self):
        d = filedialog.askdirectory(title="Chọn Thư viện Skills Trung tâm")
        if d:
            self.library_path_var.set(d)
            self.refresh_git_status()

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
        """Lưu cấu hình vào file config.json."""
        self.config.library_path = self.library_path_var.get().strip()
        self.config.git_remote_url = self.git_remote_url_var.get().strip()
        self.config.selected_agents = [k for k, v in self.agent_vars.items() if v.get()]
        for k, v in self.path_vars.items():
            self.config.agent_paths[k] = v.get().strip()

        self.config_mgr.save_config()
        self.log("[Config] Đã lưu cấu hình thành công vào config.json.")

    def link_git_repo(self):
        """Khởi tạo hoặc liên kết Git Repo theo git_remote_url."""
        lib_str = self.library_path_var.get().strip()
        remote_url = self.git_remote_url_var.get().strip()

        if not lib_str:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đường dẫn Thư viện Skills Lib Path trước.")
            return

        if not remote_url:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Git Remote URL (Ví dụ: https://github.com/user/skills.git).")
            return

        self.save_current_config()
        ok, msg = self.git_engine.ensure_git_repo_linked(Path(lib_str), remote_url)
        if ok:
            messagebox.showinfo("Thành công", msg)
            self.log(f"[Git Link] {msg}")
        else:
            messagebox.showerror("Lỗi Git Link", msg)
            self.log(f"[Git Link Error] {msg}")

        self.refresh_git_status()

    def refresh_git_status(self):
        """Cập nhật Badge trạng thái Git."""
        lib_str = self.library_path_var.get().strip()
        if not lib_str or not Path(lib_str).exists():
            self.lbl_git_status.configure(text="🔴 Chưa chọn thư mục Skills Lib", fg="#f56565")
            return

        res = self.git_engine.get_git_status(Path(lib_str))
        if res.status == "UP_TO_DATE":
            self.lbl_git_status.configure(text="🟢 Up-to-date (Git synced)", fg="#48bb78")
        elif res.status == "AHEAD":
            self.lbl_git_status.configure(text=f"🔵 Local Ahead ({res.ahead_count} commits)", fg="#4299e1")
        elif res.status == "BEHIND":
            self.lbl_git_status.configure(text=f"🟧 Remote Ahead ({res.behind_count} commits pending)", fg="#ed8936")
        elif res.status == "DIVERGED":
            self.lbl_git_status.configure(text=f"🔴 Conflict (Diverged: +{res.ahead_count}/-{res.behind_count})", fg="#f56565")
        elif res.status == "OFFLINE":
            self.lbl_git_status.configure(text="⚠️ Offline Mode", fg="#ecc94b")
        else:
            self.lbl_git_status.configure(text=f"ℹ️ {res.error_message}", fg="#a0aec0")

    def preview_changes(self):
        """Xem trước tiến trình đồng bộ."""
        lib_str = self.library_path_var.get().strip()
        if not lib_str or not Path(lib_str).exists():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn Thư viện Skills Lib Path hợp lệ trước.")
            return

        self.save_current_config()
        lib_path = Path(lib_str)

        self.log("\n--- 🔍 PREVIEW SUMMARY ---")
        res = self.sync_engine.scan_and_sync_upstream(
            lib_path, self.config.agent_paths, self.config.selected_agents, self.config.ignore_patterns
        )

        if res.files_synced_to_library:
            self.log(f"Phát hiện {len(res.files_synced_to_library)} file sửa mới ở Agent:")
            for f in res.files_synced_to_library:
                self.log(f"  • {f}")
        else:
            self.log("Không có file sửa mới ở Agent. Library đã cập nhật.")

        self.refresh_git_status()

    def run_smart_sync(self):
        """Tiến trình 1-Click Smart Sync (Auto Init/Link Git -> Upstream Sync -> Git Sync -> Deploy Adapters)."""
        lib_str = self.library_path_var.get().strip()
        remote_url = self.git_remote_url_var.get().strip()

        if not lib_str:
            messagebox.showerror("Lỗi", "Chưa nhập đường dẫn Thư viện Skills Lib Path.")
            return

        self.save_current_config()
        lib_path = Path(lib_str)

        self.log("\n🚀 === KHỞI ĐỘNG SMART SYNC ===")

        # BƯỚC 0: TỰ ĐỘNG KHỞI TẠO HOẶC KẾT NỐI GIT NẾU CÓ URL
        if remote_url:
            self.log(f"[Step 0/3] Kiểm tra liên kết Git Remote URL: {remote_url}")
            ok_link, msg_link = self.git_engine.ensure_git_repo_linked(lib_path, remote_url)
            self.log(f"  {'✓' if ok_link else '⚠️'} {msg_link}")

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

        self.refresh_git_status()
        self.log("🎉 === SMART SYNC HOÀN TẤT THÀNH CÔNG ===\n")
