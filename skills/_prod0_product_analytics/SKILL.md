---
name: _prod0_product_analytics
description: Quản lý tổng quan dữ liệu phân tích sản phẩm (Product Analytics Core Coordinator). Tự động đọc brief số liệu thô (từ Mixpanel/Amplitude) theo phase/sprint để tạo báo cáo sức khỏe sản phẩm, phát hiện điểm nghẽn (bottleneck) và kết nối chỉ đạo cho các skill khác ở Product Side.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Product Analytics Core Coordinator Skill

Skill này đóng vai trò là **Bộ não Điều phối (Core Coordinator)** cho toàn bộ hoạt động bên Product Side. Nhiệm vụ chính là nhận dữ liệu thô từ các công cụ đo lường (như Mixpanel, Amplitude), phân tích hiệu quả vận hành của sản phẩm qua từng Sprint/Phase, chỉ ra điểm nghẽn trải nghiệm (UX bottleneck) và kích hoạt các skill chuyên biệt khác để xử lý.

---

## 1. Cấu trúc Tài nguyên & Phân tách Cấp độ

Skill này liên kết dữ liệu ở 2 cấp độ:

### A. Cấp độ Dự án (Project-level - Cố định)
* **`prd.md`** hoặc **`product_side/prd.md`**: Yêu cầu sản phẩm, để AI hiểu luồng tính năng lý thuyết.
* **`_tracking_plan.md`**: Kế hoạch đo lường sự kiện, để biết sự kiện nào map với chỉ số nào.
* **[mixpanel_mapping.md](./references/mixpanel_mapping.md)**: Hướng dẫn map các sự kiện thô từ Mixpanel vào phễu sản phẩm.
* **[standard_funnels.md](./references/standard_funnels.md)**: Các phễu đo lường tiêu chuẩn (Activation, Onboarding, Feature Retention).

### B. Phân tách Cấp độ Tài liệu
* **Tài liệu đầu não (Cố định ở `3_product_analytics/`):**
  - `product_metrics.md` ← Nhật ký lưu trữ chỉ số tích lũy qua tất cả Phase/Sprint.
  - `product_overview.md` ← Báo cáo tổng hợp sức khỏe sản phẩm và bài học kinh nghiệm dài hạn.
* **Tài liệu vận hành (Động ở thư mục phase `<active_phase_dir>/`):**
  - `<active_phase_dir>/analytics_input.md` ← Brief đầu vào chứa số liệu thô Mixpanel/Amplitude của phase đó.

---

## 2. Các Chế độ Hỗ trợ

AI tự động chuyển đổi giữa 3 chế độ vận hành chính dựa trên yêu cầu của host:

### Chế độ 1: Quick Setup & Khởi tạo Metric Log (Quick Setup Mode)
* **Trigger:** Khi host yêu cầu: "Setup product analytics cho dự án" hoặc "Setup analytics từ brief".
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`. Nếu không có, fallback về `./`. Tự động tạo thư mục này nếu chưa tồn tại.
  2. Copy các tệp đầu não: `product_metrics.md` và `product_overview.md` từ references của skill sang `3_product_analytics/` (nếu chưa có).
  3. Copy tệp vận hành: `analytics_input.md` từ references sang `<active_phase_dir>/analytics_input.md`.
  4. Báo cáo khởi tạo cấu trúc cho Phase/Sprint thành công.

### Chế độ 2: Phân tích Sprint & Cảnh báo Điểm nghẽn (Sprint Analysis & Bottleneck Alert Mode)
* **Trigger:** Khi host yêu cầu: "Phân tích số liệu sprint này", "Tìm lỗi/điểm nghẽn sản phẩm" hoặc cung cấp số liệu Mixpanel mới.
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`.
  2. Đọc số liệu mới trong `<active_phase_dir>/analytics_input.md` và đối chiếu với lịch sử trong `3_product_analytics/product_metrics.md`.
  3. Map số liệu Mixpanel theo hướng dẫn tại `mixpanel_mapping.md` và `standard_funnels.md` để vẽ ra bức tranh phễu chuyển đổi hiện tại.
  4. Phát hiện điểm rơi tự do (Drop-off points) lớn nhất.
  5. Xuất ra **Danh sách Cảnh báo Điểm nghẽn (Bottleneck Alert List)** và lưu vào `3_product_analytics/product_overview.md`.
  6. Đưa ra chỉ định kích hoạt skill tiếp theo:
      * *Nếu có lỗi UX/Blocker:* Đề xuất kích hoạt `prod4_ux_feedback` để tìm nguyên nhân và đề xuất UI/UX mới.
      * *Nếu cần tối ưu tỷ lệ chuyển đổi:* Đề xuất kích hoạt `prod5_ab_testing` để lên kế hoạch thử nghiệm.

### Chế độ 3: Đánh giá Tổng thể & Đúc rút Bài học (Product Review Mode)
* **Trigger:** Khi kết thúc một Phase hoặc khi host yêu cầu: "Review hiệu quả sản phẩm đợt này", hoặc "Tổng kết chỉ số HEART".
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`.
  2. Tổng hợp dữ liệu từ `3_product_analytics/product_metrics.md` và các đề xuất cải tiến đã triển khai.
  3. Đánh giá sự thay đổi của chỉ số theo thời gian (Uplift trend).
  4. Viết đúc rút bài học (Product Lessons Learned) vào `3_product_analytics/product_overview.md`.
  5. Cập nhật lại các giả định ban đầu về người dùng để cải thiện độ chính xác cho các kế hoạch phát triển tiếp theo.


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

