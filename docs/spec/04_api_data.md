# API & Data Specification: Skills Auto Sync Tool (`_spec4_api_data`)

> **Version:** 2.3.0  
> **Last Updated:** 2026-08-06  
> **Target Audience:** Backend Developers, Dev Agents, Software Architects  

---

## 1. Schema Cấu hình Tối giản (`config.json` Specification)

File `config.json` sẽ nằm ở thư mục hệ thống chuẩn tùy theo hệ điều hành (chứ không nằm cùng cấp với file thực thi):
* **macOS:** `~/Library/Application Support/Skills_Sync/config.json`
* **Windows:** `%APPDATA%\Skills_Sync\config.json`

### Schema JSON của `config.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SkillsSyncConfig",
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "description": "Phiên bản cấu hình hệ thống"
    },
    "lang": {
      "type": "string",
      "enum": ["en", "vi"],
      "description": "Ngôn ngữ hiển thị (en = Tiếng Anh, vi = Tiếng Việt)"
    },
    "agents": {
      "type": "object",
      "properties": {
        "anti": { "type": "integer", "enum": [0, 1], "description": "1 = kích hoạt Antigravity, 0 = bỏ qua" },
        "codex": { "type": "integer", "enum": [0, 1], "description": "1 = kích hoạt Codex, 0 = bỏ qua" },
        "claude": { "type": "integer", "enum": [0, 1], "description": "1 = kích hoạt Claude Code, 0 = bỏ qua" }
      },
      "required": ["anti", "codex", "claude"]
    },
    "skills_lib": {
      "type": "string",
      "description": "Đường dẫn tuyệt đối tới Thư viện Skill gốc (git repository)"
    },
    "git_repo": {
      "type": "string",
      "description": "Liên kết Git Remote Repository để pull/push đồng bộ"
    },
    "ignore_patterns": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Danh sách các pattern file/thư mục cần bỏ qua khi sync"
    }
  },
  "required": ["version", "lang", "agents", "skills_lib", "git_repo", "ignore_patterns"]
}
```

---

## 2. Đặc tả Đường dẫn Mặc định của các Agent theo Hệ điều hành

Khi một Agent được set bằng `1`, Sync Engine tự động định vị thư mục làm việc của Agent đó theo quy chuẩn sau:

### macOS:
* **Antigravity:** `~/.gemini/config` (Resolved to `/Users/<username>/.gemini/config`)
* **Codex:** `~/.codex` (Resolved to `/Users/<username>/.codex`)
* **Claude Code:** `~/.claude` (Resolved to `/Users/<username>/.claude`)

### Windows:
* **Antigravity:** `%USERPROFILE%\.gemini\config` (Resolved to `C:\Users\<username>\.gemini\config`)
* **Codex:** `%USERPROFILE%\.codex` (Resolved to `C:\Users\<username>\.codex`)
* **Claude Code:** `%USERPROFILE%\.claude` (Resolved to `C:\Users\<username>\.claude`)

---

## 3. API Interface cho Module Upstream & Git Engine (`sync_engine.py` / `git_engine.py`)

Các hàm nghiệp vụ chính được thiết kế phục vụ cho luồng CLI & UI:

### `scan_and_sync_upstream(library_path: Path, agent_paths: dict, selected_agents: list, ignore_patterns: list, dry_run: bool = False) -> UpstreamSyncResult`
* **Mô tả:** Duyệt qua các Agent hoạt động. Áp dụng bộ lọc `ignore_patterns` (bỏ qua `.system` của Codex). So sánh file giữa các Agent cục bộ với `skills_lib`. Nếu file ở Agent mới hơn, chép ngược về `skills_lib` và đánh dấu dirty.
* **Output Data Structure:**
  ```python
  @dataclass
  class UpstreamSyncResult:
      files_synced_to_library: list[str]  # File được gom từ Agent về Library
      agents_updated: list[str]           # Danh sách các agent được cập nhật
      has_library_changes: bool           # True nếu Library có file mới
  ```

### `ensure_git_repo_linked(repo_path: Path, remote_url: str, lang: str = "en") -> Tuple[bool, str]`
* **Mô tả:** Đảm bảo thư mục `skills_lib` liên kết chính xác với remote git.
* **Return:** `True` và chuỗi dịch thông báo thành công hoặc lỗi tương ứng với `lang`.

### `get_git_status(repo_path: Path, lang: str = "en") -> GitStatusResult`
* **Mô tả:** So sánh HEAD cục bộ với remote tracking branch (`origin/main`).
* **Output Data Structure:**
  ```python
  @dataclass
  class GitStatusResult:
      status: str  # "UP_TO_DATE", "BEHIND", "AHEAD", "DIVERGED", "OFFLINE", "AUTH_ERROR", "NOT_FOUND_ERROR", "NO_GIT"
      ahead_count: int
      behind_count: int
      dirty_files: list[str]
      error_message: str
  ```

### `execute_smart_sync(repo_path: Path, mode: str, lang: str = "en") -> Tuple[bool, str]`
* **Mô tả:** Thực hiện hành động Git cụ thể dựa theo `mode`, dịch thông báo trả về theo `lang`:
  * `mode="AUTO_PULL"`: Chạy `git pull --ff-only origin main`.
  * `mode="AUTO_PUSH"`: Chạy `git add . && git commit -m "..." && git push origin main`.
  * `mode="AUTO_MERGE"`: Chạy pull merge và push.
  * `mode="FORCE_PULL"`: Chạy `git reset --hard origin/main`.
  * `mode="FORCE_PUSH"`: Chạy `git push --force-with-lease origin main`.

---

## 4. Đặc tả Adapter Chuyển đổi Quy tắc & Phân phối (`adapter_engine.py`)

Module `adapter_engine.py` xử lý việc render các file cấu hình từ tệp quy tắc gốc `AGENTS.md` tại thư mục tổng và sao chép kỹ năng tới các Agent:

### Mapping Table:

| Source (In Thư viện tổng) | Target Agent | Destination Path | Điều kiện Deploy | Transformation (Xử lý bởi Code) |
| :--- | :--- | :--- | :--- | :--- |
| `AGENTS.md` | Antigravity | `<anti_lib>/AGENTS.md` | Khi `agents.anti == 1` | Sao chép nguyên bản Markdown UTF-8, đồng bộ timestamp |
| `AGENTS.md` | Codex | `<codex_lib>/AGENTS.md` | Khi `agents.codex == 1` | Sao chép nguyên bản Markdown UTF-8, đồng bộ timestamp |
| `AGENTS.md` | Claude Code | `<claude_lib>/CLAUDE.md` | Khi `agents.claude == 1` | **Đổi tên thành CLAUDE.md**, tự động bổ sung Header Metadata cho Claude, đồng bộ timestamp |
| `skills/` (Toàn bộ folder) | Antigravity | `<anti_lib>/skills/` | Khi `agents.anti == 1` | Sao chép đè toàn bộ thư mục và tệp |
| `skills/` (Toàn bộ folder) | Codex | `<codex_lib>/skills/` | Khi `agents.codex == 1` | Sao chép đè, bỏ qua và giữ nguyên thư mục `.system` của Codex |
| `skills/` (Toàn bộ folder) | Claude Code | `<claude_lib>/skills/` | Khi `agents.claude == 1` | Sao chép đè toàn bộ thư mục và tệp |

---

## 5. Đặc tả Định dạng Log (`sync_history.log`)

Ứng dụng ghi lịch sử hoạt động dạng log văn bản đặt trong cùng thư mục hệ thống chứa file `config.json`:

```text
2026-08-06 11:45:00 [INFO] CLI Sync Engine started (lang: vi).
2026-08-06 11:45:01 [INFO] Active agents: Antigravity, Codex. (Claude is disabled)
2026-08-06 11:45:01 [INFO] Upstream scan complete. Synced 1 file from Codex.
2026-08-06 11:45:02 [INFO] Git status: AHEAD 1.
2026-08-06 11:45:04 [INFO] Git push success. Commit: a1b2c3d.
2026-08-06 11:45:05 [INFO] Downstream deploy to Antigravity and Codex complete.
2026-08-06 11:45:05 [INFO] Smart Sync completed successfully in 5.2s.
```
