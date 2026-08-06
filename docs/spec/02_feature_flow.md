# Feature Flow & State Specification: Skills Auto Sync Tool (`_spec2_feature_flow`)

> **Version:** 2.2.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Developers, Dev Agents, QA Engineers  

---

## 1. Sơ đồ Chuyển Trạng thái Engine CLI (CLI State Diagram)

Sơ đồ mô tả vòng đời hoạt động của ứng dụng dòng lệnh (CLI):

```mermaid
stateDiagram-v2
    [*] --> Init: Mở file thực thi hoặc Lối tắt (Shortcut/Alias)

    state Init {
        [*] --> CheckConfigExists: Tìm config.json cùng cấp với file thực thi
        CheckConfigExists --> ConfigMissing: Chưa có config.json
        ConfigMissing --> CreatePlaceholderAndExit: Tạo config mẫu & Thoát
        CheckConfigExists --> ReadConfigSuccess: Đọc config thành công
        ReadConfigSuccess --> ResolvePaths: Tự động dò đường dẫn Agent active
    }

    Init --> CLI_Menu: ResolvePaths
    
    state CLI_Menu {
        [*] --> WaitingForInput: Hiển thị Menu lựa chọn (Active/Disabled status)
        WaitingForInput --> ProcessCommand: Nhập phím số & Enter
    }

    CLI_Menu --> OneTimeSync: Command = "1" (Sync ngay)
    CLI_Menu --> AutoWatchMode: Command = "2" (Chạy giám sát nền)
    CLI_Menu --> CleanupEnv: Command = "3" (Dọn dẹp môi trường)
    CLI_Menu --> ExitApp: Command = "4" (Thoát)

    state OneTimeSync {
        [*] --> UpstreamScan: Quét các Agent active (anti, codex, claude = 1)
        UpstreamScan --> SyncToTong: Chép file mới sang skills_lib
        SyncToTong --> GitSync: Khởi chạy Git Sync (Fetch/Pull/Push)
        GitSync --> DeployDownstream: Copy skills_lib ngược lại các Active Agent Dirs
        DeployDownstream --> ShowResultAndReturn: In log kết quả ra Terminal
    }

    state AutoWatchMode {
        [*] --> StartWatcherDaemon: Kích hoạt luồng chạy nền (Background Thread/Process)
        StartWatcherDaemon --> WatchPaths: Giám sát file system của các active folders
        WatchPaths --> TriggerAutoSync: Phát hiện file sửa đổi hoặc Git Commit mới
        TriggerAutoSync --> WatchPaths: Hoàn tất Sync & Tiếp tục lắng nghe
    }

    state CleanupEnv {
        [*] --> ConfirmCleanup: Hiển thị cảnh báo & Hỏi xác nhận (y/N)
        ConfirmCleanup --> CancelCleanup: Nhập 'N' hoặc phím khác
        ConfirmCleanup --> ExecuteCleanup: Nhập 'y'
        state ExecuteCleanup {
            [*] --> CleanLibrary: Xóa file/folder trong skills_lib ngoại trừ `.git`
            CleanLibrary --> CleanActiveAgents: Xóa rules file (AGENTS.md/CLAUDE.md) và folder `skills` của active agents (giữ lại `.system` cho Codex)
        }
        ExecuteCleanup --> ReturnToMenu: Hoàn tất
        CancelCleanup --> ReturnToMenu: Hủy
    }

    OneTimeSync --> CLI_Menu: Hoàn tất / Trở lại Menu chính
    AutoWatchMode --> CLI_Menu: Nhấn Ctrl+C để dừng
    CleanupEnv --> CLI_Menu: Hoàn tất / Trở lại Menu chính
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
    Engine->>Engine: Đọc config.json cùng cấp
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
