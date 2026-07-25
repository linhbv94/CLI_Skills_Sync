---
name: _spec6_demo_presentation
description: Soạn thảo Feature Demo Playbooks, Prototype Clickthrough Specs và Visual Presentation Prompts cho Stakeholder Handoff và Live Demo.
---

# Demo Playbook & Stakeholder Presentation Spec (`_spec6_demo_presentation`)

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-24  

---

## 1. Mục đích & Phạm vi

Skill này chịu trách nhiệm đóng gói kịch bản trình diễn tính năng (Interactive Demo Playbooks), kịch bản thao tác Prototype (Prototype Clickthrough Spec), thông số hiển thị slide/video (Presentation Prompts) và tài liệu bàn giao ngắn gọn cho Stakeholders/Clients.

### Đầu ra chính (Outputs):
1. **Interactive Demo Playbook:** Kịch bản demo theo mốc thời gian (Timeline Script) giúp presenter/user dẫn dắt buổi demo thuyết phục, nổi bật "Wow Factor".
2. **Prototype Clickthrough Flow Spec:** Chuỗi thao tác click từng điểm (Hotspot mapping) để trình diễn mượt mà trên Figma / Prototype.
3. **Visual Presentation & Slide Prompts:** Gợi ý hình ảnh visual, slide layout prompt để dựng bài thuyết trình ấn tượng.
4. **Demo Contingency & FAQ Playbook:** Bộ câu hỏi thường gặp từ Stakeholders và phương án dự phòng khi môi trường demo gặp sự cố.

---

## 2. Quy trình Thực hiện Đặc tả Demo (4 Bước)

### Bước 1 — Định hình "Wow Moment" & Thông điệp Cốt lõi
Xác định:
- Điểm đắt giá nhất của tính năng (Key Value Proposition)?
- Người xem demo là ai? (CPO, Investor, Client, Internal Team).
- Cấu trúc bài demo 3 hồi: **Problem (Nỗi đau) → Solution (Giải pháp) → Wow Result (Kết quả ấn tượng)**.

### Bước 2 — Thiết lập Kịch bản Demo Chi tiết (Timeline Script)
Phân chia từng bước theo phút:
- `00:00 - 01:00`: Đặt vấn đề & Ngữ cảnh người dùng.
- `01:00 - 03:00`: Thao tác tính năng trực tiếp (Live Walkthrough).
- `03:00 - 04:00`: Trình diễn kết quả và tác động (Outcome & Metrics).
- `04:00 - 05:00`: Hỏi đáp (Q&A).

### Bước 3 — Chuẩn bị Dữ liệu Mẫu (Demo Seed Data)
Liệt kê dữ liệu mẫu đẹp, chân thực để nạp vào hệ thống trước khi demo (Tránh dữ liệu rác như `"test 123"`, `"asdfgh"`).

### Bước 4 — Đóng gói Slide & Presentation Prompts
Sinh các prompt mô tả slide / infographic minh họa cho bài trình bày:
```text
A sleek 16:9 presentation slide showing product architecture overview. Dark minimalist background, neon teal highlights, clean typography. Highlighting seamless integration between Frontend UI, AI Spec Engine, and Automated Testing.
```

---

## 3. Template Mẫu Output Spec Demo

```markdown
# Feature Demo Playbook: [Tên Tính Năng]

> **Dành cho:** Presenter, Product Manager, Sales/Pre-sales, Stakeholders  

## 1. Demo Overview & Wow Factor

- **Mục tiêu Demo:** Trình diễn khả năng tự động tạo đặc tả từ ý tưởng thô trong 30 giây.
- **Đối tượng xem:** CPO, Technical Leads & Client Board.
- **Wow Factor:** AI tự nhận diện điểm khuyết và bổ sung ma trận lỗi tự động.

## 2. Step-by-Step Demo Script (Kịch bản Trình diễn)

| Thời gian | Hành động Presenter | Lời thoại Gợi ý (Voice Script) | Giao diện Hướng tới |
| :--- | :--- | :--- | :--- |
| `00:00 - 00:30` | Mở màn hình chính | *"Chào anh/chị, hôm nay tôi xin trình diễn tính năng Spec Generator thế hệ mới..."* | Dashboard Màn hình chính |
| `00:30 - 01:30` | Dán đoạn ý tưởng thô & Bấm Generate | *"Chỉ với 2 dòng ý tưởng đơn giản, hãy xem hệ thống biến nó thành bộ Spec đầy đủ như thế nào..."* | Màn hình Loading State |
| `01:30 - 03:00` | Cuộn xem User Flow & API Spec | *"Như anh/chị thấy, không chỉ có User Flow rõ ràng, toàn bộ API Contract và Gherkin AC đã sẵn sàng cho Dev thi công."* | Màn hình Result Spec |

## 3. Prepared Demo Data (Dữ liệu Mẫu)

- **Input Prompt Mẫu:** `Tạo tính năng thanh toán qua MoMo cho app học tiếng Anh`
- **Tài khoản Demo:** `demo.admin@productos.ai` / Pass: `Demo2026!`

## 4. Demo Contingency (Phương án Dự phòng)

- **Nếu API bị chậm:** Chuyển sang xem bản Clickthrough Prototype đã chuẩn bị sẵn tại link backup.
- **Nếu lỗi mạng:** Sử dụng file PDF Spec đính kèm sẵn trong gói Demo Handoff Package.
```

---

## 4. Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-24):** Cập nhật tên skill thành `_spec6_demo_presentation` chuẩn hóa Demo Playbook, Prototype Clickthrough Specs, và Stakeholder Handoff Presentations.
