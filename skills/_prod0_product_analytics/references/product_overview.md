# Product Performance Overview (Tổng quan Hiệu quả Sản phẩm)

Tài liệu này lưu trữ báo cáo đánh giá tổng quan, các bài học rút ra và danh sách điểm nghẽn UX (Bottleneck Alerts) cần xử lý khẩn cấp.

---

## 🚨 Danh sách Cảnh báo Điểm nghẽn (Active UX Bottlenecks)
*Nơi lưu trữ các điểm rơi tự do của phễu cần giải quyết. AI tự động ghi nhận khi phân tích sprint.*

- **[CẢNH BÁO MẪU] Drop-off tại Luồng Onboarding (Sprint 1)**
  - **Mô tả:** Tỷ lệ chuyển tiếp từ `onboarding_started` sang `onboarding_completed` sụt giảm còn **45%** (dưới mức tiêu chuẩn 60%).
  - **Điểm rơi:** Tập trung chủ yếu ở câu hỏi số 3 (Target Band selection).
  - **Action item đề xuất:** Kích hoạt `prod4_ux_feedback` để viết lại microcopy và thiết kế lại giao diện màn hình chọn Band điểm.

---

## 💡 Đúc rút Bài học Sản phẩm (Product Lessons Learned)
*Tổng hợp các bài học rút ra sau mỗi đợt A/B test hoặc tối ưu hóa.*

### [Bài học 1] - Đơn giản hóa Onboarding
* **Hạng mục tối ưu:** Rút ngắn onboarding từ 5 câu hỏi xuống 3 câu hỏi (Sprint 2).
* **Kết quả:** Tỷ lệ Onboard % tăng từ **45%** lên **72%** (Uplift +60%).
* **Bài học rút ra:** Cắt giảm ma sát (friction) ban đầu mang lại hiệu quả to lớn cho tỷ lệ Adoption. Chỉ nên hỏi những thông tin tối thiểu bắt buộc để setup app.
