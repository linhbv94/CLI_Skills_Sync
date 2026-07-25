# Ads Setup & Targeting Playbook (Hướng dẫn thiết lập quảng cáo)

Tài liệu này hướng dẫn cách cấu trúc chiến dịch quảng cáo (Meta Ads / TikTok Ads) và nhắm mục tiêu (Targeting) tối ưu cho ngân sách nhỏ của các dự án startup/SaaS.

---

## 1. Cấu trúc Chiến dịch Kiểm thử (Testing Campaign Structure)

Khi bắt đầu chạy quảng cáo cho sản phẩm mới, mục tiêu là tìm ra **Thông điệp quảng cáo (Creative Angle)** hoạt động tốt nhất.

*   **Loại chiến dịch:** ABO (Adset Budget Optimization - Tự quản lý ngân sách nhóm) để đảm bảo các nhóm quảng cáo được chi tiêu đều tiền.
*   **Mô hình cấu trúc:** `1 Chiến dịch -> 3 Nhóm quảng cáo (3 tệp định vị) -> 3 Mẫu quảng cáo mỗi nhóm (A/B testing hình ảnh/video).`

```text
Campaign: [TEST] - Tên Sản Phẩm
├── Ad Set 1: Broad (Nhắm rộng, không chọn sở thích)
│   ├── Ad Creative A (Video Short dạng Painpoint)
│   └── Ad Creative B (Hình ảnh dạng Feature Showcase)
├── Ad Set 2: Interest (Sở thích chuyên ngành của ICP)
│   ├── Ad Creative A
│   └── Ad Creative B
└── Ad Set 3: Competitor Lookalike (Tệp tương tự khách đối thủ)
    ├── Ad Creative A
    └── Ad Creative B
```

---

## 2. Cấu trúc Chiến dịch Bám đuôi (Retargeting Campaign Structure)

Chiến dịch này dùng để thuyết phục những người đã từng tương tác nhưng chưa đăng ký mua hàng.

*   **Tệp đối tượng nhắm mục tiêu (Custom Audiences):**
    *   Người đã truy cập Landing Page trong vòng 30 ngày qua nhưng chưa tới trang Thank-you (chưa chuyển đổi).
    *   Người đã tương tác với trang Facebook/Instagram/Threads trong 30 ngày qua.
*   **Creative Angle:** Sử dụng mẫu quảng cáo **Objection Handling (Giải quyết nỗi sợ)** hoặc **Social Proof (Đánh giá khách hàng)** từ `ad_copy_frameworks.md`.

---

## 3. Chỉ số đo lường hiệu quả (Key Metrics to Track)

Để quyết định tắt hay giữ một mẫu quảng cáo, hãy theo dõi các chỉ số sau:
1.  **CTR Link (Click-through Rate - Tỷ lệ bấm vào link):** Đạt trên **1.5%** là tốt. Dưới 1% cần đổi Hook hoặc hình ảnh.
2.  **CPC (Cost per Click - Chi phí mỗi click):** Càng thấp càng tốt (phụ thuộc vào thị trường quốc gia chạy ads).
3.  **CPA (Cost per Acquisition - Chi phí một lượt chuyển đổi/đăng ký):** Chỉ số quan trọng nhất. Nếu CPA < Giá trị trọn đời của khách hàng (LTV) thì campaign có lãi.
