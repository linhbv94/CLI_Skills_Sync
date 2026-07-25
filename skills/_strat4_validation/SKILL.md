---
name: _strat4_validation
description: Thiết kế thử nghiệm và kiểm chứng giả định (Experiment Design & Hypothesis Validation) sau khi có đề xuất chiến lược.
---

# Experiment & Hypothesis Validation — Thiết kế Kiểm chứng & Thử nghiệm Giả định

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-23  

---

## 1. Mục tiêu (Purpose)

Sau khi [`_strat0_system`](../_strat0_system/SKILL.md) chốt Đề xuất Chiến lược (*Recommendation*), luôn tồn tại các giả định chưa kiểm chứng hoặc các điểm mù (*unknowns*).

Nhiệm vụ của skill này là **xác định chính xác cần kiểm chứng cái gì** và **thiết kế phương pháp thử nghiệm (Validation Plan)** nhanh nhất với chi phí thấp nhất trước khi dốc toàn lực xây dựng.

---

## 2. Các Phương pháp Kiểm chứng (Validation Methods)

Tùy thuộc vào bản chất của điểm chưa biết (*Unknown*), lựa chọn công cụ kiểm chứng phù hợp:

- **Need IDI (In-Depth Interview):** Phỏng vấn sâu người dùng khi cần đào sâu động lực / nỗi đau.
- **Need Prototype / Mockup:** Làm bản mẫu tương tác nhanh (Figma/Clickable) để test luồng trải nghiệm.
- **Need Smoke Test / Landing Page:** Dựng trang chào hàng giả lập để đo lực cầu (Demand Intent / Waitlist).
- **Need A/B Testing:** Thử nghiệm biến thể giao diện/copy (chuyển tiếp sang [`_prod5_ab_testing`](../_prod5_ab_testing/SKILL.md)).
- **Need Survey / Poll:** Khảo sát định lượng khi cần xác nhận quy mô nhóm nhu cầu.

---

## 3. Cấu trúc Output Bắt buộc

```markdown
### 🔬 Kế hoạch Kiểm chứng Giả định (Validation Plan)

1. **Giả định Cần Kiểm chứng (Hypothesis):** [Giả định cốt lõi quyết định sự thành bại của đề xuất]
2. **Phương pháp Kiểm chứng (Validation Method):** [Need IDI / Prototype / Landing Page / A/B Test / Survey]
3. **Tiêu chí Thành công (Success Criteria / Baseline Metric):** [Chỉ số đo lường thế nào là ĐẠT?]
4. **Unknowns & Risk Mitigations:** [Rủi ro nếu thử nghiệm thất bại và phương án dự phòng]
5. **Hành động Tiếp theo:** [Các bước triển khai MVP/Test ngắn hạn]
```

---

## 4. Phối hợp Hệ thống (Orchestration & Delegation)

Skill này được điều phối bởi [`_strat0_system`](../_strat0_system/SKILL.md) ở Bước 7 (Recommendation & Validation Required).

Nếu kết quả yêu cầu A/B Test giao diện cụ thể:
- Chuyển giao nhiệm vụ cho [`_prod5_ab_testing`](../_prod5_ab_testing/SKILL.md).

---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-23):**
  - Khởi tạo chuẩn hóa skill thiết kế thử nghiệm và kiểm chứng giả định theo đúng quy tắc `AGENTS.md`.