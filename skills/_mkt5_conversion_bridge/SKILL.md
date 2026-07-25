---
name: _mkt5_conversion_bridge
description: Thiết kế phễu chuyển đổi, lập kế hoạch Lead Magnet, viết kịch bản kêu gọi hành động (CTA) và tin nhắn (DM Playbook) trên Threads để thu hút traffic tự nhiên từ Threads về sản phẩm.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Threads Conversion Bridge Skill

Skill này hướng dẫn AI Agent đóng vai trò **Conversion Rate Optimization (CRO) & Funnel Architect**. Nhiệm vụ chính là giúp kết nối lượng traffic tiếp cận tự nhiên trên Threads (TOFU) đi vào các phễu chuyển đổi sâu hơn như Landing Page, dùng thử sản phẩm hoặc tham gia nhóm cộng đồng kín (BOFU).

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Mọi thông tin cấu trúc nằm trong thư mục cấu hình và ngữ cảnh dự án:
1. **`2_marketing_campaign/inputs/product_profile.md`** ← ĐỌC ĐẦU TIÊN để hiểu USP, đối tượng ICP và mục tiêu CTA chính của sản phẩm (Project-level).
2. **`references/conversion_funnels.md`** ← Các mô hình phễu chuyển đổi an toàn trên Threads.
3. **`references/cta_templates.md`** ← Thư viện mẫu câu kêu gọi hành động và kịch bản nhắn tin.
4. **`<active_campaign_dir>/campaign_tracker.md`** ← Xem lịch trình và chèn các bài chuyển đổi vào mạch chiến dịch tổng thể. 
   - *Standalone Fallback:* Nếu chạy độc lập không có chiến dịch tổng (không có `active_campaign.txt` hoặc không tìm thấy thư mục chiến dịch), Agent tự động sử dụng thư mục hiện tại `./` làm gốc và tự khởi tạo file `./campaign_tracker.md` hoặc các thư mục tương ứng khi cần.

---

## 2. Các Chế độ Hỗ trợ

AI tự động kích hoạt chế độ phù hợp dựa trên yêu cầu của host:

### Chế độ 1: Thiết kế Phễu Chuyển đổi (Funnel Architecture Mode)
*   **Trigger:** Khi host hỏi "Nên thiết kế phễu chuyển đổi thế nào cho sản phẩm X?", hoặc "Làm sao để có người dùng thử Beta?".
*   **Quy trình xử lý:**
    1.  Đọc `2_marketing_campaign/inputs/product_profile.md` để hiểu sản phẩm (Niche, ICP, USP, Primary CTA).
    2.  Đề xuất một mô hình phễu phù hợp từ `conversion_funnels.md` (Ví dụ: Auto-DM đối với SaaS cần tặng template, Bio Bridge đối với sản phẩm cần đăng ký trực tiếp).
    3.  Lập danh sách các tài nguyên cần chuẩn bị (Ví dụ: File Notion Template, Landing Page Link, setup ManyChat).

### Chế độ 2: Sinh Content Chuyển đổi & Kịch bản CTA (Copywriting Mode)
*   **Trigger:** Khi host yêu cầu "Viết bài CTA cho sản phẩm", "Lên bài tặng quà kéo tương tác", hoặc "Viết kịch bản nhắn tin".
*   **Quy trình xử lý:**
    1.  Xác định Niche và ICP từ `2_marketing_campaign/inputs/product_profile.md`.
    2.  Chọn mẫu CTA từ `cta_templates.md` phù hợp với tone giọng của kênh (Kênh Brand chính chủ: trang trọng và uy tín; Kênh Member cá nhân: tự nhiên, kể chuyện bài học thực tế).
    3.  **Xác định Thư mục Lưu trữ:** Đọc file `active_campaign.txt` để lấy `<active_campaign_dir>`. Nếu chạy độc lập, `<active_campaign_dir>` sẽ fallback về thư mục hiện tại `./`.
    4.  Tự động tạo các thư mục đầu ra `<active_campaign_dir>/threads_posts/` hoặc `<active_campaign_dir>/member_posts/[username]/` nếu chúng chưa tồn tại.
    5.  Gán **Unique ID** cho bài đăng (Ví dụ: `POST_B002` cho kênh Brand chính diện, hoặc `POST_[username]_M002` cho kênh Member).
    6.  Lưu bài viết thành file riêng tại thư mục chiến dịch tương ứng:
        - Bài đăng chính diện/Brand: `<active_campaign_dir>/threads_posts/POST_B[Số thứ tự]_[tên_ngắn].md`
        - Bài đăng Member: `<active_campaign_dir>/member_posts/[username]/POST_[username]_M[Số thứ tự]_[tên_ngắn].md`
    7.  Xuất ra bản nháp bài đăng gồm:
        *   Nội dung bài viết chia sẻ giá trị/kể câu chuyện (Storytelling).
        *   Dòng kêu gọi hành động (CTA) tối ưu tương tác nhận quà.
        *   Nội dung bình luận đầu tiên (Comment Drop) nếu dùng Phễu Comment Drop.
        *   Tin nhắn DM gửi tặng khách hàng (DM Script) tương ứng.

### Chế độ 3: Tối ưu Trang Cá nhân (Bio Optimization Mode)
*   **Trigger:** Khi host yêu cầu "Tối ưu bio Threads cho Founder", hoặc "Sửa bio trang chính chủ".
*   **Quy trình xử lý:**
    1.  Dựa trên cấu trúc Bio trong `cta_templates.md`.
    2.  Đọc USP và ICP của sản phẩm hiện tại để viết ngắn gọn, xúc tích trong giới hạn ký tự của Threads (dưới 150 ký tự).
    3.  Đưa ra 2 phương án Bio mẫu để host lựa chọn.


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

