---
name: _mkt3_facebook_posts
description: Lên kế hoạch, viết bài Fanpage/Profile và seeding Group Facebook với cấu trúc dài, hỗ trợ lists/bullet points, icon và CTA linh hoạt phù hợp với hành vi người dùng Facebook.
---

> **Version:** 1.1.0  
> **Last Updated:** 2026-07-22  


# Facebook Brand & Seeding Content Skill

Skill này giúp AI Agent đóng vai trò là một **Facebook Content Specialist & Community Growth Marketer**. Nhiệm vụ chính là sản xuất nội dung đa dạng trên nền tảng Facebook, bao gồm bài viết Fanpage chính thức, bài chia sẻ trên trang cá nhân của Founder/Expert, và kịch bản seeding Group tự nhiên để vượt qua bộ lọc kiểm duyệt của admin và thuật toán Facebook.

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Mọi thông tin cấu trúc nằm trong thư mục cấu hình và ngữ cảnh dự án:
1.  `2_marketing_campaign/inputs/product_profile.md`: Bộ khung thông tin sản phẩm và phân khúc khách hàng (Project-level).
2.  `<active_campaign_dir>/content_pillars.md`: Thư viện Tuyến nội dung (Content Pillars/Angles) dùng chung cho tất cả các kênh Marketing (Facebook Fanpage/Group, Threads, Short Videos/Reels...).
3.  `2_marketing_campaign/setup/channels.md`: Cấu trúc định nghĩa tài khoản chính diện và tài khoản thành viên.
4.  `2_marketing_campaign/setup/facebook_rules.md` hoặc `references/facebook_content_rules.md`: Quy chuẩn viết bài và seeding trên Facebook.

---

## 2. Các Dạng Nội dung & Cấu trúc Đặc thù (Facebook Layouts)

Khác với Threads yêu cầu không dùng gạch đầu dòng và dưới 500 từ, Facebook cho phép bài viết dài hơn (500 - 1200 từ) và yêu cầu cấu trúc trực quan dễ quét mắt (scannable).

### A. Bài đăng Fanpage chính diện (Brand Page)
- **Mục tiêu:** Xây dựng uy tín thương hiệu, công bố tính năng (Showcase), chia sẻ kiến thức chuyên sâu (Edu).
- **Cấu trúc:**
  1.  **Hook (Tiêu đề nổi bật):** Dùng hoa mỹ hoặc gây tò mò, có thể viết in hoa hoặc đặt trong emoji 📌 🚨 💡.
  2.  **Giới thiệu vấn đề (Problem):** Đưa ra nỗi đau (Pain Point) thực tế của ICP.
  3.  **Giải pháp & Lợi ích (Solution & Benefits):** Trình bày rõ ràng bằng **danh sách gạch đầu dòng (Bullet Points)** kèm các icon thích hợp.
  4.  **Lời kêu gọi hành động (Direct CTA):** Nút đăng ký, link truy cập trực tiếp hoặc kêu gọi comment để nhận tài liệu.

### B. Bài đăng cá nhân / Đội ngũ (Founder/Expert Profile)
- **Mục tiêu:** Kể chuyện (Storytelling), Build in Public, chia sẻ trải nghiệm thực tế để xây dựng nhân hiệu.
- **Cấu trúc:**
  1.  **Hook tự sự:** Câu mở đầu mang tính chia sẻ cá nhân ("Bữa giờ...", "Thề là...", "Mình vừa nhận ra...").
  2.  **Cốt truyện (Story):** Chia sẻ tình huống thực tế, khó khăn gặp phải, quá trình giải quyết.
  3.  **Bài học rút ra (Takeaway):** Ghi rõ giá trị cốt lõi, bài học cho người đọc (cho phép dùng gạch đầu dòng nhẹ nhàng).
  4.  **Kêu gọi tương tác gián tiếp (Soft CTA):** Hỏi ý kiến độc giả hoặc hướng dẫn DM/Inbox nhận tài liệu.

### C. Bài đăng Seeding Group (Community Outreach)
- **Mục tiêu:** Tiếp cận tệp người dùng tự nhiên trong các cộng đồng lớn mà không bị Admin xóa bài.
- **Cấu trúc:**
  1.  **Hook thảo luận/hỏi đáp:** Đóng vai người học đang gặp bế tắc hoặc người vừa tìm ra cách giải quyết hay ("Mng cho em hỏi...", "Có bác nào bị như em không...", "Review nhanh...").
  2.  **Chia sẻ chân thật (Value sharing):** Không nhắc tên sản phẩm lộ liễu. Tập trung vào nỗi đau và cách vượt qua.
  3.  **Tương tác tự nhiên:** Nhờ mọi người tư vấn thêm hoặc gợi ý giải pháp qua comment seeding.

---

## 3. Quy trình Sinh Nội dung (Workflow)

### Bước 1: Đọc Hồ sơ Sản phẩm & Tuyến nội dung
- Đọc `2_marketing_campaign/inputs/product_profile.md` và `2_marketing_campaign/inputs/content_pillars.md` để nắm thông tin cốt lõi của sản phẩm (USP, Pain points, ICP) và các tuyến nội dung, định dạng được thiết lập của dự án.

### Bước 2: Xác định Tài khoản & Kênh Đăng bài
- Đọc `2_marketing_campaign/setup/channels.md` để lấy thông tin tài khoản đăng bài. Xác định rõ định vị của người đăng để viết đúng ngôi xưng và cá tính.

### Bước 3: Tạo Nội dung với Định dạng File & Unique ID
- Đọc file `active_campaign.txt` để xác định thư mục chiến dịch hoạt động (`<active_campaign_dir>`).
- Gán **Unique ID** cho bài đăng Facebook để dễ quản lý:
  - Bài Fanpage/Brand chính diện: `POST_FB_B[Số thứ tự]` (Ví dụ: `POST_FB_B001`).
  - Bài Cá nhân/Đại sứ/Member: `POST_FB_[username]_M[Số thứ tự]` (Ví dụ: `POST_FB_dan_M001`).
- Lưu bài viết thành file riêng tại thư mục chiến dịch tương ứng:
  - Bài Brand: `<active_campaign_dir>/facebook_posts/POST_FB_B[Số thứ tự]_[tên_ngắn].md`
  - Bài Member: `<active_campaign_dir>/facebook_posts/member/[username]/POST_FB_[username]_M[Số thứ tự]_[tên_ngắn].md`
  *(Tự động tạo các thư mục này nếu chưa có).*
- Nếu bài viết có yêu cầu đính kèm meme/ảnh minh họa, sinh kèm một detailed English image generation prompt phù hợp với nội dung bài viết theo quy định của [AGENTS.md](../../AGENTS.md).
- **Thư viện Mẫu Prompt Tham khảo (Visual Pattern Presets):**
  *AI không bị bó buộc vào 1 khuôn mẫu cố định mà linh hoạt thử nghiệm các layout khác nhau (Single Comic Strip, Meme Infographic, Split Screen, 2x2 Grid...) dựa trên nội dung bài.*
  
  * **Pattern A: 2x2 Grid Presentation Slides (Dạng 4 slide xếp lưới 2x2):**
    Dùng khi bài viết có 4 ý chính/lầm tưởng/lời khuyên cần tóm tắt trực quan:
    ```markdown
    A single composite image featuring a 2x2 grid layout of 4 distinct presentation slides, each in a 16:9 landscape aspect ratio. Bright, playful 2D cartoon style with bold Vietnamese typography and clean borders separating the 4 slides:
    - Top-Left (Slide 1): [Mô tả]. Headline: "[Tiêu đề 1]" and subtext "[Phụ đề]".
    - Top-Right (Slide 2): [Mô tả]. Speech bubble: "[Nội dung 2]".
    - Bottom-Left (Slide 3): [Mô tả]. Title: "[Nội dung 3]".
    - Bottom-Right (Slide 4): [Mô tả]. Title: "[Nội dung 4]".
    [Color palette & styling notes].
    ```
  * **Pattern B: Single Storytelling/Meme Panel (Dạng ảnh đơn 1 khung cảnh):**
    Dùng cho bài viết tự sự, build-in-public, hoặc tình huống hài hước/meme.
  * **Pattern C: Before vs After Split Screen (Dạng ảnh chia đôi đối lập):**
    Dùng cho các bài so sánh phương pháp cũ vs mới, hoặc trước và sau khi dùng sản phẩm.

### Bước 4: Áp dụng Quy chuẩn Viết & Seeding Facebook
- Viết bài theo đúng cấu trúc đặc thù của Facebook, tuân thủ file `facebook_content_rules.md` (giới hạn từ dài hơn, cho phép bullet points và emojis phù hợp, tránh văn phong AI giáo điều).
- Đi kèm kịch bản bài viết phải có **Kịch bản Seeding/Comment** cho các thành viên trong Organic Pod tương tác tự nhiên, thảo luận hoặc chêm link khéo léo sau 30-60 phút.

---

## Lịch sử Cập nhật (Changelog)

- **v1.1.0 (2026-07-22):**
  - Bổ sung cấu trúc mẫu Prompt tạo ảnh Infographic dạng lưới 2x2 (4 slide tỉ lệ 16:9) chuẩn hóa.
- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

