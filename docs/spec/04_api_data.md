# API & Data Specification: Skills Auto Sync Tool (`_spec4_api_data`)

> **Version:** 1.1.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** Backend Developers, Dev Agents, Software Architects  

---

## 1. Schema Cấu hình Cục bộ (`config.json` Specification)

File `config.json` lưu trữ tại thư mục cấu hình cá nhân người dùng:
* macOS: `~/.config/skills_auto_sync/config.json` (hoặc cùng thư mục thực thi app).
* Windows: `%APPDATA%\skills_auto_sync\config.json`.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SkillsSyncConfig",
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "example": "1.1.0"
    },
    "library_path": {
      "type": "string",
      "description": "Đường dẫn tuyệt đối tới thư viện Skill gốc",
      "example": "/Users/vic/skills_library"
    },
    "selected_agents": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["antigravity", "codex", "claude"]
      },
      "description": "Danh sách các agent kích hoạt trên máy này"
    },
    "agent_paths": {
      "type": "object",
      "properties": {
        "antigravity": { "type": "string" },
        "codex": { "type": "string" },
        "claude": { "type": "string" }
      },
      "required": ["antigravity", "codex", "claude"]
    },
    "ignore_patterns": {
      "type": "array",
      "items": { "type": "string" },
      "default": [
        "**/.system/**",
        "**/.git/**",
        "**/.DS_Store",
        "**/desktop.ini",
        "**/*.tmp",
        "**/*.bak*"
      ]
    },
    "git_settings": {
      "type": "object",
      "properties": {
        "auto_fetch": { "type": "boolean", "default": true },
        "auto_push": { "type": "boolean", "default": true },
        "branch": { "type": "string", "default": "main" }
      }
    }
  },
  "required": ["version", "library_path", "selected_agents", "agent_paths"]
}
```

---

## 2. API Interface cho Module Upstream & Git Engine (`sync_engine.py`)

Module `sync_engine.py` quản lý đồng bộ 3 nguồn dữ liệu và thực thi các lệnh Shell Git an toàn:

### `scan_and_sync_upstream(library_path: str, agent_paths: dict, ignore_patterns: list) -> UpstreamSyncResult`
* **Mô tả:** Duyệt qua các thư mục Agent được active (`antigravity`, `codex`, `claude`), bỏ qua tất cả đường dẫn khớp với `ignore_patterns` (đặc biệt là `.codex/skills/.system`). Nếu phát hiện file skill ở Agent có `modified_time` hoặc `md5_hash` mới hơn Library gốc, copy file đó ngược về Library gốc.
* **Data Structure Output:**
  ```python
  @dataclass
  class UpstreamSyncResult:
      files_synced_to_library: list[str]  # Danh sách file vừa gom từ Agent về Library
      agents_updated: list[str]            # Danh sách Agent vừa nhận file gom mới
      has_library_changes: bool           # True nếu làm Library dirty (cần git commit)
  ```

### `git_fetch(repo_path: str) -> bool`
* **Mô tả:** Chạy `git fetch origin` để cập nhật thông tin remote branch.
* **Return:** `True` nếu thành công, `False` nếu mất mạng hoặc lỗi Git.

### `get_git_status(repo_path: str) -> GitStatusResult`
* **Mô tả:** Đánh giá số lượng commit lệch giữa local và remote `origin/main`.
* **Data Structure Output:**
  ```python
  @dataclass
  class GitStatusResult:
      status: str  # "UP_TO_DATE", "BEHIND", "AHEAD", "DIVERGED", "DIRTY", "ERROR"
      ahead_count: int
      behind_count: int
      dirty_files: list[str]
  ```

### `execute_smart_sync(repo_path: str, mode: str) -> bool`
* **Mô tả:** Thực thi pull/push dựa theo `mode`:
  * `mode="AUTO_PULL"`: Run `git pull --ff-only origin main`
  * `mode="AUTO_PUSH"`: Run `git add . && git commit -m "sync: upstream changes from agent" && git push origin main`
  * `mode="FORCE_PULL"`: Run `git reset --hard origin/main`
  * `mode="FORCE_PUSH"`: Run `git push --force-with-lease origin main`

---

## 3. Đặc tả Adapter Chuyển đổi Quy tắc & Loại trừ (`adapter_engine.py`)

Module `adapter_engine.py` thực hiện đọc file nguồn và render file đích cho từng Agent, đồng thời thực thi bộ lọc loại trừ `ignore_patterns`:

### Mapping Table:

| Source File (In Library) | Target Agent | Destination File Path | Ignore / Exclusion Rules | Output Transformation |
| :--- | :--- | :--- | :--- | :--- |
| `shared_rules/agents.md` | Antigravity | `<antigravity_path>/AGENTS.md` | Không áp dụng | Giữ nguyên format Markdown UTF-8 |
| `shared_rules/agents.md` | Codex | `<codex_path>/AGENTS.md` | Không áp dụng | Giữ nguyên format Markdown UTF-8 |
| `shared_rules/agents.md` | Claude Code | `<claude_path>/CLAUDE.md` | Không áp dụng | Thêm Header Metadata dành riêng cho Claude Memory |
| `skills/` (Toàn bộ folder) | Antigravity | `<antigravity_path>/skills/` | `.git`, `.DS_Store` | Copy đè toàn bộ thư mục & files |
| `skills/` (Toàn bộ folder) | Codex | `<codex_path>/skills/` | **BẮT BUỘC GIỮ NGUYÊN `<codex_path>/skills/.system`**, không xóa hay copy đè vào `.system` | Copy đè các thư mục skill thường |
| `skills/` (Toàn bộ folder) | Claude Code | `<claude_path>/skills/` | `.git`, `.DS_Store` | Copy đè các thư mục skill tương ứng |

---

## 4. Định dạng Log & Backup File Spec

### Log File Format (`sync_history.log`)
Ghi theo chuẩn JSON Lines (JSONL) để dễ dàng đọc/parse:
```json
{"timestamp": "2026-07-25T18:35:00Z", "event": "SMART_SYNC_START", "os": "macOS"}
{"timestamp": "2026-07-25T18:35:01Z", "event": "UPSTREAM_SYNC_DETECTED", "source_agent": "antigravity", "modified_file": "skills/my_skill/SKILL.md"}
{"timestamp": "2026-07-25T18:35:01Z", "event": "LIBRARY_UPDATED", "files_copied": 1}
{"timestamp": "2026-07-25T18:35:02Z", "event": "GIT_PUSH_SUCCESS", "commit_hash": "a1b2c3d"}
{"timestamp": "2026-07-25T18:35:02Z", "event": "SMART_SYNC_COMPLETE", "status": "SUCCESS", "duration_ms": 1340}
```

