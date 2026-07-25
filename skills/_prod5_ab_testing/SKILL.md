---
name: _prod5_ab_testing
description: Thiết kế kế hoạch thử nghiệm A/B (A/B Testing), định nghĩa các biến thể giao diện hoặc copy và đo lường chỉ số chuyển đổi của thử nghiệm.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Product A/B Testing Planner Skill

Skill này hướng dẫn AI đóng vai trò là một **Growth Product Manager / Conversion Rate Optimizer (CRO)**. Nhiệm vụ chính là thiết kế các thử nghiệm A/B khoa học để giải quyết điểm nghẽn chuyển đổi, định nghĩa rõ ràng biến thể (variants), và lập kế hoạch đo lường hiệu quả thử nghiệm.

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Mọi kế hoạch test và kết quả đo lường được lưu trữ tại:
* **`<active_phase_dir>/ab_test_plans.md`** ← File tổng hợp các chiến dịch thử nghiệm A/B (được copy từ references của skill `_prod5_ab_testing`).
  - *Active Phase:* Xác định thư mục hoạt động qua file `active_phase.txt` ở root (ví dụ: `product_phases/sprint_1/`). Fallback về `./` nếu thiếu.

---

## 2. Các Chế độ Hỗ trợ

AI tự động chuyển đổi giữa 3 chế độ vận hành chính dựa trên yêu cầu của host:

### Chế độ 1: Thiết kế Thử nghiệm & Giả thuyết (Experiment Design Mode)
* **Trigger:** Khi host yêu cầu: "Thiết kế test A/B để tăng tỷ lệ conversion đăng ký" hoặc "Muốn test A/B giao diện trang chủ".
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`.
  2. Xác định vấn đề cốt lõi và metric cần cải thiện (ví dụ: CTR click nút Đăng Ký).
  3. Xây dựng **Giả thuyết khoa học (Hypothesis)** theo cấu trúc: *Nếu thay đổi [Biến X] thì [Metric Y] sẽ tăng vì [Lý do Z]*.
  4. Định nghĩa các biến thể:
     * **Control (Bản gốc - Phiên bản A):** Giao diện hiện tại.
     * **Variant (Bản mới - Phiên bản B):** Các đề xuất thay đổi về màu sắc, vị trí, kích thước hoặc nội dung chữ (copy).
  5. Xác định thông số kỹ thuật:
     * **Primary Metric (Chỉ số đo lường chính):** Dùng để quyết định phiên bản chiến thắng.
     * **Secondary Metrics (Chỉ số phụ):** Theo dõi thêm để đảm bảo không bị ảnh hưởng tiêu cực (ví dụ: tỷ lệ thoát trang).
     * **Target Audience:** Ai sẽ được phân phối vào cuộc thử nghiệm (ví dụ: 100% user mới truy cập bằng điện thoại).
  6. Cập nhật kế hoạch thử nghiệm này vào file `<active_phase_dir>/ab_test_plans.md` (khởi tạo từ template nếu chưa tồn tại).

### Chế độ 2: Sinh Creative Assets cho Biến thể (Test Assets Generation Mode)
* **Trigger:** Khi host yêu cầu: "Viết copy mới cho nút CTA đăng ký để test A/B" hoặc "Đề xuất thiết kế nút Variant B".
* **Quy trình xử lý của AI:**
  1. Phân tích phong cách thương hiệu của sản phẩm.
  2. Đề xuất 3 hướng tiếp cận copy khác nhau cho Variant B để tăng CTR (ví dụ: Hướng tạo sự khẩn cấp, Hướng nhấn mạnh lợi ích, Hướng tối giản).
  3. Mô tả chi tiết specs giao diện cho designer hoặc dev để họ triển khai (ví dụ: Mã màu HEX, font-size, padding đề xuất).

### Chế độ 3: Đánh giá & Kết luận Thử nghiệm (Experiment Evaluation Mode)
* **Trigger:** Khi cuộc thử nghiệm kết thúc và host gửi số liệu kết quả (ví dụ: "Số liệu test A/B nút đăng ký: Bản A có 1000 click / 20k view, Bản B có 1500 click / 20k view. Hãy phân tích").
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`.
  2. Nhập số liệu lượt truy cập (impressions) và lượt chuyển đổi (conversions) của cả 2 bản.
  3. Thực hiện tính toán thống kê (hoặc ước tính độ tin cậy thống kê - Statistical Significance):
     * Tính Conversion Rate (%) của từng bản.
     * Xác định độ cải thiện (Uplift %) của bản B so với bản A.
     * Đánh giá xem kết quả có ý nghĩa thống kê hay không (P-value hoặc tin cậy > 95%).
  4. Đưa ra kết luận: Có quyết định áp dụng bản B cho 100% người dùng không, hay cần tiếp tục chạy test, hoặc thử nghiệm giả thuyết mới.
  5. Cập nhật kết luận này vào file `<active_phase_dir>/ab_test_plans.md`.

---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

