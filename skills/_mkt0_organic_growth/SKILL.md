---
name: _mkt0_organic_growth
description: Lên kế hoạch chiến dịch, sinh kịch bản tương tác và nội dung kéo tăng trưởng tự nhiên cho team vận hành tài khoản Threads thật. AI đọc campaign_tracker.md để hiểu trạng thái chiến dịch, đọc team_roster.md để biết thành viên, rồi gen kịch bản nhiệm vụ có timeline giãn cách an toàn và nội dung 3 tầng cho từng người.
---

> **Version:** 1.1.0  
> **Last Updated:** 2026-07-24  


# Threads Organic Growth Skill

Skill này giúp AI Agent đóng vai trò **Growth & Content Specialist** cho team vận hành Threads. Mô hình hoạt động dựa trên **Organic Pod** — mỗi thành viên sử dụng tài khoản thật của riêng mình (khác thiết bị, khác IP, khác hành vi tự nhiên), phối hợp tương tác để khuếch đại reach mà không bị thuật toán quét spam.

### 1. Cấp độ Dự án (Project-level Context - Cố định)
Nằm trong thư mục `2_marketing_campaign/` để cung cấp bối cảnh chung của sản phẩm (được khởi tạo từ references của skill `_mkt0_organic_growth`):
- **[product_profile.md](../../../2_marketing_campaign/inputs/product_profile.md)**: USP, ICP và thông tin sản phẩm.
- **[competitor_analysis.md](../../../2_marketing_campaign/inputs/competitor_analysis.md)**: Tuyến nội dung, hook và visual đối thủ thành công.
- **[brand_guidelines.md](../../../2_marketing_campaign/inputs/brand_guidelines.md)**: Quy chuẩn Tone & Mood của Brand.
- **[team_roster.md](../../../2_marketing_campaign/setup/team_roster.md)**: Danh sách thành viên team và giờ online.
- **[channels.md](../../../2_marketing_campaign/setup/channels.md)**: Các kênh truyền thông (Main & Ambassador).

### 2. Cấp độ Chiến dịch (Campaign-level Execution - Thay đổi động)
Nằm trong thư mục chiến dịch chạy thực tế (Ví dụ: `mkt_july_camp/`). Agent xác định thư mục này bằng cách đọc file `active_campaign.txt` tại thư mục gốc của workspace hoặc qua chỉ định trực tiếp trong prompt của Host.
- **`<active_campaign_dir>/campaign_tracker.md`**: Tracker lịch đăng bài, mục tiêu, phase đợt này (được copy từ references của skill `_mkt0_organic_growth`).
- **`<active_campaign_dir>/content_pillars.md`**: Thư viện Tuyến nội dung (Content Pillars/Angles) áp dụng chung cho TẤT CẢ các kênh Marketing (Threads, Facebook, IG Reels, TikTok, Short Videos...). Được copy từ references sang thư mục chiến dịch để người dùng cập nhật & tùy biến thường xuyên theo từng đợt chạy.
- **`<active_campaign_dir>/performance_log.md`**: Nhật ký hiệu quả chi tiết của chiến dịch đợt này (được copy từ references của skill `_mkt0_organic_growth`).

---

## Chế độ vận hành

Skill này hoạt động ở **4 chế độ**. AI tự xác định chế độ dựa vào yêu cầu của host:

| Yêu cầu của host | Chế độ | Đầu ra |
|---|---|---|
| Chứa từ khóa "Setup chiến dịch", có khối [MỤC TIÊU], [TEAM]... | **Quick Setup Mode** | Tự fill `team_roster.md` + `campaign_tracker.md`, báo cáo lại |
| "Lên kế hoạch chiến dịch", "Giúp tôi plan", "Bài nào nên đăng tiếp?" | **Campaign Mode** | Bảng liệt kê bài viết theo phase + gợi ý nội dung dựa trên `content_pillars.md` |
| "Gen kịch bản cho bài \[X\]", "Bài sắp đăng, cần phân công team" | **Per-Post Mode** | Bảng nhiệm vụ theo timeline + nội dung 3 tầng |
| "Review hiệu quả", "Phân tích kết quả", "Nên điều chỉnh gì?", có khối [BÁO CÁO] | **Review Mode** | Phân tích pattern + đề xuất điều chỉnh chiến dịch |

## Quick Setup Mode — Tự Đọc và Map 1 File Brief Đầu Vào

Trigger: host gửi prompt có cụm "Setup dự án từ brief" hoặc "Setup chiến dịch". Agent sẽ đọc file `_marketing_brief.md` từ `2_marketing_campaign/_marketing_brief.md` (hoặc khởi tạo từ references của skill `_mkt0_organic_growth` nếu chưa tồn tại) và file PRD của dự án (nếu được chỉ định).

### Bước QS-1: Đọc và phân tích Brief

Agent đọc file `_marketing_brief.md` và trích xuất:
- **Thông tin sản phẩm:** USP, ICP, CTA chính -> Điền vào `2_marketing_campaign/inputs/product_profile.md` (copy từ references của skill `_mkt0_organic_growth`).
- **Thông tin đối thủ:** Các tuyến bài viết viral, phong cách visual -> Điền vào `2_marketing_campaign/inputs/competitor_analysis.md` (copy từ references của skill `_mkt0_organic_growth`).
- **Tone & Mood:** Quy định xưng xô, từ khóa, Do's & Don'ts -> Điền vào `2_marketing_campaign/inputs/brand_guidelines.md` (copy từ references of skill `_mkt0_organic_growth`).
- **Hồ sơ nhân vật AI:** Lấy mô tả ngoại hình tiếng Việt, **dịch sang tiếng Anh chuẩn kỹ thuật (Midjourney tags)** -> Điền vào `2_marketing_campaign/inputs/ai_character.md` (copy từ references của skill `_mkt0_organic_growth`).
- **Thư viện Tuyến nội dung, Mẫu Hooks, Pattern Tương tác:** Tự động copy `content_hooks.md` và `audience_patterns.md` vào `2_marketing_campaign/inputs/` và copy `content_pillars.md` từ references sang `<active_campaign_dir>/content_pillars.md` làm thư viện tuyến nội dung dùng chung cho tất cả các kênh đợt này.
- **Danh sách thành viên:** Username, giờ online -> Điền vào `2_marketing_campaign/setup/team_roster.md` (copy từ references của skill `_mkt0_organic_growth`).
- **Danh sách kênh:** Main & Ambassador -> Điền vào `2_marketing_campaign/setup/channels.md` (copy từ references của skill `_mkt0_organic_growth`).

### Bước QS-2: Khởi tạo thư mục Chiến dịch Active

Dựa trên chỉ định thư mục chiến dịch của Host (hoặc lấy từ `active_campaign.txt`), Agent tự động tạo thư mục chiến dịch mới và copy các templates từ references của skill `_mkt0_organic_growth` sang:
- Copy `campaign_tracker.md` từ references của skill sang `<active_campaign_dir>/campaign_tracker.md`.
- Copy `content_pillars.md` từ references của skill sang `<active_campaign_dir>/content_pillars.md`.
- Copy `performance_log.md` từ references của skill sang `<active_campaign_dir>/performance_log.md`.
- Copy `personal_log.md` từ references của skill sang `<active_campaign_dir>/personal_log.md`.
- Đọc template `experiments.md` từ references của skill, trích xuất thông tin Pains, Hooks, ICP, Messages, CTA cụ thể của sản phẩm từ brief đầu vào và điền để tạo file `<active_campaign_dir>/experiments.md`.
- Tự động điền phase ban đầu và lịch trình đề xuất cho tuần đầu tiên vào `<active_campaign_dir>/campaign_tracker.md`.

### Bước QS-3: Báo cáo và xác nhận

Sau khi phân tách và điền xong tất cả các file cấu hình, xuất ra màn hình tóm tắt:

```
✅ Đã onboarding thành công dự án từ _marketing_brief.md!
└ Đã cấu hình các file inputs tại 2_marketing_campaign/inputs/ (gồm product_profile, brand_guidelines, competitor_analysis, ai_character, content_pillars, content_hooks, audience_patterns)
└ Đã cấu hình các file nhân sự/kênh tại 2_marketing_campaign/setup/
└ Đã khởi tạo thư mục chiến dịch active tại: [Đường dẫn thư mục chiến dịch]
  ├ campaign_tracker.md: [số phase] phase — [mục tiêu chiến dịch]
  ├ performance_log.md: (Sẵn sàng log chỉ số)
  ├ personal_log.md: (Sẵn sàng cho team)
  └ experiments.md: (Thư viện thử nghiệm của chiến dịch)

Bạn có muốn điều chỉnh thông tin nào trong các file cấu hình đã gen không?
```


## Campaign Mode — Lên Kế Hoạch Chiến Dịch

### Bước CM-1: Đọc cả hai file bắt buộc

Đọc `<active_campaign_dir>/campaign_tracker.md` và `2_marketing_campaign/setup/team_roster.md`. Nếu một trong hai chưa được điền hoặc chưa được tạo, nhắc host thực hiện trước.

### Bước CM-2: Báo cáo trạng thái hiện tại

Trước khi đề xuất bất cứ điều gì, xuất rà màn hình nọi dung sau:

```
⏳ TRẠNG THÁI CHIẾN DỊCH

Phase hiện tại : [tên phase]
Tiến độ           : Bài [X] / [Tổng]
Bài gần nhất    : [mô tả ngắn] (đăng [ngày]) — đang ở trạng thái: [trạng thái]
Bài tiếp theo    : [mô tả ngắn] — dự kiến [ngày]
Ghi chú           : [nếu có]
```

### Bước CM-3: Đề xuất các bài viết theo phase

Dựa vào phase hiện tại trong tracker và content mix mục tiêu, đề xuất 3–5 bài viết tiếp theo:

| Gợi ý bài | Kênh | Goal | Pattern giao y | Hướng nội dung ngắn | Ưu tiên |
|---|---|---|---|---|---|
| ... | brand / founder / member | ... | ... | ... | cao / trung bình / thấp |

- **Brand channel posts** và **Organic Pod posts** cần được phân biệt rõ — không trộn đức điềm goal giữa hai kênh.
- Brand channel tập trung vào **Trust / Product Discovery / Conversion**.
- Organic Pod tập trung vào **Reach / Engagement / Relatable content**.

### Bước CM-4: Gợi ý cập nhật tracker

Sau khi host xác nhận kế hoạch, gợi ý những dòng cần điền vào `<active_campaign_dir>/campaign_tracker.md` (host tự copy và cập nhật):

```
Các dòng cần thêm vào bảng Content Calendar:
| [#] | [ngày] | [kênh] | [phase] | [goal] | [pattern] | planned | |
...
```

---

## Per-Post Mode — Sinh Kịch Bản Từng Bài

### Bước 0: Đọc File Bắt buộc (BUẦU TIÊN)

Trước khi làm bất cứ điều gì, hãy đọc `2_marketing_campaign/setup/team_roster.md` để nắm:
- **Số lượng thành viên** → quyết định bao nhiêu "lượt" tương tác trong kịch bản
- **Username từng người** → gán nhiệm vụ cụ thể cho đúng người
- **Giờ online của từng thành viên** → lên timeline giãn cách thực tế, không phải lý thuyết
- **Vai trò** (host / co-host / supporter) → phân loại ai đăng bài gốc, ai vào tương tác

Nếu `team_roster.md` chưa được điền, hãy nhắc host điền trước khi tiếp tục.

---

### Bước 1: Thu thập Thông tin Chiến dịch & Giả thuyết Thử nghiệm

- **Đọc file thử nghiệm chiến dịch:** Đọc `<active_campaign_dir>/experiments.md` để xác định các giả thuyết (Hypothesis) đang cần test (ví dụ: Nỗi đau cụ thể, Hook, Core Message, CTA...). Chọn ra **ít nhất 1 giả thuyết chưa chạy hoặc cần test thêm** để làm mục tiêu cho bài viết này.
- **Sản phẩm / Chủ đề bài viết:** Tên, điểm nổi bật, nỗi đau giải quyết được (đối chiếu với giả thuyết nỗi đau được chọn từ file thử nghiệm).
- **Đối tượng mục tiêu (Niche):** Threads đang muốn tiếp cận ai (Developer, Designer, Marketer...)?
- **Mục tiêu chiến dịch:** Tăng tương tác? Kéo traffic? Tăng follower? Giới thiệu tính năng khéo?

---

### Bước 2: Thiết lập Ma trận Phối hợp (Content Matrix)

Với mỗi bài viết trong kế hoạch, chọn tổ hợp:
1. **Người đăng:** Thành viên có vai trò `host` hoặc `co-host` theo `2_marketing_campaign/setup/team_roster.md`.
2. **Goal & Hypothesis:** Lấy từ các mục tiêu chiến dịch định vị trong `brand_guidelines.md`/`content_pillars.md` và **khớp với giả thuyết thử nghiệm** đã chọn từ `<active_campaign_dir>/experiments.md`.
3. **Pattern:** Chọn từ `audience_patterns.md` hoặc tuyến bài viết cụ thể trong `content_pillars.md` phù hợp để test giả thuyết đó.
4. **Hook:** Lấy mẫu tương ứng từ `content_hooks.md` để phát triển hook 1-3 dòng đầu (hoặc lấy trực tiếp từ Hook Experiment của file thử nghiệm).
5. **Tone & CTA:** Phù hợp với tính cách thật của người đăng và quy định tone tại `brand_guidelines.md`.

---

### Bước 3: Sinh Kịch bản & Phân tách File với Unique ID

AI phải gán **Unique ID** cho từng nội dung được sinh ra để quản lý và đối chiếu:
- **Kênh Host/Brand (Bài gốc):** Định danh dạng `POST_B[Số thứ tự]` (Ví dụ: `POST_B001`, `POST_B002`). Lưu thành file riêng tại thư mục chiến dịch: `<active_campaign_dir>/threads_posts/POST_B[Số thứ tự]_[tên_ngắn].md`.
- **Kênh Member (Bài đăng cá nhân):** Định danh dạng `POST_[username]_M[Số thứ tự]` (Ví dụ: `POST_dan_M001`). Lưu thành file riêng tại thư mục chiến dịch: `<active_campaign_dir>/member_posts/[username]/POST_[username]_M[Số thứ tự]_[tên_ngắn].md`.

Xuất kịch bản tổng quan dưới dạng **bảng nhiệm vụ theo timeline**, gán rõ tên thành viên (lấy từ `team_roster.md`) kèm theo Unique ID tương ứng.

#### Cấu trúc Timeline Chuẩn An Toàn

| Thời điểm | Người thực hiện | Unique ID nhiệm vụ | Hành động & Kịch bản chi tiết | Ghi chú an toàn |
|---|---|---|---|---|
| **T+0** (Ngay khi đăng) | Host | `POST_B001` | Đăng bài gốc (Xem file threads_posts/POST_B001.md) | — |
| **T+30 phút** | — | — | ❌ Không ai tương tác | Tránh dấu hiệu seeding tức thì |
| **T+1–2 giờ** | Supporter 1 | `COMMENT_dan_001` | Comment thảo luận (Xem file member_posts/dan/POST_dan_M001.md) | Vào từ tab Following hoặc Search — không dùng link trực tiếp |
| **T+2–3 giờ** | Supporter 2 | `COMMENT_cuong_001` | Comment thảo luận (Xem file member_posts/cuong/POST_cuong_M001.md) | Cách Supporter 1 tối thiểu 10–15 phút |
| **T+3–5 giờ** | Supporter 3+ | `REPOST_hai_001` | Chia sẻ kèm góc nhìn | Tiếp tục giãn cách 10–15 phút/người |
| **T+nửa ngày** | Host | `REPLY_host_001` | Reply comment của team | Kéo dài vòng đời bài |

> **Lưu ý:** Timeline trên là khung tham chiếu. AI phải điều chỉnh theo giờ online thực tế của từng thành viên được ghi trong `team_roster.md`. Nếu một supporter chỉ online buổi tối, đừng lên lịch nhiệm vụ cho họ vào buổi sáng.

---

### Bước 4: Viết Nội dung theo 3 Tầng Output và Tách File Riêng Biệt

Mỗi bài viết gốc và kịch bản tương tác (comment, reply) của từng thành viên phải được lưu thành **các file markdown riêng biệt** trong thư mục của họ tại folder chiến dịch active. Nội dung trong mỗi file được viết song song **2 hoặc 3 tầng** tùy mức độ phức tạp:

#### 🟢 Tầng 1 — Bản nháp hoàn chỉnh (Copy/Paste ngay)
Câu thoại / bài viết viết sẵn, đúng văn phong tự nhiên, đúng vai trò của người thực hiện. Host hoặc thành viên có thể dùng ngay nếu cần gấp.

#### 🟡 Tầng 2 — Tóm gọn ý chính (Để member tự viết lại)
Tóm lại 2–3 ý cốt lõi cần truyền đạt. Member dùng ý này để **tự viết lại theo văn phong của họ**, hoặc nhờ AI cá nhân của họ viết lại — đảm bảo không bị thuật toán quét ra cùng một văn phong/tác giả.

> Ví dụ: *"Ý chính: hỏi về trải nghiệm thực tế khi dùng tính năng X, tỏ ra tò mò chân thật, kết bằng câu hỏi mở. Tone: thoải mái, không cần formal."*

#### ⚪ Tầng 3 — Chỉ có khi nhiệm vụ phức tạp
Nếu nhiệm vụ **đơn giản** (thả tim, follow, lướt xem bài cũ, bình luận dạo bài người khác để warm-up), **bỏ qua Tầng 1 và Tầng 2**, chỉ cần mô tả hành động ngắn gọn:

> Ví dụ: *"Lướt feed 1–2 phút, like dạo 1–2 bài bất kỳ trong tab Following trước khi làm nhiệm vụ chính."*

---

## Quy tắc Nội dung Bắt buộc

### Chống Bot & Spam

- **Độ dài tối thiểu:** Comment trên **5 từ**, có nghĩa, chứa từ khóa liên quan bài viết.
- **Cấm:** Câu rập khuôn ("hay quá", "chấm"), lạm dụng chỉ emoji, copy-paste comment người khác.
- **Bắt buộc có:** Câu hỏi mở ở cuối comment để kích thích host reply → tạo chuỗi hội thoại.
- **Văn phong:** Viết theo kiểu chat tự nhiên của giới trẻ/dân mạng Việt Nam:
  - Sử dụng viết tắt: `k/ko`, `t`, `m`, `vs`, `e`, `b`, `mng`, `đc`, `xíu`.
  - Sử dụng Yahoo emojis cổ điển: `=))`, `:))))`, `^^` và các emoji khác một cách phù hợp.
  - Cho phép viết sai chính tả nhẹ hoặc teen code tự nhiên (ví dụ: `dị đó`, `tới nái liền`).
  - Tránh tuyệt đối văn phong PR/quảng cáo học thuật khô khan.

### Chống Giọng AI (Anti-AI Tone)

- **Cấm** liệt kê gạch đầu dòng (`-`, `*`) hoặc đánh số (`1.`, `2.`) trong bài đăng.
- Viết dưới dạng đoạn văn siêu ngắn (1–2 câu) xuống dòng, tạo khoảng trống thị giác tự nhiên.
- **Cấm** từ ngữ rập khuôn: *dạo gần đây, vô cùng, vượt trội, giải pháp đột phá, điểm đặc biệt nhất, hãy cùng mình khám phá...*
- Chỉ dùng từ khẩu ngữ tự nhiên: *thề là, nói thật thì, đợt này, bữa trước, mình thấy, bác nào, kiểu như, cơ mà, dị á...*

### Nguyên tắc "1 Goal"

Mỗi bài đăng chỉ tập trung hoàn thành **đúng 1 mục tiêu chính**. Không nhét nhiều CTA vào 1 bài.

### Quy tắc "2 Không – 2 Có" cho Comment

| | Quy tắc |
|---|---|
| ❌ Không | Khen ngợi chung chung, vô thưởng vô phạt |
| ❌ Không | Copy-paste comment của người khác |
| ✅ Có | Câu hỏi mở ở cuối để kích thích hội thoại |
| ✅ Có | Văn phong Gen Z, viết thường, tiếng lóng tự nhiên |

---

## Quy tắc An Toàn Tương tác cho Team

### Giai Đoạn 1 — Lần Đầu Kết Nối (Chỉ làm MỘT LẦN duy nhất)

Đây là bước **onboarding** cho thành viên chưa follow tài khoản host. Đây là trường hợp **DUY NHẤT** được phép dùng link trực tiếp do host gửi qua chat nội bộ.

> **Quy trình bắt buộc theo thứ tự:**
> 1. Click link bài viết gốc (từ chat nội bộ) → bài mở ra trên Threads
> 2. **Không tương tác ngay** — click vào **tên / avatar của host** để vào trang cá nhân
> 3. Lướt xem **2–3 bài cũ** trên tường — ở lại tối thiểu **15–20 giây mỗi bài**
> 4. Thả **tim** nhẹ nhàng 1–2 bài (không cần comment ở bước này)
> 5. Bấm **Follow**
> 6. Quay lại bài gốc → tương tác (comment/like) theo nhiệm vụ được giao
>
> ✅ Mục đích: Để thuật toán Meta ghi nhận đây là sự quan tâm tự nhiên, không phải hành vi seeding tức thì theo link.

---

### Giai Đoạn 2 — Các Lần Tương Tác Tiếp Theo (TUYỆT ĐỐI KHÔNG DÙNG LINK TRỰC TIẾP)

Sau khi đã follow, **không bao giờ** vào bài qua link trực tiếp từ chat nội bộ nữa. Chỉ dùng 3 cách sau:

- **Cách 1:** Lướt tab **"Đang theo dõi" (Following)** → tìm bài tự nhiên.
- **Cách 2:** **Search thủ công** tên username của host trên thanh tìm kiếm → Meta đánh giá rất cao hành vi gõ phím này.
- **Cách 3:** Host **Tag nhẹ** thành viên dưới comment → thành viên vào từ **Thông báo (Notification)**.

### Warm-up Trước Khi Làm Nhiệm Vụ (BẮT BUỘC)

> Không mở app lên là đi làm nhiệm vụ ngay. Quy trình: **Lướt feed (1–2 phút) → Like dạo bài hot → Rồi mới vào làm nhiệm vụ chính.**

### Tuyệt đối Không

- Không để 2 tài khoản của **cùng 1 người** tương tác trực tiếp với nhau.
- Không tương tác chéo với bài vừa đăng **dưới 30 phút**.
- Không để cả team làm nhiệm vụ **cùng một thời điểm** (giãn cách tối thiểu 10–15 phút/người).
- Không để hành vi theo chuỗi cố định (Supporter A luôn tương tác trước B, B luôn trước C) → xáo trộn thứ tự mỗi chiến dịch.

---

## Ví dụ Kịch bản Đơn Giản (3 thành viên)

> *Giả sử team có: Host (@brand_account), Mem A (@nguyen_van_a — online tối), Mem B (@tran_thi_b — online trưa & tối)*

**Bài: Host vừa đăng bài chia sẻ kiến thức lúc 9:00 sáng**

| Thời điểm | Người | Nhiệm vụ |
|---|---|---|
| 9:00 | Host | ✅ Đăng bài |
| 9:00–11:00 | Tất cả | ⏳ Không tương tác — để bài "hít thở" |
| 11:30 | Mem B *(online trưa)* | Warm-up 1–2 phút → Vào từ Following → Comment tầng 1 hoặc tự viết theo tầng 2 |
| 12:00–19:00 | — | Bài tiếp tục lưu thông tự nhiên |
| 20:30 | Mem A *(online tối)* | Warm-up → Search username host → Comment thảo luận tiếp |
| 21:30+ | Host | Reply comment của Mem B và Mem A → kéo dài vòng đời bài |

---

## Review Mode — Phân Tích Hiệu Quả & Điều Chỉnh Chiến Dịch

Trigger: host gửi dữ liệu hiệu quả bài viết (có khối [BÁO CÁO]) hoặc yêu cầu phân tích / điều chỉnh chiến dịch.

### Bước R-1: Nạp dữ liệu

1. Đọc `<active_campaign_dir>/performance_log.md` — lấy các log bài đã có.
2. Đọc `<active_campaign_dir>/campaign_tracker.md` — lấy bối cảnh kế hoạch (phase, goal ban đầu, nội dung mix dự kiến).
3. Nếu host gửi dữ liệu mới trong prompt (khối [BÁO CÁO]), **ghi vào `<active_campaign_dir>/performance_log.md` trước** rồi mới phân tích.

### Bước R-2: Cập nhật `campaign_tracker.md`

Điền các cột Views, Comments, Rating trong bảng Content Calendar dựa vào dữ liệu vừa được log. Không thay đổi các cột khác.

### Bước R-3: Phân tích pattern

Với tất cả bài đã có trong log, phân tích:

| Câu hỏi phân tích | Dữ liệu cần |
|---|---|
| Goal nào cho Views cao nhất? | So sánh avg Views theo Goal |
| Pattern nào tạo Comment depth tốt nhất? | So sánh comment depth theo Pattern |
| Kênh nào perform ổn định hơn? | brand vs founder vs member |
| Khung giờ nào tương tác tốt hơn? | So sánh giờ đăng vs mức độ tương tác |
| Thành viên nào đưa ra comment có ảnh hưởng nhất? | Bài nào có comment depth tốt — thành viên nào tham gia? |
| Có dấu hiệu bị filter không? | Bài nào có comment bị ẩn, seeding không đủ người? |
| Tỉ lệ content mix thực tế vs kế hoạch? | So sánh Goal phân bổ thực tế và target trong tracker |

### Bước R-4: Xuất báo cáo và đề xuất

Xuất ra theo cấu trúc:

```
📊 BÁO CÁO HIỆU QUẢ — [tên chiến dịch] — [ngày]

Tổng bài đã log : X bài
Phase hiện tại : Phase [X]

⭐ Hoạt động tốt:
- [Goal/Pattern] — avg [X] views, [Y] comments
- [Quan sát cụ thể nào đang rõ ràng]

⚠️ Cần chú ý:
- [Vấn đề nào đang xuất hiện]

🔄 ĐỀ XUẤT ĐIỀU CHỄNH:
1. [Hành động cụ thể — ví dụ: tăng tần suất Reach content, rút ngắn Phase 2 xuống 1 tuần...]
2. [...]
3. [...]

📅 BÀI VIẾT TIẾP THEO NÊN LÀ:
[Gợi ý 2–3 bài phù hợp với data vừa phân tích]
```

Sau đó:
1. Cập nhật phần **Pattern Analysis** trong `<active_campaign_dir>/performance_log.md` với kết quả phân tích mới nhất.
2. Ghi nhận kết luận thực tế và các **Bài học rút ra (Lessons Learned)** vào `<active_campaign_dir>/campaign_overview.md`.
3. **Cơ chế Tự học & Đồng bộ Thử nghiệm (Back-propagation & Experiment Tracking):** 
   - Agent tự động cập nhật hoặc đề xuất cập nhật các thay đổi cần thiết vào file quy chuẩn `2_marketing_campaign/inputs/brand_guidelines.md` và các file tham chiếu phụ trợ để tối ưu cho các đợt sinh bài tiếp theo.
   - **Cập nhật experiments.md:** 
     * **Khi lên lịch (Per-Post Mode):** Ghi chú trạng thái lập lịch ngay bên cạnh giả thuyết được test trong `<active_campaign_dir>/experiments.md`. Định dạng: `- [Giả thuyết] (Test: POST_ID | Status: Scheduled)`
     * **Khi review kết quả (Review Mode):** Cập nhật kết quả thực tế bên cạnh giả thuyết đã test trong `<active_campaign_dir>/experiments.md`. Định dạng: `- [Giả thuyết] (Test: POST_ID | Result: [Views]/[Likes] | [Rating])`
     * Mẫu chuẩn này cũng phải được áp dụng đồng bộ cho file `2_marketing_campaign/templates/experiments.md`.


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

