# Các Phễu Sản phẩm Tiêu chuẩn (Standard Product Funnels)

Tài liệu này định nghĩa các cấu trúc phễu đo lường chuẩn mà AI cần thiết lập khi phân tích dữ liệu sản phẩm.

---

## 1. Phễu Đăng ký & Kích hoạt (Registration & Activation Funnel)
Dùng để đo lường hiệu quả chuyển đổi từ người dùng mới thành người dùng có hoạt động ý nghĩa đầu tiên (Aha! Moment).

* **Bước 1: Tiếp cận** ➔ Sự kiện: `login_screen_viewed`
* **Bước 2: Tạo tài khoản** ➔ Sự kiện: `sign_up`
* **Bước 3: Nhập môn** ➔ Sự kiện: `onboarding_started` ➔ `onboarding_completed`
* **Bước 4: Trải nghiệm Aha!** ➔ Sự kiện: `mock_test_started` (cho thấy user đã sẵn sàng thử tính năng chính).

---

## 2. Phễu Giữ chân người dùng (Retention Cohorts)
Dùng để theo dõi xem người dùng có quay lại sử dụng sản phẩm hay không.

* **Day 1 Retention:** Người dùng kích hoạt sự kiện bất kỳ (ví dụ: `dashboard_viewed`) sau 24-48 giờ kể từ lúc đăng ký.
* **Day 7 Retention:** Người dùng quay lại sau 7 ngày.
* **Quy chuẩn đánh giá:**
  * Day 1 Retention > 40%: Tốt.
  * Day 7 Retention > 20%: Ổn định.
  * Dưới mức này: Gắn cảnh báo giữ chân yếu, cần tối ưu lại giá trị cốt lõi hoặc cơ chế nhắc nhở (notifications).

---

## 3. Phễu Chuyển đổi Doanh thu (Monetization Funnel)
Dùng để đo lường tỷ lệ trả phí của người dùng.

* **Bước 1:** `dashboard_viewed`
* **Bước 2:** Click xem gói cước ➔ `subscription_card_clicked`
* **Bước 3:** Bắt đầu thanh toán ➔ `checkout_started`
* **Bước 4:** Thanh toán thành công ➔ `payment_completed`
