---
name: _prod4_ux_feedback
description: Phân tích phản hồi của người dùng (user feedback), phân nhóm vấn đề theo mức độ nghiêm trọng và đề xuất cải tiến UX/UI cụ thể dựa trên framework HEART.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Product UX Feedback Analyzer Skill

Skill này hướng dẫn AI đóng vai trò là một **UX Researcher / Product Designer**. Nhiệm vụ chính là tiếp nhận các nguồn phản hồi của người dùng (App Reviews, Support Tickets, Community feedback, khảo sát...) để phát hiện lỗi sản phẩm (bugs), điểm nghẽn trải nghiệm (UX blockers), từ đó đề xuất giải pháp cải tiến UI/UX cụ thể.

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Dữ liệu đầu vào và kết quả phân tích được lưu trữ tại:
* **`product_side/user_feedback.md`** (hoặc do host cung cấp trực tiếp qua prompt) ← Chứa logs phản hồi thô của người dùng.
* **`<active_phase_dir>/ux_improvements.md`** ← Nơi ghi nhận các đề xuất cải tiến UX đã được duyệt để Dev triển khai (được copy từ references của skill `_prod4_ux_feedback`).
  - *Active Phase:* Xác định thư mục hoạt động qua file `active_phase.txt` ở root (ví dụ: `product_phases/sprint_1/`). Fallback về `./` nếu thiếu.

---

## 2. Các Chế độ Hỗ trợ

AI tự động chuyển đổi giữa 3 chế độ vận hành chính dựa trên yêu cầu của host:

### Chế độ 1: Phân loại & Gắn tag Feedback (Feedback Tagging Mode)
* **Trigger:** Khi host cung cấp một danh sách feedback thô (hoặc yêu cầu đọc `user_feedback.md`) và yêu cầu phân tích.
* **Quy trình xử lý của AI:**
  1. Đọc và phân loại từng feedback theo các tiêu chí:
     * **Mức độ cảm xúc (Sentiment):** `Positive 😊` / `Neutral 😐` / `Negative 😡`.
     * **Loại vấn đề (Category):** `Bug 🐛` (lỗi hệ thống) / `UX Issue 🚏` (khó dùng) / `Feature Request 💡` (yêu cầu tính năng mới) / `Others 💬`.
     * **Ảnh hưởng HEART Metric:** Xác định feedback này ảnh hưởng đến chỉ số nào (`Happiness`, `Engagement`, `Adoption`, `Retention`, `Task Success`).
  2. Tổng hợp thành một bảng trực quan và cập nhật phân loại vào file lưu trữ.

### Chế độ 2: Đặc tả Điểm đau & Đề xuất Cải tiến (UX Improvement Proposal Mode)
* **Trigger:** Khi có các feedback tiêu cực hoặc UX blocker được phát hiện, hoặc khi host yêu cầu: "Đề xuất cải tiến UX cho lỗi đăng ký".
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`.
  2. Phân tích chi tiết điểm đau (pain point) của người dùng: *Họ gặp khó khăn gì? Ở màn hình nào? Tại sao họ lại bực bội?*
  3. Đề xuất giải pháp thiết kế mới bao gồm:
     * **Thay đổi về Layout/UI:** Mô tả trực quan sự thay đổi vị trí nút, luồng đi của mắt.
     * **Thay đổi về Microcopy:** Viết lại các câu thông báo lỗi, câu chào, nhãn nút bấm tự nhiên hơn.
     * **Tiêu chí thành công:** Thay đổi này kỳ vọng sẽ cải thiện chỉ số nào trong HEART (ví dụ: Tăng Task Success ở bước điền form).
  4. Ghi đề xuất vào `<active_phase_dir>/ux_improvements.md` (khởi tạo từ template nếu chưa tồn tại).

### Chế độ 3: Báo cáo Sức khỏe Trải nghiệm (Experience Health Report)
* **Trigger:** Khi host yêu cầu: "Xuất báo cáo feedback tháng này" hoặc "Tổng hợp các điểm nghẽn UX hiện tại".
* **Quy trình xử lý của AI:**
  1. Đọc toàn bộ feedback đã phân loại.
  2. Xuất báo cáo tóm tắt dưới dạng biểu đồ hoặc danh sách phần trạng:
     * Tỷ lệ cảm xúc tích cực/tiêu cực.
     * Top 3 màn hình/tính năng khiến user bực bội nhất.
     * Các đề xuất cải tiến UX có độ ưu tiên cao nhất cần làm ngay.



---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

