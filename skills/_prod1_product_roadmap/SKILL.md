---
name: _prod1_product_roadmap
description: Quản lý ưu tiên hóa tính năng trong Product Backlog và cập nhật Product Roadmap (Now/Next/Later) theo RICE framework và HEART metrics.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Product Roadmap & Prioritization Skill

Skill này hướng dẫn AI đóng vai trò là một **Product Manager (PM)**. Nhiệm vụ chính là giúp quản lý danh sách tính năng (Product Backlog), chấm điểm ưu tiên dựa trên các framework khoa học, và tự động cập nhật bản lộ trình phát triển sản phẩm (Product Roadmap) định kỳ.

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Mọi dữ liệu backlog và lộ trình đầu não được đọc và cập nhật tại:
* **`3_product_analytics/product_roadmap.md`** ← Chứa cấu trúc Roadmap (Now, Next, Later) và bảng Backlog chấm điểm (được copy từ references của skill `_prod1_product_roadmap`).

---

## 2. Các Chế độ Hỗ trợ

AI tự động chuyển đổi giữa 3 chế độ vận hành chính dựa trên yêu cầu của host:

### Chế độ 1: Chấm điểm Ưu tiên Backlog (RICE Prioritization Mode)
* **Trigger:** Khi host gửi danh sách tính năng mới cần đánh giá hoặc yêu cầu: "Chấm điểm RICE cho các tính năng mới".
* **Quy trình xử lý của AI:**
  1. Yêu cầu host cung cấp thông tin hoặc tự ước tính dựa trên dữ liệu sản phẩm hiện có theo 4 chỉ số của **RICE Framework**:
     * **Reach (Phạm vi):** Có bao nhiêu người dùng sẽ bị ảnh hưởng bởi tính năng này trong một khoảng thời gian (ví dụ: 1 tháng)?
     * **Impact (Tác động):** Tính năng này giúp ích cho người dùng đến mức nào (3 = Rất lớn, 2 = Lớn, 1 = Vừa, 0.5 = Ít, 0.25 = Cực kỳ ít)?
     * **Confidence (Độ tin cậy):** Chúng ta tự tin bao nhiêu % về các ước tính trên (100% = Cao, 80% = Vừa, 50% = Thấp)?
     * **Effort (Công sức):** Mất bao nhiêu người-tháng (person-months) để Dev và QA hoàn thành (ví dụ: 1, 2, 0.5)?
  2. Tính điểm RICE theo công thức: `RICE Score = (Reach * Impact * Confidence) / Effort`.
  3. Sắp xếp lại danh sách backlog theo điểm RICE từ cao xuống thấp và cập nhật vào phần Backlog của file `3_product_analytics/product_roadmap.md` (khởi tạo từ template nếu chưa tồn tại).

### Chế độ 2: Cập nhật Lộ trình Sản phẩm (Roadmap Updating Mode)
* **Trigger:** Khi host yêu cầu: "Cập nhật Roadmap đợt này" hoặc "Sắp xếp lại các hạng mục Now/Next/Later".
* **Quy trình xử lý của AI:**
  1. Phân bổ các tính năng từ Backlog vào 3 cột mốc thời gian:
     * **Now (Hiện tại):** Các tính năng có điểm RICE cao nhất và đang được Dev triển khai (thường trong sprint/tháng hiện tại).
     * **Next (Tiếp theo):** Các tính năng chuẩn bị thiết kế specs và chuẩn bị làm ở sprint/tháng tiếp theo.
     * **Later (Tương lai/Ý tưởng):** Các ý tưởng tính năng điểm thấp hơn hoặc cần nghiên cứu thêm.
  2. Ghi nhận sự thay đổi và cập nhật trực tiếp vào file `3_product_analytics/product_roadmap.md`.

### Chế độ 3: Khởi tạo Specs Nhanh cho Tính năng (Draft PRD Mode)
* **Trigger:** Khi một tính năng ở mục **Now** cần chuẩn bị tài liệu kỹ thuật để bàn giao cho Dev, hoặc host yêu cầu: "Viết PRD nhanh cho tính năng X".
* **Quy trình xử lý của AI:**
  1. Đọc file `active_phase.txt` để xác định `<active_phase_dir>`.
  2. Tự động sinh tài liệu yêu cầu sản phẩm (PRD) sơ bộ gồm:
     * **Context & Problem:** Tại sao cần làm tính năng này?
     * **User Stories:** Các kịch bản sử dụng của user.
     * **Functional Requirements:** Các yêu cầu chức năng bắt buộc.
     * **Out of Scope:** Những gì không làm trong version này để tránh phình scope.
  3. Tự động tạo thư mục `<active_phase_dir>/prds/` nếu chưa tồn tại và lưu file nháp vào `<active_phase_dir>/prds/prd_[tên_tính_năng].md` để chuẩn bị bàn giao cho đội kỹ thuật.


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

