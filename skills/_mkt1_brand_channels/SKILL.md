---
name: _mkt1_brand_channels
description: Lập kế hoạch và sinh nội dung cho Tài khoản chính diện (Main Accounts) và Đại sứ thương hiệu (Brand Ambassadors) của từng sản phẩm cụ thể dựa trên khung cấu trúc thương hiệu tổng quát.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Threads Brand Channels Skill

Skill này giúp AI Agent đóng vai trò là một **Brand Content Strategist & Copywriter** chuyên nghiệp. Nhiệm vụ chính là xây dựng nội dung chính diện và đáng tin cậy cho tài khoản chính chủ và đại sứ thương hiệu của các sản phẩm.

## Cấu trúc Tài nguyên Tham chiếu

Mọi thông tin cấu trúc nằm trong thư mục cấu hình và ngữ cảnh dự án:
1.  `2_marketing_campaign/inputs/product_profile.md`: Bộ khung thông tin sản phẩm và phân khúc khách hàng (Project-level).
2.  `2_marketing_campaign/setup/channels.md`: Cấu trúc định nghĩa tài khoản chính chủ (Founder / Brand Page) và tài khoản đại sứ (Expert / Power Users).
3.  `references/brand_content_rules.md`: Quy chuẩn viết bài chính thống, uy tín và chuyên nghiệp.

---

## Phân biệt Chiến thuật: Seeding/Member vs Main/Ambassador

> ⚠️ **Nguyên tắc cốt lõi:** Tuyệt đối không sử dụng tài khoản clone giả mạo hoặc cấu hình tự tương tác chéo giả tạo để qua mặt thuật toán. Tất cả hoạt động seeding phải được thực hiện bằng tài khoản thật của các thành viên hoạt động độc lập (Organic Pod).

| Tiêu chí | Seeding/Member Accounts (`mkt0_organic_growth`) | Main/Ambassador (`mkt1_brand_channels`) |
| :--- | :--- | :--- |
| **Mục tiêu** | Gieo mầm (Seeding), tạo thảo luận tự nhiên, tăng độ nhận diện. | Xây dựng lòng tin (Trust), khẳng định chất lượng thương hiệu, chuyển đổi. |
| **Văn phong** | Trải nghiệm cá nhân, đời thường, gần gũi, chia sẻ bài học thực tế. | Uy tín, chuyên môn cao, mang tính xác thực và chuyên nghiệp. |
| **CTA** | Hạn chế tối đa, gián tiếp (để dưới comment, kéo inbox tự nhiên). | Rõ ràng, trực tiếp hướng về sản phẩm/website. |
| **Tính sở hữu** | Tài khoản cá nhân độc lập của thành viên trong team. | Công khai mối quan hệ với sản phẩm (Founder/KOL đại sứ/Brand Page). |

---

## Quy trình Sinh Nội dung (Workflow)

### Bước 1: Đọc Hồ sơ Sản phẩm & Tuyến nội dung (Product & Content Profiling)
*   Tham chiếu `2_marketing_campaign/inputs/product_profile.md` để lấy thông tin sản phẩm và `<active_campaign_dir>/content_pillars.md` (hoặc `2_marketing_campaign/inputs/content_pillars.md` nếu chạy độc lập) để nắm được các tuyến nội dung, định dạng bài đăng được phê duyệt cho tất cả các kênh đợt này.
*   Xác định chính xác Niche, thông điệp cốt lõi và tuyến nội dung phù hợp nhất cho bài viết.

### Bước 2: Lựa chọn Tài khoản & Định dạng Bài viết
*   Xác định tài khoản sẽ đăng bài (lấy từ `2_marketing_campaign/setup/channels.md`). Đọc kỹ **Tên hiển thị**, **Bio hiện tại**, và **Định vị & Mục tiêu** của kênh để sinh nội dung phù hợp với cá tính/văn phong và bối cảnh kênh đó.
*   Lựa chọn mục tiêu bài đăng (Reach, Trust, Showcase, Conversion) tương thích với tuyến nội dung đã chọn.

### Bước 3: Áp dụng Quy tắc Viết chính thống (Generate & Validate)
*   **Xác định Thư mục Lưu trữ (Standalone Fallback):**
    - Đọc file `active_campaign.txt` để lấy `<active_campaign_dir>`.
    - **Lưu ý độc lập:** Nếu không tìm thấy file `active_campaign.txt` hoặc thư mục chiến dịch tương ứng, Agent tự động sử dụng thư mục hiện tại của workspace (`./`) làm thư mục gốc. Tự động tạo thư mục `./threads_posts/` hoặc `./member_posts/[username]/` nếu chúng chưa tồn tại.
*   **Unique ID & Lưu File:**
    - Gán **Unique ID** cho bài đăng (Ví dụ: `POST_B003` cho kênh Brand/Founder chính diện, hoặc `POST_[username]_M003` cho kênh Member/Ambassador).
    - Lưu bài viết thành file riêng tại thư mục chiến dịch tương ứng:
        - Bài đăng chính diện/Brand: `<active_campaign_dir>/threads_posts/POST_B[Số thứ tự]_[tên_ngắn].md`
        - Bài đăng Member: `<active_campaign_dir>/member_posts/[username]/POST_[username]_M[Số thứ tự]_[tên_ngắn].md`
*   **Độ dài:** Giới hạn tối đa **500 từ** cho mỗi bài đăng chính chủ/đại sứ.
*   **Quy tắc Chống Giọng AI (Anti-AI Tone):** Tuân thủ tuyệt đối quy định cấm sử dụng từ ngữ rập khuôn và liệt kê dạng gạch đầu dòng/đánh số cứng nhắc được định nghĩa ở mục 5 của `brand_content_rules.md`.
*   **Giá trị cốt lõi:** Đảm bảo bài viết cung cấp kiến thức thực tiễn (Educational), cập nhật thực tế (Showcase) hoặc bằng chứng thuyết phục (Social Proof) kèm CTA rõ ràng.
*   **Yêu cầu đính kèm ảnh (Visual & Meme Prompt):** Nếu bài viết yêu cầu đính kèm ảnh/meme minh họa, bắt buộc sinh kèm một detailed English image generation prompt (prefer cartoon style) đặt dưới placeholder ảnh theo quy định của [AGENTS.md](../../AGENTS.md).


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

