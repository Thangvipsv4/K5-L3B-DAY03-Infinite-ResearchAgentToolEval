# Team

## Thông tin nhóm

- Tên nhóm: Infinite
- Lớp: L3B
- Repo nhóm: K5-L3B-DAY03-Infinite-ResearchAgentToolEval
- URL repo: https://github.com/Thangvipsv4/K5-L3B-DAY03-Infinite-ResearchAgentToolEval
- Nhánh nộp: `main`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Vũ Trọng Thắng | 2A202604022 | tvu6483@gmail.com | [Thangvipsv4](https://github.com/Thangvipsv4) | Xây dựng tool mới `research_notes`, tích hợp registry/schema và viết unit test. |
| 2 | Phạm Hà Nam | 2A202604023 | Chưa cung cấp | https://github.com/phamhanam | Xây dựng Streamlit UI, lưu transcript và ghi nhận live-chat evidence. |
| 3 | Trần Trọng Đạt | 2A202604030 | 26ai.dattt5@vinuni.edu.vn | https://github.com/dtr-uep | Thực hiện các vòng thử nghiệm v0–v3 và ghi giả thuyết, metric vào version log, viết eval group. |

## Báo cáo cá nhân và bằng chứng đóng góp

### Vũ Trọng Thắng — 2A202604022

- **Phụ trách:** Tool nghiên cứu mới và kiểm thử.
- **Đóng góp:** Tạo `research_notes`, đăng ký tool, khai báo schema và viết 3 unit test cho happy path, input không hợp lệ và lỗi file JSON.
- **Bằng chứng:** `starter_v0/tools/research_notes/`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`, `starter_v0/tests/test_tools_todo.py`; báo cáo [2A202604022_VuTrongThang.md](report/team/2A202604022_VuTrongThang.md).

### Phạm Hà Nam — 2A202604023

- **Phụ trách:** UI Streamlit và live-chat evidence.
- **Đóng góp:** Xây dựng `app.py`, lưu transcript, thêm dependency Streamlit và đối chiếu transcript trong B4 của báo cáo nhóm.
- **Bằng chứng:** Commit `62ba7c3`, `3cb29c8`; `starter_v0/app.py`, `starter_v0/transcripts/`; báo cáo [2A202604023_PhamHaNam.md](report/team/2A202604023_PhamHaNam.md).

### Trần Trọng Đạt — 2A202604030

- **Phụ trách:** Các vòng thử nghiệm prompt/tool declaration v0–v3. Viết eval test.
- **Đóng góp:** Ghi lại giả thuyết, artifact, hash và metric trước/sau cho các phiên bản trong version log; hỗ trợ phân tích kết quả và hoàn thiện báo cáo nhóm. Viết eval test.
- **Bằng chứng:** `starter_v0/artifacts/version_log.csv`, các run v0–v3 trong `starter_v0/runs/`. Báo cáo cá nhân [2A202604030_TranTrongDat.md](report/team/2A202604030_TranTrongDat.md).
