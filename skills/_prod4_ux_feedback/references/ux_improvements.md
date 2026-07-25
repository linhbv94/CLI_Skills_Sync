# Product UX UI Improvements Specification (Yêu cầu Cải tiến UX/UI)

Tài liệu này tổng hợp các đề xuất cải tiến UI/UX chi tiết từ việc phân tích feedback người dùng, sẵn sàng để bàn giao cho Designer hoặc Developer thiết kế và code.

---

## 🛠️ Danh sách Hạng mục Cải tiến UX/UI

### [Hạng mục mẫu] Tối ưu hóa UI/UX và Microcopy luồng Chọn Band mục tiêu (Onboarding Step 3)
* **Mã sự kiện liên quan:** `onboarding_step_viewed`, `onboarding_step_submitted` (step_number = 3)
* **Điểm đau (Pain Point):** Người dùng bối rối vì không hiểu band điểm IELTS là gì (đối với người mới bắt đầu học). Ma sát cao dẫn tới 30% người dùng out khỏi app tại bước này.
* **Đề xuất Giải pháp:**
  * **Thay đổi Layout:** Thêm nút tooltip giải thích nhỏ bên cạnh các lựa chọn band điểm (ví dụ: "Band 6.5 là gì?").
  * **Thay đổi Microcopy:**
    * *Cũ:* "Select your target band score."
    * *Mới:* "Mục tiêu điểm IELTS của bạn là bao nhiêu? (Nếu chưa rõ, bạn có thể chọn 'Không bắt buộc')"
  * **Metric kỳ vọng:** Tăng tỷ lệ hoàn thành Onboarding lên > 70%.
  * **Dev Status:** Chưa cài 🔴
  * **Product Test:** Chưa test 🟡
