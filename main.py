import os
import sys
import time
import shutil
import argparse
from pathlib import Path

# Suppress macOS Tk deprecation warning (just in case)
os.environ["TK_SILENCE_DEPRECATION"] = "1"

from src.config_manager import ConfigManager
from src.sync_engine import SyncEngine
from src.adapter_engine import AdapterEngine
from src.git_engine import GitEngine

CURRENT_LANG = "en"

LOCALIZED = {
    "en": {
        "menu_title": "======================================================================\n⚡ SKILLS AUTO SYNC TOOL (v2.2.0) - CLI INTERACTIVE MENU\n======================================================================",
        "config_loaded": "[INFO] Config file loaded from: {}\n",
        "config_settings": "[CONFIG SETTINGS]",
        "skills_lib": "  └─ Central Library (skills_lib): {}",
        "git_repo": "  └─ Repository (git_repo):      {}",
        "active_agents": "[ACTIVE AGENTS]",
        "detected_changes": "[DETECTED CHANGES]",
        "no_changes": "[SYSTEM STATUS: NO CHANGES]",
        "agent_status_active": "[ACTIVE] ",
        "agent_status_disabled": "[DISABLED]",
        "agent_msg_skills_rules": "➔ Detected: {} new/modified skills, rules file changed.",
        "agent_msg_skills": "➔ Detected: {} new/modified skills.",
        "agent_msg_rules": "➔ Detected: rules file changed.",
        "agent_msg_uptodate": "➔ Up-to-date.",
        "agent_msg_error": "➔ Folder scanning error (Check paths/configuration).",
        "git_behind": "➔ There is/are {} new commit(s) on Remote (Behind).",
        "git_ahead_dirty": "➔ There is/are {} commit(s) to push & {} uncommitted file(s).",
        "git_ahead": "➔ There is/are {} local commit(s) to push (Ahead).",
        "git_dirty": "➔ Central Library has {} uncommitted file(s).",
        "git_diverged": "➔ Conflict (Diverged) - Both Local and Remote have new commits.",
        "git_offline": "➔ No internet connection (Offline Mode).",
        "git_auth_error": "➔ Authentication failed (Missing/Expired SSH Key or Token).",
        "git_not_found": "➔ Remote Repository not found (Incorrect link).",
        "git_uptodate": "➔ Up-to-date.",
        "git_error": "➔ Git error: {}",
        "select_option": "PLEASE SELECT AN OPTION (Type number and press Enter):",
        "option_sync": "  [1] Sync now (Smart Sync Now)",
        "option_refresh": "  [2] Refresh status",
        "option_cleanup": "  [3] Clean up environment",
        "option_exit": "  [4] Exit application",
        "your_choice": "Your choice (1/2/3/4): ",
        "invalid_choice": "\n❌ Invalid choice. Please enter a number between 1 and 4.",
        "exit_msg": "\nThank you for using the tool! Goodbye.",
        
        # Init config screen
        "init_config_title": "======================================================================\n⚡ SKILLS AUTO SYNC TOOL - INITIAL CONFIGURATION\n======================================================================",
        "init_config_created": "[INFO] Created a default config.json file in the same directory.",
        "init_config_path": "[INFO] Config file path: {}\n",
        "init_config_guide": "💡 Please open config.json with a Text Editor to configure:\n  - 'skills_lib': Absolute path to your Central Library.\n  - 'git_repo': Git remote repository link to sync.\n  - 'agents': Set 1 to enable, 0 to disable.",
        "press_enter_exit": "\nPress Enter to exit the application...",
        
        # Sync progress screen
        "sync_start": "\n>>> Starting Smart Sync (Local & Git)...",
        "sync_check_git": "\n[1/3] Checking Git Repository...",
        "sync_err_lib_empty": "❌ Error: Central Library (skills_lib) is empty/not configured.",
        "sync_git_local_only": "  ⚠️ Git Remote not configured. Running in Local Sync mode.",
        "sync_active_agents": "  Active Agents: {}",
        "sync_active_agents_none": "None",
        "sync_scan_upstream": "\n[2/3] Scanning Upstream changes from Agents to Central Library...",
        "sync_files_collected": "  ✓ Collected {} new/modified file(s) from Agent to Central Library:",
        "sync_no_files_collected": "  ✓ No new/modified files detected at Agent.",
        "sync_git_remote": "\n[3/3] Evaluating & Syncing Git Remote...",
        "sync_git_pulling": "  ➔ Remote has {} new commit(s). Pulling...",
        "sync_git_pushing": "  ➔ Local changes detected. Pushing to Git Remote...",
        "sync_git_offline": "  ⚠️ Offline Mode: Bypassing network sync, running locally.",
        "sync_deploy_downstream": "\n>>> Deploying Rules & Distributing Skills locally (Deploy downstream)...",
        "sync_deploy_rules_ok": "  ✓ Deployed AGENTS.md/CLAUDE.md successfully to active agents.",
        "sync_deploy_skills_ok": "  ✓ Copied Skills successfully to active agents: {}",
        "sync_completed": "\n🎉 === SMART SYNC COMPLETED SUCCESSFULLY ===",
        "press_enter_back": "\nPress Enter to return to the Menu...",
        
        # Conflict / Diverged Menu
        "conflict_title": "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n⚠️ DETECTED GIT REMOTE CONFLICT (DIVERGED)\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        "conflict_desc": "Both Local and Remote have new commits that need to be unified.",
        "conflict_ff_error": "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n⚠️ ERROR: CANNOT AUTO PULL FAST-FORWARD (Local changes exist)\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        "conflict_ff_desc": "Local history or untracked files (e.g. .DS_Store) are blocking auto pull.",
        "conflict_prompt": "Please select a resolution method:",
        "conflict_opt_merge": "  [m] Auto Merge & Pull (Recommended)",
        "conflict_opt_remote": "  [a] Accept Remote version (Reset & Pull - git reset --hard)",
        "conflict_opt_local": "  [b] Accept Local version (Push Force - git push --force-with-lease)",
        "conflict_opt_offline": "  [c] Bypass network sync for now, proceed with local downstream",
        "conflict_opt_cancel": "  [d] Cancel and return",
        "conflict_choice": "\nYour choice (m/a/b/c/d): ",
        "conflict_offline_sync": "  ➔ Bypassing network sync, running locally.",
        "conflict_cancelled": "  ➔ Synchronization cancelled.",
        
        # Cleanup
        "cleanup_title": "\n⚠️ WARNING: This process will WIPE:",
        "cleanup_warn1": "  1. All files and folders in Central Library (skills_lib) except for the .git and .gitignore directories.",
        "cleanup_warn2": "  2. AGENTS.md and the entire skills/ directory of active Agents (except Codex's .system folder).",
        "cleanup_warn3": "  This action CANNOT BE UNDONE.",
        "cleanup_confirm": "\nAre you sure you want to clean up all data? (y/N): ",
        "cleanup_cancelled": "➔ Cleanup cancelled.",
        "cleanup_start_lib": "\n[1/2] Cleaning up Central Library (skills_lib)...",
        "cleanup_deleted": "  ✓ Deleted: {}",
        "cleanup_sync_remote": "  ➔ Syncing and pushing cleanup state to Git Remote...",
        "cleanup_remote_ok": "  ✓ Successfully updated and wiped the repository on Git Remote.",
        "cleanup_remote_err": "  ⚠️ Git Warning: Force push to Remote failed: {}",
        "cleanup_lib_not_exists": "  ⚠️ Central Library directory does not exist.",
        "cleanup_lib_not_configured": "  ⚠️ skills_lib is not configured.",
        "cleanup_start_agents": "\n[2/2] Cleaning up active Agents...",
        "cleanup_agent_rules": "  ✓ Deleted rules of {}: {}",
        "cleanup_agent_skills": "  ✓ Deleted skills folder of {}",
        "cleanup_agent_skills_err": "  ❌ Error cleaning up skills of {}: {}",
        "cleanup_codex_system": "  ✓ Cleaned up skills of Codex (Preserved .system)",
        "cleanup_completed": "\n🎉 ENVIRONMENT CLEANED UP SUCCESSFULLY!"
    },
    "vi": {
        "menu_title": "======================================================================\n⚡ SKILLS AUTO SYNC TOOL (v2.2.0) - CLI INTERACTIVE MENU\n======================================================================",
        "config_loaded": "[INFO] File cấu hình nạp từ: {}\n",
        "config_settings": "[CONFIG SETTINGS]",
        "skills_lib": "  └─ Thư viện tổng (skills_lib): {}",
        "git_repo": "  └─ Repository (git_repo):      {}",
        "active_agents": "[ACTIVE AGENTS]",
        "detected_changes": "[PHÁT HIỆN THAY ĐỔI MỚI (DETECTED CHANGES)]",
        "no_changes": "[TRẠNG THÁI HỆ THỐNG: KHÔNG CÓ THAY ĐỔI (SYSTEM STATUS: NO CHANGES)]",
        "agent_status_active": "[ACTIVE] ",
        "agent_status_disabled": "[DISABLED]",
        "agent_msg_skills_rules": "➔ Phát hiện: {} skills mới/chỉnh sửa, file rules mới.",
        "agent_msg_skills": "➔ Phát hiện: {} skills mới/chỉnh sửa.",
        "agent_msg_rules": "➔ Phát hiện: file rules mới.",
        "agent_msg_uptodate": "➔ Đã đồng bộ mới nhất (Up-to-date).",
        "agent_msg_error": "➔ Lỗi quét thư mục (Hãy kiểm tra cấu hình).",
        "git_behind": "➔ Có {} commit mới trên Remote chưa kéo (Behind).",
        "git_ahead_dirty": "➔ Có {} commit chưa đẩy & {} tệp sửa đổi chưa commit.",
        "git_ahead": "➔ Có {} commit cục bộ mới chưa đẩy (Ahead).",
        "git_dirty": "➔ Thư viện có {} tệp sửa đổi chưa commit.",
        "git_diverged": "➔ Xung đột (Diverged) - Cả Local và Remote đều có commit mới.",
        "git_offline": "➔ Không có kết nối mạng (Offline Mode).",
        "git_auth_error": "➔ Lỗi xác thực (Chưa cấu hình SSH Key / Token).",
        "git_not_found": "➔ Không tìm thấy Repository trên Remote (Sai link).",
        "git_uptodate": "➔ Đã đồng bộ mới nhất (Up-to-date).",
        "git_error": "➔ Lỗi kiểm tra Git: {}",
        "select_option": "VUI LÒNG CHỌN CHỨC NĂNG (Nhập số tương ứng rồi nhấn Enter):",
        "option_sync": "  [1] Đồng bộ ngay (Smart Sync Now)",
        "option_refresh": "  [2] Làm mới trạng thái (Refresh status)",
        "option_cleanup": "  [3] Dọn dẹp môi trường (Clean up environment)",
        "option_exit": "  [4] Thoát ứng dụng",
        "your_choice": "Lựa chọn của bạn (1/2/3/4): ",
        "invalid_choice": "\n❌ Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 4.",
        "exit_msg": "\nCảm ơn bạn đã sử dụng công cụ! Tạm biệt.",
        
        # Init config screen
        "init_config_title": "======================================================================\n⚡ SKILLS AUTO SYNC TOOL - CẤU HÌNH BAN ĐẦU\n======================================================================",
        "init_config_created": "[INFO] Đã tạo file config.json mẫu cùng cấp với file chạy.",
        "init_config_path": "[INFO] Đường dẫn file cấu hình: {}\n",
        "init_config_guide": "💡 Vui lòng mở file config.json bằng Text Editor để điền thông số:\n  - 'skills_lib': Đường dẫn tuyệt đối đến Central Library của bạn.\n  - 'git_repo': Link Git remote repository để đồng bộ.\n  - 'agents': Thiết lập 1 cho agent muốn dùng, 0 để tắt.",
        "press_enter_exit": "\nNhấn Enter để thoát ứng dụng...",
        
        # Sync progress screen
        "sync_start": "\n>>> Bắt đầu tiến trình Smart Sync cục bộ & Git...",
        "sync_check_git": "\n[1/3] Kiểm tra Git Repository...",
        "sync_err_lib_empty": "❌ Lỗi: Thư viện tổng (skills_lib) trống.",
        "sync_git_local_only": "  ⚠️ Git Remote chưa cấu hình. Chạy chế độ chỉ đồng bộ cục bộ (Local Sync).",
        "sync_active_agents": "  Active Agents: {}",
        "sync_active_agents_none": "Không có",
        "sync_scan_upstream": "\n[2/3] Quét thay đổi Upstream từ Agent về Thư viện tổng...",
        "sync_files_collected": "  ✓ Đã gom {} file sửa đổi mới từ Agent về Thư viện tổng:",
        "sync_no_files_collected": "  ✓ Không phát hiện file sửa đổi mới ở Agent.",
        "sync_git_remote": "\n[3/3] Đánh giá & Đồng bộ Git Remote...",
        "sync_git_pulling": "  ➔ Phát hiện Remote có {} commit mới. Đang pull...",
        "sync_git_pushing": "  ➔ Phát hiện có thay đổi local mới. Đang push lên Git Remote...",
        "sync_git_offline": "  ⚠️ Offline Mode: Bỏ qua kết nối mạng, chạy đồng bộ cục bộ.",
        "sync_deploy_downstream": "\n>>> Triển khai Quy tắc & Phân bổ Skills cục bộ (Deploy downstream)...",
        "sync_deploy_rules_ok": "  ✓ Triển khai AGENTS.md/CLAUDE.md thành công tới các Agent.",
        "sync_deploy_skills_ok": "  ✓ Sao chép Skills thành công tới các Agent: {}",
        "sync_completed": "\n🎉 === SMART SYNC HOÀN TẤT THÀNH CÔNG ===",
        "press_enter_back": "\nNhấn Enter để quay lại Menu...",
        
        # Conflict / Diverged Menu
        "conflict_title": "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n⚠️ PHÁT HIỆN XUNG ĐỘT DỮ LIỆU GIT REMOTE (DIVERGED)\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        "conflict_desc": "Cả máy cục bộ và Git Remote đều có những commit mới chưa được đồng nhất.",
        "conflict_ff_error": "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n⚠️ LỖI: KHÔNG THỂ AUTO PULL FAST-FORWARD (Có thay đổi local chưa commit)\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        "conflict_ff_desc": "Lịch sử cục bộ hoặc file rác (như .DS_Store) đang chặn việc pull tự động.",
        "conflict_prompt": "Vui lòng lựa chọn phương án xử lý:",
        "conflict_opt_merge": "  [m] Tự động hợp nhất (Auto Merge & Pull - Khuyên dùng)",
        "conflict_opt_remote": "  [a] Chấp nhận bản trên Remote (Reset & Pull - git reset --hard)",
        "conflict_opt_local": "  [b] Chấp nhận bản cục bộ (Push Force - git push --force)",
        "conflict_opt_offline": "  [c] Bỏ qua lỗi đồng bộ mạng lần này, tiếp tục chạy Downstream cục bộ",
        "conflict_opt_cancel": "  [d] Quay lại (Hủy bỏ sync)",
        "conflict_choice": "\nLựa chọn của bạn (m/a/b/c/d): ",
        "conflict_offline_sync": "  ➔ Bỏ qua đồng bộ mạng, tiếp tục cục bộ.",
        "conflict_cancelled": "  ➔ Đã hủy bỏ tiến trình đồng bộ.",
        
        # Cleanup
        "cleanup_title": "\n⚠️ CẢNH BÁO: Tiến trình này sẽ XÓA SẠCH:",
        "cleanup_warn1": "  1. Tất cả file và folder trong Thư viện tổng (skills_lib) ngoại trừ thư mục quản lý .git và .gitignore.",
        "cleanup_warn2": "  2. File AGENTS.md và toàn bộ nội dung thư mục skills/ của các Agent active (ngoại trừ .system của Codex).",
        "cleanup_warn3": "  Hành động này KHÔNG THỂ HOÀN TÁC.",
        "cleanup_confirm": "\nBạn có chắc chắn muốn dọn dẹp toàn bộ dữ liệu? (y/N): ",
        "cleanup_cancelled": "➔ Đã hủy bỏ tiến trình dọn dẹp.",
        "cleanup_start_lib": "\n[1/2] Đang dọn dẹp Thư viện tổng (skills_lib)...",
        "cleanup_deleted": "  ✓ Đã xóa: {}",
        "cleanup_sync_remote": "  ➔ Đang đồng bộ và đẩy thay đổi dọn dẹp lên Git Remote...",
        "cleanup_remote_ok": "  ✓ Đã cập nhật và xóa sạch kho lưu trữ trên Git Remote.",
        "cleanup_remote_err": "  ⚠️ Cảnh báo Git: Không thể force push lên Remote: {}",
        "cleanup_lib_not_exists": "  ⚠️ Thư mục skills_lib không tồn tại.",
        "cleanup_lib_not_configured": "  ⚠️ skills_lib chưa cấu hình.",
        "cleanup_start_agents": "\n[2/2] Đang dọn dẹp các Agent active...",
        "cleanup_agent_rules": "  ✓ Đã xóa rules của {}: {}",
        "cleanup_agent_skills": "  ✓ Đã xóa folder skills của {}",
        "cleanup_agent_skills_err": "  ❌ Lỗi dọn dẹp skills của {}: {}",
        "cleanup_codex_system": "  ✓ Đã dọn dẹp skills của Codex (Đã giữ lại .system)",
        "cleanup_completed": "\n🎉 DỌN DẸP MÔI TRƯỜNG THÀNH CÔNG!"
    }
}

def t(key, *args):
    """Lấy chuỗi dịch tương ứng theo cấu hình ngôn ngữ."""
    text = LOCALIZED[CURRENT_LANG].get(key, LOCALIZED["en"].get(key, ""))
    if args:
        return text.format(*args)
    return text

def clear_screen():
    """Xóa màn hình console tùy theo HĐH."""
    os.system("cls" if os.name == "nt" else "clear")

def run_one_time_sync(config_mgr, sync_engine, adapter_engine, git_engine):
    """Thực thi Smart Sync đồng bộ 3 nguồn một lần."""
    config = config_mgr.config
    print(t("sync_start"))

    # 1. Liên kết và kiểm tra Git Repo
    print(t("sync_check_git"))
    if not config.skills_lib:
        print(t("sync_err_lib_empty"))
        return False

    has_git = False
    if config.git_repo:
        success, msg = git_engine.ensure_git_repo_linked(Path(config.skills_lib), config.git_repo, lang=CURRENT_LANG)
        print(f"  {'✓' if success else '❌'} {msg}")
        if not success:
            return False
        has_git = True
    else:
        print(t("sync_git_local_only"))

    # 2. Gom Agent Paths và danh sách Agent kích hoạt
    defaults = config_mgr.get_default_agent_paths()
    agent_paths = {
        "antigravity": defaults["anti"],
        "codex": defaults["codex"],
        "claude": defaults["claude"]
    }

    selected_agents = []
    if config.agents.get("anti") == 1:
        selected_agents.append("antigravity")
    if config.agents.get("codex") == 1:
        selected_agents.append("codex")
    if config.agents.get("claude") == 1:
        selected_agents.append("claude")

    agents_list_str = ', '.join(selected_agents) if selected_agents else t("sync_active_agents_none")
    print(t("sync_active_agents", agents_list_str))

    # 3. Quét thay đổi Upstream từ Agent -> Library
    print(t("sync_scan_upstream"))
    rules_synced, rules_msg = adapter_engine.sync_rules_upstream(
        Path(config.skills_lib), agent_paths, selected_agents, lang=CURRENT_LANG
    )
    if rules_synced:
        print(f"  ✓ {rules_msg}")

    up_res = sync_engine.scan_and_sync_upstream(
        Path(config.skills_lib), agent_paths, selected_agents, config.ignore_patterns
    )
    if up_res.has_library_changes:
        print(t("sync_files_collected", len(up_res.files_synced_to_library)))
        for f in up_res.files_synced_to_library:
            print(f"    - {f}")
    else:
        print(t("sync_no_files_collected"))

    # 4. Kiểm tra và đồng bộ Git Remote
    print(t("sync_git_remote"))
    if has_git:
        git_res = git_engine.get_git_status(Path(config.skills_lib), lang=CURRENT_LANG)
        is_offline = (git_res.status == "OFFLINE")

        if git_res.status == "DIVERGED":
            print(t("conflict_title"))
            print(t("conflict_desc"))
            print(t("conflict_prompt"))
            print(t("conflict_opt_merge"))
            print(t("conflict_opt_remote"))
            print(t("conflict_opt_local"))
            print(t("conflict_opt_offline"))
            print(t("conflict_opt_cancel"))
            
            choice = input(t("conflict_choice")).strip().lower()
            if choice == "m":
                ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_MERGE", lang=CURRENT_LANG)
                print(f"  ➔ {m}")
                if not ok:
                    return False
            elif choice == "a":
                ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PULL", lang=CURRENT_LANG)
                print(f"  ➔ {m}")
            elif choice == "b":
                ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PUSH", lang=CURRENT_LANG)
                print(f"  ➔ {m}")
            elif choice == "c":
                print(t("conflict_offline_sync"))
                is_offline = True
            else:
                print(t("conflict_cancelled"))
                return False

        elif git_res.status == "BEHIND":
            print(t("sync_git_pulling", git_res.behind_count))
            ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_PULL", lang=CURRENT_LANG)
            print(f"  ➔ {m}")
            if not ok:
                print(t("conflict_ff_error"))
                print(t("conflict_ff_desc"))
                print(t("conflict_prompt"))
                print(t("conflict_opt_merge"))
                print(t("conflict_opt_remote"))
                print(t("conflict_opt_local"))
                print(t("conflict_opt_offline"))
                print(t("conflict_opt_cancel"))
                
                choice = input(t("conflict_choice")).strip().lower()
                if choice == "m":
                    ok2, m2 = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_MERGE", lang=CURRENT_LANG)
                    print(f"  ➔ {m2}")
                    if not ok2:
                        return False
                elif choice == "a":
                    ok2, m2 = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PULL", lang=CURRENT_LANG)
                    print(f"  ➔ {m2}")
                    if not ok2:
                        return False
                elif choice == "b":
                    ok2, m2 = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PUSH", lang=CURRENT_LANG)
                    print(f"  ➔ {m2}")
                    if not ok2:
                        return False
                elif choice == "c":
                    print(t("conflict_offline_sync"))
                else:
                    print(t("conflict_cancelled"))
                    return False

        elif git_res.status == "AHEAD" or up_res.has_library_changes or rules_synced:
            print(t("sync_git_pushing"))
            ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_PUSH", lang=CURRENT_LANG)
            print(f"  ➔ {m}")

        elif git_res.status == "OFFLINE":
            print(t("sync_git_offline"))
        elif git_res.status == "AUTH_ERROR":
            print(f"  ⚠️ {git_res.error_message}")
            print(t("conflict_offline_sync"))
        elif git_res.status == "NOT_FOUND_ERROR":
            print(f"  ⚠️ {git_res.error_message}")
            print(t("conflict_offline_sync"))
        elif git_res.status == "NO_GIT":
            print(f"  ⚠️ {git_res.error_message}")
        else:
            print(f"  ✓ {git_res.error_message if git_res.error_message else t('git_uptodate')}")
    else:
        print(t("sync_git_local_only"))

    # 5. Triển khai Downstream (Library -> Agents)
    print(t("sync_deploy_downstream"))
    deployed_rules = adapter_engine.deploy_adapters(Path(config.skills_lib), agent_paths, selected_agents, lang=CURRENT_LANG)
    deployed_skills = sync_engine.deploy_skills_to_agents(
        Path(config.skills_lib), agent_paths, selected_agents, config.ignore_patterns
    )
    
    if deployed_rules:
        print(t("sync_deploy_rules_ok"))
    if deployed_skills:
        print(t("sync_deploy_skills_ok", ', '.join(deployed_skills)))
        
    print(t("sync_completed"))
    return True

def run_cleanup_environment(config_mgr, git_engine):
    """Xóa sạch tệp cấu hình quy tắc và nội dung kỹ năng ở thư viện tổng và các agent."""
    config = config_mgr.config
    print(t("cleanup_title"))
    print(t("cleanup_warn1"))
    print(t("cleanup_warn2"))
    print(t("cleanup_warn3"))
    
    confirm = input(t("cleanup_confirm")).strip().lower()
    if confirm != "y":
        print(t("cleanup_cancelled"))
        return

    print(t("cleanup_start_lib"))
    if config.skills_lib:
        lib_path = Path(config.skills_lib)
        if lib_path.exists():
            for item in lib_path.iterdir():
                if item.name in [".git", ".gitignore"]:
                    continue
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    print(t("cleanup_deleted", item.name))
                except Exception as e:
                    print(f"  ❌ Error: {e}")
            
            # Đồng bộ thay đổi này lên Git Remote!
            print(t("cleanup_sync_remote"))
            git_engine.run_cmd(["add", "-A"], cwd=lib_path)
            git_engine.run_cmd(["commit", "-m", "Clean up environment: remove all rules and skills"], cwd=lib_path)
            code, out, err = git_engine.run_cmd(["push", "--force", "origin", "main"], cwd=lib_path)
            if code == 0:
                print(t("cleanup_remote_ok"))
            else:
                print(t("cleanup_remote_err", err))
        else:
            print(t("cleanup_lib_not_exists"))
    else:
        print(t("cleanup_lib_not_configured"))

    print(t("cleanup_start_agents"))
    defaults = config_mgr.get_default_agent_paths()
    agent_paths = {
        "antigravity": defaults["anti"],
        "codex": defaults["codex"],
        "claude": defaults["claude"]
    }
    selected_agents = []
    if config.agents.get("anti") == 1:
        selected_agents.append("antigravity")
    if config.agents.get("codex") == 1:
        selected_agents.append("codex")
    if config.agents.get("claude") == 1:
        selected_agents.append("claude")

    for agent_name in selected_agents:
        agent_dir_str = agent_paths.get(agent_name, "")
        if not agent_dir_str:
            continue
        agent_dir = Path(agent_dir_str)
        if not agent_dir.exists():
            continue

        # Xóa file rules (AGENTS.md / CLAUDE.md)
        rules_name = "CLAUDE.md" if agent_name == "claude" else "AGENTS.md"
        rules_file = agent_dir / rules_name
        if rules_file.exists():
            try:
                rules_file.unlink()
                print(t("cleanup_agent_rules", agent_name, rules_name))
            except Exception as e:
                print(f"  ❌ Error: {e}")

        # Dọn dẹp folder skills
        skills_dir = agent_dir / "skills"
        if skills_dir.exists():
            try:
                if agent_name == "codex":
                    # Cô lập .system của Codex
                    for item in skills_dir.iterdir():
                        if item.name == ".system":
                            continue
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                    print(t("cleanup_codex_system"))
                else:
                    shutil.rmtree(skills_dir)
                    print(t("cleanup_agent_skills", agent_name))
            except Exception as e:
                print(t("cleanup_agent_skills_err", agent_name, e))

    print(t("cleanup_completed"))

def print_detected_changes(config, config_mgr, sync_engine, git_engine):
    """Quét nhanh và hiển thị trạng thái thay đổi mới tại Agent và Git Remote."""
    defaults = config_mgr.get_default_agent_paths()
    agent_paths = {
        "antigravity": defaults["anti"],
        "codex": defaults["codex"],
        "claude": defaults["claude"]
    }
    selected_agents = []
    if config.agents.get("anti") == 1:
        selected_agents.append("antigravity")
    if config.agents.get("codex") == 1:
        selected_agents.append("codex")
    if config.agents.get("claude") == 1:
        selected_agents.append("claude")
        
    upstream_msg = {}
    has_changes = False
    
    # Quét rules (AGENTS.md/CLAUDE.md)
    for agent_name in selected_agents:
        agent_dir = Path(agent_paths[agent_name])
        rule_changed = False
        mtime_lib = 0.0
        lib_rule = Path(config.skills_lib) / "AGENTS.md"
        if lib_rule.exists():
            mtime_lib = lib_rule.stat().st_mtime
            
        agent_rule_file = agent_dir / ("CLAUDE.md" if agent_name == "claude" else "AGENTS.md")
        if agent_rule_file.exists():
            if agent_rule_file.stat().st_mtime > mtime_lib:
                rule_changed = True
                
        # Quét skills
        try:
            up_res = sync_engine.scan_and_sync_upstream(
                Path(config.skills_lib),
                agent_paths,
                [agent_name],
                config.ignore_patterns,
                dry_run=True
            )
            count = len(up_res.files_synced_to_library)
            
            if count > 0 and rule_changed:
                upstream_msg[agent_name] = t("agent_msg_skills_rules", count)
                has_changes = True
            elif count > 0:
                upstream_msg[agent_name] = t("agent_msg_skills", count)
                has_changes = True
            elif rule_changed:
                upstream_msg[agent_name] = t("agent_msg_rules")
                has_changes = True
            else:
                upstream_msg[agent_name] = t("agent_msg_uptodate")
        except Exception:
            upstream_msg[agent_name] = t("agent_msg_error")

    git_msg = ""
    # Quét Git Remote
    if config.git_repo:
        try:
            git_res = git_engine.get_git_status(Path(config.skills_lib), lang=CURRENT_LANG)
            if git_res.status == "BEHIND":
                git_msg = t("git_behind", git_res.behind_count)
                has_changes = True
            elif git_res.status == "AHEAD":
                if git_res.ahead_count > 0:
                    dirty_count = len(git_res.dirty_files) if git_res.dirty_files else 0
                    if dirty_count > 0:
                        git_msg = t("git_ahead_dirty", git_res.ahead_count, dirty_count)
                    else:
                        git_msg = t("git_ahead", git_res.ahead_count)
                    has_changes = True
                else:
                    dirty_count = len(git_res.dirty_files) if git_res.dirty_files else 0
                    if dirty_count > 0:
                        git_msg = t("git_dirty", dirty_count)
                        has_changes = True
                    else:
                        git_msg = t("git_uptodate")
            elif git_res.status == "DIVERGED":
                git_msg = t("git_diverged")
                has_changes = True
            elif git_res.status == "OFFLINE":
                git_msg = t("git_offline")
            elif git_res.status == "AUTH_ERROR":
                git_msg = t("git_auth_error")
            elif git_res.status == "NOT_FOUND_ERROR":
                git_msg = t("git_not_found")
            elif git_res.status == "NO_GIT":
                git_msg = f"➔ {git_res.error_message}"
            else:
                git_msg = t("git_uptodate")
        except Exception as e:
            git_msg = t("git_error", str(e))
    else:
        git_msg = f"[DISABLED] ({t('git_repo', '')})"

    if has_changes:
        print(t("detected_changes"))
    else:
        print(t("no_changes"))

    for agent_name in ["anti", "codex", "claude"]:
        full_name = "antigravity" if agent_name == "anti" else ("codex" if agent_name == "codex" else "claude")
        if config.agents.get(agent_name) == 1:
            print(f"  ├─ Agent {full_name.capitalize()}: {upstream_msg.get(full_name, '')}")
        else:
            print(f"  ├─ Agent {full_name.capitalize()}: {t('agent_status_disabled')}")
            
    print(f"  └─ Git Remote:  {git_msg}")

def main():
    parser = argparse.ArgumentParser(description="Skills Auto Sync Tool CLI")
    parser.add_argument("--cli", action="store_true", help="Chạy chế độ dòng lệnh (Mặc định)")
    args = parser.parse_args()

    config_mgr = ConfigManager()
    config = config_mgr.config

    global CURRENT_LANG
    CURRENT_LANG = config.lang if hasattr(config, "lang") else "en"
    if CURRENT_LANG not in ["en", "vi"]:
        CURRENT_LANG = "en"

    # Kiểm tra cấu hình ban đầu
    if not config.skills_lib:
        clear_screen()
        print(t("init_config_title"))
        print(t("init_config_created"))
        print(t("init_config_path", config_mgr.config_file))
        print(t("init_config_guide"))
        print("======================================================================")
        input(t("press_enter_exit"))
        sys.exit(0)

    sync_engine = SyncEngine()
    adapter_engine = AdapterEngine()
    git_engine = GitEngine()

    while True:
        clear_screen()
        defaults = config_mgr.get_default_agent_paths()
        
        # In Giao diện chính ASCII
        print(t("menu_title"))
        print(t("config_loaded", config_mgr.config_file))
        print(t("config_settings"))
        print(t("skills_lib", config.skills_lib))
        print(t("git_repo", config.git_repo))
        print()
        
        print(t("active_agents"))
        anti_status = t("agent_status_active") if config.agents.get("anti") == 1 else t("agent_status_disabled")
        codex_status = t("agent_status_active") if config.agents.get("codex") == 1 else t("agent_status_disabled")
        claude_status = t("agent_status_active") if config.agents.get("claude") == 1 else t("agent_status_disabled")
        
        print(f"  ├─ Antigravity: {anti_status}  ➔ {defaults['anti']}")
        print(f"  ├─ Codex:       {codex_status}  ➔ {defaults['codex']}")
        print(f"  └─ Claude:      {claude_status}  ➔ {defaults['claude']}")
        print("======================================================================")
        
        # Hiển thị phát hiện thay đổi mới
        print_detected_changes(config, config_mgr, sync_engine, git_engine)
        print("======================================================================")
        
        print(t("select_option"))
        print(t("option_sync"))
        print(t("option_refresh"))
        print(t("option_cleanup"))
        print(t("option_exit"))
        print("======================================================================")
        
        choice = input(t("your_choice")).strip()
        if choice == "1":
            run_one_time_sync(config_mgr, sync_engine, adapter_engine, git_engine)
            input(t("press_enter_back"))
        elif choice == "2":
            # Làm mới trạng thái: chỉ cần loop tiếp để hiển thị lại thông tin mới nhất
            continue
        elif choice == "3":
            run_cleanup_environment(config_mgr, git_engine)
            input(t("press_enter_back"))
        elif choice == "4":
            print(t("exit_msg"))
            import platform
            system = platform.system()
            if system == "Darwin":
                import subprocess
                subprocess.Popen(["osascript", "-e", 'tell application "Terminal" to close front window'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif system == "Windows":
                try:
                    import ctypes
                    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
                    if hwnd != 0:
                        # Gửi message WM_CLOSE (0x0010) để tắt cửa sổ console
                        ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)
                except Exception:
                    pass
            sys.exit(0)
        else:
            print(t("invalid_choice"))
            time.sleep(1.5)

if __name__ == "__main__":
    main()
