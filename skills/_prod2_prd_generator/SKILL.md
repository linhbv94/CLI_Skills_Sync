---
name: _prod2_prd_generator
description: Hỗ trợ viết, cập nhật và đồng bộ tài liệu PRD (Master PRD và Child PRD) chuẩn hóa dựa trên các template có sẵn, phân tích nghiệp vụ, thiết kế giao diện UI/UX và thiết lập data tracking events.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Hướng dẫn Vận hành Skill: prod5_prd_generator

Kỹ năng này hướng dẫn AI Agent cách viết, cập nhật và đồng bộ tài liệu PRD (Product Requirement Document) cho sản phẩm ở hai cấp độ: **Master PRD** (Tổng thể sản phẩm) và **Child PRD** (Chi tiết tính năng), dựa trên các template chuẩn hóa trong dự án.

---

## 1. Nguyên tắc Tổng quan

*   **Đọc hiểu bối cảnh:** Trước khi tạo hoặc sửa bất kỳ tài liệu PRD nào, Agent phải tìm đọc các file cấu hình và hồ sơ sản phẩm ở root (ví dụ: `active_phase.txt` để xác định phase hiện tại, `2_marketing_campaign/inputs/product_profile.md` nếu có để hiểu về định vị sản phẩm).
*   **Văn phong & Ngôn ngữ:** Tuân thủ quy định ngôn ngữ (Tiếng Việt chuyên nghiệp, rõ ràng, gãy gọn; giữ nguyên các thuật ngữ kỹ thuật tiếng Anh phổ biến như *event, property, tracking, dev, QA, flow, user property, API*).
*   **Tính nhất quán:** Mọi ID yêu cầu (FR, NFR, BR, AC, SE, RAA) trong tài liệu phải được đánh số tăng dần và liên kết logic với nhau (ví dụ: AC phải ánh xạ cụ thể đến FR nào).
*   **Yêu cầu kỹ thuật & Quyền quyết định của Dev:** Đối với các yêu cầu phi chức năng (NFR) hoặc luồng xử lý hệ thống (Mechanism & System Flows), bắt buộc phải gắn kèm ghi chú làm rõ: *"Đây là đề xuất hướng xử lý từ góc độ Product, còn lại Đội ngũ Lập trình (Dev) có toàn quyền quyết định phương án triển khai kỹ thuật cuối cùng."*
*   **Vị trí lưu trữ:**
    *   **Master PRD** luôn được đặt cố định tại: `1_product_requirements/_master_prd.md`.
    *   **Kế hoạch Tracking (Tracking Plan)** luôn được đặt cố định tại: `3_product_analytics/_tracking_plan.md`.
    *   **Các Child PRD** (đặc tả tính năng chi tiết) luôn được đặt cố định tại thư mục: `1_product_requirements/` (ví dụ: `1_product_requirements/prd_cms.md`, `1_product_requirements/prd_practice.md`).
    *   Tất cả tên tệp và thư mục phải tuân thủ **snake_case**, không dùng khoảng trắng và không dùng dấu gạch ngang `-`.

---

## 2. Quy trình Thực hiện Nhiệm vụ

### Chế độ 1: Tạo mới / Cập nhật Master PRD
Khi được yêu cầu viết Master PRD cho sản phẩm:
1.  **Đọc Template tham chiếu:** Xem cấu trúc chuẩn tại [references/master_prd_template.md](references/master_prd_template.md).
2.  **Thu thập dữ liệu đầu vào:** Hỏi User hoặc tự động đọc các file liên quan để làm rõ:
    *   *Vision, North Star & Success Metrics* (mục tiêu cốt lõi và các chỉ số đo lường chính/phụ).
    *   *Problem Statement & Chân dung người dùng* (Primary/Secondary User).
    *   *Acquisition Channels, Aha Moment & Monetization Strategy* (Chiến lược tăng trưởng & Kinh doanh).
    *   *High-level User Journey & Product Loop*.
3.  **Lập danh sách tính năng (Functional Requirements):** Liệt kê các tính năng lớn cần làm và gán sẵn link tương đối đến các Child PRD sẽ có trong tương lai.
4.  **Xác định Rủi ro & Giả định:** Thiết lập bảng RAA (Risks, Assumptions, Actions) để quản trị rủi ro ngay từ đầu.
5.  **Tạo tệp tin:** Ghi nội dung ra file Markdown và trả về đường dẫn cùng cấu trúc tệp cho User.

### Chế độ 2: Tạo mới / Cập nhật Child PRD (Tính năng chi tiết)
Khi được yêu cầu viết đặc tả chi tiết cho một tính năng (Child PRD):
1.  **Đọc Template tham chiếu:** Xem cấu trúc chuẩn tại [references/child_prd_template.md](references/child_prd_template.md).
2.  **Đặc tả UI/UX & UI States:**
    *   Yêu cầu hoặc mô tả luồng đi của màn hình (User Flow).
    *   **Bắt buộc** định nghĩa rõ 5 trạng thái giao diện: *Default, Empty, Loading, Error, và Validation* để Dev/Designer thực thi.
3.  **Phân rã Yêu cầu kỹ thuật:**
    *   *Functional Requirements (FR):* Định dạng bằng bảng rõ ràng.
    *   *Non-Functional Requirements (NFR):* Hiệu năng, bảo mật, hạ tầng.
    *   *Business Rules (BR):* Các ràng buộc logic của nghiệp vụ (ví dụ: OTP hết hạn sau 5 phút).
4.  **Thiết lập Yêu cầu Đo lường (Data Tracking):**
    *   Định nghĩa rõ các Event cần track: *Event Name, Trigger Condition, Properties* đi kèm và *Purpose* (Mục đích).
    *   Bước này phải liên kết chặt chẽ với skill `prod4_tracking_plan` để đồng bộ event list.
5.  **Viết Tiêu chí Nghiệm thu (Acceptance Criteria - AC):**
    *   Viết AC theo chuẩn **Given-When-Then** (Gherkin format) để QA dễ dàng chuyển đổi thành Test Case.
6.  **Xác định Edge Cases & Error Handling:** Liệt kê các tình huống bất thường (mất mạng, lỗi API...) và cách hệ thống xử lý để bảo vệ trải nghiệm người dùng.
7.  **Đánh số thứ tự các phần diễn giải đặc thù & Tịnh tiến chỉ mục (Quy tắc N):**
    *   *Trường hợp tính năng phức tạp (cần diễn giải chi tiết như phân quyền admin CMS, thuật toán, cơ chế offline...):*
        *   Tạo một hoặc nhiều mục diễn giải chi tiết bắt đầu từ số 4 (ví dụ: `## 4. Phân quyền Admin CMS`, `## 5. Cơ chế lưu trữ offline`).
        *   Đặt `N` là số thứ tự của phần diễn giải cuối cùng đó (ví dụ: nếu có 2 phần diễn giải thì `N = 5`).
        *   Các phần tiếp theo sẽ tự động tịnh tiến theo công thức: `## [N+1]. Mechanism & System Flows` (và các tiểu mục tương ứng là `### [N+1].1`, `### [N+1].2`), `## [N+2]. Edge Cases & Error Handling`, `## [N+3]. Data Tracking Requirements`, `## [N+4]. Acceptance Criteria`, `## [N+5]. Future Enhancements`, `## [N+6]. Dependencies & Open Questions`, `## [N+7]. Version History & Changelog`.
    *   *Trường hợp tính năng đơn giản (không cần phần diễn giải đặc thù):*
        *   Bỏ qua toàn bộ các section diễn giải đặc thù này (tương đương `N = 3`).
        *   Mục tiếp theo sẽ là `## 4. Mechanism & System Flows` (và các tiểu mục là `### 4.1`, `### 4.2`), sau đó là `## 5. Edge Cases & Error Handling`, v.v.

### Chế độ 3: Quy trình Cập nhật & Tổng hợp Tính năng Sprint (Sprint Editing Workflow)
Khi có các yêu cầu chỉnh sửa hoặc cập nhật tính năng cho sprint mới, Agent phải tuân thủ nghiêm ngặt quy trình 3 bước sau đây:
1.  **Bước 1: Tập hợp dữ liệu thô (Scattered Information Collection):**
    *   Đọc và tổng hợp toàn bộ thông tin ghi chú rời rạc, yêu cầu mới của sprint vào một file tập trung (mặc định là `next_sprint.md` ở root).
2.  **Bước 2: Cập nhật PRDs (PRD Synchronization):**
    *   Phân tách các thông tin thô từ `next_sprint.md` và cập nhật về đúng các Child PRD của từng module tương ứng (ví dụ: yêu cầu CMS cập nhật vào `prd_cms.md`, yêu cầu Shadowing/Practice cập nhật vào `prd_practice.md`, yêu cầu Mixpanel cập nhật vào `_tracking_plan.md`).
    *   **Cập nhật đồng thời vào Master PRD** để đảm bảo tính đồng bộ tổng thể và tầm nhìn toàn dự án không bị đứt gãy.
    *   *Quy tắc*: Các yêu cầu phi chức năng (NFR) hoặc luồng xử lý (Mechanism) phải đi kèm ghi chú phân rõ quyền quyết định kỹ thuật của Dev.
3.  **Bước 3: Tạo Tài liệu Tổng quan Sprint (Sprint Overview Generation):**
    *   Tổng hợp và viết lại toàn bộ nội dung thay đổi, cập nhật của sprint đó vào một tệp tổng quan kỹ thuật dưới dạng file bàn giao (ví dụ: `plane_task/overview_[MMDD].md`).

---

## 3. Đồng bộ lên Google Docs (Quy tắc Bắt buộc)

Khi User yêu cầu đồng bộ nội dung PRD (.md) lên Google Docs, Agent phải thực hiện theo quy trình tối ưu hóa RPC sau đây:

1.  **Đọc cấu hình bảo mật:** Đọc file `~/.gemini/config/google_apps_script.json` (Windows: `C:\Users\<username>\.gemini\config\google_apps_script.json`) để lấy `web_app_url` và `khoa`.
2.  **Biên dịch mã (Eval Architecture):**
    *   Tuyệt đối **không gọi API rời rạc** để thêm từng dòng (gây chậm và dễ timeout).
    *   Biên dịch toàn bộ cấu trúc file MD thành một đoạn mã Google Apps Script động duy nhất chứa các lệnh thao tác trực tiếp trên server-side (ví dụ: `body.appendParagraph()`, `body.appendTable()`).
    *   Đóng gói đoạn mã này vào trường `ma` của payload JSON kèm trường xác thực `khoa`.
3.  **Quy chuẩn Định dạng (Styling Rules):**
    *   *Phông chữ:* Thống nhất **Arial** cho toàn bộ tài liệu.
    *   *Tiêu đề 1 (H1):* Cỡ 18, Bold, Navy (#1a365d), giãn dòng 1.3.
    *   *Tiêu đề 2 (H2):* Cỡ 13, Bold, Teal (#2c7a7b), giãn dòng 1.2.
    *   *Tiêu đề 3 (H3):* Cỡ 11, Bold, Xám đậm (#2d3748), giãn dòng 1.15.
    *   *Văn bản & Danh sách:* Cỡ 10.5, Xám đậm (#2d3748), giãn dòng 1.15.
    *   *Bảng biểu:* Viền mảnh xám (#cbd5e0, 0.75), Header row nền xám nhạt (#edf2f7), chữ in đậm.
    *   *Inline Code:* Phông Arial, cỡ 9.5, chữ xám đậm, nền xám nhạt (#edf2f7).
    *   *Tối ưu hóa:* Gom các thuộc tính lại và cập nhật bằng `setAttributes(attrs)` để giảm thiểu RPC calls trên server.
4.  **Dọn dẹp & Chống Timeout:**
    *   Với file PRD lớn, chia nhỏ nội dung gửi tuần tự bằng các action: `start` (đặt text tạm `TEMP_REPLACE_ME`), `append` (chèn tiếp nội dung), và `end` (tìm và xóa paragraph `TEMP_REPLACE_ME` ở vị trí đầu tài liệu).
5.  **Ghi nhớ Doc ID:**
    *   Khi sync thành công, nếu file `.md` cục bộ chưa có metadata Google Doc ID ở đầu file, Agent phải tự động ghi thêm dòng `Google Doc ID: [ID]` dưới tiêu đề chính hoặc phần Document Control để phục vụ cho các lần tự động sync tiếp theo.
6.  **Gửi dữ liệu qua Web App URL:**
    *   Sử dụng PowerShell (`Invoke-RestMethod`) hoặc `curl` tùy HĐH.
    *   **Lưu ý Encoding:**
        *   *PowerShell:* Phải chuyển payload string thành UTF-8 byte array (`[System.Text.Encoding]::UTF8.GetBytes($payload)`) trước khi gửi qua `-Body` và chỉ định `-ContentType 'application/json; charset=utf-8'`.
        *   *curl:* Dùng `--data-binary` thay vì `-d` để giữ nguyên byte UTF-8 và truyền header `-H "Content-Type: application/json; charset=utf-8"`.

---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

