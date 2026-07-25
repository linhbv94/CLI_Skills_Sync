---
name: _strat1_problem
description: Tái định hình và bóc tách vấn đề gốc rễ (Problem Framing & Root Cause Analysis), xác định stakeholder, mục tiêu và giả định ẩn.
---

# Problem Framing & Root Cause Analysis — Tái định hình & Bóc tách Vấn đề Gốc rễ

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-23  

---

## 1. Mục tiêu & Phạm vi (Purpose & Scope)

Skill này là **công cụ phân tích nền tảng được gọi gần như 100%** trong các luồng tư duy chiến lược.

Nhiệm vụ cốt lõi là không chấp nhận trực diện yêu cầu ban đầu (tránh bẫy triệu chứng bề nổi), mà bóc tách sâu để tìm ra **bài toán thực sự (Actual Problem)** cần giải quyết.

---

## 2. Các Thành phần Phân tích Cốt lõi

1. **Problem Framing (Tái định hình Vấn đề):** Đặt lại câu hỏi từ góc nhìn First Principles. Vấn đề thực sự nằm ở đâu?
2. **Root Cause Analysis (Phân tích Nguyên nhân Gốc rễ):** Sử dụng phương pháp 5 Whys / Cause-and-Effect để tìm nguyên nhân sâu xa.
3. **Stakeholder Mapping (Bản đồ Bên liên quan):** Ai sở hữu vấn đề? Ai chịu ảnh hưởng chính (Người dùng, Business, Kỹ thuật, Vận hành)?
4. **Goal Alignment (Định hướng Mục tiêu):** Trạng thái mong muốn (*Desired State*) là gì và có khớp với tầm nhìn sản phẩm không?
5. **Assumption Discovery (Bóc tách Giả định Ẩn):** Tìm các niềm tin/giả thiết ngầm chưa được kiểm chứng.

---

## 3. Cấu trúc Input & Output Quy chuẩn

### Ví dụ Input
> *"Tôi muốn thêm tính năng [X] vào ứng dụng."*

### Cấu trúc Output Bắt buộc

```markdown
### 🎯 Bản Phân tích Tái định hình Vấn đề (Problem Framing Report)

1. **Vấn đề Thực sự (Actual Problem):** [Bóc tách bản chất gốc rễ, khác biệt so với yêu cầu bề nổi]
2. **Trạng thái Hiện tại (Current State):** [Bối cảnh, điểm nghẽn hoặc nỗi đau hiện tại]
3. **Trạng thái Mong muốn (Desired State):** [Kết quả mục tiêu cần đạt được]
4. **Bản đồ Stakeholders:** [Ai sở hữu vấn đề & Ai chịu ảnh hưởng]
5. **Giả định Ẩn (Hidden Assumptions):** [Các điều kiện ngầm được coi là đúng nhưng chưa kiểm chứng]
6. **Câu hỏi Mở (Open Questions):** [Các điểm mơ hồ cần làm rõ]
```

---

## 4. Phối hợp Hệ thống (Orchestration & Delegation)

Skill này được điều phối trực tiếp bởi [`_strat0_system`](../_strat0_system/SKILL.md) ở Bước 1 (Problem Framing).

Sau khi tái định hình xong bài toán:
- Chuyển sang mở rộng hướng giải quyết tại [`_strat2_solution`](../_strat2_solution/SKILL.md).
- Nếu vấn đề chạm đến chiến lược kinh doanh, gọi [`_strat5_business`](../_strat5_business/SKILL.md) để hỗ trợ domain framework.

---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-23):**
  - Khởi tạo chuẩn hóa skill phân tích vấn đề gốc rễ theo đúng quy tắc `AGENTS.md`.