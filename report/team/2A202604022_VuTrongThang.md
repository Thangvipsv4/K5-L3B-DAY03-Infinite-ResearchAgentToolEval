# Báo cáo cá nhân — VuTrongThang_2A202604022

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Vũ Trọng Thắng
- MSSV: 2A202604022
- Email: tvu6483@gmail.com

## 2. Phần việc phụ trách

- Xây dựng tool mới research_notes để lưu các ghi chú nghiên cứu vào file JSON cục bộ.
- Đăng ký tool vào hệ thống thông qua tools/__init__.py và khai báo schema trong artifacts/tools.yaml.
- Viết unit test để kiểm tra hoạt động của tool, bao gồm trường hợp thành công, đầu vào không hợp lệ và lỗi khi xử lý file JSON.

## 3. Đóng góp cụ thể

- Tạo starter_v0/tools/research_notes/tool.py với chức năng lưu ghi chú nghiên cứu gồm tiêu đề, nội dung và nguồn tham khảo.
- Tạo starter_v0/tools/research_notes/TOOL.md để mô tả chức năng, đầu vào, đầu ra và cơ chế xác nhận trước khi ghi file.
- Cập nhật starter_v0/tools/__init__.py để đăng ký hàm save_research_note vào TOOL_FUNCTIONS.
- Cập nhật starter_v0/artifacts/tools.yaml để khai báo tool và các tham số đầu vào.
- Bổ sung 3 unit test cho research_notes:

    + Happy path: kiểm tra ghi chú được lưu thành công.
    + Bad input: kiểm tra đầu vào không hợp lệ, chẳng hạn tiêu đề rỗng.
    + Failure path: kiểm tra lỗi dữ liệu JSON và bảo đảm tool trả về thông tin lỗi thay vì làm chương trình bị crash.

- Chạy kiểm thử toàn bộ dự án và xác nhận kết quả: 84 passed, 0 failed, 0 skipped.

## 4. Bằng chứng

- File/commit/PR:

    + starter_v0/tools/research_notes/tool.py
    + starter_v0/tools/research_notes/TOOL.md
    + starter_v0/tools/__init__.py
    + starter_v0/artifacts/tools.yaml
    + starter_v0/tests/test_tools_todo.py

- AI/công cụ đã dùng và cách tự kiểm tra kết quả:

    + Sử dụng ChatGPT để hỗ trợ giải thích yêu cầu, rà soát logic và hỗ trợ xây dựng unit test.
    + Sử dụng Visual Studio Code để chỉnh sửa và quản lý source code.
    + Sử dụng Python và pytest để chạy kiểm thử.
    + Tự kiểm tra bằng cách chạy pytest tests/test_tools_todo.py -v, sau đó chạy pytest tests/ -v để kiểm tra toàn bộ test suite.
    + Kết quả kiểm thử toàn bộ: 84 passed, không có test thất bại hoặc bị bỏ qua.

## 5. Tự đánh giá

Đã hoàn thành phần xây dựng một tool mới và tích hợp tool vào hệ thống theo cấu trúc của dự án. Tôi cũng viết unit test cho các trường hợp hoạt động bình thường, đầu vào không hợp lệ và lỗi khi xử lý dữ liệu.

Qua phần việc này, tôi hiểu rõ hơn quy trình xây dựng một tool cho agent: xác định chức năng, thiết kế input/output, đăng ký tool, thiết lập guardrail và kiểm thử các nhánh xử lý lỗi.
