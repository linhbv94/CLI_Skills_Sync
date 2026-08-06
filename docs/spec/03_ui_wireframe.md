# CLI & Wireframe Specification: Skills Auto Sync Tool (`_spec3_ui_wireframe`)

> **Version:** 2.3.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Developers, Dev Agents, QA Engineers  

---

## 1. Giao diện Cấu hình Ban đầu (Onboarding Wireframe)

Khi khởi chạy ứng dụng lần đầu tiên (hoặc file `config.json` chưa tồn tại trong thư mục hệ thống AppData / Application Support):

### A. Màn hình chọn Ngôn ngữ (Language Selection)
```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL - ONBOARDING SETUP
======================================================================
Please select your language / Vui lòng chọn ngôn ngữ hiển thị:

  [1] English
  [2] Tiếng Việt

Your choice / Lựa chọn của bạn (1/2): 2_
```

### B. Màn hình chọn AI Agents (Agents Selection Setup)
```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL - CẤU HÌNH BAN ĐẦU (Tiếng Việt)
======================================================================
💡 Vui lòng thiết lập kích hoạt (1) hoặc vô hiệu hóa (0) cho các AI Agent.
Thứ tự nhập tương ứng: Antigravity, Codex, Claude Code.
Ví dụ: 1,1,0 để bật Antigravity & Codex, tắt Claude.

Nhập cấu hình Agents (ví dụ: 1,1,0): 1,1,0_
```

### C. Màn hình nhập Thư viện tổng (Central Library Path)
```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL - CẤU HÌNH BAN ĐẦU (Tiếng Việt)
======================================================================
[INFO] File cấu hình đang được tạo tại: /path/to/Application Support/Skills_Sync/config.json

💡 Vui lòng nhập đường dẫn tuyệt đối đến Thư viện tổng của bạn (skills_lib).
Đây là thư mục trung tâm để đồng bộ kỹ năng và quy tắc.

Nhập đường dẫn (ví dụ: /path/to/skills_lib): /path/to/skills_lib_
```

### D. Màn hình nhập Git Repository (Git Remote URL Setup)
```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL - CẤU HÌNH BAN ĐẦU (Tiếng Việt)
======================================================================
💡 Vui lòng dán link Git Remote Repository (HTTPS/SSH) để đồng bộ đám mây.
(Nếu bạn muốn chạy chế độ Offline cục bộ không dùng Git, chỉ cần nhấn Enter để bỏ qua).

Nhập link repo (Nhấn Enter để bỏ qua): https://github.com/dummy/skills_library_
```

---

## 2. Giao diện Menu chính trên Terminal (Main CLI Menu Wireframe)

Sau khi onboarding hoàn tất hoặc khi mở app những lần sau:

### A. Phiên bản Tiếng Việt (`lang = vi`)
```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL (v2.3.0) - CLI INTERACTIVE MENU
======================================================================
[INFO] File cấu hình nạp từ: /path/to/Application Support/Skills_Sync/config.json

[CONFIG SETTINGS]
  └─ Thư viện tổng (skills_lib): /path/to/skills_lib
  └─ Repository (git_repo):      https://github.com/dummy/skills_library

[ACTIVE AGENTS]
  ├─ Antigravity: [ACTIVE]  ➔ /path/to/active_agents/.gemini/config
  ├─ Codex:       [ACTIVE]  ➔ /path/to/active_agents/.codex
  └─ Claude:      [DISABLED] ➔ /path/to/active_agents/.claude

======================================================================
[TRẠNG THÁI HỆ THỐNG: KHÔNG CÓ THAY ĐỔI (SYSTEM STATUS: NO CHANGES)]
  ├─ Agent Antigravity: ➔ Đã đồng bộ mới nhất (Up-to-date).
  ├─ Agent Codex:       ➔ Đã đồng bộ mới nhất (Up-to-date).
  ├─ Agent Claude:      [DISABLED]
  └─ Git Remote:        ➔ Đã đồng bộ mới nhất (Up-to-date).
======================================================================
VUI LÒNG CHỌN CHỨC NĂNG (Nhập số tương ứng rồi nhấn Enter):

  [1] Đồng bộ ngay (Smart Sync Now)
  [2] Làm mới trạng thái (Refresh status)
  [3] Dọn dẹp môi trường (Clean up environment)
  [4] Sửa cấu hình (Edit configuration)
  [5] Mở thư mục cấu hình (Open config folder)
  [6] Thoát ứng dụng

Lựa chọn của bạn (1/2/3/4/5/6): _
```

---

## 3. Giao diện Sửa cấu hình (Submenu: Edit configuration Wireframe)

Khi người dùng nhập `4` từ Menu chính:

### Phiên bản Tiếng Việt
```text
======================================================================
⚡ SKILLS AUTO SYNC TOOL - CHỈNH SỬA CẤU HÌNH (EDIT CONFIG)
======================================================================
Vui lòng lựa chọn thông số cần thay đổi:

  [1] Sửa đường dẫn Thư viện tổng (skills_lib)
  [2] Sửa link Git Remote Repository (git_repo)
  [3] Sửa cấu hình kích hoạt AI Agents
  [4] Sửa ngôn ngữ hiển thị (lang)
  [5] Trở về Menu chính

Lựa chọn của bạn (1/2/3/4/5): 3_
```

#### Khi chọn 1 (Sửa Library Path) kèm hủy bỏ:
```text
💡 Vui lòng nhập đường dẫn tuyệt đối đến Thư viện tổng của bạn (skills_lib).
(Nhập 'q' để hủy bỏ và quay lại mà không lưu).

Nhập đường dẫn (ví dụ: /path/to/skills_lib): q_
```

#### Khi chọn 2 (Sửa Git Repo) kèm hủy bỏ:
```text
💡 Nhập link Git Remote Repository mới của bạn.
(Nhấn Enter để trống ➔ Đồng bộ cục bộ Offline, hoặc nhập 'q' để hủy bỏ).

Nhập link mới (Enter để xóa): q_
```

#### Khi chọn 3 (Sửa Agents) kèm hủy bỏ:
```text
💡 Thiết lập kích hoạt (1) hoặc vô hiệu hóa (0) cho các AI Agent (Antigravity, Codex, Claude Code).
Ví dụ nhập: 1,1,0 (Nhập 'q' để hủy bỏ).

Nhập cấu hình Agents mới (ví dụ: 1,1,0): q_
```

#### Khi chọn 4 (Sửa Language) kèm hủy bỏ:
```text
💡 Chọn ngôn ngữ hiển thị mới.
(Nhập 'q' để hủy bỏ).

Chọn ngôn ngữ hiển thị mới (1 cho en, 2 cho vi): q_
```

---

## 4. Giao diện Mở thư mục cấu hình (Open config folder Wireframe)

Khi người dùng nhập `5` từ Menu chính, CLI chạy subprocess mở thư mục Finder / Explorer:

```text
➔ Đang mở thư mục hệ thống chứa file config.json...
  Đường dẫn: /path/to/Application Support/Skills_Sync

✓ Đã mở thư mục thành công. Quay lại Menu chính sau 2 giây...
```

---

## 5. Giao diện Xử lý Xung đột Git Diverged (Git Conflict Resolution Wireframe)

Khi trạng thái Git là `DIVERGED` (Cả Local và Remote đều có commit mới khác nhau), hệ thống dừng luồng Smart Sync tự động và hiển thị Menu xử lý:

```text
⚠️ PHÁT HIỆN XUNG ĐỘT GIT REMOTE (Commits khác nhau trên Local & Remote)
======================================================================
Vui lòng lựa chọn phương án xử lý xung đột:
  [m] Tự động hợp nhất (Auto Merge & Pull - Khuyên dùng)
  [a] Lấy bản của Remote (Ghi đè Local bằng Remote Commits)
  [b] Đẩy đè bản Local lên (Ghi đè Remote bằng Local Commits)
  [c] Bỏ qua lỗi đồng bộ mạng lần này, tiếp tục chạy Downstream cục bộ
  [d] Quay lại (Hủy bỏ sync)
======================================================================
Lựa chọn của bạn (m/a/b/c/d): _
```
