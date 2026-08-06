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

def clear_screen():
    """Xóa màn hình console tùy theo HĐH."""
    os.system("cls" if os.name == "nt" else "clear")

def run_one_time_sync(config_mgr, sync_engine, adapter_engine, git_engine):
    """Thực thi Smart Sync đồng bộ 3 nguồn một lần."""
    config = config_mgr.config
    print("\n>>> Bắt đầu tiến trình Smart Sync cục bộ & Git...")

    # 1. Liên kết và kiểm tra Git Repo
    print("\n[1/3] Kiểm tra Git Repository...")
    if not config.skills_lib:
        print("❌ Lỗi: Thư viện tổng (skills_lib) trống.")
        return False

    has_git = False
    if config.git_repo:
        success, msg = git_engine.ensure_git_repo_linked(Path(config.skills_lib), config.git_repo)
        print(f"  {'✓' if success else '❌'} {msg}")
        if not success:
            return False
        has_git = True
    else:
        print("  ⚠️ Git Remote chưa cấu hình. Chạy chế độ chỉ đồng bộ cục bộ (Local Sync).")

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

    print(f"  Active Agents: {', '.join(selected_agents) if selected_agents else 'Không có'}")

    # 3. Quét thay đổi Upstream từ Agent -> Library
    print("\n[2/3] Quét thay đổi Upstream từ Agent về Thư viện tổng...")
    rules_synced, rules_msg = adapter_engine.sync_rules_upstream(
        Path(config.skills_lib), agent_paths, selected_agents
    )
    if rules_synced:
        print(f"  ✓ {rules_msg}")

    up_res = sync_engine.scan_and_sync_upstream(
        Path(config.skills_lib), agent_paths, selected_agents, config.ignore_patterns
    )
    if up_res.has_library_changes:
        print(f"  ✓ Đã gom {len(up_res.files_synced_to_library)} file sửa đổi mới từ Agent về Library:")
        for f in up_res.files_synced_to_library:
            print(f"    - {f}")
    else:
        print("  ✓ Không phát hiện file sửa đổi mới ở Agent.")

    # 4. Kiểm tra và đồng bộ Git Remote
    print("\n[3/3] Đánh giá & Đồng bộ Git Remote...")
    if has_git:
        git_res = git_engine.get_git_status(Path(config.skills_lib))
        is_offline = (git_res.status == "OFFLINE")

        if git_res.status == "DIVERGED":
            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("⚠️ PHÁT HIỆN XUNG ĐỘT DỮ LIỆU GIT REMOTE (DIVERGED)")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Cả máy cục bộ và Git Remote đều có những commit mới chưa được đồng nhất.")
            print("Vui lòng lựa chọn phương án xử lý:")
            print("  [m] Tự động hợp nhất (Auto Merge & Pull - Khuyên dùng)")
            print("  [a] Chấp nhận bản trên Remote (Reset & Pull - git reset --hard)")
            print("  [b] Chấp nhận bản cục bộ (Push Force - git push --force-with-lease)")
            print("  [c] Chế độ Offline (Offline Sync - chỉ đồng bộ cục bộ trên máy này)")
            print("  [d] Quay lại (Hủy bỏ sync)")
            
            choice = input("\nLựa chọn của bạn (m/a/b/c/d): ").strip().lower()
            if choice == "m":
                ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_MERGE")
                print(f"  ➔ {m}")
                if not ok:
                    return False
            elif choice == "a":
                ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PULL")
                print(f"  ➔ {m}")
            elif choice == "b":
                ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PUSH")
                print(f"  ➔ {m}")
            elif choice == "c":
                print("  ➔ Chuyển sang Offline Sync cục bộ.")
                is_offline = True
            else:
                print("  ➔ Đã hủy bỏ tiến trình đồng bộ.")
                return False

        elif git_res.status == "BEHIND":
            print(f"  ➔ Phát hiện Remote có {git_res.behind_count} commit mới. Đang pull...")
            ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_PULL")
            print(f"  ➔ {m}")
            if not ok:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("⚠️ LỖI: KHÔNG THỂ AUTO PULL FAST-FORWARD (Có thay đổi local chưa commit)")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Lịch sử cục bộ hoặc file rác (như .DS_Store) đang chặn việc pull tự động.")
                print("Vui lòng lựa chọn phương án xử lý:")
                print("  [m] Tự động hợp nhất (Auto Merge & Pull - Khuyên dùng)")
                print("  [a] Chấp nhận bản trên Remote (Reset & Pull - git reset --hard)")
                print("  [b] Chấp nhận bản cục bộ (Push Force - git push --force-with-lease)")
                print("  [c] Bỏ qua lỗi đồng bộ mạng lần này, tiếp tục chạy Downstream cục bộ")
                print("  [d] Quay lại (Hủy bỏ sync)")
                
                choice = input("\nLựa chọn của bạn (m/a/b/c/d): ").strip().lower()
                if choice == "m":
                    ok2, m2 = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_MERGE")
                    print(f"  ➔ {m2}")
                    if not ok2:
                        return False
                elif choice == "a":
                    ok2, m2 = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PULL")
                    print(f"  ➔ {m2}")
                    if not ok2:
                        return False
                elif choice == "b":
                    ok2, m2 = git_engine.execute_smart_sync(Path(config.skills_lib), "FORCE_PUSH")
                    print(f"  ➔ {m2}")
                    if not ok2:
                        return False
                elif choice == "c":
                    print("  ➔ Bỏ qua lỗi đồng bộ mạng, tiếp tục cục bộ.")
                else:
                    print("  ➔ Đã hủy bỏ tiến trình đồng bộ.")
                    return False

        elif git_res.status == "AHEAD" or up_res.has_library_changes or rules_synced:
            print("  ➔ Phát hiện có thay đổi local mới. Đang push lên Git Remote...")
            ok, m = git_engine.execute_smart_sync(Path(config.skills_lib), "AUTO_PUSH")
            print(f"  ➔ {m}")

        elif git_res.status == "OFFLINE":
            print("  ⚠️ Offline Mode: Bỏ qua kết nối mạng, chạy đồng bộ cục bộ.")
        elif git_res.status == "AUTH_ERROR":
            print(f"  ⚠️ {git_res.error_message}")
            print("  ➔ Bỏ qua Git Remote, tiếp tục đồng bộ cục bộ.")
        elif git_res.status == "NOT_FOUND_ERROR":
            print(f"  ⚠️ {git_res.error_message}")
            print("  ➔ Bỏ qua Git Remote (Vui lòng kiểm tra lại link git_repo trong config.json), tiếp tục đồng bộ cục bộ.")
        elif git_res.status == "NO_GIT":
            print(f"  ⚠️ {git_res.error_message}")
        else:
            print("  ✓ Trạng thái Git: Đã đồng bộ mới nhất (Up-to-date).")
    else:
        print("  ⚠️ Bỏ qua đồng bộ mạng (Git Remote chưa cấu hình).")

    # 5. Triển khai Downstream (Library -> Agents)
    print("\n>>> Triển khai Quy tắc & Phân bổ Skills cục bộ (Deploy downstream)...")
    deployed_rules = adapter_engine.deploy_adapters(Path(config.skills_lib), agent_paths, selected_agents)
    deployed_skills = sync_engine.deploy_skills_to_agents(
        Path(config.skills_lib), agent_paths, selected_agents, config.ignore_patterns
    )
    
    if deployed_rules:
        print(f"  ✓ Triển khai AGENTS.md/CLAUDE.md thành công tới các Agent.")
    if deployed_skills:
        print(f"  ✓ Sao chép Skills thành công tới các Agent: {', '.join(deployed_skills)}")
        
    print("\n🎉 === SMART SYNC HOÀN TẤT THÀNH CÔNG ===")
    return True

def get_monitored_state(config, selected_agents, agent_paths) -> dict:
    """Quét và lấy trạng thái file hiện tại (dung lượng & time sửa đổi) để phục vụ watcher."""
    state = {}
    
    # 1. Quét skills_lib/skills
    skills_lib_path = Path(config.skills_lib) / "skills"
    if skills_lib_path.exists():
        for root, dirs, files in os.walk(skills_lib_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    rel_path = file_path.relative_to(skills_lib_path)
                    if not SyncEngine.is_ignored(str(rel_path), config.ignore_patterns):
                        stat = file_path.stat()
                        state[f"lib:{rel_path.as_posix()}"] = (stat.st_size, stat.st_mtime)
                except Exception:
                    pass

    # 2. Quét các Agent active
    for agent_name in selected_agents:
        agent_dir_str = agent_paths.get(agent_name, "")
        if not agent_dir_str:
            continue
        agent_dir = Path(agent_dir_str)
        agent_skills_dir = agent_dir / "skills" if (agent_dir / "skills").exists() or agent_name == "claude" else agent_dir
        
        if agent_skills_dir.exists():
            for root, dirs, files in os.walk(agent_skills_dir):
                if ".system" in dirs:
                    dirs.remove(".system") # Loại bỏ folder hệ thống Codex
                for file in files:
                    file_path = Path(root) / file
                    try:
                        rel_path = file_path.relative_to(agent_skills_dir)
                        if not SyncEngine.is_ignored(str(rel_path), config.ignore_patterns):
                            stat = file_path.stat()
                            state[f"{agent_name}:{rel_path.as_posix()}"] = (stat.st_size, stat.st_mtime)
                    except Exception:
                        pass
    return state

def run_watcher_daemon(config_mgr, sync_engine, adapter_engine, git_engine):
    """Giám sát liên tục các thư mục (Polling mỗi 3s) và đồng bộ tự động."""
    config = config_mgr.config
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

    clear_screen()
    print("======================================================================")
    print("👁️ ĐANG KHỞI ĐỘNG CHẾ ĐỘ GIÁM SÁT CHẠY NỀN...")
    print("======================================================================")
    print("[INFO] Đang theo dõi các thay đổi file tại:")
    print(f"  - Thư viện tổng (skills_lib): {config.skills_lib}")
    for agent in selected_agents:
        print(f"  - Agent {agent}: {agent_paths[agent]}")
    print("\n[INFO] Hệ thống sẽ tự động đồng bộ khi phát hiện sự kiện thay đổi file.")
    print("[INFO] Nhấn [Ctrl + C] để dừng giám sát và quay lại Menu chính.")
    print("----------------------------------------------------------------------")

    # Lấy trạng thái ban đầu
    last_state = get_monitored_state(config, selected_agents, agent_paths)
    print(f"[{time.strftime('%H:%M:%S')}] Watcher Daemon đang chạy...")

    try:
        while True:
            time.sleep(3)
            current_state = get_monitored_state(config, selected_agents, agent_paths)
            
            # So sánh sự khác biệt
            if current_state != last_state:
                print(f"\n[{time.strftime('%H:%M:%S')}] [EVENT] Phát hiện thay đổi file hệ thống!")
                
                # Tìm xem thay đổi từ đâu
                for key in current_state:
                    if key not in last_state:
                        print(f"  ➔ File mới thêm: {key}")
                    elif current_state[key] != last_state[key]:
                        print(f"  ➔ File sửa đổi: {key}")
                for key in last_state:
                    if key not in current_state:
                        print(f"  ➔ File bị xóa: {key}")

                # Kích hoạt Smart Sync
                run_one_time_sync(config_mgr, sync_engine, adapter_engine, git_engine)
                print("----------------------------------------------------------------------")
                print(f"[{time.strftime('%H:%M:%S')}] Giám sát đang chạy...")
                
                # Cập nhật state mới nhất
                last_state = get_monitored_state(config, selected_agents, agent_paths)
    except KeyboardInterrupt:
        print("\n\n[INFO] Đã dừng giám sát Daemon. Trở lại Menu chính...")
        time.sleep(1)

def run_cleanup_environment(config_mgr, git_engine):
    """Xóa sạch tệp cấu hình quy tắc và nội dung kỹ năng ở thư viện tổng và các agent."""
    config = config_mgr.config
    print("\n⚠️ CẢNH BÁO: Tiến trình này sẽ XÓA SẠCH:")
    print("  1. Tất cả file và folder trong Thư viện tổng (skills_lib) ngoại trừ thư mục quản lý .git.")
    print("  2. File AGENTS.md và toàn bộ nội dung thư mục skills/ của các Agent active (ngoại trừ .system của Codex).")
    print("  Hành động này KHÔNG THỂ HOÀN TÁC.")
    
    confirm = input("\nBạn có chắc chắn muốn dọn dẹp toàn bộ dữ liệu? (y/N): ").strip().lower()
    if confirm != "y":
        print("➔ Đã hủy bỏ tiến trình dọn dẹp.")
        return

    print("\n[1/2] Đang dọn dẹp Thư viện tổng (skills_lib)...")
    if config.skills_lib:
        lib_path = Path(config.skills_lib)
        if lib_path.exists():
            for item in lib_path.iterdir():
                if item.name == ".git":
                    continue
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    print(f"  ✓ Đã xóa: {item.name}")
                except Exception as e:
                    print(f"  ❌ Lỗi xóa {item.name}: {e}")
            
            # Đồng bộ thay đổi này lên Git Remote!
            print("  ➔ Đang đồng bộ và đẩy thay đổi dọn dẹp lên Git Remote...")
            git_engine.run_cmd(["add", "-A"], cwd=lib_path)
            git_engine.run_cmd(["commit", "-m", "Clean up environment: remove all rules and skills"], cwd=lib_path)
            code, out, err = git_engine.run_cmd(["push", "--force", "origin", "main"], cwd=lib_path)
            if code == 0:
                print("  ✓ Đã cập nhật và xóa sạch kho lưu trữ trên Git Remote.")
            else:
                print(f"  ⚠️ Cảnh báo Git: Không thể force push lên Remote: {err}")
        else:
            print("  ⚠️ Thư mục skills_lib không tồn tại.")
    else:
        print("  ⚠️ skills_lib chưa cấu hình.")

    print("\n[2/2] Đang dọn dẹp các Agent active...")
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
                print(f"  ✓ Đã xóa rules của {agent_name}: {rules_name}")
            except Exception as e:
                print(f"  ❌ Lỗi xóa rules của {agent_name}: {e}")

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
                    print(f"  ✓ Đã dọn dẹp skills của Codex (Đã giữ lại .system)")
                else:
                    shutil.rmtree(skills_dir)
                    print(f"  ✓ Đã xóa folder skills của {agent_name}")
            except Exception as e:
                print(f"  ❌ Lỗi dọn dẹp skills của {agent_name}: {e}")

    print("\n🎉 DỌN DẸP MÔI TRƯỜNG THÀNH CÔNG!")

def print_detected_changes(config, config_mgr, sync_engine, git_engine):
    """Quét nhanh và hiển thị trạng thái thay đổi mới tại Agent và Git Remote."""
    print("[PHÁT HIỆN THAY ĐỔI MỚI (DETECTED CHANGES)]")
    
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
            msg_parts = []
            if count > 0:
                msg_parts.append(f"{count} skills mới/chỉnh sửa")
            if rule_changed:
                msg_parts.append("file rules mới")
                
            if msg_parts:
                upstream_msg[agent_name] = f"➔ Phát hiện: {', '.join(msg_parts)}."
            else:
                upstream_msg[agent_name] = "➔ Đã đồng bộ mới nhất (Up-to-date)."
        except Exception:
            upstream_msg[agent_name] = "➔ Lỗi quét thư mục (Hãy kiểm tra cấu hình)."

    for agent_name in ["anti", "codex", "claude"]:
        full_name = "antigravity" if agent_name == "anti" else ("codex" if agent_name == "codex" else "claude")
        if config.agents.get(agent_name) == 1:
            print(f"  ├─ Agent {full_name.capitalize()}: {upstream_msg.get(full_name, '➔ Bỏ qua.')}")
        else:
            print(f"  ├─ Agent {full_name.capitalize()}: [DISABLED]")

    # Quét Git Remote
    if config.git_repo:
        try:
            git_res = git_engine.get_git_status(Path(config.skills_lib))
            if git_res.status == "BEHIND":
                print(f"  └─ Git Remote: ➔ Có {git_res.behind_count} commit mới trên Remote chưa kéo (Behind).")
            elif git_res.status == "AHEAD":
                print(f"  └─ Git Remote: ➔ Có {git_res.ahead_count} commit cục bộ mới chưa đẩy (Ahead).")
            elif git_res.status == "DIVERGED":
                print(f"  └─ Git Remote: ➔ Xung đột (Diverged) - Cả Local và Remote đều có commit mới.")
            elif git_res.status == "OFFLINE":
                print(f"  └─ Git Remote: ➔ Không có kết nối mạng (Offline Mode).")
            elif git_res.status == "AUTH_ERROR":
                print(f"  └─ Git Remote: ➔ Lỗi xác thực (Chưa cấu hình SSH Key / Token).")
            elif git_res.status == "NOT_FOUND_ERROR":
                print(f"  └─ Git Remote: ➔ Không tìm thấy Repository trên Remote (Sai link).")
            elif git_res.status == "NO_GIT":
                print(f"  └─ Git Remote: ➔ {git_res.error_message}")
            else:
                print(f"  └─ Git Remote: ➔ Đã đồng bộ mới nhất (Up-to-date).")
        except Exception as e:
            print(f"  └─ Git Remote: ➔ Lỗi kiểm tra Git: {str(e)}")
    else:
        print("  └─ Git Remote: [DISABLED] (Git Remote chưa cấu hình)")

def main():
    parser = argparse.ArgumentParser(description="Skills Auto Sync Tool CLI")
    parser.add_argument("--cli", action="store_true", help="Chạy chế độ dòng lệnh (Mặc định)")
    args = parser.parse_args()

    config_mgr = ConfigManager()
    config = config_mgr.config

    # Kiểm tra cấu hình ban đầu
    if not config.skills_lib:
        clear_screen()
        print("======================================================================")
        print("⚡ SKILLS AUTO SYNC TOOL - CẤU HÌNH BAN ĐẦU")
        print("======================================================================")
        print(f"[INFO] Đã tạo file config.json mẫu cùng cấp với file chạy.")
        print(f"[INFO] Đường dẫn file cấu hình: {config_mgr.config_file}\n")
        print("💡 Vui lòng mở file config.json bằng Text Editor để điền thông số:")
        print("  - 'skills_lib': Đường dẫn tuyệt đối đến Central Library của bạn.")
        print("  - 'git_repo': Link Git remote repository để đồng bộ.")
        print("  - 'agents': Thiết lập 1 cho agent muốn dùng, 0 để tắt.")
        print("======================================================================")
        input("\nNhấn Enter để thoát ứng dụng...")
        sys.exit(0)

    sync_engine = SyncEngine()
    adapter_engine = AdapterEngine()
    git_engine = GitEngine()

    while True:
        clear_screen()
        defaults = config_mgr.get_default_agent_paths()
        
        # In Giao diện chính ASCII
        print("======================================================================")
        print("⚡ SKILLS AUTO SYNC TOOL (v2.1.0) - CLI INTERACTIVE MENU")
        print("======================================================================")
        print(f"[INFO] File cấu hình nạp từ: {config_mgr.config_file}\n")
        print("[CONFIG SETTINGS]")
        print(f"  └─ Thư viện tổng (skills_lib): {config.skills_lib}")
        print(f"  └─ Repository (git_repo):      {config.git_repo}\n")
        
        print("[ACTIVE AGENTS]")
        anti_status = "[ACTIVE] " if config.agents.get("anti") == 1 else "[DISABLED]"
        codex_status = "[ACTIVE] " if config.agents.get("codex") == 1 else "[DISABLED]"
        claude_status = "[ACTIVE] " if config.agents.get("claude") == 1 else "[DISABLED]"
        
        print(f"  ├─ Antigravity: {anti_status}  ➔ {defaults['anti']}")
        print(f"  ├─ Codex:       {codex_status}  ➔ {defaults['codex']}")
        print(f"  └─ Claude:      {claude_status}  ➔ {defaults['claude']}")
        print("======================================================================")
        
        # Hiển thị phát hiện thay đổi mới
        print_detected_changes(config, config_mgr, sync_engine, git_engine)
        print("======================================================================")
        
        print("VUI LÒNG CHỌN CHỨC NĂNG (Nhập số tương ứng rồi nhấn Enter):")
        print("  [1] Đồng bộ ngay (Smart Sync Now)")
        print("  [2] Giám sát chạy nền (Auto-Sync Watcher Daemon)")
        print("  [3] Dọn dẹp môi trường (Clean up environment)")
        print("  [4] Thoát ứng dụng")
        print("======================================================================")
        
        choice = input("Lựa chọn của bạn (1/2/3/4): ").strip()
        if choice == "1":
            run_one_time_sync(config_mgr, sync_engine, adapter_engine, git_engine)
            input("\nNhấn Enter để quay lại Menu...")
        elif choice == "2":
            run_watcher_daemon(config_mgr, sync_engine, adapter_engine, git_engine)
        elif choice == "3":
            run_cleanup_environment(config_mgr, git_engine)
            input("\nNhấn Enter để quay lại Menu...")
        elif choice == "4":
            print("\nCảm ơn bạn đã sử dụng công cụ! Tạm biệt.")
            sys.exit(0)
        else:
            print("\n❌ Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 4.")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
