---
name: _spec0_system
description: Điều phối đóng gói tài liệu bàn giao (Hand-off Package) và kịch bản trình diễn (Demo Playbook). Quản lý tính nhất quán giữa các đặc tả và cung cấp Machine-Readable Contract cho AI Execution Agents.
---

# Specification System — Core Coordinator (Hand-off, Demo & Machine-Readable Contract)

> **Version:** 1.5.0  
> **Last Updated:** 2026-07-24  

---

## 1. Triết lý Hoạt động & Ranh giới Nhiệm vụ

Skill này đóng vai trò là **Tầng điều phối trung tâm (Orchestrator)** của toàn bộ hệ thống Đặc tả (Specification System) trong Product OS.

### A. Triết lý Cốt lõi
1. **Phục vụ Bàn giao (Hand-off):** Cung cấp tài liệu đầy đủ, chính xác, gãy gọn cho Developer triển khai code, UI/UX Designer thiết kế giao diện, và QA/Tester thiết lập kịch bản kiểm thử.
2. **Phục vụ Trình diễn (Demo):** Cung cấp kịch bản demo (Demo Playbook), clickthrough flow và visual presentation cho Stakeholders, Clients và Team.
3. **Machine-Readable Contract cho AI Execution Agents:** Mọi đặc tả được sinh ra không chỉ dành cho con người đọc, mà **bắt buộc chính các AI Execution Agents (Dev Agent, UI Agent, Test Agent) phải đọc làm Ground Truth chuẩn mực** trước khi viết code, dựng UI hoặc chạy test nhằm triệt tiêu hoàn toàn lỗi suy diễn (Zero-Hallucination Execution).

### B. Phân định Ranh giới với Product Side (`_prod_`)

| Tiêu chí | Product Side (`_prod_`) | Spec Side (`_spec_`) |
| :--- | :--- | :--- |
| **Bản chất** | Ra quyết định chiến lược, ưu tiên feature, theo dõi sức khỏe sản phẩm. | Mô tả chi tiết **xây như thế nào (How to Build)** và **demo như thế nào (How to Demo)**. |
| **Chủ thể sử dụng** | CPO, PM, Product Owner. | Dev, Designer, QA, Stakeholder/Client, và **AI Execution Agents**. |
| **Đầu ra chính** | Master PRD, Roadmap (RICE), Metrics Log, UX Feedback, AB Test. | BPMN, Flows, Wireframe Specs, API Contracts, Gherkin Acceptance Criteria, Demo Playbooks. |

---

## 2. Các Skill Chuyên môn trong Specification Track

Specification System điều phối 6 skill chuyên sâu:

- [`_spec1_business_process`](../_spec1_business_process/SKILL.md): Đặc tả quy trình nghiệp vụ vĩ mô (BPMN 2.0, Swimlane Diagrams, SIPOC, Decision Matrix).
- [`_spec2_feature_flow`](../_spec2_feature_flow/SKILL.md): Đặc tả User Flow, System Flow, State Diagrams & Sequence Logic.
- [`_spec3_ui_wireframe`](../_spec3_ui_wireframe/SKILL.md): Đặc tả Screen Specs, Component States, Responsive Layouts & Visual Prompts.
- [`_spec4_api_data`](../_spec4_api_data/SKILL.md): Đặc tả API Contracts (REST/GraphQL), JSON Schemas, ERD & Integration.
- [`_spec5_qa_acceptance`](../_spec5_qa_acceptance/SKILL.md): Đặc tả Acceptance Criteria (Gherkin), Edge Cases, Validation & QA Checklist.
- [`_spec6_demo_presentation`](../_spec6_demo_presentation/SKILL.md): Soạn thảo Feature Demo Playbooks, Prototype Clickthrough & Presentation Prompts.

---

## 3. Quy trình Điều phối 6 Bước (Specification Workflow)

### Bước 1 — Tiếp nhận & Phân tích Yêu cầu Hand-off / Demo
Xác định:
- Đối tượng thụ hưởng chính: Dev, Designer, QA, Stakeholder, hay AI Execution Agent?
- Phạm vi đặc tả: Quy trình nghiệp vụ tổng thể (`_spec1`) hay Chi tiết tính năng (`_spec2`..`_spec6`)?
- Ngữ cảnh tính năng từ Master PRD ([`_prod2_prd_generator`](../../_prod2_prd_generator/SKILL.md)) hoặc `_product_input.md`.

### Bước 2 — Phân bổ Nhiệm vụ tới các Sub-Skills
Ủy quyền cho các skill chuyên sâu tùy theo nhu cầu:
- Cần đặc tả quy trình nghiệp vụ tổng thể / BPMN / Swimlane? Gọi [`_spec1_business_process`](../_spec1_business_process/SKILL.md).
- Cần đặc tả luồng logic/chuyển trạng thái tính năng? Gọi [`_spec2_feature_flow`](../_spec2_feature_flow/SKILL.md).
- Cần đặc tả UI/wireframe/layout? Gọi [`_spec3_ui_wireframe`](../_spec3_ui_wireframe/SKILL.md).
- Cần đặc tả API/Database schema? Gọi [`_spec4_api_data`](../_spec4_api_data/SKILL.md).
- Cần đặc tả tiêu chí nghiệm thu/test case? Gọi [`_spec5_qa_acceptance`](../_spec5_qa_acceptance/SKILL.md).
- Cần lập kịch bản demo tính năng? Gọi [`_spec6_demo_presentation`](../_spec6_demo_presentation/SKILL.md).

### Bước 3 — Kiểm tra Tính Machine-Readable (Zero-Hallucination Quality Gate)
Đảm bảo output đạt tiêu chuẩn để AI Agents đọc hiểu trực tiếp:
- Tên biến, enum values, HTTP status codes, data types phải rõ ràng.
- Các điều kiện rẽ nhánh (if/else), state transitions không được mơ hồ.
- Cấu trúc Given-When-Then chuẩn Gherkin để Auto-test agent parse được.

### Bước 4 — Kiểm tra Tính Nhất quán (Cross-Spec Consistency Check)
Đối chiếu chéo giữa các tài liệu đặc tả:
- Screen Wireframe (`_spec3`) có khớp với User Flow (`_spec2`) và BPMN (`_spec1`) không?
- API Payload (`_spec4`) có cung cấp đủ data cho Screen Component (`_spec3`) không?
- Acceptance Criteria (`_spec5`) có bao phủ hết tất cả State trong State Diagram (`_spec2`) không?

### Bước 5 — Đóng gói Bộ Handoff Package & Demo Playbook
Gom toàn bộ kết quả vào cấu trúc tài liệu lưu tại thư mục dự án hoặc phase active (theo `active_phase.txt`).

### Bước 6 — Fast-Track Handoff Mode (Dành cho Vibe Coding / Tool nhỏ)
Khi người dùng chạy Vibe Coding hoặc app đơn giản:
- Tự động bỏ qua quy trình 6 bước dài dòng.
- Đóng gói duy nhất **1 file Handoff Spec rút gọn** chứa: (1) Core Flow, (2) UI Layout wireframe prompt, (3) Key API contract, và (4) 3 Acceptance Criteria chính để Dev Agent thi công ngay.

---

## 4. Tiêu chí Hoàn thành Bộ Spec (Definition of Done)

Bộ Specification đạt chuẩn khi và chỉ khi:

✓ **Dev-ready:** Developer / Dev Agent có thể viết mã trực tiếp mà không cần hỏi lại logic.  
✓ **Design-ready:** Designer / UI Agent có thể dựng layout/component chính xác.  
✓ **Test-ready:** QA / Test Agent có thể chạy test cases tự động/thủ công ngay lập tức.  
✓ **Demo-ready:** Người dùng có thể cầm Demo Playbook để trình diễn mượt mà cho Client/Stakeholders.  
✓ **Machine-readable:** Cấu trúc dữ liệu và điều kiện logic sạch sẽ, không mơ hồ.  

---

## 5. Lịch sử Cập nhật (Changelog)

- **v1.5.0 (2026-07-24):** Bổ sung sub-skill `_spec1_business_process` (BPMN 2.0, Swimlane Diagrams, Decision Matrix) và sắp xếp lại thứ tự 7 skills Specification Track theo phân cấp từ Vĩ mô (Macro) đến Vi mô (Micro).
- **v1.4.0 (2026-07-24):** Tái cấu trúc toàn bộ `_spec0_system` theo triết lý Hand-off, Demo & Machine-Readable Contract cho AI Execution Agents.
