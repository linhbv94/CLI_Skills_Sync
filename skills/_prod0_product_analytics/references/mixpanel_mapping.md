# Hướng dẫn Map sự kiện Mixpanel (Mixpanel Event Mapping Guidelines)

Tài liệu này hướng dẫn AI Agent cách ánh xạ (map) các sự kiện thô xuất ra từ Mixpanel vào phễu sản phẩm để phục vụ phân tích.

---

## 1. Ánh xạ Sự kiện Thô sang Phễu Chuyển đổi

Khi đọc số liệu thô từ `analytics_input.md`, hãy map theo bảng quy chuẩn sau:

| Sự kiện thô Mixpanel | Vị trí trong Phễu | Ý nghĩa & Metric đo lường |
| :--- | :--- | :--- |
| `login_screen_viewed` | **TOFU** | Tổng số lượt mở trang đăng nhập/đăng ký. Dùng để tính tỷ lệ bắt đầu tạo tài khoản. |
| `sign_up` | **TOFU** | Đăng ký tài khoản thành công. Tỷ lệ chuyển đổi đăng ký = `sign_up` / `login_screen_viewed`. |
| `onboarding_started` | **MOFU** | Bắt đầu luồng Onboarding. Dùng để đo tỷ lệ chấp nhận (Adoption) của Onboarding. |
| `onboarding_completed` | **MOFU** | Hoàn thành Onboarding. Tỷ lệ hoàn thành = `onboarding_completed` / `onboarding_started`. |
| `dashboard_viewed` | **MOFU** | Xem màn hình chính (Active usage). |
| `mock_test_started` | **Aha! Moment** | Lượt thi thử bắt đầu (Hành vi kích hoạt - Activation). |
| `mock_test_completed` | **Engagement** | Hoàn thành bài thi thử (Giá trị cốt lõi sản phẩm). |
| `payment_completed` | **BOFU** | Giao dịch mua gói cước thành công. |

---

## 2. Cách phát hiện điểm rơi tự do (Drop-off Bottlenecks)
* **Luật phân tích:** Tính tỷ lệ chuyển tiếp giữa các bước liên tiếp (Step Conversion Rate). Nếu bước nào có tỷ lệ chuyển tiếp **dưới 60%**, AI phải tự động gắn cờ `[CẢNH BÁO ĐIỂM NGHẼN]` tại vị trí đó.
* **Ví dụ:**
  * Bước 1: `onboarding_started` = 1000 users.
  * Bước 2: `onboarding_completed` = 450 users.
  * ➔ Tỷ lệ chuyển tiếp = 45%. AI gắn cảnh báo drop-off tại luồng Onboarding và đề xuất kiểm tra UX bằng `prod4_ux_feedback`.
