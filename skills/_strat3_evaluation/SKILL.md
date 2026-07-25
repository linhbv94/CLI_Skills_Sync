---
name: _strat3_evaluation
description: Phân tích đánh đổi (Trade-off Analysis), đánh giá tác động đa chiều (User, Business, Tech, Risk, Cost/Benefit) cho từng giải pháp.
---

# Trade-off & Impact Evaluation — Đánh giá Đánh đổi & Tác động Đa chiều

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-23  

---

## 1. Mục tiêu & Ý nghĩa (Purpose & Mindset)

> 🔥 **Đây là nơi thể hiện tư duy Product thực sự.**

Nhiệm vụ của skill này là mổ xẻ từng phương án giải pháp (từ [`_strat2_solution`](../_strat2_solution/SKILL.md)), đánh giá ưu/nhược điểm, rủi ro, độ phức tạp và sự đánh đổi (*trade-offs*) một cách sòng phẳng và minh bạch.

---

## 2. Khung Phân tích Đa chiều (Evaluation Matrix)

Mỗi Option được đánh giá qua các trục:

1. **User Impact & Value:** Trải nghiệm người dùng tốt lên hay xấu đi?
2. **Business Impact:** Tác động đến doanh thu, chuyển đổi, giữ chân (*Retention*) hay KPIs.
3. **Technical Complexity & Scalability:** Chi phí lập trình, nợ kỹ thuật (*technical debt*), khả năng chịu tải.
4. **Analytics Impact:** Có dễ đo lường không? Ảnh hưởng gì đến dữ liệu hiện có?
5. **Risk & Dependency Profile:** Phụ thuộc vào bên thứ 3 nào? Kịch bản xấu nhất (*worst-case*) là gì?
6. **Cost / Benefit & ROI:** Tỷ lệ giữa lợi ích thu về và công sức bỏ ra (*effort vs impact*).

---

## 3. Cấu trúc Output Bắt buộc

```markdown
### 📊 Bản Phân tích Đánh đổi & Tác động (Evaluation Matrix)

#### 🔹 Option A: [Tên Phương án]
- **Pros (Ưu điểm):** [Các giá trị vượt trội]
- **Cons (Nhược điểm):** [Các điểm yếu hoặc rủi ro phát sinh]
- **Technical Complexity:** [Thấp / Trung bình / Cao]
- **Scalability & Maintenance:** [Tác động đến bảo trì dài hạn]
- **Analytics Impact:** [Tác động tới việc đo lường số liệu]
- **Business Impact:** [Mức độ đóng góp mục tiêu kinh doanh]
- **Core Trade-off:** [Đổi cái gì để lấy cái gì?]

---

#### 🔹 Option B: [Tên Phương án]
...
```

---

## 4. Phối hợp Hệ thống (Orchestration & Delegation)

Skill này được điều phối trực tiếp bởi [`_strat0_system`](../_strat0_system/SKILL.md) ở Bước 6 (Trade-off & Risk Analysis).

Sau khi đánh giá xong:
- Kết quả sẽ được [`_strat0_system`](../_strat0_system/SKILL.md) dùng để chốt **Strategic Recommendation** và đi qua **Decision Quality Gate**.
- Các điểm chưa chắc chắn sẽ được chuyển sang [`_strat4_validation`](../_strat4_validation/SKILL.md) để thiết kế kế hoạch kiểm chứng.

---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-23):**
  - Khởi tạo chuẩn hóa skill đánh giá đánh đổi và tác động theo đúng quy tắc `AGENTS.md`.