# Campaign Overview Template (Tổng quan & Đánh giá Chiến dịch)

*Hướng dẫn: Khi chạy chiến dịch mới, copy file này vào folder chiến dịch (ví dụ: `campaigns/launch-july/campaign_overview.md`). File này lưu trữ KPIs thực tế và là nơi Agent đúc rút bài học để tự cập nhật bộ Skill của hệ thống.*

---

## 1. Kết quả KPI Chiến dịch
- **Tên chiến dịch:** [Ví dụ: Launch July 2026 - Ra mắt tính năng X]
- **KPI Đặt ra:** [Ví dụ: 500 lượt đăng ký trải nghiệm Beta]
- **Kết quả Đạt được:** [Ví dụ: 620 lượt đăng ký (Đạt 124%)]
- **Trạng thái:** `hoàn thành` / `chưa đạt`

---

## 2. Nhật ký Đánh giá & Bài học kinh nghiệm (Lessons Learned)
*Mục này sẽ do Agent tự động phân tích và viết vào khi chạy Review Mode.*

### Bài học 1: Hiệu quả của Hook & Định dạng bài viết
- **Phát hiện:** [Ví dụ: Các bài viết dùng Hook dạng "Đứa nào muốn..." có lượt tương tác cao gấp 3 lần các bài chia sẻ lý thuyết PEEL.]
- **Hành động áp dụng ngược lại hệ thống:** [Đã cập nhật file brand_guidelines.md để ưu tiên phong cách viết Gen Z trực diện, hạn chế lý thuyết khô khan.]

### Bài học 2: Phản hồi về Visual & Nhân vật AI
- **Phát hiện:** [Ví dụ: Ảnh nhân vật AI mặc trang phục style_cafe tại bối cảnh sáng sủa thu hút lượt profile visit cao hơn style_stress.]
- **Hành động áp dụng ngược lại hệ thống:** [Đã ghi nhận trong ai_character.md để ưu tiên sử dụng style_cafe cho các phase tiếp theo.]

### Bài học 3: Tần suất và Seeding của Team
- **Phát hiện:** [Ví dụ: Khoảng cách seeding T+30 phút ban đầu giữ an toàn tốt, không có bài nào bị thuật toán Threads ẩn comment.]
- **Hành động áp dụng ngược lại hệ thống:** [Tiếp tục duy trì timeline giãn cách seeding trong các kịch bản tương lai.]
