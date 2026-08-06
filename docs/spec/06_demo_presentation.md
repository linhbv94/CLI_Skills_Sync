# Demo & Presentation Specification: Skills Auto Sync Tool (`_spec6_demo_presentation`)

> **Version:** 2.1.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Product Manager, Stakeholders, End-Users, AI Video/Image Agents  

---

## 1. Kịch bản Trình diễn Demo Dòng lệnh (Live CLI Demo Playbook)

Kịch bản demo 3 phút chứng minh khả năng chạy đồng bộ nhanh thông qua giao diện dòng lệnh tương tác trên cả macOS và Windows, sử dụng cấu hình mới:

```text
⏱️ THỜI LƯỢNG DEMO: 3 PHÚT
🎯 MỤC TIÊU DEMO: Cho thấy sự tiện lợi khi tạo 1 skill mới trên MacBook, chạy CLI Sync và tự động đồng bộ sang Windows chỉ với phím bấm "1" dựa theo cấu hình agent active.
```

### Phân đoạn 1 (0:00 - 1:00): Bối cảnh & Khởi động Ứng dụng
1. Mở thư mục chứa file thực thi trên **MacBook**. Click đúp file nhị phân `skill_auto_sync` (Unix Executable hoặc Alias ngoài Desktop).
2. Hệ thống tự động mở Terminal, nạp cấu hình `config.json` cùng cấp và hiển thị menu lựa chọn:
   - Các thông số `skills_lib` và `git_repo` được hiển thị rõ ràng.
   - Trạng thái các Agent được hiển thị: `Antigravity: [ACTIVE]`, `Codex: [ACTIVE]`, `Claude: [PAUSED]`.
3. Giải thích rằng file cấu hình chỉ chứa toggles `0` hoặc `1` để app tự lấy đường dẫn mặc định trên macOS.

### Phân đoạn 2 (1:00 - 2:00): Sửa đổi Skill & Chạy Smart Sync (Option 1)
1. Tiến hành chỉnh sửa file `SKILL.md` tại thư mục Antigravity (`anti_lib`).
2. Trên màn hình Terminal đang mở, người dùng nhập `1` và nhấn Enter.
3. CLI hiển thị tiến độ chạy trong 2 giây:
   - Phát hiện thay đổi cục bộ ở Antigravity ➔ Gom về Thư viện tổng (`skills_lib`).
   - Tự động chạy git commit & push lên GitHub remote repository (`git_repo`).
   - Deploy ngược bản mới sang thư mục Codex (`codex_lib`).
   - Ghi nhận bỏ qua Claude do đang tắt trong config.
4. Người dùng mở Codex kiểm tra ➔ Skill đã tự động đồng bộ tức thì.

### Phân đoạn 3 (2:00 - 3:00): Đồng bộ về máy thứ hai (Windows)
1. Di chuyển sang máy **Windows**. Click đúp lối tắt Shortcut `skill_auto_sync` ngoài Desktop.
2. Giao diện CMD hiện lên. Người dùng nhập `1` ➔ Enter.
3. Engine thực hiện git fetch ➔ Phát hiện remote có commit mới (Behind) ➔ Tự động chạy `git pull --ff-only` ➔ Đồng bộ bản mới nhất xuống các thư mục active agent của máy Windows (`anti` và `codex`).
4. Đóng demo ➔ Hoàn tất quy trình đồng bộ nhanh gọn, không cần cấu hình UI phức tạp.

---

## 2. Dynamic Visual Presentation Prompts (Dành cho AI Image / Video Generation)

Khi cần tạo hình ảnh minh họa hoặc slide trình diễn công cụ:

### Prompt 1: Mockup Giao diện Dòng lệnh (CLI Terminal Presentation)
> **Prompt:** A high-end, premium presentation of a developer CLI tool. A dark mode Terminal window with vibrant green and cyan text on a translucent background showing "⚡ SKILLS AUTO SYNC TOOL" menu options with Antigravity and Codex active, and Claude paused. Next to the laptop displaying the Mac terminal is a Windows screen with a Command Prompt showing the same sync progress. Sleek modern workspace environment, soft ambient lighting, high contrast, clean typography, 8k resolution.

### Prompt 2: Quy trình Đồng bộ File Cục bộ (File Watcher Visualization)
> **Prompt:** Futuristic 3D abstract diagram showing files flowing bidirectionally. A glowing central drive labeled "Central Repository" connects to three terminal shells representing "Antigravity Agent", "Codex Agent" and "Claude Agent". Smooth glowing laser streams showing data sync. Dark background with subtle grid lines, cyan and orange accent colors, professional slide design.

---

## 3. Bản Tóm tắt Giá trị Sản phẩm (Product Pitch Summary)

* **Vấn đề (Problem):** Người dùng sử dụng nhiều máy tính và nhiều Agent khác nhau. Việc sao chép thủ công các file skill rất mất thời gian và dễ nhầm lẫn phiên bản.
* **Giải pháp (Solution):** **Skills Auto Sync Tool CLI** — Chỉ cần chạy 1 file thực thi duy nhất, nhấn phím `1` để đồng bộ toàn bộ (quét cục bộ các agent được bật, đồng bộ Git Remote, và phân bổ đè đúng định dạng quy chuẩn). Trạng thái các Agent được bật tắt đơn giản qua toggle `0`/`1` trong `config.json` cùng cấp.
