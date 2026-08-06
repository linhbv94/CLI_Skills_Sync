# System Specification Overview: Skills Auto Sync Tool (`_spec0_system`)

> **Version:** 2.2.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Lead Developer, Dev Agents, Test Agents, Product Owner  

---

## 1. Tổng quan Sản phẩm (Product Overview)

**Skills Auto Sync Tool** là ứng dụng dòng lệnh (CLI/Terminal) siêu nhẹ, chạy đa nền tảng (macOS & Windows), giúp tự động hóa việc quản lý và đồng bộ thư viện kỹ năng (Skills Library) giữa các máy làm việc của người dùng và các AI Agents cục bộ (bao gồm `Antigravity`, `Codex`, và `Claude Code`). Việc kích hoạt hoặc vô hiệu hóa từng Agent được cấu hình linh hoạt qua file `config.json`.

### Các nguyên tắc cốt lõi:
1. **Nguồn chuẩn duy nhất (Single Source of Truth):** Central Skills Library (`skills_lib`) là thư mục gốc lưu trữ toàn bộ các skills. Cấu trúc thư mục tối giản tối đa, chỉ bao gồm:
   - Thư mục `skills/` (chứa các kỹ năng con).
   - Tệp `AGENTS.md` (chứa các chỉ thị/rules chung cho Agent).
   *Hoàn toàn không có thư mục trung gian như shared_rules/.*
2. **Tự động chuyển đổi quy tắc (Rules Auto-Mapping):** Tệp `AGENTS.md` ở thư viện tổng được đồng bộ trực tiếp sang Antigravity và Codex làm `AGENTS.md` cùng cấp với folder `skills`. Nếu là Claude Code, Sync Engine sẽ **tự động sao chép và đổi tên thành CLAUDE.md** tại thư mục của Claude, đồng thời đính kèm thêm các header metadata đặc trưng của Claude. Logic này được xử lý hoàn toàn tự động ở mã nguồn Python.
3. **Cấu hình cùng cấp (Same-Directory Config):** File cấu hình `config.json` nằm cùng thư mục với file thực thi thực tế để người dùng dễ dàng chỉnh sửa thủ công và tránh bị ghi đè chéo giữa các máy tính khác nhau khi sync qua Git.
4. **Phân phối Agents linh hoạt:** Tự động phát hiện đường dẫn mặc định của các Agent trên hệ thống. Quét và đồng bộ chéo giữa thư viện tổng (`skills_lib`) và các Agent được bật (`anti`, `codex`, `claude`) với giá trị `1` trong config.

---

## 2. Bản đồ Hồ sơ Đặc tả (Specification Index)

Tất cả các tài liệu đặc tả liên kết bằng đường dẫn tương đối:

- 📋 [01_business_process.md](01_business_process.md): Sơ đồ Swimlane vĩ mô & Ma trận Quyết định Smart Sync (`_spec1_business_process`)
- 🔄 [02_feature_flow.md](02_feature_flow.md): Luồng Logic, User Flow, State Machine & Resolution Flow (`_spec2_feature_flow`)
- 🎨 [03_ui_wireframe.md](03_ui_wireframe.md): Giao diện Dòng lệnh CLI Terminal (`_spec3_ui_wireframe`)
- 🗄️ [04_api_data.md](04_api_data.md): Schema config.json tối giản & Module API Specs (`_spec4_api_data`)
- 🧪 [05_qa_acceptance.md](05_qa_acceptance.md): Tiêu chí Nghiệm thu Gherkin & Ma trận Edge Cases (`_spec5_qa_acceptance`)
- 🎬 [06_demo_presentation.md](06_demo_presentation.md): Kịch bản Trình diễn Demo CLI (`_spec6_demo_presentation`)

---

## 3. Kiến trúc Tổng thể Hệ thống (System Architecture)

```text
                               ┌───────────────────────────┐
                               │  Git Remote (git_repo)    │
                               └─────────────┬─────────────┘
                                             │ (git pull/push)
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Machine (Mac / Win)                                                                    │
│                                                                                        │
│  ┌────────────────────────┐         ┌──────────────────────────────────────────────┐   │
│  │ CLI Sync Engine (Bin)  │         │ Central Skills Library (skills_lib)          │   │
│  │   [config.json] ◄──────┼────────>│  ├── skills/                                 │   │
│  └────────────────────────┘         │  └── AGENTS.md (Root File Rules)             │   │
│                                     └──────────────────────┬───────────────────────┘   │
│                                                            │ (Deploy / Adapt)          │
│                                  ┌─────────────────────────┼────────────────────────┐  │
│                                  ▼                         ▼                        ▼  │
│                       ┌────────────────────┐    ┌──────────────────┐     ┌────────────┐│
│                       │ Antigravity        │    │ Codex            │     │ Claude     ││
│                       │ (anti_lib)         │    │ (codex_lib)      │     │ (claude)   ││
│                       │ Config: anti=1     │    │ Config: codex=1  │     │ Config:    ││
│                       │  ├── skills/       │    │  ├── skills/     │     │  ├── skills││
│                       │  └── AGENTS.md     │    │  └── AGENTS.md   │     │  └── CLAUDE.md│
│                       └────────────────────┘    └──────────────────┘     └────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Đặc tả Định dạng File Thực thi & Cơ chế Phím tắt (Shortcuts)

| Hệ điều hành | Định dạng File | Cơ chế Phím tắt 1-Click |
| :--- | :--- | :--- |
| **Windows** | `.exe` (PE Binary) | Tạo **Windows Shortcut** trỏ đến file `.exe` thật. Ghim shortcut này ra Desktop hoặc Taskbar. Thư mục làm việc (Start in) vẫn giữ nguyên là folder chứa `.exe` và `config.json`. |
| **macOS** | **Unix Executable** (Không đuôi) | **1. macOS Alias:** Tạo Alias cho file `skills_sync` và kéo ra Desktop/Dock.<br>**2. Automator App:** Tạo App Automator chứa lệnh `cd /folder_chua_tool && ./skills_sync` ghim vào Dock.<br>**3. Command Script:** Click đúp file `.command` ngoài Desktop. |

---

## 5. Ranh giới Nghiệp vụ & Phạm vi (Scope Matrix)

| Tính năng | Trong Phạm vi (In-Scope) | Ngoài Phạm vi (Out-of-Scope) |
| :--- | :--- | :--- |
| **Giao diện** | Giao diện dòng lệnh CLI tương tác đơn giản | Giao diện đồ họa Desktop GUI (Tkinter, CustomTkinter) |
| **Agent Hỗ trợ** | Antigravity, Codex, Claude Code (bật tắt qua toggle `0`/`1`) | Custom LLM plugins tự định nghĩa bên ngoài |
| **Cơ chế Sync** | Auto Git Pull/Push & Đồng bộ chéo giữa các thư mục cục bộ | Giao diện merge code 3-way đồ họa phức tạp |
| **Lưu cấu hình** | `config.json` cùng cấp với file thực thi | Đồng bộ config settings trực tiếp qua server cloud riêng |

---

## 6. Tiêu chuẩn Thực thi cho AI Execution Agents (Ground Truth)

Khi AI Dev Agent thực thi viết mã dự án này, bắt buộc tuân thủ:
1. Ngôn ngữ: **Python 3.10+** (sử dụng thư viện chuẩn, module `subprocess`, `shutil`, `pathlib`).
2. Giao diện: Tuyệt đối không import `tkinter` hay các thư viện GUI. Sử dụng CLI Menu chuẩn nhập phím bằng `input()`.
3. Đặt tên file & thư mục: Tuân thủ quy chuẩn **snake_case** (không dùng `-`).
4. Định vị file cấu hình: Sử dụng đường dẫn động xác định theo vị trí của file thực thi (`sys.executable` hoặc `__file__`).
