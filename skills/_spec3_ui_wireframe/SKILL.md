---
name: _spec3_ui_wireframe
description: Đặc tả giao diện màn hình (Screen Specs), trạng thái UI Component, bố cục Responsive và Visual Wireframe Prompts cho UI/UX Handoff và AI UI Agents.
---

# UI Wireframe & Component Specification (`_spec3_ui_wireframe`)

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-24  

---

## 1. Mục đích & Phạm vi

Skill này chịu trách nhiệm đặc tả chi tiết giao diện người dùng (UI), kiến trúc thành phần (Component Hierarchy), trạng thái thể hiện (Component States), hành vi thích ứng (Responsive Layouts) và sinh các mô tả trực quan (Visual Wireframe Prompts).

### Đầu ra chính (Outputs):
1. **Screen Layout & Section Specification:** Đặc tả vùng giao diện (Header, Sidebar, Main Content, Modal, Drawer, Footer).
2. **Component Specs & Design System Tokens:** Thuộc tính props, kích thước, khoảng cách, màu sắc, font style và icon của từng UI Component.
3. **Component States Matrix:** Trạng thái trực quan chi tiết (Default, Hover, Active, Disabled, Loading Spinner, Error Border, Empty View).
4. **Responsive Layout Guidelines:** Quy tắc hiển thị trên Mobile (375px), Tablet (768px), và Desktop (1440px+).
5. **Visual Wireframe Prompts (Dành cho AI UI Generation & Demo):** Đoạn prompt mô tả tự nhiên tiếng Anh để sinh mockups qua ChatGPT/DALL-E hoặc đưa trực tiếp cho AI UI Agent dựng layout HTML/CSS/React.

---

## 2. Quy trình Thực hiện Đặc tả UI (4 Bước)

### Bước 1 — Phân rã Màn hình thành Cây Thành phần (Component Hierarchy)
- Liệt kê cấu trúc cây component:
  ```
  Screen: [Dashboard]
  └── Header (Component)
  └── MainLayout (Layout)
      ├── MetricsGrid (Container)
      │   └── MetricCard (Component x 4)
      └── DataChart (Component)
  ```

### Bước 2 — Đặc tả Chi tiết từng UI Component & Props
Xác định cho từng Component:
- **Component Name:** Ví dụ `ButtonPrimary`, `InputField`, `DataTable`.
- **Props/Inputs:** `label`, `variant`, `disabled`, `loading`, `onClick`.
- **Micro-interactions:** Hover transition (0.2s ease-in-out), Click feedback ripple.

### Bước 3 — Định nghĩa Ma trận Trạng thái (Component States)
- **Empty State:** Hiển thị gì khi chưa có dữ liệu? (Illustration, Friendly Copy, CTA button "Tạo mới").
- **Loading State:** Skeleton loader hay Spinner overlay?
- **Error State:** Inline error message bên dưới input field với viền đỏ (#E53E3E).

### Bước 4 — Sinh Visual Wireframe Prompts
Mô tả giao diện bằng tiếng Anh tự nhiên để phục vụ Handoff visual & Demo:
```text
A clean modern SaaS Dashboard wireframe layout, dark mode UI theme with deep slate background (#0F172A). Top header features a search bar, notification bell, and user avatar on the right. Main content area displays 4 metric summary cards at the top (Total Users, Revenue, Conversion Rate, Active Sessions) with glowing gradient borders, followed by a wide line chart and a data table below. Sleek typography, minimalist iconography, high contrast UI.
```

---

## 3. Template Mẫu Output Spec UI Wireframe

```markdown
# UI Specification: [Tên Màn Hình / Feature]

> **Target Audience:** Frontend Dev, UI/UX Designer, AI UI Execution Agent  

## 1. Component Hierarchy & Layout

- **Màn hình:** `UserProfilePage` (`/settings/profile`)
- **Bố cục chính:** 2 cột (Left Sidebar 280px + Right Content Flex 1)

### Visual Layout Diagram (ASCII / Text Grid)
```text
+-----------------------------------------------------------------------+
| Header: Logo | Search Input                     | Notifications | Avatar|
+---------------------+-------------------------------------------------+
| Sidebar Navigation  | Main Content Area                               |
| - Profile Settings  | H1: Profile Settings                            |
| - Security         | [ Avatar Upload Circle ]                        |
| - Billing           | Form Field: Full Name [                    ]    |
| - Notifications     | Form Field: Email     [                    ]    |
|                     | [ Save Changes Button ]                         |
+---------------------+-------------------------------------------------+
```

## 2. Component Specifications & States

### Component: `AvatarUpload`
- **Props:** `currentUrl: string`, `onUploadSuccess: (url) => void`, `maxSizeMb: 5`
- **States:**
  - `DEFAULT`: Hiển thị ảnh hiện tại hoặc Avatar chữ cái đầu. Hover có icon Camera mờ.
  - `UPLOADING`: Nền tối 50%, hiển thị Progress Bar hình tròn (Circular Loader).
  - `ERROR`: Viền đỏ `#E53E3E`, bên dưới xuất hiện text `"Dung lượng file vượt quá 5MB"`.

## 3. Responsive Breakpoint Rules

| Component | Mobile (< 768px) | Desktop (>= 1024px) |
| :--- | :--- | :--- |
| `Sidebar Navigation` | Animate thành Bottom Navigation Bar hoặc Drawer Slide-out | Cố định bên trái (Width 280px) |
| `Form Action Buttons` | Sticky ở đáy màn hình (Full Width 100%) | Nằm góc phải Form (Auto Width) |

## 4. Visual Wireframe Prompt (AI Image / UI Agent)

> *Clean UI mockup of a User Profile Settings page for a modern Web Application, desktop view (16:9 aspect ratio). Left column displays navigation links, right column shows user form with avatar image picker, text inputs, and primary action buttons. Professional slate blue color scheme, sleek typography, clean lines.*
```

---

## 4. Lịch sử Cập nhật (Changelog)

- **v1.0.0 (2026-07-24):** Cập nhật tên skill thành `_spec3_ui_wireframe` chuẩn hóa đặc tả Screen Specs, Component States, Responsive Rules và Visual Wireframe Prompts cho AI UI Execution Agents.
