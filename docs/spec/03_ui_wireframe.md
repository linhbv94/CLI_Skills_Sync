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

---

## 6. Đặc tả Giao diện Ứng dụng Desktop GUI (Desktop GUI App Specification)

Phiên bản Desktop GUI hoạt động song song với CLI, chia sẻ chung file cấu hình `config.json`. Giao diện được thiết kế theo phong cách tối giản hiện đại (Modern Glassmorphism) với các thành phần điều khiển trực quan.

### A. Sơ đồ Bố cục Giao diện (GUI Layout Diagram)

```text
+-----------------------------------------------------------------------------------------+
|  ⚡ SKILLS AUTO SYNC TOOL (v2.4.0)                               [ EN / VI ]  [🌙/☀️/💻] |
+-----------------------------------------------------------------------------------------+
| CONFIGURATION PANEL (CẤU HÌNH)         | SYSTEM STATUS & LOGS (TRẠNG THÁI & NHẬT KÝ)    |
|                                        |                                                |
| [ ] Active Agents:                     | [SYSTEM STATUS: NO CHANGES / KHÔNG THAY ĐỔI]   |
|   [x] Antigravity                      |   ├─ Antigravity: Up-to-date                   |
|   [x] Codex                            |   ├─ Codex:       Up-to-date                   |
|   [ ] Claude Code                      |   └─ Git Remote:  Up-to-date                   |
|                                        | ---------------------------------------------- |
| Skills Library Path (Thư viện tổng):   | [LOGS]                                         |
| [ /Users/vic/skills_lib             ]  | 2026-08-07 09:00:00 [INFO] GUI App started.    |
| [ Browse... ] or paste path/link       | 2026-08-07 09:00:02 [INFO] Git status checked. |
|                                        |                                                |
| Git Repository (Link repo Git):        |                                                |
| [ https://github.com/dummy/skills  ]  |                                                |
| Paste HTTPS/SSH repository link        |                                                |
|                                        |                                                |
+-----------------------------------------------------------------------------------------+
| [⚡ Smart Sync Now]  [🔄 Refresh Status]  [🧹 Clean Up]  [📁 Open Config]    [❌ Quit]  |
+-----------------------------------------------------------------------------------------+
```

### B. Đặc tả Chi tiết các Component & Tương tác (Component Specifications)

#### 1. Header Area (Thanh Tiêu đề)
*   **Tiêu đề:** "⚡ SKILLS AUTO SYNC TOOL (v2.4.0)".
*   **Bộ chuyển đổi Ngôn ngữ (Language Switcher):**
    *   Nút bấm chuyển đổi giữa `EN` và `VI` (Segmented control hoặc Toggle button).
    *   **Logic lưu trữ:** Khi nhấn switch, ngôn ngữ hiển thị thay đổi ngay lập tức trên UI và cập nhật trực tiếp trường `"lang"` vào `config.json` ngay tức thì (auto-save).
*   **Bộ chuyển đổi Giao diện (Theme Switcher):**
    *   Bộ 3 nút bấm biểu tượng tương ứng với: `🌙 Dark` (Tối), `☀️ Light` (Sáng), `💻 System` (Theo hệ thống).
    *   **Logic lưu trữ:** Khi thay đổi, cập nhật trường `"theme"` trong `config.json` ngay tức thì. Giao diện thay đổi CSS theme tương ứng mà không cần reload.

#### 2. Configuration Panel (Khung Cấu hình - Bên trái)
*   **Chọn AI Agents (Agent Selection):**
    *   Nhóm Checkbox: `[ ] Antigravity`, `[ ] Codex`, `[ ] Claude Code`.
    *   **Logic lưu trữ:** Người dùng tích chọn/bỏ chọn. Giá trị được ghi nhận tạm thời trên UI, tự động lưu vào `"agents"` của `config.json` khi nhấn **Smart Sync Now** hoặc **Refresh Status**.
*   **Skills Library Path (Thư viện tổng):**
    *   Ô nhập liệu (Text Input) cho phép dán (paste) đường dẫn thư mục cục bộ hoặc link trực tiếp.
    *   Nút **`[ Browse... ]`**: Khi bấm sẽ mở Finder (macOS) hoặc File Explorer (Windows) để chọn thư mục cục bộ, tự động điền đường dẫn tuyệt đối vào ô nhập liệu.
    *   **Logic lưu trữ:** Lưu vào `"skills_lib"` của `config.json` khi nhấn **Smart Sync Now** hoặc **Refresh Status**.
*   **Git Repository (Link repo Git):**
    *   Ô nhập liệu (Text Input) cho phép dán (paste) link Git Remote URL.
    *   **Logic lưu trữ:** Lưu vào `"git_repo"` của `config.json` khi nhấn **Smart Sync Now** hoặc **Refresh Status**.

#### 3. System Status & Logs (Khung Trạng thái & Nhật ký - Bên phải)
*   **Khung Trạng thái (System Status Block):**
    *   Hiển thị tóm tắt trạng thái của từng Agent được kích hoạt và Git Remote (Up-to-date, Behind, Ahead, Diverged, Offline, Error). Màu sắc linh hoạt: xanh lá cho đồng bộ, cam cho có cập nhật, đỏ cho lỗi.
*   **Khung Nhật ký (Console Logs Block):**
    *   Một vùng hiển thị văn bản (Text Area/Console Output) cuộn tự động xuống cuối (auto-scroll).
    *   Render dòng log theo thời gian thực tương đương với CLI. Có các huy hiệu màu sắc (Color badges) phân biệt `[INFO]`, `[SUCCESS]` (Teal), `[WARN]` (Cam), và `[ERROR]` (Đỏ).

#### 4. Action Footer (Thanh Chức năng - Phía dưới)
*   **`[⚡ Smart Sync Now]` (Nút chính - Primary CTA):**
    *   **Hành vi:**
        1. Đọc tất cả cấu hình trên UI (agents, skills_lib, git_repo) và lưu ngay vào `config.json`.
        2. Vô hiệu hóa (disable) toàn bộ các control cấu hình và nút chức năng khác trên UI để tránh thao tác trùng lặp.
        3. Hiển thị biểu tượng xoay (loading spinner) trên nút.
        4. Gọi hàm backend thực thi đồng bộ và xuất log ra log box.
        5. Khi hoàn tất, khôi phục trạng thái các nút bấm.
*   **`[🔄 Refresh Status]`:**
    *   **Hành vi:** Lưu cấu hình hiện tại vào `config.json`, quét nhanh trạng thái thư mục và Git mà không chạy đồng bộ file (dry run). Cập nhật trạng thái hiển thị bên phải.
*   **`[🧹 Clean Up]`:**
    *   **Hành vi:** Xóa các file rác/temp trong các thư mục agent và làm sạch log trên màn hình.
*   **`[📁 Open Config]`:**
    *   **Hành vi:** Mở thư mục hệ thống chứa `config.json` bằng Finder/Explorer.
*   **`[❌ Quit]`:**
    *   **Hành vi:** Đóng cửa sổ ứng dụng và thoát an toàn.

---

## 7. Giao diện Hộp thoại Giải quyết Xung đột Git trên GUI (Git Conflict Modal Specs)

Khi Git Engine báo cáo trạng thái `DIVERGED` trong quá trình đồng bộ:
1. Giao diện GUI sẽ hiển thị một Modal Overlay mờ đè lên toàn bộ app.
2. Hiển thị tiêu đề cảnh báo: `⚠️ Git Remote Conflict Detected / Phát hiện Xung đột Git Remote`.
3. Cung cấp 5 nút bấm hành động rõ ràng tương ứng với các giải pháp:
    *   **`[ Auto Merge & Pull ]`** (Khuyên dùng): Tự động gộp code.
    *   **`[ Overwrite Local (Force Pull) ]`** (Lấy bản của Remote): Ghi đè cục bộ.
    *   **`[ Overwrite Remote (Force Push) ]`** (Đẩy đè bản Local lên): Ghi đè Remote.
    *   **`[ Skip Remote Sync (Offline Mode) ]`** (Bỏ qua sync mạng): Chỉ đồng bộ local.
    *   **`[ Cancel Sync ]`** (Hủy bỏ): Đóng modal và dừng tiến trình.

---

## 8. Visual Wireframe Prompt (AI Image / UI Agent Generation)

> *A clean, premium, and modern Desktop App UI design for a developer utility tool called "Skills Sync". The screen is split into a left configuration column and a right console log console. Modern glassmorphism style with a deep dark slate-gray gradient background (#0d1117). Sleek typography using 'Inter'. Left column has neat controls: Agent check-boxes, library path text box with a browse button, and a git remote input. Right column shows a dark console output log block with terminal styled status lines and colorful status icons. The header has language toggle button (EN/VI) and theme selectors (Dark/Light/System) side-by-side. The bottom contains a row of flat, rounded action buttons including a glowing green "Smart Sync Now" button. High-end developer app interface.*

---

## 9. Lịch sử Cập nhật (Changelog)

*   **v2.4.0 (2026-08-07):** Bổ sung đặc tả chi tiết giao diện Desktop GUI song song với CLI. Định nghĩa thêm cấu hình `theme` trong `config.json`. Thêm sơ đồ layout GUI, đặc tả tương tác switch ngôn ngữ/giao diện, hộp thoại giải quyết xung đột dạng modal, và quy chuẩn auto-save cấu hình.
*   **v2.3.0 (2026-08-06):** Thiết kế lại luồng Onboarding CLI, chuyển đổi đường dẫn file config.json sang thư mục hệ thống chuẩn (AppData/Application Support) và thêm menu giải quyết xung đột Git Diverged.

