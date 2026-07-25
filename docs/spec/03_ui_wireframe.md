# UI & Wireframe Specification: Skills Auto Sync Tool (`_spec3_ui_wireframe`)

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** UI/UX Designers, Frontend Developers, UI Agents  

---

## 1. Bố cục Giao diện Màn hình chính (Main Dashboard Spec)

Giao diện ứng dụng dạng cửa sổ gọn nhẹ (Kích thước chuẩn: `780px x 560px`, Không cho phép resize quá nhỏ):

```text
+-----------------------------------------------------------------------------------+
| ⚡ Skills Auto Sync Tool (v1.0.0)                         [OS: macOS Arm64] [_][X] |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  📌 1. NGUỒN DỮ LIỆU TỔNG (CENTRAL LIBRARY)                                        |
|  Library Path: [/Users/vic/skills_library                       ] [ Browse... ]   |
|  Git Status:   🟢 Up-to-date (origin/main) | Last Sync: 2026-07-25 18:30         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  🤖 2. CHỌN AGENTS ĐỒNG BỘ TRÊN MÁY NÀY                                           |
|  [X] Antigravity   Path: [~/.gemini/config                       ] [ Auto-Detect ]|
|  [X] Codex         Path: [~/.codex/skills                        ] [ Auto-Detect ]|
|  [X] Claude Code   Path: [~/.claude                              ] [ Auto-Detect ]|
|                                                                                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  📊 3. THÔNG TIN XEM TRƯỚC (PREVIEW SUMMARY)                                       |
|  +-----------------------------------------------------------------------------+  |
|  | - File skills/video_editor/skill.md: Updated (Modified 5 mins ago)         |  |
|  | - File shared_rules/agents.md: Up-to-date                                  |  |
|  | - Target Agents: Antigravity, Codex, Claude Code                           |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 🔍 Preview Changes ]            [ ⚙️ Settings ]         [ 🚀 SMART SYNC NOW ] |
|                                                                                   |
+-----------------------------------------------------------------------------------+
| 💡 Log: Smart Sync completed successfully in 1.2s. 3 agents updated.             |
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
