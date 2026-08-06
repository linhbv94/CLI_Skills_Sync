# QA & Acceptance Specification: Skills Auto Sync Tool (`_spec5_qa_acceptance`)

> **Version:** 2.2.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** QA Engineers, Test Agents, Automation Testers  

---

## 1. Tiêu chí Nghiệm thu Chuẩn Gherkin (Acceptance Criteria)

### Kịch bản 1: Tự động kéo thay đổi mới từ Git Remote qua CLI cho các Active Agent
```gherkin
Scenario: Chạy Smart Sync khi Git Remote có commit mới
  Given Thư viện tổng "/Users/vic/skills_library" ở trạng thái sạch (clean)
  And Remote branch "origin/main" có 2 commit mới chưa pull
  And File config.json có cấu hình: "anti": 1, "codex": 1, "claude": 0
  When Người dùng chạy file thực thi và nhập phím "1" rồi nhấn Enter
  Then Ứng dụng tự động gọi git pull fast-forward thành công
  And Cập nhật file "AGENTS.md" của Antigravity và Codex từ thư viện tổng
  And KHÔNG cập nhật thư mục Claude vì "claude": 0
  And In thông báo ra Terminal: "Đã tự động kéo commit mới từ Git và cập nhật các Agent."
```

### Kịch bản 2: Đồng bộ ngược Upstream từ các Active Agent về Thư viện tổng & Push Git
```gherkin
Scenario: Phát hiện thay đổi cục bộ ở Agent, gom về Central Library và Push
  Given Người dùng chỉnh sửa file trong thư mục Antigravity "~/.gemini/config/skills/my_skill/SKILL.md"
  And Thư mục Antigravity đang active trong config ("anti": 1)
  And File tương ứng trong Thư viện tổng có timestamp cũ hơn
  When Người dùng chạy ứng dụng CLI, chọn Option "1" và nhấn Enter
  Then Ứng dụng phát hiện file ở Antigravity mới hơn
  And Thực hiện sao chép file đó ngược về Thư viện tổng (skills_lib)
  And Tự động sao chép sang Codex ("codex": 1) để đồng bộ chéo
  And Thực hiện git commit & git push lên GitHub
  And In thông báo thành công: "Phát hiện có thay đổi local mới. Đang push lên Git Remote..."
```

### Kịch bản 3: Bỏ qua tuyệt đối thư mục hệ thống `.system` của Codex
```gherkin
Scenario: Giữ nguyên thư mục hệ thống của Codex khi sync chéo
  Given Thư mục Codex "/Users/vic/.codex/skills" có chứa folder hệ thống ẩn ".system"
  And Codex đang active ("codex": 1)
  When Ứng dụng thực hiện quét hoặc deploy skills cục bộ
  Then Folder ".system" KHÔNG bao giờ bị sao chép sang Thư viện tổng (skills_lib)
  And Folder ".system" trong Codex KHÔNG bị ghi đè hoặc xóa bỏ
```

### Kịch bản 4: Xử lý Xung đột Git Remote qua Hợp nhất Tự động [m] (Auto Merge)
```gherkin
Scenario: Chọn giải quyết xung đột Git bằng cách trộn (merge) commit tự động
  Given Cả Thư viện tổng local và Git Remote đều có commit mới tạo ra xung đột (Diverged)
  When Người dùng chạy CLI, chọn Option "1" (Smart Sync) và gặp bảng hỏi
  Then Tiến trình dừng lại hiển thị menu xử lý xung đột m/a/b/c/d
  When Người dùng nhập phím "m" và nhấn Enter (Tự động hợp nhất)
  Then Ứng dụng thực thi git add, git commit local và git pull --no-rebase
  And Tự động merge các thay đổi và push kết quả merge lên Git Remote
  And Tiếp tục deploy downstream tới các active agents bình thường
```

---

## 2. Ma trận Trường hợp Biên (Edge Cases Matrix)

| ID Test | Phân loại | Tình huống (Edge Case) | Hành vi Mong đợi của CLI Engine | Kết quả |
| :--- | :--- | :--- | :--- | :--- |
| `TC_EDGE_01` | Mạng | Mất mạng hoặc không kết nối được Git Server | Không crash app. In thông báo `[Offline Mode]`, tiếp tục sync cục bộ giữa các Agent active và Thư viện tổng. | Pass Criteria |
| `TC_EDGE_02` | Config | Chưa tồn tại file `config.json` cùng cấp | Tự động tạo file `config.json` mẫu chứa cấu trúc toggles và paths trống, in thông báo hướng dẫn lên Terminal rồi dừng. | Pass Criteria |
| `TC_EDGE_03` | Hệ thống file | Thư mục agent active bị người dùng xóa nhầm | Tự tạo lại thư mục trống bằng `os.makedirs()` trước khi deploy skills để tránh lỗi IO. | Pass Criteria |
| `TC_EDGE_04` | Mã hóa | File skill chứa ký tự Tiếng Việt UTF-8 đặc biệt | Đọc ghi chính xác bằng mã hóa `utf-8`, không làm hỏng font hay lỗi hiển thị ký tự. | Pass Criteria |
| `TC_EDGE_05` | Phân quyền | File bị khóa quyền ghi (Permission Denied) | Bắt lỗi `PermissionError`, in thông báo lỗi rõ ràng ra màn hình Terminal và tiếp tục sync các file khác. | Pass Criteria |
| `TC_EDGE_06` | Git Tool | Máy tính chưa cài đặt Git CLI | 1. Khi `git_repo` trống: Hoạt động bình thường ở chế độ chỉ đồng bộ cục bộ.<br>2. Khi `git_repo` có cấu hình: Dừng lại và in thông báo: `❌ Git CLI chưa được cài đặt.` | Pass Criteria |
| `TC_EDGE_07` | Lựa chọn CLI | Nhập ký tự không hợp lệ tại CLI Menu chính | In thông báo `[Error] Lựa chọn không hợp lệ, vui lòng nhập lại (1-4)` và hiển thị lại Menu. | Pass Criteria |
| `TC_EDGE_08` | Xác thực | Cài Git rồi nhưng chưa đăng nhập hoặc hết hạn Token / SSH Key | 1. **Ngăn chặn treo app (No Hang):** Thiết lập `GIT_TERMINAL_PROMPT=0` để tắt bảng nhập mật khẩu của OS, khiến Git CLI trả lỗi lập tức thay vì treo vĩnh viễn.<br>2. **Thông báo & Bỏ qua:** Trả về trạng thái `AUTH_ERROR` với mô tả lỗi chi tiết, bỏ qua đồng bộ mạng và tiếp tục chạy đồng bộ cục bộ (Local Sync). | Pass Criteria |

---

## 3. Danh mục Kiểm tra Chất lượng (QA Validation Checklist)

- [ ] **Khởi chạy Độc lập:** Chạy thử file nhị phân được đóng gói trên cả Windows (`.exe` kèm Shortcut) và macOS (Unix Executable kèm Alias hoặc Automator App).
- [ ] **Config cùng cấp:** Đảm bảo `config.json` được đọc ghi tại đúng thư mục chứa file thực thi thật.
- [ ] **Bật tắt Agent:** Xác minh khi set `claude: 0`, thư mục Claude hoàn toàn bị bỏ qua; khi set `claude: 1`, thư mục Claude tự động được tìm kiếm và đồng bộ hoàn chỉnh.
- [ ] **Cô lập Codex:** Thư mục `.system` của Codex hoàn toàn được bảo vệ và cô lập.
- [ ] **Đóng app gọn gàng:** Không tạo tiến trình chạy ngầm vô thời hạn trừ khi được chọn chạy chế độ Watcher (Option 2). Nhấn Ctrl+C dừng Watcher an toàn.
