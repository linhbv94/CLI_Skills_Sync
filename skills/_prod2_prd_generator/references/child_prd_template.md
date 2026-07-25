# PRD: [Tên tính năng / Module]

---

## DOCUMENT CONTROL

*   **Google Doc ID:** `xxx`
*   **Tab ID:** `xxx`
*   **Parent Master PRD:** [Link đến Master PRD tương ứng](master_prd_template.md)

---

## 1. Overview & Context
*   **Mục tiêu tính năng:** [Tại sao làm tính năng này? Nó giải quyết nỗi đau nào của user hoặc đóng góp gì vào KPIs sản phẩm?]
*   **Đối tượng sử dụng:** [Ai sẽ dùng tính năng này?]

---

## 2. UI/UX Design & User Flow

### 2.1 Figma Link & Assets
*   **Design Link:** [Link Figma dẫn trực tiếp đến Frame/Screen của tính năng này]
*   **Assets:** [Link thư mục chứa icon, ảnh, hoặc tài nguyên thiết kế cần thiết]

### 2.2 User Flow / User Journey
*Mô tả luồng đi của user qua từng màn hình bằng text hoặc sơ đồ.*

`Trạng thái bắt đầu` $\rightarrow$ `Hành động của User` $\rightarrow$ `Màn hình tiếp theo` $\rightarrow$ `Kết quả mong muốn`

### 2.3 UI States Requirements (Yêu cầu trạng thái giao diện)
*Đặc tả giao diện cho từng trạng thái bắt buộc:*
*   **Default State:** Giao diện chuẩn khi có đầy đủ dữ liệu.
*   **Empty State:** Hiển thị màn hình trống kèm nút gợi ý hành động khi chưa có dữ liệu.
*   **Loading State:** Hiển thị Skeleton Loader hoặc Spinner khi đang tải dữ liệu.
*   **Error State:** Thông báo lỗi thân thiện khi API lỗi hoặc mất kết nối mạng.
*   **Validation State:** Hiển thị thông báo đỏ báo lỗi nhập liệu ngay dưới trường nhập (inline validation).

---

## 3. Requirements

### 3.1 Functional Requirements (FR)
*Đặc tả chi tiết các yêu cầu chức năng.*

| ID | User Role | Action / Behavior | Expected System Response | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | User | Click nút "Đăng ký" | Kiểm tra thông tin, nếu hợp lệ thì lưu DB và chuyển sang trang Onboarding | Must-have |
| **FR-02** | ... | ... | ... | ... |

### 3.2 Non-Functional Requirements (NFR)
*Đặc tả các yêu cầu phi chức năng.*

*   **NFR-01 (Performance):** Tốc độ phản hồi API khi submit form không quá 2 giây.
*   **NFR-02 (Security):** Toàn bộ thông tin nhạy cảm (mật khẩu, số điện thoại) phải được mã hóa trước khi truyền tải.

### 3.3 Business Rules (BR)
*Các quy tắc nghiệp vụ/ràng buộc logic cần tuân thủ.*

*   **BR-01:** Mỗi số điện thoại chỉ được đăng ký tối đa 1 tài khoản trên hệ thống.
*   **BR-02:** Mã OTP có hiệu lực trong vòng 5 phút và chỉ được gửi lại sau tối thiểu 60 giây.

---

## [Optional] 4. [Detailed Section Name] (Ví dụ: Phân quyền Admin, Cơ chế đồng bộ...)
*Mục này chỉ xuất hiện khi tính năng phức tạp, cần diễn giải sâu về mặt nghiệp vụ hoặc logic đặc thù.*
*Nếu cần thêm các phần diễn giải đặc thù khác, hãy tiếp tục đánh số ## 5. [Tên phần tiếp theo], và đặt N = [Số thứ tự của phần diễn giải cuối cùng].*
*Nếu tính năng đơn giản và không cần phần diễn giải đặc thù nào, hãy bỏ qua hoàn toàn mục này (khi đó đặt N = 3).*

---

## [N+1]. Mechanism & System Flows
*Cách hệ thống xử lý ngầm đằng sau giao diện.*
*(Lưu ý: Nếu không có phần diễn giải đặc thù ở trên thì N = 3, mục này sẽ là ## 4. Mechanism & System Flows và các tiểu mục là ### 4.1, ### 4.2)*

### [N+1].1 Luồng nghiệp vụ (Business Logic Flowchart)
*Sử dụng Mermaid hoặc vẽ sơ đồ mô tả thuật toán xử lý dữ liệu.*

### [N+1].2 Luồng hệ thống (System Interaction / API Sequence)
*Mô tả cách Client tương tác với Server và các dịch vụ bên thứ ba (Third-party).*

---

## [N+2]. Edge Cases & Error Handling
*Các tình huống ngoại lệ phát sinh ngoài luồng chính và cách hệ thống tự phục hồi. (Nếu N = 3 thì mục này là ## 5)*

| ID | Scenario (Tình huống ngoại lệ) | System Response (Cách xử lý của hệ thống) |
| :--- | :--- | :--- |
| **EC-01** | User đang điền form thì bị mất kết nối mạng | Lưu nháp dữ liệu vào LocalStorage, hiển thị thông báo offline và khôi phục khi có mạng |
| **EC-02** | Người dùng gửi yêu cầu OTP liên tiếp 5 lần | Khóa chức năng gửi OTP của số điện thoại đó trong 15 phút, hiển thị thông báo lý do |

---

## [N+3]. Data Tracking Requirements (Yêu cầu đo lường)
*Đặc tả các sự kiện cần bắn về hệ thống Analytics để đo lường hiệu quả tính năng. (Nếu N = 3 thì mục này là ## 6)*

| Event Name | Trigger Condition | Properties (Thuộc tính đi kèm) | Purpose (Mục đích) |
| :--- | :--- | :--- | :--- |
| `click_register_button` | Khi user click vào nút Đăng ký | `source_screen` (string), `device_type` (string) | Đo lường tỷ lệ bắt đầu đăng ký |
| `register_success` | Khi hệ thống tạo tài khoản thành công | `user_id` (string), `registration_method` (email/phone) | Đo tỷ lệ chuyển đổi đăng ký thành công |

---

## [N+4]. Acceptance Criteria (Tiêu chí nghiệm thu)
*Định rõ tiêu chuẩn để kiểm thử viên (QA) duyệt hoàn thành tính năng. (Nếu N = 3 thì mục này là ## 7)*

*   **AC-01 (Đăng ký thành công):**
    *   **Given:** Người dùng đang ở màn hình Đăng ký và đã nhập đúng, đủ thông tin.
    *   **When:** Người dùng click nút "Đăng ký".
    *   **Then:** Hệ thống tạo tài khoản mới trong cơ sở dữ liệu, gửi email chào mừng và chuyển hướng người dùng đến màn hình Onboarding trong vòng 2 giây.

---

## [N+5]. Future Enhancements (Nâng cấp tương lai)
*(Nếu N = 3 thì mục này là ## 8)*
*Các ý tưởng hoặc tính năng mở rộng của riêng module này sẽ được đánh giá và triển khai ở các phase sau.*

*   **Idea 1:** [Ví dụ: Bổ sung nút Pause/Resume chương trình khuyến mại để quản trị viên linh hoạt dừng chiến dịch đột xuất]
*   **Idea 2:** [Ví dụ: Tích hợp báo cáo tự động gửi qua Slack khi có mã khuyến mại đạt giới hạn lượt dùng]

---

## [N+6]. Dependencies & Open Questions
*(Nếu N = 3 thì mục này là ## 9)*

*   **Dependencies (Phụ thuộc):** Tính năng này phụ thuộc vào API Xác thực (Auth API) đang được phát triển ở sprint này.
*   **Open Questions (Câu hỏi còn bỏ ngỏ):** Có nên tích hợp đăng nhập nhanh bằng Google/Apple ngay trong phase này hay không?

---

## [N+7]. Version History & Changelog
*(Nếu N = 3 thì mục này là ## 10)*

| Version | Date | Author | Description of Changes | Status |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | [DD/MM/YYYY] | [Tên người viết] | Initial Draft | Draft / Under Review / Approved |

