---
name: _mkt4_short_videos
description: Lên ý tưởng và viết kịch bản Short Video (FB Reels, IG Reels, TikTok, YouTube Shorts) dạng 9:16 cho sản phẩm. Hỗ trợ 2 định dạng: kịch bản dùng AI sản xuất (voiceover + visual prompts tiếng Anh) và kịch bản quay chụp thủ công (placeholder).
---

> **Version:** 2.0.0  
> **Last Updated:** 2026-07-25  


# Short Video Production Skill

Skill này giúp AI Agent đóng vai trò **Short Video Content Director & Scriptwriter**. Nhiệm vụ chính là chuyển hóa các tính năng độc bản (USP) và giải pháp nỗi đau của sản phẩm thành các kịch bản video ngắn (9:16) thu hút, sẵn sàng để sản xuất hàng loạt.

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Mọi thông tin cấu trúc nằm trong thư mục cấu hình và ngữ cảnh dự án:
1. **`2_marketing_campaign/inputs/product_profile.md`** ← ĐỌC ĐẦU TIÊN để lấy thông tin sản phẩm và khách hàng ICP (Project-level).
2. **`<active_campaign_dir>/content_pillars.md`** ← ĐỌC BẮT BUỘC để lấy danh sách tuyến nội dung (Content Pillars) & thư viện Series áp dụng chung cho tất cả các kênh (Facebook, Threads, IG Reels, TikTok, Short Videos). User sẽ cập nhật file này thường xuyên theo từng chiến dịch.
3. **[video_hooks.md](./references/video_hooks.md)** ← Thư viện hook giữ chân người xem.
4. **[ai_video_playbook.md](./references/ai_video_playbook.md)** ← Hướng dẫn viết kịch bản tối ưu cho AI sản xuất (VO + Visual Prompts).
5. **[manual_video_playbook.md](./references/manual_video_playbook.md)** ← Quy trình quay chụp thủ công (Đang tạm ngưng).

---

## 2. Các Chế độ Hỗ trợ

AI tự động kích hoạt chế độ phù hợp dựa trên yêu cầu của host:

### Chế độ 0: Khởi tạo Lịch trình Video (Campaign Reel Planning Mode)
*   **Trigger:** Khi host yêu cầu "Khởi tạo chiến dịch video ngắn", "Lập kế hoạch video cho campaign mới", hoặc "Tạo file reel_plan.md".
*   **Quy trình xử lý:**
    1. Đọc tệp cấu hình chiến dịch active từ `active_campaign.txt` để xác định thư mục đầu ra `<active_campaign_dir>`.
    2. Đọc brief sản phẩm tại `2_marketing_campaign/inputs/product_profile.md` và thư viện tuyến nội dung tại `<active_campaign_dir>/content_pillars.md` để rút ra danh sách các Series phù hợp cho Short Videos (ví dụ: Tuyến Vocabulary Upgrade cho Series A Split Screen, Tuyến Addressing Fears & Tips cho Series B).
    3. Tạo file kế hoạch tổng quan `<active_campaign_dir>/short_videos/reel_plan.md` theo cấu trúc sau:
       - **Dòng 1:** Thêm Google Doc ID nếu có yêu cầu đồng bộ (VD: `*Google Doc ID: \`[ID]\`*`).
       - **1. Mục tiêu & Chiến lược:** Xác định tần suất (VD: 2 reels/ngày), kênh đăng (IG, TikTok, FB), và công cụ sản xuất.
       - **2. Các Series Song Song:** Định vị rõ cấu trúc của các tuyến nội dung chạy song song dựa trên `content_pillars.md` (VD: Tuyến A - Cung cấp kiến thức/từ vựng nâng band, Tuyến B - Chia sẻ mẹo/tips thực chiến giải quyết nỗi đau của ICP).
       - **3. Lịch Content Calendar:** Lập bảng lịch đăng theo ngày (Day 1 đến Day 14...), chỉ định rõ ID của từng video dạng `VID_D[Số]_[Ký tự Series]` (ví dụ: `VID_D01_A`, `VID_D01_B`).
       - **4. Quy tắc Caption & Hashtag:** Định nghĩa mẫu caption/hashtag cho giai đoạn Warmup (Phase 0) và giai đoạn Seeding (Phase 2).
       - **5. File Structure:** Phác thảo cây thư mục kịch bản sẽ được lưu trữ dạng phẳng trực tiếp trong `short_videos/` dạng `reel_day[Số thứ tự].md` (như `reel_day01.md`, `reel_day02.md`... Tuyệt đối không chia subfolder lẻ `day[Số]/` gây rối mắt và bất tiện).
    4. Trình bày nội dung file `reel_plan.md` cho host review trước khi ghi file thật.

### Chế độ 1: Lên ý tưởng Video (Short Video Ideation Mode)
*   **Trigger:** Khi host yêu cầu "Lên ý tưởng video ngắn cho sản phẩm X", hoặc "Tuần này nên làm những chủ đề video nào?".
*   **Quy trình xử lý:**
    1.  Đọc `2_marketing_campaign/inputs/product_profile.md` để hiểu sản phẩm và `<active_campaign_dir>/content_pillars.md` để lấy định hướng tuyến nội dung.
    2.  Đề xuất 3 ý tưởng video ngắn theo 3 hướng tiếp cận khác nhau dựa trên `content_pillars.md`:
        *   *Ý tưởng 1 (Pain point / Addressing Fears):* Đánh thẳng vào nỗi sợ/sự bực bội của ICP.
        *   *Ý tưởng 2 (Product Demo / Showcase):* Trực quan hóa giải pháp độc bản của sản phẩm.
        *   *Ý tưởng 3 (Storytelling / Case study):* Câu chuyện thay đổi trước-sau khi dùng sản phẩm.
    3.  Mỗi ý tưởng phải đề xuất sẵn: 1 Hook phù hợp từ `video_hooks.md`, mô tả ngắn về visual chính, và mục tiêu chuyển đổi.

### Chế độ 2: Viết kịch bản AI Video (AI Script Generation Mode) - MẶC ĐỊNH
*   **Trigger:** Khi host yêu cầu "Viết kịch bản video ngắn", "Sinh script Reels", hoặc "Làm kịch bản cho ý tưởng X bằng AI".
*   **Quy trình xử lý:**
    1.  Đọc quy chuẩn kịch bản trong `ai_video_playbook.md` và các quy định tuyến nội dung (định dạng, visual style, series structure) tại `<active_campaign_dir>/content_pillars.md`.
    2.  Chọn ra Hook tốt nhất từ `video_hooks.md` và tinh chỉnh phù hợp với tuyến nội dung đã định vị trong `content_pillars.md`.
    3.  Gán **Unique ID** cho video theo **Ngày (Day)** (Áp dụng từ chiến dịch tiếp theo): dạng `VID_D[Số thứ tự]_A` (cho Series A Vocab của ngày đó) và `VID_D[Số thứ tự]_B` (cho Series B Tips của ngày đó). Ví dụ: `VID_D01_A` và `VID_D01_B`.
    4.  Lưu kịch bản thành file chung của ngày tại thư mục tương ứng: `<active_campaign_dir>/short_videos/reel_day[Số thứ tự].md`.
    5.  **Quy tắc Visual Prompts trong kịch bản:**
        *   **Không ghi prompt ảnh tĩnh** (Midjourney/DALL-E 3) trực tiếp vào file kịch bản ngày. Các prompt ảnh tĩnh (Step 1) được quản lý và sinh riêng trong file `<active_campaign_dir>/short_videos/visual_prompt.md`.
        *   Trong file kịch bản ngày, chỉ ghi **AI Video Generation Prompts (Motion)** (Step 2) cho các công cụ như Grok/Kling/Luma, sử dụng ảnh tĩnh từ Step 1 làm First Frame.
        *   **Quy tắc Bố cục & Vị trí Khuôn mặt (Mandatory Face Composition & 60% Height Rule):** Mặt nhân vật luôn nằm **chính giữa trục ngang (`centered horizontally`)** và ở **độ cao ~60% tính từ đáy ảnh lên (`positioned at 60% vertical height / upper-middle region`)**. Sử dụng nhất quán góc chụp `Medium close-up portrait shot` cho tất cả ảnh để kích thước mặt đồng nhất, tránh tình trạng ảnh mặt quá to hoặc lệch vị trí khi dựng Reels / Split Screen và chừa 40% khoảng trống bên dưới cho Subtitles.
        *   **Quy tắc rõ mặt và khẩu hình tự nhiên (Anti-Downward Face & Anti-Lip Glitch):** Tuyệt đối không cho phép nhân vật cúi gằm mặt xuống bàn/sách/laptop hoặc che mặt. Khuôn mặt của nhân vật chính phải luôn rõ ràng và sắc nét các chi tiết (`face fully visible`, `clear facial features`) hướng trực diện/ngước nhìn camera (`looking at the camera`, `looking up from notebook`). **Đặc biệt cấm mô tả gây mím/biến dạng khẩu hình** (như `biting lip`, `pursed lips`, `pressed lips`, `covering mouth`). Luôn yêu cầu cơ miệng thả lỏng tự nhiên hoặc hơi hé mở (`lips relaxed`, `mouth slightly open`, `lips slightly parted`) để AI video generator có thể chạy khẩu hình (lip-sync) chuẩn xác không bị méo mặt.
        *   **Quy tắc chống lỗi biến dạng vật thể ở tay (Anti-Hand Object Glitch):** Tránh mô tả nhân vật cầm nắm các vật thể nhỏ (bút, điện thoại, giấy, cốc nước...) trên tay để hạn chế lỗi AI làm biến mất hoặc méo mó vật thể khi chuyển động. Không yêu cầu đếm ngón tay hoặc cử chỉ biểu thị số lượng; AI video thường tái tạo ngón tay không chính xác. Ưu tiên cử chỉ tay không tự nhiên, không định lượng (`gentle natural hand gestures`, `resting chin on hand`, `adjusting hair`).
        *   **Quy tắc chống nét căng đét giả tạo (Anti-Plastic/Uncanny Look):** Không dùng các từ khóa bóng bẩy như `8k`, `hyperrealistic`, `smooth skin`. Bắt buộc chèn các từ khóa tạo texture ảnh chụp thật: `candid photography`, `raw photo`, `natural skin texture`, `shot on iPhone`, và render motion ở độ phân giải `1080p`.
        *   **Quy tắc khung hình đơn, không dính người đối diện (Single Person / No Over-the-Shoulder):** Tuyệt đối không sử dụng góc máy `over-the-shoulder` (nhìn từ sau vai/dính vai người đối diện). Tránh dùng các từ khóa gợi ý bối cảnh đối thoại dính người khác. Luôn chỉ định rõ: `single person in frame`, `only one person in frame`, `no other people`, `no examiner`, `no interviewer`, `avoid over-the-shoulder shots`.
        *   **Quy tắc định nghĩa giọng nói & tông giọng (Voice & Tone Prompt):** Bắt buộc phải khai báo rõ giới tính, độ tuổi, sắc tộc, tông giọng (hesitant/confident), tốc độ nói (slow/natural) trực tiếp trong prompt tạo video dưới dạng khối ngoặc vuông `[Voice: ...]` dựa trên tệp `brand_guidelines.md` và `ai_character.md` của dự án. Mặc định dùng `clear neutral Vietnamese accent`; chỉ ghi giọng vùng miền khi brand guidelines hoặc host chỉ định rõ. Ví dụ:
            *   *Với vai ngập ngừng/lỗi sai (Ví dụ: Low Level):* `[Voice: [Đặc tả giọng nhân vật], speaking hesitantly with low confidence, slow pacing, nervous tone]`
            *   *Với vai tự tin/nâng cấp (Ví dụ: High Level):* `[Voice: [Đặc tả giọng nhân vật], speaking confidently with high energy, natural speed, friendly and steady tone]`

        *   **Nguồn Voiceover (Thuyết minh):** Sử dụng các công cụ Text-to-Speech như ElevenLabs (giọng tự nhiên nhất), FPT.AI / Vbee, hoặc dùng trực tiếp tính năng TTS của CapCut (Cô gái hoạt bát / Thanh niên tự tin) khi dựng video.
        *   **Yêu cầu cô đọng nội dung và Pacing cho tuyến bài nói nhiều (ví dụ: Tuyến chia sẻ mẹo/tips):** Tổng thời lượng đọc tối ưu trong vòng 10s. Giới hạn độ dài thoại tối đa **40 âm tiết** cho mỗi prompt đơn lẻ.
            *   *Option 1 (Full Speech - Khuyên dùng):* Khi Hook + ý chính không quá 40 âm tiết, gộp thành **một prompt duy nhất** để giảm số clip cần gen và giữ chuyển cảnh tự nhiên. Dùng tốc độ nói bình thường: `speaking with a friendly, warm and clear tone`; phần thời gian còn lại dành cho biểu cảm/cử chỉ.
            *   *Option 2 (Tách 2 Prompt):* Chỉ tách Hook và Content thành hai prompt khi tổng lời thoại vượt 40 âm tiết, cần hai visual khác nhau, hoặc tool không khớp khẩu hình ổn định với thoại dài.
        *   **Câu chốt giá trị (Mandatory Outcome Line):** Sau hướng dẫn/mẹo chính và trước CTA, bắt buộc thêm một câu ngắn nêu lợi ích trực tiếp người xem nhận được. Câu này khép vòng nội dung, tránh video kết thúc cụt ở phần hướng dẫn. Ví dụ: “Câu trả lời sẽ rõ ràng và dễ triển khai hơn nhiều.” Không dùng claim tuyệt đối hoặc chưa kiểm chứng như “giám khảo sẽ đánh giá cao ngay”, “chắc chắn tăng band”.
        *   **Kết luận song ngữ trong cùng prompt (Bilingual Conclusion):** Với Reel dạy tiếng Anh có câu mẫu English, gộp câu kết luận tiếng Việt vào **cùng prompt thoại của clip nội dung cuối**; không tạo clip kết luận riêng. Ghi rõ thứ tự: nói xong câu English → ngắt nhẹ khoảng 0.5 giây → nói câu kết luận tiếng Việt. Câu kết luận **có thể chính là CTA**; được phép thêm từ đệm tự nhiên để lời nói liền mạch, không cần ép khác ý hoặc khác câu chữ.
        *   **Biến thể cấu trúc so sánh/đối thoại (Ví dụ: Question & Answer / Wrong vs Right):** Hỗ trợ dạng split screen/so sánh góc nhìn ở 0-12s, kết thúc bằng CTA ở 12-15s.
        *   **Quy tắc khớp khẩu hình & Động tác tự nhiên (Motion Prompt):**
            *   Mở đầu prompt motion bằng câu ngắn cố định: `Use reference image as the starting frame.` Không cần nhắc lại tên file hay mô tả dài về ảnh nguồn; người sản xuất đính kèm đúng reference image khi chạy prompt.
            *   Bắt buộc chèn trực tiếp nội dung đối thoại vào prompt dưới dạng `saying: "[Câu thoại]"` bằng ngôn ngữ tương ứng để AI khớp khẩu hình.
            *   Bổ sung các cử chỉ tay tự nhiên phù hợp với biểu cảm (`natural hand gestures`, `fidgeting with hands`, `shrugging`), chớp mắt tự nhiên (`natural eye blinking`), chuyển động đầu/vai (`head nods`, `subtle body swaying`).
            *   Bổ sung chuyển động camera cầm tay nhẹ (`slight handheld camera motion`) để tăng độ chân thực cho cảnh quay.
        *   **Cơ chế Reusable CTA Clips (Clip CTA dùng chung):** Không cần gen hành động chỉ tay riêng cho từng video. Viết CTA clip dài 3s bắt đầu bằng `Use reference image as the starting frame.`; người sản xuất tự chọn và đính kèm ảnh tham chiếu khi chạy. Thoại CTA phải bắt đầu trong 3 giây đầu của clip. Tuyệt đối không mô tả hoặc yêu cầu AI sinh UI/button (ví dụ `Save button`); dùng cử chỉ tay tự nhiên, không định hướng vào UI. Có thể tái sử dụng clip CTA này cho cùng Style Tag bối cảnh.
        *   **Cấu trúc chi tiết cho từng Video Script:** Mỗi video trong file tuần phải hiển thị rõ phần **On-Screen Elements & Audio** bao gồm:
            *   *Hook Text:* Text hiển thị nổi bật ở 0-2s.
            *   *Audio/SFX:* Mô tả cụ thể nhạc nền (Ducking giảm âm lượng khi nhân vật nói, tăng volume khi Hook/CTA) và âm thanh bổ trợ (SFX ngơ ngác/record scratch cho phiên bản sai/cũ, SFX chuyên nghiệp/sparkle/ding cho phiên bản đúng/mới, click sound cho CTA).
            *   *CTA Text:* Nội dung chữ kêu gọi hành động cụ thể cho bài đó.


### Chế độ 3: Viết kịch bản Quay thủ công (Manual Script Mode)
*   **Trigger:** Khi host yêu cầu viết kịch bản tự quay chụp thủ công.
*   **Quy trình xử lý:**
    1.  Hiện tại chế độ này đang ở trạng thái **tạm ngưng** hoạt động theo yêu cầu của team vận hành.
    2.  Xuất ra thông báo nhắc nhở host:
        > "⚠️ Hiện tại quy trình quay video thủ công đang được đặt ở chế độ tạm ngưng để tập trung 100% tài nguyên cho AI Video. Tôi sẽ tự động chuyển sang viết kịch bản tối ưu cho AI sản xuất (`ai_video_playbook.md`). Bạn có muốn tiếp tục không?"
    3.  Nếu host vẫn yêu cầu quay thủ công, tham chiếu cấu trúc của `manual_video_playbook.md` để phác thảo sơ bộ A-Roll và B-Roll cho host.

---

## Lịch sử Cập nhật (Changelog)

- **v2.0.0 (2026-07-25):**
  - Cho phép câu kết luận song ngữ dùng trực tiếp làm CTA, có thể thêm từ đệm để lời nói tự nhiên; bỏ yêu cầu CTA phải khác câu chữ/kết luận.
- **v1.9.0 (2026-07-25):**
  - Chuẩn hóa kết luận tiếng Việt trong cùng prompt thoại sau câu English, với nhịp ngắt nhẹ; CTA nói trong 3 giây đầu và không mô tả UI/button.
- **v1.8.0 (2026-07-25):**
  - Cấm prompt yêu cầu đếm ngón tay/cử chỉ biểu thị số lượng; thay bằng cử chỉ tay tự nhiên, không định lượng.

