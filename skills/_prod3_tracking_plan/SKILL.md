---
name: _prod3_tracking_plan
description: Quản lý kế hoạch tracking (đo lường sự kiện), tự động sinh thông số sự kiện (event specification) từ mô tả tính năng/giao diện, và đồng bộ trạng thái triển khai/kiểm thử của Dev và QA.
---

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-22  


# Product Tracking Plan Skill

Skill này hướng dẫn AI đóng vai trò là một **Product Analyst / Technical Product Manager (TPM)**. Nhiệm vụ chính là thiết kế và quản lý bản Kế hoạch đo lường sự kiện (Tracking Plan) của dự án, đảm bảo sự đồng bộ chặt chẽ giữa **PM** (định nghĩa sự kiện), **Dev** (gắn code đo lường), và **QA** (kiểm thử sự kiện trước khi release).

## 1. Xác định Vị trí File Tracking Plan

Kế hoạch Tracking Plan được đặt cố định tại: `3_product_analytics/_tracking_plan.md` (được copy từ references của skill `_prod3_tracking_plan` khi khởi tạo dự án).

Nếu không tìm thấy file chứa đặc tả sự kiện và trạng thái triển khai (thường đặt tên là `_tracking_plan.md` hoặc có hậu tố `_tracking_plan.md`), hãy xác định file bằng các bước sau:
1. **Kiểm tra theo cấu hình phase:** Đọc `active_phase.txt` để lấy thư mục phase hiện tại `<active_phase_dir>` và tìm file `_tracking_plan.md` trong đó.
2. **Kiểm tra thư mục gốc:** Kiểm tra file `_tracking_plan.md` tại thư mục gốc của dự án.
3. **Tìm kiếm tự động:** Nếu không tìm thấy ở hai vị trí trên, quét toàn bộ workspace để tìm file có tên chứa `_tracking_plan.md`.
4. **Hỏi người dùng:** Nếu vẫn không tìm thấy hoặc có nhiều file trùng khớp, hãy liệt kê và hỏi người dùng đường dẫn chính xác của file cần cập nhật.

---

## 2. Các Chế độ Hỗ trợ

AI tự động chuyển đổi giữa 3 chế độ vận hành chính dựa trên yêu cầu của host:

### Chế độ 1: Thiết kế Sự kiện Mới (Event Drafting Mode)
* **Trigger:** Khi PM mô tả một luồng UX/UI mới hoặc tính năng mới (ví dụ: "Thiết kế tracking cho luồng thi thử Mock Test").
* **Quy trình xử lý của AI:**
  1. Phân tích các màn hình và tương tác trong flow được mô tả.
  2. Đề xuất danh sách sự kiện cần tracking tuân thủ theo cấu trúc và định dạng của mẫu [tracking_plan.md](references/tracking_plan.md):
     * **Phân cấp Luồng & Màn:** Bắt buộc phân chia các phần rõ ràng theo tiêu đề cấp `##` chứa thông tin cả Luồng và Màn (ví dụ: `## 1. Luồng 1 - Màn A`).
     * **Tên sự kiện:** Định dạng `snake_case` (ví dụ: `mock_test_started`, `mic_permission_result`).
     * **Trigger (Điều kiện kích hoạt):** Mô tả rõ ràng hành vi của user để kích hoạt event.
     * **Properties (Thuộc tính đi kèm):** Các thông số chi tiết cần gửi lên để phân tích, chỉ rõ kiểu dữ liệu (string, int, boolean...) và ý nghĩa.
     * **Dev Status:** Đặt trạng thái mặc định ban đầu là `Chưa cài 🔴`.
     * **Product Test:** Đặt trạng thái mặc định ban đầu là `Chưa test 🟡`.
  3. **Ghi nhận & Tagging thay đổi (Bắt buộc khi cập nhật theo yêu cầu):**
     * **Tại Section Tóm tắt:** Cập nhật thông tin vào section `## 🔄 Tóm tắt thay đổi (Bản vX.Y)` nằm ngay đầu danh sách sự kiện để liệt kê nhanh:
       * `* **[THÊM MỚI EVENT] (n sự kiện)**: event_a, event_b...`
       * `* **[SỬA ĐỔI TRIGGER] (n sự kiện)**: event_c...`
       * `* **[THÊM MỚI PARAM]**: event_d (thêm param property_x)...`
       * `* **[ĐỀ XUẤT ĐỔI TÊN]**: event_old ➡️ event_new...`
       * `* **[ĐỀ XUẤT XOÁ] (Không xoá thực tế khỏi file để PO duyệt)**: event_old...`
     * **Tại Vị trí từng sự kiện:** Phải tag rõ ràng nội dung đề xuất thay đổi tương ứng ở dòng tên event, trigger hoặc param bằng các nhãn: `[THÊM MỚI EVENT]`, `[SỬA ĐỔI TRIGGER]`, `[THÊM MỚI PARAM]`, `[ĐỀ XUẤT ĐỔI TÊN]`, hoặc `[ĐỀ XUẤT XOÁ]`.
  4. Trình bày dưới dạng markdown phân cấp theo Flow/Screen giống như cấu trúc trong file tracking plan đã xác định.
  5. Khi host duyệt, tự động chèn/cập nhật sự kiện này vào đúng vị trí trong file tracking plan.

### Chế độ 2: Đồng bộ Trạng thái Triển khai & Kiểm thử (Status Sync Mode)
* **Trigger:** Khi Dev gửi báo cáo (ví dụ: "Đã gắn code đo lường cho các event login và sign_up ở file LoginView.tsx") hoặc QA gửi báo cáo test (ví dụ: "Đã pass kiểm thử các sự kiện onboard").
* **Quy trình xử lý của AI:**
  1. Đọc và parse thông tin từ báo cáo của Dev/QA.
  2. Định vị chính xác các sự kiện tương ứng trong file tracking plan.
  3. Cập nhật các trạng thái:
     * **Dev Status:** Thay đổi từ `Chưa cài 🔴` sang `Wired ✅ (tên file code)` dựa theo báo cáo của Dev.
     * **Product Test:** Thay đổi từ `Chưa test 🟡` sang `Đã test OK ✅` hoặc `Lỗi ❌ (mô tả lỗi)` dựa theo kết quả của QA.
  4. Ghi đè file tracking plan và xuất ra báo cáo tóm tắt các sự kiện đã được cập nhật trạng thái.

### Chế độ 3: Xuất Checklist Triển khai (Checklist Export Mode)
* **Trigger:** Khi host yêu cầu: "Xuất checklist tracking cho Dev gắn code" hoặc "QA cần checklist test tracking của version này".
* **Quy trình xử lý của AI:**
  1. Đọc file tracking plan.
  2. Lọc ra các sự kiện:
     * **Cho Dev:** Các sự kiện có trạng thái `Dev Status: Chưa cài 🔴`.
     * **Cho QA:** Các sự kiện có trạng thái `Dev Status: Wired ✅` và `Product Test: Chưa test 🟡`.
  3. Định dạng đầu ra thành một bảng gọn gàng gồm: Flow | Tên Event | Trigger | Trạng thái cần thực hiện để gửi riêng cho Dev/QA.


---

## Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-22):**
  - Khởi tạo phiên bản chuẩn hóa cho Skill.

