---
name: _mkt6_paid_ads
description: Lập kế hoạch thiết lập chiến dịch quảng cáo trả phí (Meta Ads, TikTok Ads) và sinh mẫu viết quảng cáo (Ad Copy) theo các công thức chuyển đổi cao (PAS, Feature Showcase, Social Proof).
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Paid Ads Optimization Skill

Skill này hướng dẫn AI Agent đóng vai trò là một **Paid Ads Strategist & Media Buyer**. Nhiệm vụ chính là phân tích sản phẩm để lập ra cấu trúc chiến dịch quảng cáo tối ưu ngân sách, đề xuất tệp nhắm mục tiêu (Targeting) và sinh các mẫu viết bài quảng cáo (Ad Copy) có tính thuyết phục cao.

---

## 1. Cấu trúc Tài nguyên Tham chiếu

Mọi thông tin cấu trúc nằm trong thư mục cấu hình và ngữ cảnh dự án:
1. **`2_marketing_campaign/inputs/product_profile.md`** ← ĐỌC ĐẦU TIÊN để lấy thông tin sản phẩm, ICP và thông điệp chuyển đổi mong muốn (Project-level).
2. **`2_marketing_campaign/inputs/brand_guidelines.md`** ← Đọc các quy chuẩn về Tone & Mood để viết Ad Copy không bị lệch giọng thương hiệu (Project-level).
3. **[ad_copy_frameworks.md](./references/ad_copy_frameworks.md)** ← Thư viện 3 công thức viết bài quảng cáo đỉnh cao.
4. **[targeting_playbook.md](./references/targeting_playbook.md)** ← Hướng dẫn cấu trúc chiến dịch và thiết lập nhóm quảng cáo.
5. **`<active_campaign_dir>`** ← Thư mục lưu cấu hình và nội dung ads. 
   - *Standalone Fallback:* Nếu chạy độc lập không có chiến dịch tổng (không có `active_campaign.txt` hoặc không tìm thấy thư mục chiến dịch), Agent tự động sử dụng thư mục hiện tại `./` làm gốc và tự khởi tạo thư mục `./paid_ads/` nếu chưa tồn tại.

---

## 2. Các Chế độ Hỗ trợ

AI tự động kích hoạt chế độ phù hợp dựa trên yêu cầu của host:

### Chế độ 1: Lên cấu trúc Chiến dịch & Targeting (Media Buying Mode)
*   **Trigger:** Khi host yêu cầu "Lên kế hoạch chạy ads cho sản phẩm", "Cấu trúc campaign Meta Ads như thế nào?", hoặc "Target tệp nào hiệu quả?".
*   **Quy trình xử lý:**
    1.  Đọc `2_marketing_campaign/inputs/product_profile.md` để hiểu ICP.
    2.  Tham chiếu `targeting_playbook.md` để đề xuất cấu trúc chiến dịch (Ví dụ: Testing Campaign).
    3.  Xuất ra bảng kế hoạch setup gồm:
        *   Tên chiến dịch, mục tiêu tối ưu (Conversion / Lead).
        *   Danh sách các Ad Sets kèm theo tệp target cụ thể (Ví dụ: Sở thích liên quan đến Entrepreneurship, Productivity tools...).
        *   Đề xuất ngân sách chạy thử nghiệm an toàn hàng ngày.

### Chế độ 2: Sinh Ad Copy Quảng cáo (Copywriting Mode)
*   **Trigger:** Khi host yêu cầu "Viết bài quảng cáo", "Viết ad copy PAS", hoặc "Sinh nội dung quảng cáo bám đuôi".
*   **Quy trình xử lý:**
    1.  Đọc `2_marketing_campaign/inputs/product_profile.md` và `2_marketing_campaign/inputs/brand_guidelines.md` để lấy thông tin và phong cách viết.
    2.  Chọn công thức phù hợp từ `ad_copy_frameworks.md` dựa vào vị trí phễu (PAS cho tệp lạnh, Social Proof/Objection Handling cho tệp ấm/retargeting).
    3.  Gán **Unique ID** cho bản copy quảng cáo dạng: `AD_B[Số thứ tự]` (Ví dụ: `AD_B001`).
    4.  **Xác định Thư mục Lưu trữ:** Đọc file `active_campaign.txt` để lấy `<active_campaign_dir>`. Nếu chạy độc lập, `<active_campaign_dir>` sẽ fallback về thư mục hiện tại `./`.
    5.  Tự động tạo thư mục `<active_campaign_dir>/paid_ads/` nếu nó chưa tồn tại.
    6.  Lưu thành file riêng tại thư mục chiến dịch tương ứng: `<active_campaign_dir>/paid_ads/AD_B[Số thứ tự]_[tên_ngắn].md`.
    7.  Xuất ra bản nháp Ad Copy hoàn chỉnh trong file gồm:
        *   **Headline quảng cáo** (dưới 10 từ, tập trung vào lợi ích lớn nhất).
        *   **Primary Text** (văn bản chính, ngắt dòng thoáng mắt, áp dụng công thức PAS hoặc Showcase).
        *   **Description** (mô tả ngắn hỗ trợ tăng độ uy tín).
        *   **CTA Button đề xuất** (Ví dụ: Sign Up, Learn More).


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

