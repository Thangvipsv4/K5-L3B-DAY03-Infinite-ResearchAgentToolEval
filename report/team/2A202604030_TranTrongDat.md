# Báo cáo cá nhân — TranTrongDat-2A202604030

## 1. Thông tin thành viên

- Họ tên: Trần Trọng Đạt
- MSSV: 2A202604030
- Email: 26ai.dattt5@vinuni.edu.vn

## 2. Phần việc phụ trách

Chạy và phân tích eval OpenAI v0–v3, điều chỉnh system prompt và description của clarify, xây dựng eval nhóm và tổng hợp phần kết quả trong báo cáo.

## 3. Đóng góp cụ thể

- Loại bỏ chỉ dẫn đoán account/URL, bổ sung yêu cầu gọi clarify khi thiếu thông tin, thử làm rõ kiểu hỏi text/yes_no trong tool description.
- Chạy base eval và ghi version log: case accuracy lần lượt là 70%, 80%, 95% và 85%, ghi nhận việc v3 giảm điểm.
- Hoàn thiện 10 case eval nhóm, gồm case cho research_notes; tổng hợp kết quả group v2/v3 đạt 9/10 và phân tích lỗi trong báo cáo nhóm.

## 4. Bằng chứng

- File/commit/PR: starter_v0/artifacts/system_prompt.md, tools.yaml, version_log.csv, starter_v0/data/eval_group.json, các run OpenAI v0-v3 và group v2/v3 trong starter_v0/runs/.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng ChatGPT/Codex hỗ trợ đề xuất prompt, eval case và phân tích kết quả, đối chiếu summary, actual_tool_calls và failures trong run JSON trước khi ghi báo cáo.

## 5. Tự đánh giá

Có thể nhận ra các chỉ dẫn mơ hồ và việc bỏ qua quy trình trong system prompt ban đầu, từ đó điều chỉnh và kiểm chứng qua eval. Tuy nhiên, vẫn còn chậm trong việc đánh giá tool schema/description từ kết quả kiểm định và xác định nguyên nhân lỗi.
