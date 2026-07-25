---
name: _spec5_qa_acceptance
description: Đặc tả Tiêu chuẩn nghiệm thu (Acceptance Criteria - Gherkin), Ma trận Edge Cases, Quy tắc Validation và QA Checklist cho QA Handoff và AI Test Agents.
---

# Acceptance Criteria & QA Specification (`_spec5_qa_acceptance`)

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-24  

---

## 1. Mục đích & Phạm vi

Skill này chịu trách nhiệm đặc tả toàn bộ tiêu chuẩn nghiệm thu (Acceptance Criteria), kịch bản kiểm thử (Test Scenarios), ma trận các trường hợp biên/ngoại lệ (Edge Cases Matrix) và danh mục kiểm thử bàn giao (QA Checklist).

### Đầu ra chính (Outputs):
1. **Acceptance Criteria (Cú pháp Gherkin Given-When-Then):** Các tiêu chí rõ ràng, không mơ hồ để xác định tính năng đã hoàn thành.
2. **Edge Cases & Negative Testing Matrix:** Các kịch bản lỗi mạng, nhập sai định dạng, vượt giới hạn bộ nhớ, race condition, và vi phạm quyền truy cập.
3. **Data Validation Rules:** Quy tắc kiểm tra tính hợp lệ dữ liệu ở cả Frontend và Backend.
4. **Machine-Readable QA Suite Spec (Dành cho AI Test Agent):** Cấu trúc kịch bản kiểm thử chuẩn hóa để **AI Test Execution Agent có thể sinh trực tiếp các tệp E2E / Integration test (như Playwright, Cypress, Jest, PyTest)** mà không cần viết thủ công.

---

## 2. Quy trình Thực hiện Đặc tả QA (4 Bước)

### Bước 1 — Viết Acceptance Criteria bằng cú pháp Gherkin
Mọi User Story / Feature đều phải có ít nhất 1 kịch bản Gherkin chuẩn:
```gherkin
Scenario: Đăng nhập thành công với thông tin hợp lệ
  Given Người dùng đang ở màn hình Đăng nhập
  When Người dùng nhập email "user@example.com" và mật khẩu "Password123"
  And Người dùng bấm nút "Đăng nhập"
  Then Hệ thống chuyển hướng tới màn hình Dashboard
  And Hiển thị thông báo chào mừng "Xin chào user@example.com"
```

### Bước 2 — Mổ xẻ Ma trận Edge Cases & Negative Scenarios
Liệt kê các kịch bản bất thường:
- **Boundary Testing:** Nhập 0 ký tự, 1 ký tự, 255 ký tự, 256 ký tự.
- **Concurrency & Race Conditions:** Bấm Submit 5 lần liên tiếp trong 100ms.
- **Network Failure:** Đang gửi API thì đứt mạng (Offline mode / Timeout).

### Bước 3 — Xây dựng Bảng Quy tắc Validation (Client vs Server)
| Field | Client Validation | Server Validation | Error Message |
| :--- | :--- | :--- | :--- |
| `email` | Format Regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` | Unique DB Check | `"Email không hợp lệ hoặc đã tồn tại."` |
| `password` | Length >= 8 | Hash check bcrypt | `"Mật khẩu phải có ít nhất 8 ký tự."` |

### Bước 4 — Đóng gói QA Handoff Checklist
Danh mục kiểm thử nhanh trước khi duyệt Release:
- [ ] Cross-browser (Chrome, Safari, Firefox)
- [ ] Mobile Responsiveness (iOS & Android views)
- [ ] Accessibility (Contrast ratio >= 4.5:1, Keyboard Navigation)
- [ ] Performance (Page load < 2.0s, API response < 500ms)

---

## 3. Template Mẫu Output Spec QA & Acceptance

```markdown
# QA & Acceptance Spec: [Tên Feature]

> **Target Audience:** QA Tester, Dev, Product Owner, AI Test Execution Agent  

## 1. Acceptance Criteria (Gherkin Scenarios)

### Scenario 1: Tạo mới dự án thành công (Happy Path)
```gherkin
Feature: Tạo mới dự án trong Workspace

  Scenario: Tạo dự án riêng tư thành công
    Given Người dùng đã đăng nhập với vai trò "Admin"
    And Người dùng đang ở đường dẫn "/projects/new"
    When Người dùng nhập tên dự án "Chiến dịch Q3"
    And Chọn chế độ riêng tư "PRIVATE"
    And Bấm nút "Tạo dự án"
    Then API "POST /api/v1/projects" trả về status 201
    And Người dùng được chuyển hướng đến "/projects/chi-en-dich-q3"
    And Dự án "Chiến dịch Q3" xuất hiện trong danh sách dự án
```

### Scenario 2: Tạo dự án trùng tên (Negative Path)
```gherkin
  Scenario: Nhập tên dự án đã tồn tại
    Given Dự án "Chiến dịch Q3" đã tồn tại trong workspace
    When Người dùng nhập tên dự án "Chiến dịch Q3" và bấm "Tạo dự án"
    Then API trả về lỗi HTTP 409 với code "PROJECT_TITLE_DUPLICATE"
    And Nút "Tạo dự án" quay lại trạng thái Active
    And Hiển thị thông báo inline đỏ: "Tên dự án đã tồn tại trong Workspace này"
```

## 2. Edge Case Matrix

| ID | Edge Case Scenario | Mong đợi Xử lý của Hệ thống | Mức độ Ưu tiên |
| :--- | :--- | :--- | :--- |
| `EC01` | User bấm Submit 10 lần liên tục | Nút Submit tự động `disabled` ngay lần bấm đầu tiên | High |
| `EC02` | Mất kết nối internet khi đang gửi API | Hiển thị Toast banner: `"Mất kết nối mạng. Đang tự động thử lại..."` | Medium |
| `EC03` | Nhập tên dự án chứa ký tự đặc biệt XSS `<script>` | Sanitize input, lưu dạng text thuần, không trigger script | Critical |

---

## 4. Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-24):** Cập nhật tên skill thành `_spec5_qa_acceptance` chuẩn hóa Acceptance Criteria (Gherkin), Edge Cases Matrix, và QA Automation Handoff cho AI Test Execution Agents.
