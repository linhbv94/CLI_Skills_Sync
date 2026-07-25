# Demo & Presentation Specification: Skills Auto Sync Tool (`_spec6_demo_presentation`)

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-25  
> **Target Audience:** Product Manager, Stakeholders, End-Users, AI Video/Image Agents  

---

## 1. Kịch bản Trình diễn Demo (Live Demo Playbook)

Kịch bản demo 3 phút chứng minh tính năng đồng bộ tự động đa máy và đa AI Agent:

```text
⏱️ THỜI LƯỢNG DEMO: 3 PHÚT
🎯 MỤC TIÊU DEMO: Cho thấy sự tiện lợi khi tạo 1 skill mới trên MacBook và tự động có mặt trên Windows chỉ với 1 Click.
```

### Phân đoạn 1 (0:00 - 1:00): Bối cảnh & Khởi động Ứng dụng
1. Mở ứng dụng **Skills Auto Sync Tool** trên **MacBook**.
2. Người dùng chỉ ra 3 Agent được tích chọn: `[X] Antigravity`, `[X] Codex`, `[X] Claude Code`.
3. Bấm nút `Auto-Detect` ➔ App lập tức hiển thị 3 đường dẫn chuẩn của các agent trên macOS.

### Phân đoạn 2 (1:00 - 2:00): Sửa đổi Skill & 1-Click Smart Sync
1. Người dùng tạo thêm 1 Skill mới có tên `skills/git_master/SKILL.md` tại thư mục Library gốc.
2. Bấm nút **`[ 🚀 SMART SYNC NOW ]`**.
3. Cửa sổ Log chạy cực nhanh:
   - `[GIT]` Committed changes: `update skills - 2026-07-25 18:35`
   - `[GIT]` Pushed to `origin/main` (Success)
   - `[DEPLOY]` Deployed to `Antigravity`, `Codex`, `Claude Code` (Success)
4. Mở ngay ứng dụng **Claude Code** hoặc **Codex** ➔ Gõ thử câu nhắc ➔ Agent lập tức kích hoạt skill `git_master` vừa tạo!

### Phân đoạn 3 (2:00 - 3:00): Trải nghiệm mượt mà trên Máy thứ hai (Windows)
1. Chuyển sang màn hình máy **Windows Văn Phòng**.
2. Mở **Skills Auto Sync Tool** ➔ Nút Git Status báo màu vàng: `[ ⬇️ 1 Commit Behind ]`.
3. Bấm **`[ 🚀 SMART SYNC NOW ]`**.
4. App tự động kéo `git_master` về và phân bổ vào `%USERPROFILE%\.codex\skills` và `%USERPROFILE%\.gemini\config\skills`.
5. Đóng demo ➔ Hoàn toàn không mất công copy tay vào 6 thư mục!

---

## 2. Dynamic Visual Presentation Prompts (Dành cho AI Image / Video Generation)

Khi cần tạo hình ảnh minh họa hoặc video demo giới thiệu công cụ cho cộng đồng:

### Prompt 1: Mockup Giao diện Đa Nền tảng (Cross-platform GUI Mockup)
> **Prompt:** A sleek, modern desktop app user interface for a developer tool named "Skills Auto Sync Tool". Dark mode theme, translucent glassmorphism background, featuring modern typography. Left panel displays checked options for Antigravity, Codex, and Claude Code agents. A prominent glowing blue button labeled "🚀 SMART SYNC NOW". Clear status indicators with green badges. Displayed on a dual-screen setup with a MacBook Pro and a Windows PC monitor in a clean tech workstation setup, 8k resolution, photorealistic, cinematic lighting.

### Prompt 2: Sơ đồ Luồng Dữ liệu Động (Data Flow Visualization)
> **Prompt:** Isometric 3D infographic showing seamless synchronization. A glowing central cube labeled "Skills Central Library" emitting glowing data streams to three futuristic laptop and desktop devices representing macOS and Windows. Colored icons for Codex, Antigravity, and Claude AI agents hovering above each device. Clean gradient background, vibrant cyan and purple color scheme, high tech UI presentation slide.

---

## 3. Bản Tóm tắt Giá trị Sản phẩm (Product Pitch Summary)

* **Vấn đề (Problem):** Dùng 3 máy tính x 2-3 AI Agents = Mỗi lần cập nhật Skill phải copy thủ công vào 6 vị trí khác nhau, rất dễ thiếu sót và lệch version.
* **Giải pháp (Solution):** **Skills Auto Sync Tool** — Quản lý 1 thư viện duy nhất + Git Sync + Tự động deploy đè đúng định dạng của từng Agent chỉ bằng 1 Click!
