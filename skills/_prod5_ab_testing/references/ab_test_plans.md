# Product A/B Testing Plans (Kế hoạch thử nghiệm A/B)

Tài liệu này lưu trữ danh sách các chiến dịch thử nghiệm A/B, giả thuyết kiểm thử và kết quả đo lường thực tế để cải thiện tỷ lệ chuyển đổi.

---

## 🔬 Danh sách Chiến dịch Thử nghiệm A/B

### [Chiến dịch mẫu 1] Onboarding Form Length Optimization (Sprint 2)
* **Giả thuyết (Hypothesis):** *Nếu rút ngắn số lượng câu hỏi Onboarding từ 5 câu xuống còn 3 câu, thì tỷ lệ hoàn thành Onboarding sẽ tăng tối thiểu 15% vì giảm thiểu ma sát tâm lý ban đầu của người dùng.*
* **Thiết lập thử nghiệm:**
  * **Control (Bản A - 5 câu):** Onboarding nguyên bản.
  * **Variant (Bản B - 3 câu):** Bỏ câu hỏi về Target Band và Prior Experience (sẽ hỏi sau ở màn hình dashboard).
  * **Primary Metric:** `onboarding_completed` / `onboarding_started` (Conversion Rate %).
  * **Đối tượng:** 100% người dùng mới trên Mobile.
* **Kết quả đo lường (Results):**
  * **Bản A (Control):** 10,000 users ➔ 4,500 completions (CR: **45.0%**)
  * **Bản B (Variant):** 10,200 users ➔ 7,344 completions (CR: **72.0%**)
  * **Uplift:** +60.0% cải thiện.
  * **Độ tin cậy (Statistical Significance):** > 99% (Đạt ý nghĩa thống kê).
* **Kết luận:** **Variant thắng**. Áp dụng 100% bản B (3 câu hỏi) cho toàn bộ người dùng mới từ ngày 05/08/2026.
