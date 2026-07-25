# AI Short Video Playbook (Quy trình sản xuất video bằng AI)

Tài liệu này hướng dẫn cách viết kịch bản dạng bảng 2 cột tối ưu cho việc tạo video bằng AI (sử dụng AI Voiceover, AI Image/Video Generator) và duy trì sự nhất quán của nhân vật chính.

---

## 1. Quy trình Gen Prompt 2 Giai đoạn Nhất quán Nhân vật (Consistent Character Pipeline)

Khi viết kịch bản chứa nhân vật chính (được mô tả trong `2_marketing_campaign/inputs/ai_character.md`), Agent phải chia khâu visual thành 2 bước rõ ràng trong kịch bản để người dùng dễ sản xuất:

```mermaid
flowchain
    A[Bước 1: Gen ảnh tĩnh - Text-to-Image] --> B[Nhập Physical Tags + cref parameter] --> C[Đầu ra: Ảnh tĩnh chất lượng cao]
    C --> D[Bước 2: Tạo chuyển động - Image-to-Video] --> E[Nhập ảnh tĩnh làm Start Frame + prompt chuyển động] --> F[Đầu ra: Video 3-4s nhất quán]
```

### Bước 1: Prompt tạo ảnh tĩnh (Cung cấp 2 phiên bản)

Để người dùng có thể linh hoạt sử dụng cả công cụ trả phí (Midjourney) lẫn công cụ phổ thông (ChatGPT/DALL-E 3 kèm ảnh đính kèm), Agent bắt buộc phải xuất ra 2 phiên bản prompt:

*   **Version A: Midjourney / Stable Diffusion (Tham số-based)**
    *   *Công thức:* `[Physical Tags từ ai_character.md] + [Trang phục/Hành động/Góc máy] + [Bối cảnh/Ánh sáng] + [Tham số --cref và --ar]`
    *   *Ví dụ:* `A medium shot of a 25-year-old Vietnamese man, short messy black hair, rectangular glasses, wearing a dark gray crewneck t-shirt, working in a crowded coffee shop, looking stressed, warm cinematic light --cref https://image.example.com/nam_dev_face.jpg --cw 100 --ar 9:16`
*   **Version B: ChatGPT / DALL-E 3 (Mô tả ngôn ngữ tự nhiên kèm ảnh đính kèm)**
    *   *Công thức:* `"Based on the [giới tính/sắc tộc] in the uploaded reference image, generate a new image of her/him. She/He has the exact same facial features, skin tone, and hair. In this new image, she/he is [Hành động/Trang phục/Góc máy] + [Bối cảnh/Ánh sáng]. The style must be a high-quality photorealistic portrait, vertical 9:16 aspect ratio, candid photography look, captured on a professional DSLR camera. Do not make it look like a drawing or 3D render."`
    *   *Ví dụ:* `Based on the Vietnamese man in the uploaded reference image, generate a new image of him. He has the exact same facial features, short messy black hair, and rectangular glasses. In this new image, he is wearing a dark gray crewneck t-shirt, working in a crowded coffee shop, looking stressed. The style must be a high-quality photorealistic portrait, vertical 9:16 aspect ratio, warm cinematic light, candid photography look, captured on a professional DSLR camera. Do not make it look like a drawing or 3D render.`

*   **Lưu ý về Kiểu tóc (Hairstyle Variations):**
    *   Để tăng tính tự nhiên qua các video, hãy chủ động thay đổi kiểu tóc của nhân vật (ví dụ: `hair in a high ponytail` - tóc đuôi ngựa cao, `hair in a messy bun` - búi tóc rối, `half-up half-down hairstyle` - buộc tóc nửa đầu, `loose hair braids` - tết tóc lỏng).
    *   **Quy tắc:** Luôn giữ nguyên màu tóc (black/dark brown) và tóc mái (bangs/fringe) từ ảnh gốc để khuôn mặt không bị thay đổi quá nhiều.

*   **Quy tắc Bố cục & Vị trí Khuôn mặt (Mandatory Face Composition Rule - Quan trọng):**
    *   **Vấn đề:** Khi sinh ảnh dọc 9:16, AI thường đặt khuôn mặt nhân vật lệch trái/phải hoặc cao/thấp tùy hứng, khiến các video (đặc biệt khi dựng Split Screen 2 nửa) bị trôi vị trí mặt lộn xộn và dễ bị che mất bởi Text Overlay / Subtitles.
    *   **Căn ngang (Horizontal Centering):** Bắt buộc đặt mặt nhân vật **chính giữa trục ngang** (`face centered horizontally in frame`).
    *   **Căn dọc (Vertical Height ~60%):** Bắt buộc đặt vị trí mắt & mặt ở **độ cao ~60% tính từ đáy ảnh lên** (thuộc 1/3 phía trên - upper-middle area), đảm bảo tầm nhìn (eye-level) đồng nhất giữa tất cả các video và chừa 40% khoảng trống bên dưới cho Subtitles/Caption.
    *   **Góc máy đồng nhất:** Luôn ưu tiên góc chụp `Medium close-up portrait shot` (khung hình từ giữa ngực lên hết đỉnh đầu) để giữ quy mô khuôn mặt đồng đều.
    *   *Từ khóa Midjourney (Version A):* `Medium close-up portrait shot of ..., face centered horizontally at 60% height of 9:16 frame, eye-level framing`
    *   *Từ khóa ChatGPT / DALL-E 3 (Version B):* `Her/His face must be perfectly centered horizontally and positioned at around 60% vertical height of the 9:16 vertical frame (upper-middle region), leaving space at the bottom for video captions.`

*   **Quy tắc chống cúi mặt (Anti-Downward Face Rules - Quan trọng):**
    *   Để tránh thuật toán AI sinh video bị méo mặt, lệch mặt hoặc sai nhân vật, **mặt của nhân vật chính phải luôn rõ ràng và hướng về phía camera**.
    *   **Cấm** viết các prompt khiến nhân vật cúi gằm mặt xuống bàn, nhìn xuống sách, nhìn chằm chằm xuống điện thoại hay máy tính (`looking down`, `writing down`, `staring down`, `looking down at a tablet`).
    *   Nếu cảnh quay yêu cầu hành động viết bài hoặc gõ laptop, hãy hướng dẫn nhân vật **ngẩng đầu/ngước mắt lên nhìn trực diện camera** trong khi tay vẫn thực hiện hành động.
    *   *Ví dụ sửa đổi:* Thay vì `writing down notes in a notebook` -> Sửa thành `looking up from her notebook, looking directly at the camera with a focused expression`. Thay vì `typing on mechanical keyboard` -> Sửa thành `typing on mechanical keyboard while looking up at the camera and smiling`.
    *   Đảm bảo mặt không bị che khuất (`face fully visible`, `unobstructed view of the face`).

*   **Quy tắc chống lỗi biến dạng vật thể ở tay (Anti-Hand Object Glitch):**
    *   Các công cụ AI Video (Kling, Luma) xử lý rất tệ các vật thể nhỏ chuyển động trên tay nhân vật (bút, điện thoại, giấy, cốc nước...). Vật thể rất dễ bị biến mất hoặc biến dạng dị dạng khi nhân vật giơ tay lên.
    *   **Bắt buộc:** Không cho nhân vật cầm nắm hay tương tác trực tiếp với các vật thể nhỏ này trên tay. Thay vào đó, hãy mô tả các cử chỉ tay không tự nhiên như: chống cằm (`resting chin on hand`), vén tóc (`adjusting hair behind ear`), chỉ tay (`gesturing with hands`), giơ ngón tay cái (`thumbs-up`).

*   **Quy tắc chống nét căng đét giả tạo (Anti-Plastic/Uncanny Look):**
    *   **Vấn đề:** Ảnh gốc bị quá sắc nét, da bóng loáng như sáp, hoặc màu quá rực sẽ làm video trông cực kỳ "giả" và "điêu" (Uncanny Valley).
    *   **Cấm sử dụng** các từ khóa tạo cảm giác giả lập 3D/tượng sáp như: `hyperrealistic`, `ultra-detailed`, `8k`, `perfect skin`, `smooth skin`.
    *   **Bắt buộc sử dụng** các từ khóa tạo texture tự nhiên của ảnh chụp đời thường: `candid photography`, `raw photo`, `natural skin texture` (giữ lại lỗ chân lông và chi tiết da tự nhiên), `shot on iPhone` hoặc `35mm photograph` để tạo độ chân thực.
    *   **Độ phân giải:** Đặt độ phân giải chuyển động là `1080p` thay vì `4k` để tránh AI làm nét gai góc và cứng nhắc một cách nhân tạo.

*   **Quy tắc khung hình đơn (Single Person / No Over-the-Shoulder Rules - Quan trọng):**
    *   **Vấn đề:** Các từ khóa mô tả bối cảnh phòng thi, phỏng vấn (`exam room`, `interview room`, `test center`) dễ khiến AI hiểu lầm có 2 người đối diện và sinh ra góc máy quay từ sau vai/dính vai người đối diện (`over-the-shoulder`).
    *   **Cấm sử dụng** góc máy `over-the-shoulder` hoặc bất kỳ mô tả nào có thể kéo theo sự xuất hiện của người thứ hai trong khung hình.
    *   **Bắt buộc sử dụng** các từ khóa chỉ định rõ ràng: `single person in frame`, `only one person in frame`, `no other people`, `no examiner`, `no interviewer`, `avoid over-the-shoulder shots`. Thay thế bối cảnh "phòng thi phỏng vấn" bằng mô tả nền trung tính hoặc cận cảnh tập trung vào nhân vật chính để tránh AI tự vẽ thêm giám khảo ngồi đối diện.





### Bước 2: Prompt tạo chuyển động (Dành cho Grok, Kling, Luma, Runway Gen-3)
*   **Quy tắc:** Sử dụng bức ảnh tĩnh vừa tạo ở Bước 1 làm **First Frame (Khung hình bắt đầu)**. Prompt chuyển động tập trung vào chuyển động cơ thể, biểu cảm và đặc biệt là khẩu hình miệng tương ứng với câu nói của nhân vật.
*   **Lip-sync (Đồng bộ khẩu hình trên Grok/Luma):** Bắt buộc chèn câu thoại của nhân vật vào prompt dưới dạng `saying: "[Câu thoại]"` bằng đúng ngôn ngữ mà nhân vật nói trong video để AI đồng bộ khẩu hình trơn tru.
*   **Cử chỉ & Chuyển động tự nhiên:** Bổ sung mô tả cử chỉ tay tự nhiên (`natural hand gestures`, `fidgeting with hands`, `shrugging`), chớp mắt tự nhiên (`natural eye blinking`), chuyển động đầu/vai (`head nods`, `subtle body swaying`).
*   **Chuyển động camera:** Thêm rung camera cầm tay nhẹ (`slight handheld camera motion`) để tăng độ chân thực cho cảnh quay.
*   *Ví dụ (Tiếng Anh):* `Using the image as starting frame, the woman speaks confidently, saying: "Beneficial. Exercise is highly beneficial." with a confident expression. She makes natural and expressive hand gestures to emphasize her words. Confident head nods, natural eye blinking, realistic lip-sync, slight handheld camera motion, 4k.`
*   *Ví dụ (Tiếng Việt):* `Using the image as starting frame, the woman speaks naturally, saying: "Dùng ngay 3 chiêu này." looking friendly. She gestures naturally with her hands, tilting her head naturally. Natural eye blinking, realistic lip-sync, slight handheld camera motion, 4k.`


---

## 2. Quy chuẩn Cấu trúc Kịch bản AI Video

Kịch bản đầu ra của từng Reel trong file tổng hợp tuần (`weekX`) không dùng bảng 2 cột đơn giản nữa, mà phải tách thành các cấu trúc chi tiết như sau:

1. **So sánh/Đặc tả Trạng thái:** Bảng so sánh giữa phiên bản lỗi/cũ (Ví dụ: Cách nói ngập ngừng, cách làm sai) và phiên bản đúng/nâng cấp (Ví dụ: Cách nói tự tin, cách làm chuẩn).
2. **Caption:** Caption gợi ý đăng mạng xã hội.
3. **On-Screen Elements & Audio (Dựng Video):**
   * **Hook (0-2s):** Ghi rõ text overlay tiếng Việt nổi bật và SFX đi kèm (Whoosh, whip, bass drop).
   * **CTA (12-15s):** Ghi rõ text overlay kêu gọi hành động cụ thể và mô tả visual (ví dụ: dùng chung clip nhân vật chính chỉ tay, hoặc hiện thẻ pop-up kính mờ).
   * **Quy chuẩn Nhạc nền & Ducking:**
     * *0-2s (Hook):* Nhạc nền to, dồn dập + SFX Whoosh.
     * *2-6s (Phiên bản lỗi/cũ):* Nhạc nền tự động ducking nhỏ xuống (-15dB). Chèn SFX ngơ ngác/hụt hẫng (awkward record scratch/cricket chirp) để tăng tính hài hước hoặc đặc tả trạng thái bối rối.
     * *6-12s (Phiên bản đúng/nâng cấp):* Nhạc nền vẫn để nhỏ. Ngay giây thứ 6 chèn SFX tự tin/chuyên nghiệp (sparkle, ding).
     * *12-15s (CTA):* Nhạc nền nổi to trở lại. Chèn SFX click chuột/pop card khi text CTA hiện lên.
4. **AI Video Generation Prompts (Motion):**
   * Prompt chuyển động (Step 2) cho bên trái (phiên bản lỗi/cũ) và bên phải (phiên bản đúng/nâng cấp).

---

## 3. Quy trình lắp ráp (Toolchain Workflow)

1.  **Bước 1: Sinh Text (Script)** -> Do Agent này tạo ra dựa trên Product Profile.
2.  **Bước 2: Sinh Tiếng nói (Voiceover)** -> Copy cột VO đưa vào ElevenLabs / CapCut AI Voice.
3.  **Bước 3: Sinh Hình ảnh & Video** -> Thực hiện quy trình 2 giai đoạn để tạo video clips:
    *   *Lưu ý phân tách file:* Theo workflow vận hành thực tế, các prompt ảnh tĩnh ở **Bước 1** được gom tập trung tại file `visual_prompt.md`. Trong các file kịch bản tuần `weekX_VID_B[Bắt đầu]_[Kết thúc].md`, ta **chỉ điền các prompt tạo chuyển động ở Bước 2 (Motion Prompts)** cho các công cụ như Grok/Kling/Luma.
    *   *Cơ chế Reusable CTA:* Gen duy nhất một clip dài 3s nhân vật chính chỉ tay xuống dưới hoặc sang bên tương ứng với mỗi bối cảnh (Style Tag) và tái sử dụng cho tất cả video cùng bối cảnh để tiết kiệm tài nguyên.
4.  **Bước 4: Biên tập (Editing)** -> Lắp ghép tất cả trong CapCut, tự tạo phụ đề (Auto Captions), chèn nhạc theo quy chuẩn âm thanh ở trên và xuất bản.
