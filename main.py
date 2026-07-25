#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

from src.config_manager import ConfigManager
from src.sync_engine import SyncEngine
from src.adapter_engine import AdapterEngine
from src.git_engine import GitEngine

def run_cli_mode():
    """Chạy Smart Sync ở chế độ dòng lệnh (CLI Mode / Silent Mode)."""
    print("⚡ [Skills Auto Sync Tool] Khởi động ở chế độ CLI...")
    config_mgr = ConfigManager()
    config = config_mgr.config

    lib_path_str = config.library_path or str(Path.cwd())
    lib_path = Path(lib_path_str)

    if not lib_path.exists():
        print(f"❌ Lỗi: Thư viện gốc '{lib_path}' không tồn tại. Vui lòng chạy GUI để cấu hình.")
        sys.exit(1)

    sync_engine = SyncEngine()
    adapter_engine = AdapterEngine()
    git_engine = GitEngine()

    print("[Step 1/3] Quét thay đổi Upstream từ các Agent active (loại trừ .system)...")
    up_res = sync_engine.scan_and_sync_upstream(
        lib_path, config.agent_paths, config.selected_agents, config.ignore_patterns
    )
    if up_res.has_library_changes:
        print(f"  ✓ Đã gom {len(up_res.files_synced_to_library)} file sửa đổi mới từ Agent về Library.")

    print("[Step 2/3] Đánh giá & Đồng bộ Git Remote...")
    git_res = git_engine.get_git_status(lib_path)
    if git_res.status == "BEHIND":
        ok, msg = git_engine.execute_smart_sync(lib_path, "AUTO_PULL")
        print(f"  {'✓' if ok else '❌'} {msg}")
    elif git_res.status == "AHEAD" or up_res.has_library_changes:
        ok, msg = git_engine.execute_smart_sync(lib_path, "AUTO_PUSH")
        print(f"  {'✓' if ok else '❌'} {msg}")
    elif git_res.status == "OFFLINE":
        print("  ⚠️ Offline Mode: Tiếp tục đồng bộ cục bộ.")
    else:
        print(f"  ✓ Status: {git_res.status}")

    print("[Step 3/3] Triển khai Adapters (AGENTS.md, CLAUDE.md) & Phân bổ Skills...")
    adapter_engine.deploy_adapters(lib_path, config.agent_paths, config.selected_agents)
    deployed = sync_engine.deploy_skills_to_agents(
        lib_path, config.agent_paths, config.selected_agents, config.ignore_patterns
    )
    print(f"  ✓ Đã cập nhật skills tới các agent: {', '.join(deployed)}")
    print("🎉 Smart Sync hoàn tất!")

def run_gui_mode():
    """Khởi chạy ứng dụng ở chế độ Giao diện Đồ họa Desktop GUI."""
    from src.ui.app_gui import AppGUI
    app = AppGUI()
    app.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Skills Auto Sync Tool - Đồng bộ Skill đa máy & đa Agent")
    parser.add_argument("--cli", action="store_true", help="Chạy ở chế độ dòng lệnh (CLI mode)")
    args = parser.parse_args()

    if args.cli:
        run_cli_mode()
    else:
        run_gui_mode()

if __name__ == "__main__":
    main()
