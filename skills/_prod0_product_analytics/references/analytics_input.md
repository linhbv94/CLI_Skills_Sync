# Product Analytics Input Brief (Dữ liệu Product Analytics đầu vào)

> **[PRODUCT ANALYTICS BOOTSTRAP]**
> Khi chạy phân tích số liệu, Agent sẽ đọc file này để lấy dữ liệu thô Mixpanel/Amplitude nhằm phân tích phễu, xác định điểm nghẽn và cập nhật nhật ký chỉ số.

*Hướng dẫn cho user: Copy/Paste số liệu thô hoặc báo cáo từ Mixpanel/Amplitude vào các phần tương ứng dưới đây cho Sprint/Phase hiện tại. Sau đó ra lệnh cho Agent: **"Phân tích số liệu sprint này"**.*

---

## 1. Thông tin Sprint/Phase hiện tại
- **Sprint/Phase Name:** [Ví dụ: Sprint 12 - Onboarding Optimization]
- **Thời gian chạy:** [Ví dụ: 01/08/2026 - 08/08/2026]
- **Mục tiêu sản phẩm đợt này:** [Ví dụ: Tăng tỷ lệ hoàn thành Onboarding lên > 70%]

---

## 2. Số liệu Sự kiện thô (Raw Mixpanel Metrics)
*Điền tổng số trigger (lượt kích hoạt) của các event trong khoảng thời gian trên:*

- `login_screen_viewed` : [Số]
- `sign_up` : [Số]
- `onboarding_started` : [Số]
- `onboarding_completed` : [Số]
- `dashboard_viewed` : [Số]
- `mock_test_started` : [Số]
- `mock_test_completed` : [Số]
- `payment_completed` : [Số]

---

## 3. Ghi chú & Quan sát thủ công (Qualitative Insights)
*Điền các phản hồi hoặc phát hiện bất thường mà tracking tool không đo được:*
- [Ví dụ: Nhiều user phản ánh trên Group Zalo là nút "Check Mic" ở màn hình phòng thi bị lag không bấm được trên Safari.]
