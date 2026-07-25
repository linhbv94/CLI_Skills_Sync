# Feature Flow & State Specification: Skills Auto Sync Tool (`_spec2_feature_flow`)

> **Version:** 1.1.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** Frontend/Backend Developers, Dev Agents, QA Engineers  

---

## 1. Sơ đồ Chuyển Trạng thái Engine (State Diagram)

Sơ đồ mô tả toàn bộ vòng đời trạng thái của **Smart Sync Engine** khi vận hành (kèm giai đoạn **Upstream Scan & Sync**):

```mermaid
stateDiagram-v2
    [*] --> Idle: Bật ứng dụng

    state Idle {
        [*] --> Ready: Nạp config.json thành công
        Ready --> PathMissing: Thiếu đường dẫn Library
    }

    Idle --> UpstreamScanning: Người dùng bấm [Smart Sync]
    
    state UpstreamScanning {
        [*] --> ScanAgentFolders: Duyệt qua các Agent active (Max 3)
        ScanAgentFolders --> ApplyFilter: Lọc bỏ .system, .git, .DS_Store
        ApplyFilter --> CompareHashes: So sánh Hash/Timestamp với Library
        CompareHashes --> CopyToLibrary: Phát hiện Agent file mới hơn
        CopyToLibrary --> MarkLibraryDirty: Cập nhật Central Library
    }

    UpstreamScanning --> Fetching: Khởi động Git Sync

    state Fetching {
        [*] --> GitFetch: Chạy git fetch origin
        GitFetch --> GitFetchSuccess: Thành công
        GitFetch --> OfflineFallback: Thất bại (Offline)
    }

    Fetching --> Analyzing: Phân tích HEAD vs origin/main

    state Analyzing {
        [*] --> CheckStatus
        CheckStatus --> UpToDate: Commits khớp nhau
        CheckStatus --> Behind: Remote có commit mới
        CheckStatus --> Ahead: Local có commit mới / Working Tree Dirty
        CheckStatus --> Conflict: Cả 2 cùng có commit mới
    }

    Analyzing --> Pulling: Status = Behind
    Analyzing --> Pushing: Status = Ahead
    Analyzing --> ResolvingConflict: Status = Conflict
    Analyzing --> DeployingAdapters: Status = UpToDate / Offline

    Pulling --> DeployingAdapters: Git Pull OK
    Pushing --> DeployingAdapters: Git Push OK
    ResolvingConflict --> DeployingAdapters: Người dùng chọn hướng xử lý

    state DeployingAdapters {
        [*] --> RenderAgentsMd: Copy shared_rules -> AGENTS.md
        RenderAgentsMd --> RenderClaudeMd: Render -> CLAUDE.md
        RenderClaudeMd --> CopySkills: Copy folder skills/ -> Agent Dirs (Loại trừ .system)
    }

    DeployingAdapters --> Success: Hoàn tất không lỗi
    DeployingAdapters --> Error: Phát hiện lỗi IO / Permission

    Success --> Idle: Quay lại trạng thái Sẵn sàng
    Error --> Idle: Hiển thị Log Lỗi
```

---

## 2. Luồng Đồng bộ Ngược 3 Nguồn (Upstream Reverse Sync Sequence)

Nhiệm vụ: Khi người dùng chỉnh sửa skill trực tiếp ở Antigravity hay Codex, Engine sẽ phát hiện, gom về Library gốc trước khi đẩy lên Git Remote.

```mermaid
sequenceDiagram
    autonumber
    participant App as Sync Engine
    participant AG as Antigravity (~/.gemini/config/skills)
    participant CX as Codex (~/.codex/skills)
    participant Library as Local Skills Library
    participant Git as Git Remote Repo

    rect rgb(255, 245, 235)
        note over App, CX: Bước 1: Quét và Lọc Thư mục
        App->>AG: Quét danh sách file trong skills/
        App->>CX: Quét danh sách file (LOẠI BỎ THƯ MỤC .system)
    end

    rect rgb(235, 248, 255)
        note over App, Library: Bước 2: Gom về Library gốc (Upstream Sync)
        App->>App: So sánh Hash / Modified Time giữa Agent & Library
        alt Phát hiện Skill ở Antigravity mới hơn Library
            App->>Library: Copy file từ Antigravity -> Library
            App->>CX: Ghi đè file tương ứng sang Codex
        else Phát hiện Skill ở Codex mới hơn Library
            App->>Library: Copy file từ Codex -> Library (Bỏ qua .system)
            App->>AG: Ghi đè file tương ứng sang Antigravity
        end
    end

    rect rgb(240, 255, 244)
        note over App, Git: Bước 3: Git Smart Sync & Deploy Adapters
        App->>Git: git status -> Phát hiện Working Tree Dirty
        App->>Git: git add . && git commit -m "sync from agent" && git push
        App->>Library: Render shared_rules/agents.md -> AGENTS.md / CLAUDE.md
    end
```

---

## 3. Luồng Khởi chạy Lần đầu & Tự động Phát hiện Đường dẫn (First-Time Setup Flow)

```mermaid
flowchart TD
    A[Bắt đầu: Mở Tool] --> B{Kiểm tra file config.json}
    B -- Đã tồn tại --> C[Nạp Cấu hình vào Bộ nhớ]
    B -- Chưa tồn tại --> D[Khởi tạo Engine Auto-Discovery]
    
    D --> E[Nhận diện Hệ điều hành: OS Platform]
    E --> F{OS là gì?}
    
    F -- macOS --> G[Set default search paths: ~/.gemini/config, ~/.codex/skills, ~/.claude]
    F -- Windows --> H[Set default search paths: %USERPROFILE%\.gemini\config, %USERPROFILE%\.codex\skills, %USERPROFILE%\.claude]
    
    G --> I[Kiểm tra sự tồn tại của thư mục trên đĩa cứng]
    H --> I
    
    I --> J[Tự động điền các Path tìm thấy vào Form]
    J --> K[Ghi file config.json ban đầu]
    C --> L[Hiển thị Giao diện Chính với dữ liệu cấu hình]
    K --> L
```

---

## 4. Chi tiết Logic Xử lý Xung đột Git (Conflict Resolution Logic)

Khi Git báo trạng thái **Diverged** (Local và Remote đều có commit mới không thể auto fast-forward):

1. **Tạm dừng tiến trình Smart Sync tự động.**
2. **Hiển thị Modal Xử lý Xung đột (Conflict Dialog)** với 3 tùy chọn:
   * **Option A: Pull & Override Local (Chấp nhận bản trên Remote):**
     * Thực thi: `git reset --hard origin/main`
     * Tác động: Bỏ tất cả thay đổi local chưa push, lấy bản remote về.
   * **Option B: Push Force (Dùng bản tại Máy hiện tại):**
     * Thực thi: `git push --force-with-lease origin main`
     * Tác động: Ghi đè bản remote bằng bản local của máy này.
   * **Option C: Manual Merge (Tự giải quyết thủ công):**
     * Thực thi: Mở cửa sổ Terminal / Git Client để người dùng tự gộp code.

