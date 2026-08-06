# Business Process Specification: Skills Auto Sync Tool (`_spec1_business_process`)

> **Version:** 2.2.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** BA, Dev Agent, System Architect, Operations  

---

## 1. Biểu đồ Quy trình Nghiệp vụ Swimlane (Macro Workflow)

Biểu đồ mô tả sự tương tác vĩ mô ở chế độ dòng lệnh (CLI): **Người dùng**, **Sync Engine (CLI App)**, **Kho chứa Git Remote** và **Thư mục Agent Cục bộ** (bao gồm `Antigravity`, `Codex`, và `Claude Code`).

```mermaid
graph TB
    subgraph User_Lane [Người Dùng]
        U1[Sửa Skill ở Agent Dirs HOẶC Mở Tool] --> U2[Mở File Thực thi / Chạy Phím tắt]
        U2 --> U3[Chọn Menu: Nhập 1 và Enter]
    end

    subgraph App_Engine_Lane [Sync App Engine]
        U3 --> E0[Đọc config.json cùng cấp]
        E0 --> E0_LOAD[Xác định các Agent Active: anti, codex, claude = 1]
        
        %% BƯỚC 1 - UPSTREAM SCAN
        E0_LOAD --> E1_SCAN[Quét & So sánh Hash/Timestamp giữa Active Agent Dirs và Thư viện tổng]
        E1_SCAN --> E1_FILTER{Lọc bỏ Thư mục Hệ thống?}
        E1_FILTER -- Loại bỏ .system, .git, .DS_Store --> E1_CHECK{Có Agent folder nào mới hơn?}
        
        E1_CHECK -- Có thay đổi ở Active Agent Dirs --> E1_REVERSE[Đồng bộ ngược -> Thư viện tổng & Ghi nhận Dirty]
        E1_CHECK -- Không --> E2[Khởi động Git Sync Workflow]
        E1_REVERSE --> E2
        
        %% BƯỚC 2 - GIT SYNC
        E2 --> E3[Gọi Git Fetch đến Remote Repo]
        E3 --> E4{Phân tích Trạng thái Git}
        
        E4 -- Git Remote có thay đổi --> E5[Thực hiện Git Pull FF-only]
        E4 -- Local/Thư viện tổng thay đổi --> E6[Auto Commit & Push lên Remote]
        E4 -- Conflict / Diverged --> E7[Hiển thị menu xử lý xung đột trên Terminal]
        E4 -- Up to Date / Offline --> E8[Chuyển tiếp qua bước Deploy]
        
        E5 --> E8
        E6 --> E8
        
        %% BƯỚC 3 - DEPLOY DOWNSTREAM
        E8 --> E9[Sao chép AGENTS.md hoặc đổi tên/render thành CLAUDE.md]
        E9 --> E10[Sao chép Skills đã đồng nhất tới các Active Agent Dirs/skills/]
        E10 --> E11[In trạng thái thành công ra Terminal & Kết thúc]
    end

    subgraph Agent_Dirs_Lane [Thư mục Agent Cục bộ]
        E1_SCAN <--> A1[Antigravity: anti_lib nếu active]
        E1_SCAN <--> A2[Codex: codex_lib nếu active]
        E1_SCAN <--> A3[Claude Code: claude_lib nếu active]
    end

    subgraph Git_Remote_Lane [Git Remote Repo]
        E3 <--> R1[Fetch Remote Branches & Commits]
        E5 <-- R2[Pull Commits mới về skills_lib]
        E6 --> R3[Push Commits của skills_lib lên Remote]
    end
```

---

## 2. Ma trận Quyết định Đồng bộ 3 Nguồn (3-Source Sync & Decision Matrix)

Engine quản lý đồng bộ đồng thời giữa:
1. **Thư mục Agent Cục bộ** (`anti_lib`, `codex_lib`, `claude_lib` - được tự động nhận diện nếu toggle tương ứng đặt bằng `1` trong `config.json`).
2. **Thư viện Tổng** (`skills_lib` - thư mục chứa git repo cục bộ).
3. **Git Remote Repository** (`git_repo` - liên kết repository cấu hình).

Bảng dưới đây quy định tất cả các luật nghiệp vụ tự động hóa:

| ID Luật | Nguồn Thay đổi (Source) | Trạng thái Git / Working Tree | Bộ lọc Loại trừ (Ignore Rules) | Hành động Tự động của Engine | Phản hồi Terminal (CLI Output) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RULE_00` | Sửa skill trực tiếp ở các Active Agent Dirs | Nút Sync được kích hoạt (Nhập 1) | Bỏ qua `.system` của Codex, `.git`, `.DS_Store` | 1. Gom file mới/sửa từ các Agent được kích hoạt ➔ `skills_lib`.<br>2. Cập nhật sang các Agent kích hoạt còn lại cục bộ.<br>3. `git commit` & `git push` lên Remote. | "Phát hiện thay đổi ở [Agent]. Đã gom về Thư viện tổng & Push Git!" |
| `RULE_01` | Các nguồn khớp nhau | Git Up-to-date & Clean | Bỏ qua `.system` | Bỏ qua các bước chép đè. Đảm bảo các Active Agent đồng bộ 100%. | "Dữ liệu đã mới nhất trên các Agent và Git." |
| `RULE_02` | Git Remote có commit mới | Remote Ahead | Bỏ qua `.system` | 1. `git pull --ff-only`.<br>2. Deploy lại Adapters & Skills sang các Active Agent Dirs. | "Đã tự động kéo commit mới từ Git và cập nhật các Agent." |
| `RULE_03` | Thư viện tổng `skills_lib` có thay đổi mới | Local Ahead | Bỏ qua `.system` | 1. Tự động `git commit` & `git push`.<br>2. Sync sang các Active Agent Dirs. | "Đã đẩy thay đổi mới lên Git Remote." |
| `RULE_04` | Xung đột Git Remote & Local | Diverged | Bỏ qua `.system` | Dừng tự động. Hiển thị menu hỏi phương án giải quyết (Terminal Input). | "⚠️ Phát hiện xung đột dữ liệu Git Remote. Vui lòng chọn..." |
| `RULE_05` | Xung đột chéo giữa các Agent | Có 2 Agent cùng sửa 1 file | Bỏ qua `.system` | Lấy file có **Modified Timestamp mới nhất** ghi đè, tạo file `.bak_{timestamp}` cho file cũ hơn để backup. | "⚠️ Xung đột file. Đã lấy bản mới nhất từ [Agent] và tạo backup." |

---

## 3. Quy tắc Loại trừ Thư mục Hệ thống (Ignore System Directories)

Khi quét và đồng bộ dữ liệu, **BẮT BUỘC** áp dụng danh sách loại trừ sau:

```text
IGNORE_PATTERNS = [
    "**/skills/.system/**",      # Thư mục hệ thống nội bộ của Codex
    "**/.git/**",                # Thư mục quản lý Git
    "**/.DS_Store",              # File cache Finder của macOS
    "**/desktop.ini",            # File cache Explorer của Windows
    "**/*.tmp",                  # File tạm thời
    "**/*.bak*"                  # Các file backup
]
```

* **Quy tắc cô lập Codex:** Thư mục `.codex/skills/.system` chứa cấu hình nội bộ của Codex. Engine **tuyệt đối không được copy .system vào skills_lib** và **tuyệt đối không xóa/ghi đè .system** khi sync từ thư viện tổng sang Codex.

---

## 4. Điểm Rủi ro & Phương án Dự phòng (Risks & Fallbacks)

1. **Lỗi kết nối Git Remote:**
   * *Tình huống:* Không thể kết nối với GitHub/GitLab (Mất mạng hoặc sai credentials).
   * *Xử lý dự phòng:* Engine tự chuyển sang chế độ **Offline Sync** (Vẫn chạy đồng bộ cục bộ giữa các Active Agent Dirs và `skills_lib` trên máy). Hiện cảnh báo đỏ/vàng trên Terminal: `[Offline Mode] Tiếp tục đồng bộ cục bộ không qua Git.`
2. **Rủi ro Ghi đè file đang chỉnh sửa dở:**
   * *Xử lý dự phòng:* Trước khi sao chép đè bất kỳ file nào từ Library sang Agent hoặc ngược lại, Engine kiểm tra mã hash MD5. Nếu file chuẩn bị bị ghi đè có thay đổi mới chưa commit, tạo file `.bak_{timestamp}` ngay tại thư mục đó để đề phòng mất dữ liệu.
