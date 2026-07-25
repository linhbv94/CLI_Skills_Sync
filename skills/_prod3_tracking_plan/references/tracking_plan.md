# Speakly — Tracking Plan & Event Specification (07/08/2026)

*Google Doc ID: `XXX`*
*Tab ID: `XXX`*

Tài liệu này định nghĩa danh sách các sự kiện (events) cần đo lường (tracking) trên toàn bộ sản phẩm Speakly, phục vụ cho việc tích hợp hệ thống analytics (GA4 và Mixpanel) và đồng bộ trạng thái giữa **Product Manager (PO)**, **Developer (Dev)**, và **QA/Tester (Product Test)**.

---

## 📌 Thuộc tính người dùng chung (User Properties)
*Các thuộc tính này cần được thiết lập một lần khi người dùng đăng nhập hoặc có thay đổi trạng thái, và sẽ tự động đính kèm vào mọi sự kiện sau đó.*

| Thuộc tính (User Property) | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `user_id` | string | ID người dùng, khớp với khóa chính/UUID trong cơ sở dữ liệu để liên kết dữ liệu hành vi với hệ thống backend (không dùng trực tiếp email/SĐT). |

---

# 📋 Chi tiết Sự kiện theo Luồng (Event List by Flow)

## 🔄 Tóm tắt thay đổi (Bản v0.2)
* **[THÊM MỚI EVENT] (n sự kiện)**: `event_name_1`, `event_name_2`, ..., `event_name_n`.
* **[SỬA ĐỔI TRIGGER] (n sự kiện)**: `event_name_n`, `event_name_n`.
* **[THÊM MỚI PARAM]**:
  * `event_name_n` (thêm param `property_name`, `property_name`).
* **[ĐỀ XUẤT ĐỔI TÊN]**:
  * Event `event_name_old` ➡️ `event_name_new`.
  * Param `property_name_old` ➡️ `property_name_new`.
* **[ĐỀ XUẤT XOÁ] (Không xoá thực tế khỏi file để PO duyệt)**:
  * Event `event_name_old` (thay thế bởi `event_name_new` hoặc lí do xoá cụ thể).
  * Param `property_name_old` (trong event `event_name_new` hoặc lí do xoá cụ thể).

---

## 1. Luồng 1 - Màn A

### `event_name`
* **Trigger**: Trigger khi nào?
* **Properties**:
  * `property_name` (type) — Mô tả thuộc tính (`value1`, `value2`, ...).
* **Dev Status**: Wired ✅ / Chưa cài 🔴
* **Product Test**: Chưa test 🟡

---

## 2. Luồng 1 - Màn B

### `event_name`
* **Trigger**: Trigger khi nào?
* **Properties**:
  * `property_name` (type) — Mô tả thuộc tính (`value1`, `value2`, ...).
* **Dev Status**: Wired ✅ / Chưa cài 🔴
* **Product Test**: Chưa test 🟡

---

## 2. Luồng 2 - Màn B

### `event_name`
* **Trigger**: Trigger khi nào?
* **Properties**:
  * `property_name` (type) — Mô tả thuộc tính (`value1`, `value2`, ...).
* **Dev Status**: Wired ✅ / Chưa cài 🔴
* **Product Test**: Chưa test 🟡