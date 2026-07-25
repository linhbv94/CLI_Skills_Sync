# Business Process Specification: Skills Auto Sync Tool (`_spec1_business_process`)

> **Version:** 1.1.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** BA, Dev Agent, System Architect, Operations  

---

## 1. Biểu đồ Quy trình Nghiệp vụ Swimlane (Macro Workflow)

Biểu đồ mô tả sự tương tác vĩ mô giữa 4 thành tố chính: **Người dùng**, **Engine đồng bộ (GUI/CLI App)**, **Kho chứa Git Remote** và **Thư mục Agent Cục bộ** (Bao gồm cơ chế **Upstream Sync**: Tự động phát hiện thay đổi trực tiếp từ thư mục Agent gom về Library trước khi Git Push).

```mermaid
graph TB
    subgraph User_Lane [Người Dùng]
        U1[Sửa Skill ở Antigravity/Codex HOẶC Mở Tool] --> U2{Chọn thao tác}
        U2 -- 1-Click Sync --> U3[Bấm Smart Sync]
        U2 -- Cấu hình --> U4[Thay đổi Path/Agent]
    end

    subgraph App_Engine_Lane [Sync App Engine]
        U3 --> E0[Đọc config.json & Auto Detect Paths]
        
        %% ĐỒNG BỘ 3 NGUỒN: BƯỚC 1 - GOM THAY ĐỔI TỪ AGENT VỀ LIBRARY
        E0 --> E1_SCAN[Quét & So sánh Hash/Timestamp giữa Agent Folders và Library]
        E1_SCAN --> E1_FILTER{Lọc bỏ Thư mục Hệ thống?}
        E1_FILTER -- Loại bỏ .system, .git, .DS_Store --> E1_CHECK{Có Agent folder nào mới hơn Library?}
        
        E1_CHECK -- Có --> E1_REVERSE[Đồng bộ ngược từ Agent -> Library & Phân bổ sang Agent còn lại]
        E1_CHECK -- Không --> E2[Khởi động Git Sync Workflow]
        E1_REVERSE --> E2
        
        %% BƯỚC 2 - GIT SMART SYNC
        E2 --> E3[Gọi Git Fetch đến Remote Repo]
        E3 --> E4{Phân tích Trạng thái Git}
        
        E4 -- Fast-Forward Behind --> E5[Thực hiện Git Pull]
        E4 -- Local / Library Modified --> E6[Auto Commit & Push lên Remote]
        E4 -- Conflict / Diverged --> E7[Kích hoạt Dialog Xử lý Manual]
        E4 -- Up to Date --> E8[Chuyển tiếp qua bước Deploy Adapters]
        
        E5 --> E8
        E6 --> E8
        
        E8 --> E9[Render shared_rules/agents.md -> AGENTS.md / CLAUDE.md]
        E9 --> E10[Sao chép Skills đã đồng nhất tới tất cả Agent Dirs active]
        E10 --> E11[Hoàn tất & Hiển thị thông báo Thành công]
    end

    subgraph Agent_Dirs_Lane [Thư mục Agent Cục bộ (Max 3 Agents)]
        E1_SCAN <--> A1[Antigravity: ~/.gemini/config/skills]
        E1_SCAN <--> A2[Codex: ~/.codex/skills - LOẠI BỎ .system]
        E1_SCAN <--> A3[Claude Code: ~/.claude/CLAUDE.md]
    end

    subgraph Git_Remote_Lane [Git Remote Repo]
        E3 <--> R1[Fetch Remote Branches & Commits]
        E5 <-- R2[Pull Commits mới về Local Library]
        E6 --> R3[Push Local Commits lên Remote Repo]
    end
```

---

## 2. Ma trận Quyết định Đồng bộ 3 Nguồn (3-Source Sync & Decision Matrix)

Engine quản lý đồng bộ đồng thời **3 Nguồn Dữ liệu**:
1. **Thư mục Agent Cục bộ** (`~/.gemini/config/skills`, `~/.codex/skills`, `~/.claude`)
2. **Thư viện Trung tâm (Local Skills Library)**
3. **Git Remote Repository**

Bảng dưới đây quy định tất cả các luật nghiệp vụ tự động hóa:

| ID Luật | Nguồn Thay đổi (Source) | Trạng thái Git / Working Tree | Bộ lọc Loại trừ (Ignore Rules) | Hành động Tự động của Engine | Phản hồi Giao diện (UI Feedback) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RULE_00` | Sửa skill trực tiếp ở Antigravity/Codex | Nút Smart Sync được bấm | Bắt buộc bỏ qua `.codex/skills/.system`, `.git`, `.DS_Store` | 1. Gom file mới/sửa từ Agent ➔ Central Library.<br>2. Cập nhật sang các Agent còn lại trên máy.<br>3. `git commit` & `git push` lên Remote. | "Đã phát hiện thay đổi ở Antigravity. Đã gom về Library & Push Git!" |
| `RULE_01` | Cả 3 nguồn bằng nhau | Git Up-to-date & Clean | Bỏ qua `.system` | Bỏ qua Pull/Push. Đảm bảo tất cả Agent đồng bộ 100%. | "Dữ liệu đã mới nhất trên 3 Agent và Git!" |
| `RULE_02` | Git Remote có commit mới | Local Behind (`behind N`) | Bỏ qua `.system` | 1. `git pull --ff-only`.<br>2. Deploy lại Adapters & Skills sang cả 3 Agent. | "Đã tự động kéo N commit mới từ Git và cập nhật 3 Agent." |
| `RULE_03` | Library có thay đổi mới | Local Ahead (`ahead N`) | Bỏ qua `.system` | 1. Auto `git add .`, `git commit -m "auto sync - {timestamp}"`, `git push`.<br>2. Sync sang các Agent active. | "Đã đẩy N commit mới lên Git Remote." |
| `RULE_04` | Xung đột Git Remote & Local | Diverged (`ahead N, behind M`) | Bỏ qua `.system` | Dừng tự động. Bật Dialog xử lý xung đột thủ công. | ⚠️ "Xung đột dữ liệu Git Remote. Cần chọn hướng xử lý." |
| `RULE_05` | Xung đột giữa 2 Agent cùng sửa | Cả Antigravity & Codex cùng sửa 1 file | Bỏ qua `.system` | Lấy file có **Modified Timestamp mới nhất** làm bản ghi đè, tạo backup `.bak_{timestamp}` cho file cũ. | ℹ️ "Đã tự động chọn bản mới nhất từ Agent [X], đã tạo backup." |

---

## 3. Quy tắc Loại trừ Thư mục Hệ thống (Ignore System Directories)

Khi quét và đồng bộ dữ liệu từ các Agent (đặc biệt là Codex và Claude Code), **BẮT BUỘC** áp dụng danh sách `IGNORE_PATTERNS` sau:

```text
IGNORE_PATTERNS = [
    "**/skills/.system/**",      # Thư mục hệ thống nội bộ của Codex (.codex/skills/.system)
    "**/.git/**",                # Thư mục quản lý Git
    "**/.DS_Store",              # File cache Finder của macOS
    "**/desktop.ini",            # File cache Explorer của Windows
    "**/*.tmp",                  # File tạm thời
    "**/*.bak*"                  # Các file backup tạm
]
```

* **Vùng cấm đụng độ:** Thư mục `.codex/skills/.system` chứa các file system prompt internal của Codex. Engine **tuyệt đối không được copy .system vào Skills Library** và **tuyệt đối không xóa/ghi đè .system** khi sync từ Library sang Codex.

---

## 4. Điểm Rủi ro & Phương án Dự phòng (Risks & Fallbacks)

1. **Rủi ro Mất mạng khi Sync Git:**
   * *Hiện tượng:* `git fetch` bị timeout.
   * *Xử lý dự phòng:* Engine tự chuyển sang chế độ **Offline Sync** (vẫn gom thay đổi từ Antigravity/Codex sang Library và đồng bộ chéo giữa các Agent trên máy mà không gọi Git). Hiển thị cảnh báo màu vàng trên UI.
2. **Rủi ro Ghi đè nhầm file đang sửa:**
   * *Xử lý dự phòng:* Trước khi ghi đè, Engine kiểm tra hash. Nếu file ở folder Agent có sửa đổi mới hơn Library, Engine sẽ tự động gom ngược về Library trước, tạo file backup `.bak_{timestamp}` an toàn.
cal Library hiện có sang các Agent trên máy mà không gọi Git). Hiển thị cảnh báo màu vàng trên UI.
2. **Rủi ro Ghi đè nhầm file đang sửa:**
   * *Hiện tượng:* Người dùng sửa skill trực tiếp ở folder của Agent (ví dụ `.codex/skills`) thay vì chỉnh ở Library tổng.
   * *Xử lý dự phòng:* Trước khi ghi đè, Engine kiểm tra hash. Nếu file ở folder Agent có sửa đổi mới hơn Library, Engine sẽ tạo file backup `.bak_{timestamp}` trước khi chèn file mới.
