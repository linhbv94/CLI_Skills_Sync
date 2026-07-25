# QA & Acceptance Specification: Skills Auto Sync Tool (`_spec5_qa_acceptance`)

> **Version:** 1.1.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** QA Engineers, Test Agents, Automation Testers  

---

## 1. Tiêu chí Nghiệm thu Chuẩn Gherkin (Acceptance Criteria)

### Kịch bản 1: Tự động Kéo thay đổi mới từ Remote Repo (Auto Pull)
```gherkin
Scenario: Đồng bộ khi Git Remote có commit mới hơn máy cục bộ
  Given Thư viện local tại "/Users/vic/skills_library" đang ở trạng thái Clean
  And Remote branch "origin/main" có 2 commit mới chưa pull
  When Người dùng mở ứng dụng và bấm nút "Smart Sync"
  Then Ứng dụng tự động chạy lệnh git pull fast-forward thành công
  And Cập nhật file "shared_rules/agents.md" sang "AGENTS.md" và "CLAUDE.md"
  And Hiển thị thông báo màu xanh "Đã tự động kéo 2 commit mới về máy."
```

### Kịch bản 2: Tự động Gom thay đổi khi sửa trực tiếp tại Antigravity (Upstream Sync)
```gherkin
Scenario: Sửa skill trực tiếp tại Antigravity, tự động gom về Library và Push Git
  Given Người dùng mở Antigravity và chỉnh sửa file "~/.gemini/config/skills/my_skill/SKILL.md"
  And File trong Library "skills/my_skill/SKILL.md" có timestamp cũ hơn
  When Người dùng bấm nút "Smart Sync" trên ứng dụng
  Then Ứng dụng phát hiện Antigravity có thay đổi mới hơn
  And Tự động copy file "SKILL.md" từ Antigravity về Central Library
  And Tự động phân bổ bản mới này sang thư mục Codex "~/.codex/skills/my_skill/SKILL.md"
  And Thực hiện git commit & git push lên Remote thành công
```

### Kịch bản 3: Bỏ qua hoàn toàn thư mục hệ thống `.system` của Codex
```gherkin
Scenario: Đồng bộ thư mục Codex nhưng loại trừ tuyệt đối folder .system
  Given Thư mục Codex "~/.codex/skills" có chứa folder nội bộ ".system/prompts.json"
  When Ứng dụng thực hiện quét Upstream Sync hoặc Deploy Adapters
  Then Thư mục ".system" KHÔNG bao giờ bị copy sang Central Library
  And Thư mục ".system" trong Codex KHÔNG bị xóa hay ghi đè bởi ứng dụng
  And Các file skill thường khác vẫn được đồng bộ chính xác
```

### Kịch bản 4: Phát hiện Xung đột và Cho phép Chọn Phương án (Conflict Handling)
```gherkin
Scenario: Hiển thị dialog chọn phương án khi phát hiện xung đột dữ liệu Git
  Given Cả máy cục bộ và Git Remote đều có commit mới tạo ra xung đột (Diverged state)
  When Người dùng bấm nút "Smart Sync"
  Then Tiến trình tự động kéo/đẩy bị dừng lại
  And Cửa sổ "Phát hiện xung đột dữ liệu Git" hiển thị với 3 lựa chọn
  When Người dùng chọn "Ưu tiên Remote (Pull & Override)" và nhấn "Thực hiện"
  Then Ứng dụng thực thi "git reset --hard origin/main"
  And Cập nhật dữ liệu từ remote đè lên local an toàn
```

---

## 2. Ma trận Trường hợp Biên (Edge Cases Matrix)

| ID Test | Phân loại | Tình huống (Edge Case) | Hành vi Mong đợi (Expected Behavior) | Trạng thái Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |
| `TC_EDGE_01` | Network | Đang sync thì ngắt kết nối Wifi / Mất mạng | Không crash app. Bật cảnh báo Offline Mode, tiếp tục sync từ Local Library sang các Agent. | Pass Criteria |
| `TC_EDGE_02` | File System | Thư mục agent (như `~/.codex/skills`) bị người dùng xóa nhầm | App tự động chạy `os.makedirs()` để khởi tạo lại thư mục trước khi copy skill. | Pass Criteria |
| `TC_EDGE_03` | System Folders | Thư mục `.codex/skills/.system` chứa dữ liệu hệ thống Codex | Bỏ qua hoàn toàn `.system` trong cả 2 chiều Sync (Upstream & Downstream). | Pass Criteria |
| `TC_EDGE_04` | OS / Encoding | File skill chứa ký tự Tiếng Việt UTF-8 và line endings mix CRLF/LF | Đảm bảo nạp và ghi file giữ nguyên định dạng UTF-8, không bị lỗi font hay đè ký tự `^M`. | Pass Criteria |
| `TC_EDGE_05` | Permission | File/Folder bị khóa quyền Write (Permission Denied) | Bắt ngoại lệ `PermissionError`, báo lỗi chi tiết đường dẫn file bị khóa lên UI Console Log. | Pass Criteria |
| `TC_EDGE_06` | Git CLI | Máy người dùng chưa cài đặt Git CLI | App kiểm tra `shutil.which('git')`. Nếu không thấy, hiện hướng dẫn tải Git và vô hiệu hóa nút Smart Sync Git. | Pass Criteria |

---

## 3. Danh mục Kiểm tra Chất lượng (QA Validation Checklist)

- [ ] **Cross-Platform Test:** Đã chạy thử nghiệm thành công trên cả macOS (Apple Silicon/Intel) và Windows 10/11.
- [ ] **Upstream Detection:** Sửa skill ở 1 Agent ➔ Smart Sync ➔ Gom về Library & Push Git ➔ Cập nhật các Agent khác thành công.
- [ ] **System Directory Isolation:** Thư mục `.codex/skills/.system` không bao giờ xuất hiện trong Central Library hay Git Repo.
- [ ] **Path Independence:** Không hard-code username (ví dụ `/Users/vic`), tự động nạp từ environment variables.
- [ ] **Zero Data Loss:** Không bao giờ tự động ghi đè file có uncommitted changes mà không có cảnh báo hoặc tạo `.bak`.
- [ ] **Performance Gate:** Thời gian thực thi Smart Sync (không tính latency mạng) dưới `2.0 giây`.

