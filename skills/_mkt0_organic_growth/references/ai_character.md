# AI Character Profile Template (Hồ sơ Nhân vật đại diện AI)

*Hướng dẫn: Định nghĩa ngoại hình cố định và phong cách visual của nhân vật AI để tạo prompt đồng nhất.*

---

## 1. Ngoại hình Cố định (Physical Traits)
- **Tên nhân vật:** [Tên nhân vật, ví dụ: Nam Dev, Ly Designer]
- **Độ tuổi / Giới tính:** [Ví dụ: 25 tuổi, Nam giới]
- **Đặc điểm gương mặt:** [Ví dụ: gương mặt trẻ trung, đeo kính gọng vuông đen, tóc đen ngắn hơi rối]
- **Dáng người:** [Ví dụ: dáng người thư sinh, cao ráo]
- **Mã link ảnh tham chiếu gốc (`--cref`):** [Dán link ảnh online hoặc file cục bộ tại đây. Nếu được cung cấp ở brief, Agent sẽ tự động phân tích ảnh này để điền các đặc điểm ngoại hình phía dưới]
- **Base Portrait Prompt (Prompt tạo ảnh gốc ban đầu):** [Agent sẽ tự động gen prompt tiếng Anh tại đây dựa trên ảnh gốc được cung cấp ở trên hoặc mô tả của Host để bạn có thể tái tạo hoặc tinh chỉnh lại ảnh nhân vật bằng Midjourney]

## 2. Thư viện Phong cách & Bối cảnh (Wardrobe & Background Tags)
*Tạo các thẻ tag ngắn để Agent gọi ra khi viết prompt hình ảnh/video cho từng bối cảnh khác nhau.*

- **`[style_casual]` (Thường ngày):** [Mô tả trang phục/bối cảnh thường ngày. Ví dụ: wearing a dark gray crewneck t-shirt, working in a modern home office with warm desk lights]
- **`[style_cafe]` (Quán cafe):** [Mô tả trang phục/bối cảnh quán cafe. Ví dụ: wearing a light blue denim jacket over a white tee, sitting at a wooden table in a crowded hipster coffee shop, laptop open]
- **`[style_professional]` (Chuyên nghiệp):** [Mô tả trang phục/bối cảnh lịch sự. Ví dụ: wearing a minimalist black long-sleeve shirt, standing in front of a white whiteboard with code architecture drawn on it]
- **`[style_stress]` (Căng thẳng/Debug):** [Mô tả bối cảnh debug code mệt mỏi. Ví dụ: wearing a gray hoodie, hands on head looking stressed at dual monitors in a dark room illuminated only by screen glow]

## 3. Quy chuẩn Prompt Visual tiếng Anh cho AI Generator
- **Khung prompt Midjourney mẫu:** `[Góc máy] + [Ngoại hình gốc] + [Thẻ phong cách chọn cho tập này] + [Hành động chi tiết trong cảnh] + [Bối cảnh/Ánh sáng] + [Tham số --cref <link> --cw 100 --ar 9:16]`
