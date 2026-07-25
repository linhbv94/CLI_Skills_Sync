# Brief Input Template (Brief dự án & Thông tin Marketing đầu vào)

> **[AGENT BOOTSTRAP — ĐỌC TRƯỚC KHI XỬ LÝ]**
> Nếu bạn đang đọc file này, hãy dừng lại và thực hiện theo thứ tự sau trước khi làm bất cứ điều gì:
> 1. Đọc **`.agents/AGENTS.md`** — định nghĩa toàn bộ quy tắc resolve paths, ngôn ngữ output, và phong cách làm việc.
> 2. Đọc **`mkt_guide.md`** — nắm quy trình 5 bước vận hành để hiểu mục tiêu của tác vụ hiện tại.
> 3. Quét thư mục **`.agents/skills/`** — xác định danh sách skill đang có để biết phạm vi hỗ trợ.
> 4. Sau khi đọc xong 3 nguồn trên, quay lại đây để phân tích brief bên dưới.

*Hướng dẫn cho user: Điền toàn bộ thông tin dự án, sản phẩm, đối thủ, nhân sự, kênh và nhân vật AI dưới đây bằng ngôn ngữ tự nhiên (tiếng Việt). Sau khi điền xong, tag file này cùng với file `master-prd` của sản phẩm rồi ra lệnh cho Agent: **"Setup dự án từ brief"**. Agent sẽ tự động phân loại, biên dịch prompt và điền vào các file cấu hình chi tiết.*

---

## 1. Thông tin Sản phẩm & Định vị (Product Brief)
*Viết tự do về sản phẩm của bạn: mục đích làm gì, giải quyết nỗi đau gì, đối tượng người dùng mong muốn là ai, link landing page là gì.*

- **Tóm tắt về sản phẩm:** 
  [Ví dụ: Đây là Antigravity, một AI coding assistant chạy trực tiếp trong IDE giúp lập trình viên viết code nhanh gấp 3 lần bằng cách tự động nghiên cứu codebase và đề xuất code.]
- **Đối tượng khách hàng mục tiêu (ICP):** 
  [Ví dụ: Lập trình viên solo, các nhà phát triển sản phẩm độc lập (Indie Hackers), Tech Lead của các startup công nghệ vừa và nhỏ.]
- **Những điểm nổi bật nhất (USP):** 
  [Ví dụ: Chạy ngay trong IDE, hiểu sâu toàn bộ workspace thay vì chỉ file hiện tại, không thu thập dữ liệu mã nguồn của khách hàng.]
- **Lời kêu gọi hành động mong muốn (CTA):** 
  [Ví dụ: Tải và cài đặt extension trên VS Code / JetBrains để nhận 14 ngày dùng thử Premium miễn phí tại link: https://antigravity.ai]

---

## 2. Nghiên cứu & Định hướng Nội dung (Competitor & Content Style)
*Những gì bạn quan sát từ đối thủ hoặc phong cách bạn muốn hướng tới.*

- **Quan sát đối thủ:**
  [Ví dụ: Đối thủ A thường làm video ngắn dạng show màn hình gõ code rất nhanh trên nhạc nền lofi, tương tác cực cao. Tuy nhiên, bài viết giải thích tính năng dài dòng của họ trên Threads thường rất ít view. Đối thủ B viết bài kể chuyện kiểu "build in public" (nhật ký phát triển sản phẩm) thì lại được đón nhận nhiệt tình.]
- **Phong cách nội dung mong muốn:**
  [Ví dụ: Xưng hô "mình - các bác" hoặc xưng tên thân mật. Văn phong viết thường, ngắn gọn, hài hước kiểu dân công nghệ. Tránh tuyệt đối giọng PR học thuật khô khan.]
- **Một số dạng bài viral trong domain:**
  [Ví dụ: NHỮNG AI MUỐN MUA NHÀ TRƯỚC TUỔI 30 THÌ VÀO ĐỌC NGAY BÀI NÀY.]

---

## 3. Nhân sự & Kênh vận hành (Team & Channels)
*Ai sẽ tham gia chiến dịch và chạy các tài khoản nào?*

- **Danh sách thành viên:**
  - [Ví dụ: Minh Phat - Leader/Host, online chủ yếu vào buổi tối (20:00 - 22:00), nick Threads: @minhphat_dev]
  - [Ví dụ: Nam Dev - Supporter, online giờ hành chính (09:00 - 18:00), nick Threads: @nam_dev]
  - [Ví dụ: Linh UI/UX - Co-host, online trưa & tối, nick Threads: @linh_designer]

- **Danh sách Kênh MXH:**
  - [Ví dụ: Kênh chính chủ Brand:
    - Tên hiển thị (Tên page): Antigravity AI
    - Username (Tên kênh): @antigravity_ai
    - Bio hiện tại: AI coding assistant chạy trực tiếp trong IDE giúp lập trình viên viết code nhanh gấp 3 lần.
    - Định vị & Mục tiêu: tập trung demo sản phẩm, tin tức, cập nhật tính năng mới]
  - [Ví dụ: Kênh Founder:
    - Tên hiển thị (Tên page): Minh Phat | Founder
    - Username (Tên kênh): @minhphat_dev
    - Bio hiện tại: Co-founder @antigravity_ai. Thích chia sẻ hành trình startup và tech stack.
    - Định vị & Mục tiêu: chia sẻ hành trình startup, build in public, xây dựng uy tín cá nhân]
  - [Ví dụ: Kênh Đại sứ:
    - Tên hiển thị (Tên page): Nam Dev | Software Engineer
    - Username (Tên kênh): @nam_dev
    - Bio hiện tại: Dev quèn chia sẻ chuyện nghề, kinh nghiệm debug và tối ưu hiệu năng.
    - Định vị & Mục tiêu: chia sẻ kinh nghiệm dev, review stack]

---

## 4. Mô tả Nhân vật đại diện AI (AI Character)
*Mô tả về nhân vật AI của bạn để tự động gen prompt tiếng Anh.*

- **Mô tả ngoại hình gốc bằng tiếng Việt:**
  [Bạn có thể tự mô tả, HOẶC nếu đã dán link ảnh ở dưới, Agent sẽ tự động xem ảnh và mô tả lại giúp bạn.]
- **Mã link ảnh khuôn mặt gốc làm tham chiếu (`--cref`):**
  *Lưu ý: Dán URL ảnh công khai của người thật (ví dụ: link ảnh kết thúc bằng .jpg/.png từ Imgur, Pinterest...) HOẶC dán đường dẫn file ảnh bạn tải về lưu trong máy (ví dụ: `mkt_campaign/setup/face.jpg`). Agent sẽ tự động xem ảnh này, phân tích đặc điểm khuôn mặt để tự động điền phần mô tả ngoại hình bằng tiếng Việt & tiếng Anh.*
  [Dán link ảnh hoặc đường dẫn file ảnh cục bộ tại đây]
- **Mô tả phong cách ăn mặc & bối cảnh thường ngày:**
  - *Thường ngày:* [Ví dụ: mặc áo thun hoodie màu xám hoặc thun đen basic, ngồi code trong góc làm việc tối giản có đèn LED ấm.]
  - *Lúc debug/Stress:* [Ví dụ: mặc áo hoodie trùm đầu, tay ôm đầu bất lực trước màn hình máy tính đầy dòng code đỏ lòm.]
  - *Lúc đi cafe:* [Ví dụ: mặc áo khoác sơ mi bên ngoài áo thun trắng, ngồi làm việc tại quán cafe đông đúc.]
