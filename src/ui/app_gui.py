import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Dict

from src.adapter_engine import AdapterEngine
from src.config_manager import ConfigManager
from src.git_engine import GitEngine
from src.sync_engine import SyncEngine


COLORS = {
    # Apple ships Tk 8.5.9 with the system Python. Its Aqua renderer can
    # silently ignore custom foreground colors in macOS dark mode, producing
    # dark text on dark surfaces. A light palette remains legible even when
    # Aqua overrides a widget's requested foreground.
    "window": "#f3f5f8",
    "surface": "#ffffff",
    "surface_alt": "#f7f8fa",
    "border": "#dce1e8",
    "text": "#171a21",
    "muted": "#5f6878",
    "subtle": "#8791a2",
    "accent": "#5b47df",
    "accent_hover": "#4937c7",
    "success": "#198754",
    "warning": "#a66300",
    "danger": "#c9364f",
    "info": "#246fbe",
}

class AppGUI(tk.Tk):
    """Compact cross-platform desktop UI for Skills Auto Sync."""

    AGENTS = (
        ("antigravity", "Antigravity", "Gemini global skills"),
        ("codex", "Codex", "System skills are protected"),
        ("claude", "Claude Code", "Claude global skills"),
    )

    def __init__(self):
        super().__init__()

        self.title("Skills Sync")
        self.geometry("920x720")
        self.minsize(820, 650)
        self.configure(bg=COLORS["window"])
        self._build_fonts()

        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.config
        self.sync_engine = SyncEngine()
        self.adapter_engine = AdapterEngine()
        self.git_engine = GitEngine()

        self.library_path_var = tk.StringVar(value=self.config.library_path)
        self.git_remote_url_var = tk.StringVar(value=self.config.git_remote_url)
        self.agent_vars: Dict[str, tk.BooleanVar] = {
            key: tk.BooleanVar(value=key in self.config.selected_agents)
            for key, _, _ in self.AGENTS
        }
        self.path_vars: Dict[str, tk.StringVar] = {
            key: tk.StringVar(value=self.config.agent_paths.get(key, ""))
            for key, _, _ in self.AGENTS
        }

        self._build_ui()
        self.refresh_git_status()

    def _build_fonts(self):
        """Build from Tk's resolved system fonts; never rely on platform font names."""
        default = tkfont.nametofont("TkDefaultFont")
        fixed = tkfont.nametofont("TkFixedFont")

        def variant(base, size, weight="normal"):
            result = base.copy()
            result.configure(size=size, weight=weight)
            return result

        self.fonts = {
            "title": variant(default, 22, "bold"),
            "section": variant(default, 12, "bold"),
            "body": variant(default, 10),
            "body_bold": variant(default, 10, "bold"),
            "small": variant(default, 9),
            "small_bold": variant(default, 9, "bold"),
            "tiny": variant(default, 8),
            "log": variant(fixed, 9),
        }

    def _build_ui(self):
        shell = tk.Frame(self, bg=COLORS["window"], padx=28, pady=24)
        shell.pack(fill=tk.BOTH, expand=True)
        shell.grid_columnconfigure(0, weight=1)
        shell.grid_rowconfigure(4, weight=1)

        self._build_header(shell)
        self._build_workspace_card(shell)
        self._build_agents_card(shell)
        self._build_action_bar(shell)
        self._build_activity_card(shell)

    def _build_header(self, parent):
        header = tk.Frame(parent, bg=COLORS["window"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(0, weight=1)

        title_group = tk.Frame(header, bg=COLORS["window"])
        title_group.grid(row=0, column=0, sticky="w")
        tk.Label(
            title_group,
            text="Skills Sync",
            font=self.fonts["title"],
            fg=COLORS["text"],
            bg=COLORS["window"],
        ).pack(anchor="w")
        tk.Label(
            title_group,
            text="One library. Every agent. Every machine.",
            font=self.fonts["body"],
            fg=COLORS["muted"],
            bg=COLORS["window"],
        ).pack(anchor="w", pady=(4, 0))

        status = tk.Frame(
            header,
            bg=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            padx=13,
            pady=8,
        )
        status.grid(row=0, column=1, sticky="e")
        self.status_dot = tk.Label(
            status,
            text="●",
            font=self.fonts["body"],
            fg=COLORS["subtle"],
            bg=COLORS["surface"],
        )
        self.status_dot.pack(side=tk.LEFT, padx=(0, 7))
        self.lbl_git_status = tk.Label(
            status,
            text="Checking Git",
            font=self.fonts["body_bold"],
            fg=COLORS["muted"],
            bg=COLORS["surface"],
        )
        self.lbl_git_status.pack(side=tk.LEFT)
        self._button(
            status,
            "↻",
            self.refresh_git_status,
            kind="ghost",
            width=3,
        ).pack(side=tk.LEFT, padx=(9, 0))

    def _card(self, parent, row, title, description, pady=(0, 14)):
        card = tk.Frame(
            parent,
            bg=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            padx=18,
            pady=16,
        )
        card.grid(row=row, column=0, sticky="ew", pady=pady)
        card.grid_columnconfigure(0, weight=1)

        tk.Label(
            card,
            text=title,
            font=self.fonts["section"],
            fg=COLORS["text"],
            bg=COLORS["surface"],
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            card,
            text=description,
            font=self.fonts["small"],
            fg=COLORS["muted"],
            bg=COLORS["surface"],
        ).grid(row=1, column=0, sticky="w", pady=(3, 12))
        return card

    def _build_workspace_card(self, parent):
        card = self._card(
            parent,
            1,
            "Workspace",
            "Central library and optional Git remote",
        )
        form = tk.Frame(card, bg=COLORS["surface"])
        form.grid(row=2, column=0, sticky="ew")
        form.grid_columnconfigure(1, weight=1)

        self._field_label(form, "Library").grid(row=0, column=0, sticky="w", padx=(0, 14))
        self._entry(form, self.library_path_var).grid(row=0, column=1, sticky="ew")
        self._button(form, "Choose", self.browse_library_path).grid(
            row=0, column=2, padx=(8, 0)
        )

        self._field_label(form, "Remote").grid(
            row=1, column=0, sticky="w", padx=(0, 14), pady=(10, 0)
        )
        self._entry(form, self.git_remote_url_var).grid(
            row=1, column=1, sticky="ew", pady=(10, 0)
        )
        self._button(form, "Connect", self.link_git_repo).grid(
            row=1, column=2, padx=(8, 0), pady=(10, 0)
        )

    def _build_agents_card(self, parent):
        card = self._card(
            parent,
            2,
            "Destinations",
            "Enable an agent and confirm its local skills folder",
        )
        list_frame = tk.Frame(card, bg=COLORS["surface"])
        list_frame.grid(row=2, column=0, sticky="ew")
        list_frame.grid_columnconfigure(1, weight=1)

        for row_index, (key, name, note) in enumerate(self.AGENTS):
            row = tk.Frame(list_frame, bg=COLORS["surface_alt"], padx=12, pady=9)
            row.grid(
                row=row_index,
                column=0,
                columnspan=3,
                sticky="ew",
                pady=(0, 7 if row_index < len(self.AGENTS) - 1 else 0),
            )
            row.grid_columnconfigure(2, weight=1)

            toggle = tk.Checkbutton(
                row,
                variable=self.agent_vars[key],
                bg=COLORS["surface_alt"],
                activebackground=COLORS["surface_alt"],
                selectcolor=COLORS["surface"],
                highlightthickness=0,
                bd=0,
                cursor="hand2",
            )
            toggle.grid(row=0, column=0, rowspan=2, padx=(0, 9))

            name_group = tk.Frame(row, bg=COLORS["surface_alt"], width=148)
            name_group.grid(row=0, column=1, rowspan=2, sticky="w")
            name_group.grid_propagate(False)
            tk.Label(
                name_group,
                text=name,
                font=self.fonts["body_bold"],
                fg=COLORS["text"],
                bg=COLORS["surface_alt"],
            ).pack(anchor="w")
            tk.Label(
                name_group,
                text=note,
                font=self.fonts["tiny"],
                fg=COLORS["muted"],
                bg=COLORS["surface_alt"],
            ).pack(anchor="w", pady=(2, 0))

            self._entry(row, self.path_vars[key], compact=True).grid(
                row=0, column=2, rowspan=2, sticky="ew", padx=(12, 8)
            )
            self._button(
                row,
                "Choose",
                lambda agent_key=key: self.browse_agent_path(agent_key),
                kind="ghost",
            ).grid(row=0, column=3, rowspan=2)

    def _build_action_bar(self, parent):
        actions = tk.Frame(parent, bg=COLORS["window"])
        actions.grid(row=3, column=0, sticky="ew", pady=(2, 14))

        self._button(
            actions,
            "Save settings",
            self.save_current_config,
            kind="ghost",
        ).pack(side=tk.LEFT)
        self._button(
            actions,
            "Preview changes",
            self.preview_changes,
            kind="secondary",
        ).pack(side=tk.RIGHT, padx=(8, 0))
        self.sync_button = self._button(
            actions,
            "Sync now",
            self.run_smart_sync,
            kind="primary",
            width=15,
        )
        self.sync_button.pack(side=tk.RIGHT)

    def _build_activity_card(self, parent):
        card = tk.Frame(
            parent,
            bg=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        card.grid(row=4, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        bar = tk.Frame(card, bg=COLORS["surface"], padx=16, pady=11)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_columnconfigure(0, weight=1)
        tk.Label(
            bar,
            text="Activity",
            font=self.fonts["body_bold"],
            fg=COLORS["text"],
            bg=COLORS["surface"],
        ).grid(row=0, column=0, sticky="w")
        self._button(bar, "Clear", self.clear_log, kind="ghost").grid(
            row=0, column=1, sticky="e"
        )

        log_wrap = tk.Frame(card, bg=COLORS["window"])
        log_wrap.grid(row=1, column=0, sticky="nsew", padx=1, pady=(0, 1))
        log_wrap.grid_columnconfigure(0, weight=1)
        log_wrap.grid_rowconfigure(0, weight=1)

        self.txt_log = tk.Text(
            log_wrap,
            font=self.fonts["log"],
            bg=COLORS["window"],
            fg=COLORS["muted"],
            insertbackground=COLORS["text"],
            selectbackground=COLORS["accent"],
            bd=0,
            padx=15,
            pady=12,
            wrap="word",
            state=tk.DISABLED,
        )
        self.txt_log.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(
            log_wrap,
            orient=tk.VERTICAL,
            command=self.txt_log.yview,
            bd=0,
            highlightthickness=0,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.txt_log.configure(yscrollcommand=scrollbar.set)
        self.txt_log.tag_configure("success", foreground=COLORS["success"])
        self.txt_log.tag_configure("warning", foreground=COLORS["warning"])
        self.txt_log.tag_configure("error", foreground=COLORS["danger"])
        self.txt_log.tag_configure("info", foreground=COLORS["info"])
        self.log("Ready. Review your folders, then preview or sync.", "info")

    def _field_label(self, parent, text):
        return tk.Label(
            parent,
            text=text,
            font=self.fonts["small_bold"],
            fg=COLORS["muted"],
            bg=COLORS["surface"],
            width=8,
            anchor="w",
        )

    def _entry(self, parent, textvariable, compact=False):
        return tk.Entry(
            parent,
            textvariable=textvariable,
            font=self.fonts["small"] if compact else self.fonts["body"],
            bg=COLORS["window"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            disabledbackground=COLORS["surface_alt"],
            disabledforeground=COLORS["subtle"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            relief=tk.FLAT,
            bd=0,
        )

    def _button(self, parent, text, command, kind="secondary", width=None):
        styles = {
            "primary": (
                COLORS["accent"],
                COLORS["text"],
                COLORS["accent_hover"],
            ),
            "secondary": (
                COLORS["surface_alt"],
                COLORS["text"],
                COLORS["border"],
            ),
            "ghost": (
                COLORS["surface"],
                COLORS["muted"],
                COLORS["surface_alt"],
            ),
        }
        bg, fg, active_bg = styles[kind]
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=self.fonts["small_bold"],
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=COLORS["text"],
            disabledforeground=COLORS["subtle"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=12,
            pady=7,
            width=width,
            cursor="hand2",
        )

    def set_git_status(self, text, color):
        self.status_dot.configure(fg=color)
        self.lbl_git_status.configure(text=text, fg=color)

    def log(self, message: str, level=""):
        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.insert(tk.END, message + "\n", level)
        self.txt_log.configure(state=tk.DISABLED)
        self.txt_log.see(tk.END)
        self.update_idletasks()

    def clear_log(self):
        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.configure(state=tk.DISABLED)

    def browse_library_path(self):
        selected = filedialog.askdirectory(title="Choose central skills library")
        if selected:
            self.library_path_var.set(selected)
            self.refresh_git_status()

    def browse_agent_path(self, agent_key: str):
        selected = filedialog.askdirectory(title=f"Choose {agent_key} skills folder")
        if selected:
            self.path_vars[agent_key].set(selected)

    def save_current_config(self, announce=True):
        self.config.library_path = self.library_path_var.get().strip()
        self.config.git_remote_url = self.git_remote_url_var.get().strip()
        self.config.selected_agents = [
            key for key, value in self.agent_vars.items() if value.get()
        ]
        for key, value in self.path_vars.items():
            self.config.agent_paths[key] = value.get().strip()
        self.config_mgr.save_config()
        if announce:
            self.log("Settings saved.", "success")

    def link_git_repo(self):
        library = self.library_path_var.get().strip()
        remote = self.git_remote_url_var.get().strip()
        if not library:
            messagebox.showwarning("Library required", "Choose a central library first.")
            return
        if not remote:
            messagebox.showwarning("Remote required", "Enter a Git remote URL first.")
            return

        self.save_current_config(announce=False)
        ok, message = self.git_engine.ensure_git_repo_linked(Path(library), remote)
        self.log(message, "success" if ok else "error")
        if not ok:
            messagebox.showerror("Git connection failed", message)
        self.refresh_git_status()

    def refresh_git_status(self):
        library = self.library_path_var.get().strip()
        if not library or not Path(library).is_dir():
            self.set_git_status("Library not set", COLORS["subtle"])
            return

        result = self.git_engine.get_git_status(Path(library))
        status_map = {
            "UP_TO_DATE": ("Up to date", COLORS["success"]),
            "AHEAD": (f"Local ahead · {result.ahead_count}", COLORS["info"]),
            "BEHIND": (f"Remote ahead · {result.behind_count}", COLORS["warning"]),
            "DIVERGED": ("Git conflict", COLORS["danger"]),
            "OFFLINE": ("Offline", COLORS["warning"]),
        }
        text, color = status_map.get(
            result.status,
            (result.error_message or result.status.replace("_", " ").title(), COLORS["subtle"]),
        )
        self.set_git_status(text, color)

    def preview_changes(self):
        library = self.library_path_var.get().strip()
        if not library or not Path(library).is_dir():
            messagebox.showwarning("Library required", "Choose a valid central library.")
            return

        self.save_current_config(announce=False)
        library_path = Path(library)
        self.log("Previewing local changes…", "info")

        rules_changed, rules_message = self.adapter_engine.sync_rules_upstream(
            library_path,
            self.config.agent_paths,
            self.config.selected_agents,
            dry_run=True,
        )
        result = self.sync_engine.scan_and_sync_upstream(
            library_path,
            self.config.agent_paths,
            self.config.selected_agents,
            self.config.ignore_patterns,
            dry_run=True,
        )

        if rules_changed:
            self.log(f"• {rules_message}")
        for file_name in result.files_synced_to_library:
            self.log(f"• {file_name}")
        if not rules_changed and not result.files_synced_to_library:
            self.log("No local agent changes found.", "success")
        else:
            count = len(result.files_synced_to_library) + int(rules_changed)
            self.log(f"{count} change(s) ready to sync.", "warning")
        self.refresh_git_status()

    def run_smart_sync(self):
        library = self.library_path_var.get().strip()
        remote = self.git_remote_url_var.get().strip()
        if not library:
            messagebox.showerror("Library required", "Choose a central library first.")
            return

        self.save_current_config(announce=False)
        library_path = Path(library)
        self.sync_button.configure(state=tk.DISABLED, text="Syncing…")
        self.log("Starting sync…", "info")

        try:
            if remote:
                ok, message = self.git_engine.ensure_git_repo_linked(
                    library_path, remote
                )
                self.log(message, "success" if ok else "warning")

            rules_changed, rules_message = self.adapter_engine.sync_rules_upstream(
                library_path,
                self.config.agent_paths,
                self.config.selected_agents,
            )
            if rules_changed:
                self.log(rules_message, "success")

            upstream = self.sync_engine.scan_and_sync_upstream(
                library_path,
                self.config.agent_paths,
                self.config.selected_agents,
                self.config.ignore_patterns,
            )
            if upstream.has_library_changes:
                self.log(
                    f"Collected {len(upstream.files_synced_to_library)} local change(s).",
                    "success",
                )

            git_status = self.git_engine.get_git_status(library_path)
            if git_status.status == "DIVERGED":
                self.log("Stopped: local and remote histories have diverged.", "error")
                messagebox.showwarning(
                    "Git conflict",
                    "Sync stopped to protect your data. Merge or rebase the repository, "
                    "then run sync again.",
                )
                return
            if git_status.status == "BEHIND":
                ok, message = self.git_engine.execute_smart_sync(
                    library_path, "AUTO_PULL"
                )
                self.log(message, "success" if ok else "error")
            elif (
                git_status.status == "AHEAD"
                or upstream.has_library_changes
                or rules_changed
            ):
                ok, message = self.git_engine.execute_smart_sync(
                    library_path, "AUTO_PUSH"
                )
                self.log(message, "success" if ok else "error")
            elif git_status.status == "OFFLINE":
                self.log("Git unavailable. Continuing with local deployment.", "warning")

            adapters = self.adapter_engine.deploy_adapters(
                library_path,
                self.config.agent_paths,
                self.config.selected_agents,
            )
            agents = self.sync_engine.deploy_skills_to_agents(
                library_path,
                self.config.agent_paths,
                self.config.selected_agents,
                self.config.ignore_patterns,
            )
            self.log(
                f"Deployed to {len(agents)} agent(s) and {len(adapters)} adapter target(s).",
                "success",
            )
            self.log("Sync complete.", "success")
        except Exception as exc:
            self.log(f"Sync failed: {exc}", "error")
            messagebox.showerror("Sync failed", str(exc))
        finally:
            self.sync_button.configure(state=tk.NORMAL, text="Sync now")
            self.refresh_git_status()
