# 06. Phase 2 Desktop App Specification & Benchmarking

Tài liệu này đặc tả kế hoạch phát triển Phase 2 (Ứng dụng Desktop có giao diện UI kết hợp song song CLI) và phân tích đối sánh (benchmarking) với các giải pháp quản lý cấu hình Agent/IDE hiện có trên thị trường.

---

## 1. Phân tích đối sánh các giải pháp hiện tại (Benchmarking)

Qua khảo sát các giải pháp đồng bộ cấu hình nhà phát triển và Agent trên GitHub/Cộng đồng, dưới đây là các hướng tiếp cận phổ biến và lý do tại sao ứng dụng của chúng ta mang lại giá trị vượt trội:

### A. Phương pháp truyền thống: Dotfiles + Symlinks (Liên kết mềm)
* **Cách hoạt động:** Người dùng gom các thư mục cấu hình ẩn (như `~/.claude/` hoặc `~/Library/Application Support/Cursor/User/`) vào một thư mục chung có quản lý Git (gọi là `~/dotfiles/`), sau đó dùng lệnh `ln -s` để tạo liên kết mềm trỏ ngược lại.
* **Hạn chế:**
  * **Không có giao diện tương tác:** Chỉ hoạt động qua lệnh dòng lệnh thủ công, khó sử dụng với người không chuyên sâu về kỹ thuật (non-dev).
  * **Không tự động chuyển đổi định dạng (Adapters):** Không thể tự động biến đổi file `AGENTS.md` thành `CLAUDE.md` kèm header đặc thù của Claude Code.
  * **Dễ bị lỗi ghi đè:** macOS/Windows khi cập nhật phần mềm hoặc ghi đè file có thể làm đứt liên kết mềm (broken symlinks).

### B. Các công cụ chuyên biệt của bên thứ ba
* **Claude Sync (`claude-sync`):** Công cụ CLI hỗ trợ mã hóa và đồng bộ cấu hình qua AWS S3 hoặc Cloudflare R2. Chỉ hỗ trợ duy nhất Claude Code và yêu cầu thuê dịch vụ Cloud Storage.
* **Cursor Git Settings Sync:** Extension hỗ trợ đồng bộ file `settings.json` của Cursor lên GitHub Gist. Không đồng bộ được rules và không hỗ trợ các Agent khác ngoài Cursor.
* **cursor2claude:** Script nhỏ hỗ trợ copy rules từ Cursor sang `CLAUDE.md`. Không hỗ trợ sync 2 chiều (bị drift dữ liệu nếu sửa ở Claude Code).

### C. Bảng so sánh tính năng
| Tính năng | Dotfiles + Git | Claude Sync | cursor2claude | **Skills Auto Sync Tool (Của ta)** |
| :--- | :--- | :--- | :--- | :--- |
| **Đồng bộ chéo đa Agent** | Thủ công | Chỉ Claude | Thủ công | **Tự động (Antigravity/Codex/Claude)** |
| **Chuyển đổi Adapter (Header)**| Không | Không | 1 chiều | **Tự động 2 chiều (AGENTS.md ↔ CLAUDE.md)** |
| **Hợp nhất tự động (Merge)** | Cần Git CLI | Không hỗ trợ | Không hỗ trợ | **Hỗ trợ menu giải quyết conflict [m]** |
| **Giao diện thân thiện** | Không | Không | Không | **CLI Song ngữ + Web UI (Phase 2)** |
| **Chạy offline hoàn toàn** | Có | Không | Có | **Có (Git-Optional mode)** |

---

## 2. Đặc tả Kiến trúc Phase 2: Song song CLI & Desktop UI

Trong Phase 2, hệ thống sẽ được nâng cấp thành mô hình **Shared Core Architecture** cho phép chạy đồng thời cả giao diện CLI gọn nhẹ và giao diện đồ họa Desktop đẹp mắt.

### A. Quản lý cấu hình tập trung (Centralized System Config)
File cấu hình `config.json` sẽ không đặt cùng cấp với file chạy (tránh lỗi Signature khi chạy macOS `.app`). `ConfigManager` sẽ định tuyến file cấu hình về các thư mục chuẩn của Hệ điều hành:
* **macOS:** `~/Library/Application Support/Skills_Sync/config.json`
* **Windows:** `%APPDATA%\Skills_Sync\config.json`

Cả bản CLI (`main.py`) và bản UI (`gui.py`) đều trỏ chung về đường dẫn này, đảm bảo dữ liệu đồng bộ thời gian thực.

### B. Kiến trúc Giao diện UI (Desktop Webview Engine)
Chúng ta sẽ sử dụng thư viện **PyWebView** để mở một Native Window của hệ điều hành và hiển thị giao diện được thiết kế bằng công nghệ Web (HTML/CSS/JS).

#### Cầu nối JavaScript Bridge (API):
Khi người dùng tương tác trên Web UI, JS sẽ gọi trực tiếp các phương thức Python thông qua cầu nối:
```javascript
// Gọi đồng bộ ngay lập tức
window.pywebview.api.run_sync().then(response => {
    if (response.success) {
        showNotification("Sync Completed!");
    }
});

// Gọi dọn dẹp môi trường
window.pywebview.api.run_cleanup().then(...);
```

#### Thiết kế giao diện (Design System):
* **Style:** Modern Glassmorphism (nền mờ sương, bo góc mịn 12px, bóng mờ nhẹ).
* **Bảng màu:**
  * Dark mode chủ đạo (Màu nền `#0d1117`, màu card `#161b22`).
  * Trạng thái hoạt động: Xanh lục Teal (`#2ea44f`).
  * Trạng thái phát hiện thay đổi: Cam Amber (`#db6d28`).
* **Tính năng trên UI:**
  * Progress Bar hiển thị trực quan từng bước đồng bộ (Step 1 -> Step 2 -> Step 3).
  * Hiển thị danh sách các Agent đang active dưới dạng thẻ card bật/tắt (Toggle switches).
  * Nút bấm **"Edit Config"** hỗ trợ mở nhanh file `config.json` trong Application Support bằng Text Editor mặc định của hệ thống.

---

## 3. Cấu hình đóng gói PyInstaller (Double Binary Build Specs)

Khi đóng gói, chúng ta sẽ định cấu hình PyInstaller để xuất ra 2 phiên bản độc lập từ cùng một source code:

### 1. Bản CLI (skills_sync / skills_sync.exe)
* **Lệnh build:**
  ```bash
  pyinstaller --onefile --name=skills_sync --icon=assets/app_icon.icns main.py
  ```
* **Đặc tính:** Chạy trực tiếp trong terminal, không mở cửa sổ đồ họa.

### 2. Bản Desktop UI (Skills Sync.app / Skills Sync.exe)
* **Lệnh build:**
  ```bash
  pyinstaller --noconsole --onefile --name="Skills Sync App" --icon=assets/app_icon.icns gui.py
  ```
* **Đặc tính:** Chạy dưới dạng Windowed App (không mở cửa sổ console màu đen), hiển thị giao diện Webview độc lập.
