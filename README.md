# Skills Auto Sync Tool (v2.2.0)

**Skills Auto Sync Tool** là ứng dụng dòng lệnh (CLI/Terminal) siêu nhẹ, chạy đa nền tảng (macOS & Windows), giúp tự động hóa việc quản lý và đồng bộ quy tắc (`AGENTS.md`) và thư viện kỹ năng (`skills/` folder) giữa các máy làm việc của người dùng và các AI Agents cục bộ (`Antigravity`, `Codex`, `Claude Code`).

---

## 1. Cấu trúc Dự án (Project Structure)

```text
├── assets/                     # Chứa logo & icon đóng gói
│   ├── app_icon.png            # Logo gốc 1024x1024
│   ├── app_icon.icns           # Icon định dạng macOS
│   └── app_icon.ico            # Icon định dạng Windows
├── dist/                       # Chứa file thực thi sau khi build
│   ├── skills_sync             # File thực thi cho macOS (độc lập)
│   ├── config.json             # File config chạy thật/test
│   └── skills_sync.command     # File phím tắt chạy nhanh trên macOS
├── docs/spec/                  # Tài liệu đặc tả hệ thống
├── src/                        # Mã nguồn Python
│   ├── config_manager.py       # Quản lý nạp/ghi config.json
│   ├── sync_engine.py          # Lọc, so sánh & đồng bộ chéo skills
│   ├── adapter_engine.py       # Xử lý quy tắc rules (AGENTS.md/CLAUDE.md)
│   └── git_engine.py           # Quản lý lệnh Git shell & xung đột
├── tests/                      # Thư mục unit tests
├── main.py                     # Entry point của ứng dụng CLI
└── README.md                   # Hướng dẫn sử dụng này
```

---

## 2. Hướng dẫn Cấu hình `config.json`

File `config.json` bắt buộc phải đặt ở **cùng thư mục với file thực thi** (`skills_sync` hoặc `skills_sync.exe`). Nếu chưa có file này, khi mở ứng dụng lần đầu tiên, tool sẽ tự động sinh file mẫu.

### Cấu trúc file mẫu:
```json
{
  "version": "2.2.0",
  "agents": {
    "anti": 1,
    "codex": 1,
    "claude": 0
  },
  "skills_lib": "/Users/username/my_skills_library",
  "git_repo": "https://github.com/username/my_skills_library.git",
  "ignore_patterns": [
    "**/.system/**",
    "**/.git/**",
    "**/.DS_Store",
    "**/desktop.ini",
    "**/*.tmp",
    "**/*.bak*"
  ]
}
```

### Các tham số cấu hình:
1. **`agents`**: Bật/tắt các AI Agent cục bộ. Điền `1` để kích hoạt đồng bộ, `0` để bỏ qua.
   * `anti`: Antigravity Agent.
   * `codex`: Codex Agent.
   * `claude`: Claude Code Agent.
2. **`skills_lib`**: Đường dẫn tuyệt đối đến thư mục chứa Thư viện Skills gốc (Central Library) trên máy bạn.
3. **`git_repo`**: Link Git Remote Repository (HTTPS/SSH) để đồng bộ commits.
   * *Mẹo:* Nếu bạn muốn chạy tool ở **chế độ offline hoàn toàn** (chỉ đồng bộ cục bộ giữa các Agent trên máy mà không sử dụng Git), hãy để trống trường này (`"git_repo": ""`).
4. **`ignore_patterns`**: Các pattern định dạng file/thư mục được Sync Engine bỏ qua không đồng bộ (như file rác hệ điều hành, file log, temp).

### Đường dẫn mặc định của các Agent:
Nếu anh để trống đường dẫn, Sync Engine tự động định vị thư mục làm việc của Agent theo quy chuẩn sau:
* **macOS:**
  * Antigravity ➔ `~/.gemini/config`
  * Codex ➔ `~/.codex`
  * Claude Code ➔ `~/.claude`
* **Windows:**
  * Antigravity ➔ `%USERPROFILE%\.gemini\config`
  * Codex ➔ `%USERPROFILE%\.codex`
  * Claude Code ➔ `%USERPROFILE%\.claude`

---

## 3. Hướng dẫn Đóng gói File Thực thi (Build Guide)

Ứng dụng sử dụng `PyInstaller` để biên dịch toàn bộ mã nguồn thành một file chạy duy nhất. PyInstaller sẽ tạo file tương ứng với hệ điều hành đang chạy nó.

### Bước 1: Cài đặt PyInstaller
Mở Terminal/CMD và cài đặt thư viện đóng gói:
```bash
pip install pyinstaller
```

### Bước 2: Chạy lệnh đóng gói

#### 🍏 Trên macOS (Build ra file Unix Executable):
Mở Terminal tại thư mục gốc của dự án và chạy:
```bash
pyinstaller --onefile --name skills_sync --icon=assets/app_icon.icns main.py
```
* Thành phẩm nằm ở: `dist/skills_sync`

#### 🪟 Trên Windows (Build ra file .exe):
Mở CMD/PowerShell tại thư mục gốc của dự án và chạy:
```cmd
pyinstaller --onefile --name skills_sync --icon=assets/app_icon.ico main.py
```
* Thành phẩm nằm ở: `dist/skills_sync.exe`

---

## 4. Hướng dẫn Sử dụng & Phím tắt (Usage & Shortcuts)

Khi chạy ứng dụng dòng lệnh, bạn sẽ tương tác thông qua menu phím số:

### Các tính năng chính:
* **[1] Đồng bộ ngay (Smart Sync Now):**
  1. Quét upstream: So sánh timestamps, file nào mới hơn ở Agent sẽ được gom ngược về Thư viện tổng.
  2. Đồng bộ Git: Tự động pull/push commits mới.
  3. Deploy downstream: Phân phối `AGENTS.md` (hoặc render đổi tên thành `CLAUDE.md` kèm header cho Claude) và folder `skills` sang các Agent còn lại cục bộ.
* **[2] Giám sát chạy nền (Auto-Sync Watcher Daemon):** Chạy một bộ watcher siêu nhẹ (chu kỳ quét 3 giây) liên tục lắng nghe thay đổi file. Khi phát hiện chỉnh sửa, tool tự động kích hoạt luồng Smart Sync. Nhấn `Ctrl + C` để thoát chế độ này an toàn.
* **[3] Dọn dẹp môi trường (Clean up environment):** Xóa sạch toàn bộ rules & skills ở thư viện tổng và các Agent active (ngoại trừ `.git` của thư viện tổng và `.system` của Codex) ➔ Tạo commit dọn dẹp và **tự động đẩy lên Git Remote** để reset sạch kho lưu trữ.
* **[4] Thoát ứng dụng.**

### Cơ chế Lối tắt (Shortcuts) 1-Click:
* **Trên Windows:** Tạo một **Windows Shortcut** trỏ tới file `skills_sync.exe`. Chuột phải vào Shortcut ➔ Chọn Properties ➔ Config phần *Start in* là đường dẫn thư mục chứa `.exe` (để file đọc được `config.json` cùng cấp). Kéo Shortcut ra Desktop hoặc Ghim vào Taskbar để click chạy nhanh.
* **Trên macOS:** Nhấp đúp vào file [dist/skills_sync.command](file:///Users/vic/_Work/Skills_Sync/dist/skills_sync.command) ngoài màn hình Desktop/Finder. File script này sẽ tự động CD về đúng thư mục chứa tệp nhị phân và chạy tool dòng lệnh ngay lập tức.

---

## 5. Các tính năng Nâng cao (Edge Cases)

* **Tự động chặn file rác hệ điều hành:** Khi chạy, tool tự động kiểm tra xem Thư viện tổng đã có file `.gitignore` chưa. Nếu chưa có, tool tự tạo file `.gitignore` chuẩn để loại bỏ hoàn toàn `.DS_Store`, `Thumbs.db`, `desktop.ini` khỏi commits.
* **Chặn đơ/treo tiến trình mật khẩu:** Cấu hình biến môi trường `GIT_TERMINAL_PROMPT=0` ngăn Git CLI đứng chờ nhập Username/Password khi chưa đăng nhập. Nếu lỗi xác thực, tool in cảnh báo `AUTH_ERROR` rõ ràng và tiếp tục chạy sync cục bộ.
* **Hợp nhất tự động [m] (Auto Merge):** Khi có xung đột `DIVERGED` (ví dụ: vừa xóa file trên Git Web vừa sửa file ở máy local), người dùng nhấn phím **`m`** để tool tự động gộp lịch sử commits, chạy pull trộn dữ liệu và đẩy ngược lên Remote an toàn tuyệt đối.
