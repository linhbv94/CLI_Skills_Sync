# System Specification Overview: Skills Auto Sync Tool (`_spec0_system`)

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** Lead Developer, Dev Agents, UI Agents, Test Agents, Product Owner  

---

## 1. Tổng quan Sản phẩm (Product Overview)

**Skills Auto Sync Tool** là ứng dụng desktop mỏng nhe, chạy đa nền tảng (macOS & Windows), giải quyết vấn đề quản lý và đồng bộ thư viện kỹ năng (Skills Library) giữa 3 thiết bị làm việc (Windows nhà, Windows công ty, MacBook) và 3 AI Agents (`Antigravity`, `Codex`, `Claude Code`).

### Các nguyên tắc cốt lõi:
1. **Nguồn chuẩn duy nhất (Single Source of Truth):** Thư viện skill cục bộ (Sync qua Git Private Repo hoặc Cloud Drive) đóng vai trò trung tâm.
2. **Đồng bộ 1-Click (Smart Sync):** Tự động phát hiện trạng thái Git (Pull/Push/Clean/Conflict) và triển khai các thay đổi chỉ với 1 click.
3. **Bộ chuyển đổi Agent (Agent Adapters):** Tự động chuyển đổi quy tắc chung (`shared_rules/agents.md`) thành `AGENTS.md` (Codex, Antigravity) và `CLAUDE.md` (Claude Code).
4. **Machine-Readable Contract:** Mọi file đặc tả trong thư mục này được thiết kế theo dạng hợp đồng máy đọc hiểu, giúp AI Execution Agents viết mã và kiểm thử không sai lệch logic (Zero-Hallucination).

---

## 2. Bản đồ Hồ sơ Đặc tả (Specification Index)

Tất cả các tài liệu đặc tả liên kết bằng đường dẫn tương đối:

- 📋 [01_business_process.md](01_business_process.md): Sơ đồ Swimlane vĩ mô & Ma trận Quyết định Smart Sync (`_spec1_business_process`)
- 🔄 [02_feature_flow.md](02_feature_flow.md): Luồng Logic, User Flow, State Machine & Resolution Flow (`_spec2_feature_flow`)
- 🎨 [03_ui_wireframe.md](03_ui_wireframe.md): Bố cục Giao diện Desktop UI & Trạng thái Component (`_spec3_ui_wireframe`)
- 🗄️ [04_api_data.md](04_api_data.md): Standard JSON Schema, Git Wrapper API & Adapter Specs (`_spec4_api_data`)
- 🧪 [05_qa_acceptance.md](05_qa_acceptance.md): Tiêu chí Nghiệm thu Gherkin & Ma trận Edge Cases (`_spec5_qa_acceptance`)
- 🎬 [06_demo_presentation.md](06_demo_presentation.md): Kịch bản Trình diễn Demo & Visual Presentation Prompts (`_spec6_demo_presentation`)

---

## 3. Kiến trúc Tổng thể Hệ thống (System Architecture)

```text
                               ┌───────────────────────────┐
                               │  Git Remote (GitHub/etc)  │
                               └─────────────┬─────────────┘
                                             │ (git pull/push)
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Machine (Mac / Win)                                                                    │
│                                                                                        │
│  ┌────────────────────────┐         ┌──────────────────────────────────────────────┐   │
│  │ GUI / CLI Sync Engine  │ ──────> │ Skills Central Library (Local Folder)       │   │
│  └────────────────────────┘         │  ├── skills/                                 │   │
│                                     │  └── shared_rules/agents.md                  │   │
│                                     └──────────────────────┬───────────────────────┘   │
│                                                            │ (Deploy / Adapt)          │
│                                  ┌─────────────────────────┼────────────────────────┐  │
│                                  ▼                         ▼                        ▼  │
│                         ┌──────────────────┐      ┌──────────────────┐    ┌───────────┐│
│                         │ Antigravity      │      │ Codex            │    │ Claude    ││
│                         │ ~/.gemini/config │      │ ~/.codex/skills  │    │ ~/.claude ││
│                         └──────────────────┘      └──────────────────┘    └───────────┘│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Ranh giới Nghiệp vụ & Phạm vi (Scope Matrix)

| Tính năng | Trong Phạm vi (In-Scope) | Ngoài Phạm vi (Out-of-Scope) |
| :--- | :--- | :--- |
| **Hệ điều hành** | macOS, Windows 10/11 | Linux (Server headless - chưa hỗ trợ GUI) |
| **Agent Hỗ trợ** | Antigravity, Codex, Claude Code | Custom LLM plugins tự định nghĩa |
| **Cơ chế Sync Git** | Auto Fast-Forward Pull, Auto Commit & Push | Built-in Merge Editor đồ họa 3-way phức tạp |
| **Lưu cấu hình** | `config.json` theo từng máy | Sync config setting qua server cloud riêng |

---

## 5. Tiêu chuẩn Thực thi cho AI Execution Agents (Ground Truth)

Khi AI Dev Agent thực thi viết mã dự án này, bắt buộc tuân thủ:
1. Ngôn ngữ: **Python 3.10+** (tận dụng `pathlib`, `dataclasses`, `subprocess`).
2. Giao diện: Sử dụng thư viện tiêu chuẩn hoặc lightweight cross-platform (như `tkinter` / `customtkinter`).
3. Đặt tên file & thư mục: Tất cả file code Python, module, asset phải viết dưới dạng `snake_case` (không dùng gạch ngang `-`).
4. Không cài đặt server daemon chạy ngầm chiếm dụng tài nguyên. App bật lên ➔ Sync ➔ Đóng gọn gàng.
