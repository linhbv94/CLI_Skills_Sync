# CLI & Wireframe Specification: Skills Auto Sync Tool (`_spec3_ui_wireframe`)

> **Version:** 2.2.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Developers, Dev Agents, QA Engineers  

---

## 1. Giao diện Menu chính trên Terminal (Main CLI Menu Wireframe)

Khi người dùng khởi chạy ứng dụng (click chạy trực tiếp hoặc thông qua Lối tắt/Alias), giao diện CLI Terminal hiển thị trạng thái các Agent dựa trên giá trị cấu hình `0` hoặc `1` trong `config.json` cùng cấp:

```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL (v2.2.0) - CLI INTERACTIVE MENU
======================================================================
[INFO] File cấu hình nạp từ: /Users/vic/2_Skills/config.json

[CONFIG SETTINGS]
  └─ Thư viện tổng (skills_lib): /Users/vic/2_Skills
  └─ Repository (git_repo):      https://github.com/linhbv94/Skills_Library

[ACTIVE AGENTS]
  ├─ Antigravity: [ACTIVE]  ➔ /Users/vic/.gemini/config
  ├─ Codex:       [ACTIVE]  ➔ /Users/vic/.codex
  └─ Claude:      [DISABLED] ➔ /Users/vic/.claude

======================================================================
VUI LÒNG CHỌN CHỨC NĂNG (Nhập số tương ứng rồi nhấn Enter):

  [1] Đồng bộ ngay (Smart Sync Now)
  [2] Giám sát chạy nền (Auto-Sync Watcher Daemon)
  [3] Dọn dẹp môi trường (Clean up environment)
  [4] Thoát ứng dụng

Lựa chọn của bạn (1/2/3/4): _
```

---

## 2. Giao diện khi chọn Chức năng 1 (Smart Sync Now Output Wireframe)

Sau khi nhập `1` và nhấn Enter, các Agent có trạng thái `[ACTIVE]` sẽ tham gia đồng bộ:

```text
>>> Bắt đầu tiến trình Smart Sync cục bộ & Git...

[1/3] Kiểm tra Git Repository...
  ✓ Git Repo đã được liên kết chính xác.
  Active Agents: antigravity, codex

[2/3] Quét thay đổi Upstream từ Agent về Thư viện tổng...
  ✓ Đã gom 1 file sửa đổi mới từ Agent về Library:
    - antigravity: general_logic/SKILL.md

[3/3] Đánh giá & Đồng bộ Git Remote...
  ➔ Phát hiện có thay đổi local mới. Đang push lên Git Remote...
  ➔ Đã push dữ liệu mới lên Git Remote thành công.

>>> Triển khai Quy tắc & Phân bổ Skills cục bộ (Deploy downstream)...
  ✓ Triển khai AGENTS.md/CLAUDE.md thành công tới các Agent.
  ✓ Sao chép Skills thành công tới các Agent: antigravity, codex

🎉 === SMART SYNC HOÀN TẤT THÀNH CÔNG ===

Nhấn Enter để quay lại Menu...
```

---

## 3. Giao diện khi chọn Chức năng 2 (Auto-Sync Watcher Daemon Wireframe)

Khi chọn `2`, Watcher Daemon chỉ giám sát các thư mục của Agent đang kích hoạt (`ACTIVE`):

```text
======================================================================
👁️ ĐANG KHỞI ĐỘNG CHẾ ĐỘ GIÁM SÁT CHẠY NỀN...
======================================================================
[INFO] Đang theo dõi các thay đổi file tại:
  - /Users/vic/2_Skills (Thư viện tổng)
  - /Users/vic/.gemini/config (Antigravity)
  - /Users/vic/.codex (Codex)
  * Chu kỳ quét: 3 giây/lần. Nhấn [Ctrl + C] để thoát chế độ giám sát.
======================================================================
[13:05:00] Giám sát đang chạy...
[13:05:12] Phát hiện có thay đổi file:
  ➔ File sửa đổi: /Users/vic/.codex/skills/python_dev/SKILL.md
>>> Bắt đầu tự động Smart Sync...
  ...
  ✓ Auto-Sync hoàn tất!
[13:05:15] Giám sát đang chạy...
```

---

## 4. Giao diện khi chọn Chức năng 3 (Clean up environment Wireframe)

Khi chọn `3`, màn hình hiển thị cảnh báo đỏ và yêu cầu xác nhận trước khi tiến hành dọn dẹp xóa sạch môi trường:

```text
⚠️ CẢNH BÁO: Tiến trình này sẽ XÓA SẠCH:
  1. Tất cả file và folder trong Thư viện tổng (skills_lib) ngoại trừ thư mục quản lý .git.
  2. File AGENTS.md và toàn bộ nội dung thư mục skills/ của các Agent active (ngoại trừ .system của Codex).
  Hành động này KHÔNG THỂ HOÀN TÁC.

Bạn có chắc chắn muốn dọn dẹp toàn bộ dữ liệu? (y/N): y

[1/2] Đang dọn dẹp Thư viện tổng (skills_lib)...
  ✓ Đã xóa: AGENTS.md
  ✓ Đã xóa: skills

[2/2] Đang dọn dẹp các Agent active...
  ✓ Đã xóa rules của antigravity: AGENTS.md
  ✓ Đã xóa folder skills của antigravity
  ✓ Đã xóa rules của codex: AGENTS.md
  ✓ Đã dọn dẹp skills của Codex (Đã giữ lại .system)

🎉 DỌN DẸP MÔI TRƯỜNG THÀNH CÔNG!

Nhấn Enter để quay lại Menu chính...
```

---

## 5. Giao diện Xử lý Xung đột Git Diverged (Git Conflict Resolution Wireframe)

Khi trạng thái Git là `DIVERGED` (Cả Local và Remote đều có commit mới khác nhau), hệ thống dừng luồng Smart Sync tự động và hiển thị Menu xử lý:

```text
⚠️ PHÁT HIỆN XUNG ĐỘT GIT REMOTE (Commits khác nhau trên Local & Remote)
======================================================================
Vui lòng lựa chọn phương án xử lý xung đột:
  [a] Lấy bản của Remote (Ghi đè Local bằng Remote Commits)
  [b] Đẩy đè bản Local lên (Ghi đè Remote bằng Local Commits)
  [c] Hủy bỏ tiến trình Smart Sync (Không thay đổi gì)
======================================================================
Lựa chọn của bạn (a/b/c): _
```
