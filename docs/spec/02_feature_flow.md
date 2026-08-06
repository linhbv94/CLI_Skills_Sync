# Feature Flow & State Specification: Skills Auto Sync Tool (`_spec2_feature_flow`)

> **Version:** 2.3.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Developers, Dev Agents, QA Engineers  

---

## 1. Sơ đồ Chuyển Trạng thái Engine CLI (CLI State Diagram)

Sơ đồ mô tả vòng đời hoạt động của ứng dụng dòng lệnh (CLI):

```mermaid
stateDiagram-v2
    [*] --> Init: Mở file thực thi hoặc Lối tắt (Shortcut/Alias)

    state Init {
        [*] --> CheckConfigExists: Tìm config.json trong thư mục hệ thống chuẩn
        CheckConfigExists --> OnboardingFlow: Chưa có config.json hệ thống
        CheckConfigExists --> ReadConfigSuccess: Đọc config thành công
        
        state OnboardingFlow {
            [*] --> SelectLanguage: Chọn Ngôn ngữ (1 en | 2 vi)
            SelectLanguage --> InputAgents: Chọn Agent (ví dụ: 1,1,0 cho anti, codex, claude)
            InputAgents --> InputSkillsLib: Dán đường dẫn skills_lib
            InputSkillsLib --> InputGitRepo: Dán link git_repo (Enter để bỏ qua)
            InputGitRepo --> SaveOnboardingConfig: Ghi config.json hệ thống
        }
        
        SaveOnboardingConfig --> ReadConfigSuccess
        ReadConfigSuccess --> ResolvePaths: Tự động dò đường dẫn Agent active
    }

    Init --> CLI_Menu: ResolvePaths
    
    state CLI_Menu {
        [*] --> WaitingForInput: Hiển thị Menu 6 chức năng (Active/Disabled status)
        WaitingForInput --> ProcessCommand: Nhập phím số & Enter
    }

    CLI_Menu --> OneTimeSync: Command = "1" (Sync ngay)
    CLI_Menu --> RefreshStatus: Command = "2" (Làm mới trạng thái)
    CLI_Menu --> CleanupEnv: Command = "3" (Dọn dẹp môi trường)
    CLI_Menu --> EditConfig: Command = "4" (Sửa cấu hình)
    CLI_Menu --> OpenConfigFolder: Command = "5" (Mở thư mục config)
    CLI_Menu --> ExitApp: Command = "6" (Thoát)

    state OneTimeSync {
        [*] --> UpstreamScan: Quét các Agent active (anti, codex, claude = 1)
        UpstreamScan --> SyncToTong: Chép file mới sang skills_lib
        SyncToTong --> GitSync: Khởi chạy Git Sync (Fetch/Pull/Push)
        GitSync --> DeployDownstream: Copy skills_lib ngược lại các Active Agent Dirs
        DeployDownstream --> ShowResultAndReturn: In log kết quả ra Terminal
    }

    state RefreshStatus {
        [*] --> ReScanState: Chạy dry-run quét lại Agent & Git Remote
        ReScanState --> PrintChanges: Cập nhật tiêu đề động & Thông tin thay đổi
    }

    state CleanupEnv {
        [*] --> ConfirmCleanup: Hiển thị cảnh báo & Hỏi xác nhận (y/N)
        ConfirmCleanup --> CancelCleanup: Nhập 'N' hoặc phím khác
        ConfirmCleanup --> ExecuteCleanup: Nhập 'y'
        state ExecuteCleanup {
            [*] --> CleanLibrary: Xóa file/folder trong skills_lib ngoại trừ `.git` và `.gitignore`
            CleanLibrary --> CleanActiveAgents: Xóa rules file (AGENTS.md/CLAUDE.md) và folder `skills` của active agents (giữ lại `.system` cho Codex)
        }
        ExecuteCleanup --> ReturnToMenu: Hoàn tất
        CancelCleanup --> ReturnToMenu: Hủy
    }

    state EditConfig {
        [*] --> WaitingForSubInput: Hiển thị Submenu chỉnh sửa cấu hình
        WaitingForSubInput --> EditSkillsLib: Chọn 1 - Sửa đường dẫn skills_lib
        WaitingForSubInput --> EditGitRepo: Chọn 2 - Sửa Git Remote URL (hoặc xóa)
        WaitingForSubInput --> EditAgents: Chọn 3 - Sửa cấu hình kích hoạt Agent (anti, codex, claude)
        WaitingForSubInput --> EditLanguage: Chọn 4 - Thay đổi ngôn ngữ (en / vi)
        
        EditSkillsLib --> SaveSubConfig: Lưu thay đổi config.json
        EditGitRepo --> SaveSubConfig
        EditAgents --> SaveSubConfig
        EditLanguage --> SaveSubConfig
        
        SaveSubConfig --> WaitingForSubInput
        WaitingForSubInput --> ReturnToMainMenu: Chọn 5 - Trở về Menu chính
    }

    state OpenConfigFolder {
        [*] --> CallSystemShellOpen: Chạy subprocess mở thư mục chứa config.json
        CallSystemShellOpen --> ReturnToMainMenuDirect: Quay lại CLI Menu chính
    }

    OneTimeSync --> CLI_Menu: Hoàn tất / Trở lại Menu chính
    RefreshStatus --> CLI_Menu: Tự động quay lại vòng lặp hiển thị mới
    CleanupEnv --> CLI_Menu: Hoàn tất / Trở lại Menu chính
    EditConfig --> CLI_Menu: Chọn 4 (Trở lại Menu chính)
    OpenConfigFolder --> CLI_Menu: Hoàn tất
    ExitApp --> [*]
```

---

## 2. Luồng Đồng bộ Ngược và Đẩy Git (CLI Sync Sequence)

```mermaid
sequenceDiagram
    autonumber
    participant User as Người Dùng (CLI)
    participant Engine as CLI Sync Engine
    participant Agent as Active Agents (anti, codex, claude)
    participant Tong as Thư viện Tổng (skills_lib)
    participant Git as Git Remote

    User->>Engine: Bật app/phím tắt, nhập 1 -> Enter
    Engine->>Engine: Đọc config.json từ đường dẫn hệ thống AppData
    Engine->>Engine: Dò đường dẫn Agent tự động theo OS
    
    Note over Engine, Agent: Bước 1: Quét các Active Agent Dirs cục bộ
    Engine->>Agent: Quét files (bỏ qua `.system` của Codex)
    Engine->>Tong: So sánh hash & modified_time
    
    alt Có file ở Agent mới hơn Thư viện Tổng
        Engine->>Tong: Copy file mới về Thư viện Tổng
        Engine->>Engine: Đánh dấu Thư viện Tổng là Dirty (có sửa đổi)
    end
    
    Note over Engine, Git: Bước 2: Đồng bộ Git Remote
    Engine->>Git: Gọi git fetch origin
    Engine->>Engine: Kiểm tra trạng thái đồng bộ Git (Ahead/Behind/Diverged)
    
    alt Trạng thái Behind (Remote có mới hơn)
        Engine->>Git: Gọi git pull --ff-only
        Git-->>Engine: Cập nhật thư viện tổng
    end
    
    alt Trạng thái Ahead (Local có mới hơn) hoặc Dirty ở bước 1
        Engine->>Git: Gọi git add . && git commit && git push
        Git-->>Engine: Lưu trữ thành công
    end
    
    Note over Engine, Agent: Bước 3: Triển khai Downstream sang các Agent
    Engine->>Tong: Đọc AGENTS.md
    Engine->>Agent: Sao chép rules (đổi tên CLAUDE.md cho Claude) và deploy folder skills/ (giữ nguyên `.system` cho Codex)
    
    Engine->>User: Thông báo thành công và dừng
```

---

## 3. Luồng Nghiệp vụ Giải quyết Xung đột Git Diverged (Conflict Resolution Flow)

Khi phát hiện trạng thái Git là `DIVERGED`:

```mermaid
stateDiagram-v2
    [*] --> DivergedState: Trạng thái Git = DIVERGED
    DivergedState --> ShowResolutionMenu: Hiển thị Menu lựa chọn giải quyết
    
    ShowResolutionMenu --> ChoiceRemote: Nhập 'a' (Remote Wins)
    ShowResolutionMenu --> ChoiceLocal: Nhập 'b' (Local Wins)
    ShowResolutionMenu --> ChoiceCancel: Nhập 'c' (Hủy)
    
    state ChoiceRemote {
        [*] --> GitResetHard: Chạy git reset --hard origin/main
        GitResetHard --> DeployDownstreamRemote: Deploy các thay đổi mới kéo về sang các Agent
    }
    
    state ChoiceLocal {
        [*] --> GitPushForce: Chạy git push --force-with-lease origin main
    }
    
    state ChoiceCancel {
        [*] --> SkipSync: Bỏ qua bước đồng bộ, tiếp tục chạy ứng dụng
    }
    
    ChoiceRemote --> FinishResolution
    ChoiceLocal --> FinishResolution
    ChoiceCancel --> FinishResolution
    
    FinishResolution --> [*]: Quay lại CLI Menu chính
```
