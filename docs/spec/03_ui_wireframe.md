# UI & Wireframe Specification: Skills Auto Sync Tool (`_spec3_ui_wireframe`)

> **Version:** 1.2.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** UI/UX Designers, Frontend Developers, UI Agents  

---

## 1. Bố cục Giao diện Màn hình chính (Main Dashboard Spec)

Giao diện ứng dụng dạng cửa sổ mỏng nhẹ, tối ưu màu nền Dark Mode tương thích cao (Kích thước chuẩn: `820px x 680px`):

```text
+-----------------------------------------------------------------------------------+
| ⚡ Skills Auto Sync Tool (v1.2.0)                         [OS: macOS Arm64] [_][X] |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  📌 1. THƯ VIỆN GỐC & GIT REMOTE REPO                                             |
|  Skills Lib Path: [/Users/vic/my_skills_lib                     ] [ Browse... ]   |
|  Git Remote URL:  [https://github.com/user/my_skills.git        ] [🔗 Link/Clone ]|
|  Git Status:      🟢 Up-to-date (Git synced)                                      |
|                                                                                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  🤖 2. CẤU HÌNH AGENTS TRÊN MÁY NÀY                                               |
|  [X] Antigravity   Path: [~/.gemini/config/skills              ] [ Auto-Detect ]|
|  [X] Codex         Path: [~/.codex/skills                      ] [ Auto-Detect ]|
|  [X] Claude Code   Path: [~/.claude                            ] [ Auto-Detect ]|
|                                                                                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 🔍 Preview Changes ]            [ ⚙️ Save Config ]      [ 🚀 SMART SYNC NOW ] |
|                                                                                   |
+-----------------------------------------------------------------------------------+
| 💡 LOG BÁO CÁO TIẾN TRÌNH                                                        |
| +-------------------------------------------------------------------------------+ |
| | [System] Đã sẵn sàng. Điền đường dẫn Library + Git Remote URL rồi bấm Sync!  | |
| | [Step 0/3] Kiểm tra liên kết Git Remote URL: https://github.com/...           | |
| | [Step 1/3] Quét thay đổi từ Agent Folders (bỏ qua .system)...                 | |
| | [Step 2/3] Kiểm tra và đồng bộ Git Remote...                                 | |
| | 🎉 === SMART SYNC HOÀN TẤT THÀNH CÔNG ===                                     | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```


---

## 2. Chi tiết Thành phần Giao diện & Trạng thái (Component Specs)

### A. Button Primary `[ 🚀 SMART SYNC NOW ]`
* **Vị trí:** Góc dưới bên phải (Bottom Right Action).
* **Màu sắc:**
  * Normal: Xanh Navy / Accent Primary (`#1a365d` / `#2b6cb0`).
  * Hover: Highlight Blue (`#3182ce`).
  * Syncing/Active: Disabled State kèm Spinner `[ ⏳ Syncing... ]`.
  * Success State: Xanh lá cây nháy nhẹ 2s (`#2f855a`).
  * Error State: Đỏ Cảnh báo (`#c53030`).

### B. Badge Trạng thái Git (Git Status Indicator)
* 🟢 **Up-to-date (Xanh lá):** Local và Remote hoàn toàn đồng nhất.
* 🔵 **Local Ahead (Xanh dương):** Có commit local cần push `[ ⬆️ 2 Commits Ahead ]`.
* 🟧 **Remote Ahead (Cam):** Có commit remote cần pull `[ ⬇️ 1 Commit Behind ]`.
* 🔴 **Conflict (Đỏ):** Xung đột dữ liệu `[ ⚠️ Diverged - Action Required ]`.

---

## 3. Cửa sổ Modal Xử lý Xung đột (Conflict Resolution Dialog)

Khi Git phát hiện trạng thái **Diverged**, hiển thị Pop-up Modal đè lên giao diện chính:

```text
+-------------------------------------------------------------------+
| ⚠️ PHÁT HIỆN XUNG ĐỘT DỮ LIỆU GIT                                 |
+-------------------------------------------------------------------+
| Cả máy cục bộ và Git Remote đều có những thay đổi mới.           |
| Vui lòng chọn phương án đồng bộ bên dưới:                        |
|                                                                   |
| (•) Ưu tiên Remote (Pull & Override)                              |
|     Lấy toàn bộ bản mới từ Git về, hủy bỏ thay đổi chưa push.     |
|                                                                   |
| ( ) Ưu tiên Local (Push Force)                                    |
|     Ghi đè bản trên Git Remote bằng dữ liệu máy hiện tại.         |
|                                                                   |
| ( ) Tự gộp thủ công (Manual Terminal Merge)                       |
|     Mở ứng dụng Terminal để tự thực hiện git merge.               |
|                                                                   |
|                      [ Bỏ qua ]     [ 🔄 Thực hiện ]            |
+-------------------------------------------------------------------+
```

---

## 4. Hướng dẫn Phong cách Thiết kế (Design System & Styling Tokens)

* **Font chữ:** System Native Fonts (macOS: `San Francisco / Helvetica Neue`, Windows: `Segoe UI`).
* **Kích thước Chữ:**
  * Title/Header: `14px` Bold.
  * Section Headers: `12px` Semi-bold.
  * Body text / Inputs: `11px` Regular.
  * Console Log: `10px` Monospace (`Consolas` / `Menlo`).
* **Theme Support:** Tự động ăn theo chế độ **Dark Mode / Light Mode** của hệ điều hành.
