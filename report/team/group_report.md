# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Infinite
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenAI

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent hỗ trợ tìm kiếm thông tin trên web và mạng xã hội, đọc URL, tra cứu bài báo khoa học và chính sách nội bộ, trình bày kết quả thành digest, và lưu ghi chú nghiên cứu vào file local khi người dùng xác nhận. Agent có thể hỏi lại khi thiếu thông tin; các lượt chạy live cũng cho thấy giới hạn khi nguồn chặn truy cập hoặc thiếu cấu hình dịch vụ gửi.

**Cách chạy UI:**

Từ thư mục `starter_v0/`, cài dependency bằng `pip install -r requirements.txt`, cấu hình provider trong `.env` theo [hướng dẫn setup](../../docs/TOOL-SETUP.md), rồi chạy `streamlit run app.py`. UI dùng Streamlit; dependency được khai báo trong [requirements.txt](../../starter_v0/requirements.txt).

**Link dùng thử (deploy):** https://quad-seed-prefers-lower.trycloudflare.com  
Đây là link tunnel dùng trong phiên live chat; tunnel tạm thời có thể không còn hoạt động sau phiên thử.


### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi người dùng để bổ sung thông tin hoặc xác nhận hành động. | không |
| `timeline` | Lấy bài đăng gần đây theo tài khoản. | không |
| `social_search` | Tìm bài đăng trên mạng xã hội theo từ khóa. | không |
| `lookup` | Tìm thông tin trên web, gồm tìm kiếm tin tức theo khoảng thời gian. | không |
| `fetch` | Đọc nội dung từ URL do người dùng cung cấp. | không |
| `format` | Trình bày các kết quả đã có theo mẫu digest. | không |
| `send` | Gửi nội dung qua Telegram; cần xác nhận trước khi gửi. | không |
| `policy` | Tìm trong tài liệu chính sách nội bộ. | không |
| `papers` | Tìm bài báo khoa học trên arXiv. | không |
| `paper_text` | Lấy nội dung văn bản của bài báo arXiv. | không |
| `research_notes` | Lưu ghi chú nghiên cứu vào JSON local sau khi xác nhận. | có |

### A3. Câu hỏi mẫu để thử

3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent:

1. `Tìm các nghiên cứu gần đây về tác động của AI đến thói quen làm việc và tư duy.`
2. `Phân tích trang này giúp tôi.` (Agent cần hỏi URL trước khi đọc.)
3. `Lấy 4 bài đăng mới nhất của tài khoản @NASA trên Twitter.`
4. `Lưu ghi chú nghiên cứu có tiêu đề "Tool evaluation" với nội dung "Eval kiểm tra lựa chọn tool và arguments."`
5. `Đăng bản tin sau lên Telegram: [nội dung].` (Kiểm tra hỏi xác nhận trước khi gửi; cần cấu hình Telegram.)

## 3. Giải pháp

v1 loại bỏ chỉ dẫn cho phép tự đoán account/URL; v2 yêu cầu dùng `clarify` khi thiếu thông tin và không tạo giá trị thay thế. Ở v3, nhóm thử làm rõ cách chọn `response_type=text` và `yes_no` trong description của `clarify`; kết quả giảm từ 95% xuống 85% case accuracy nên không xem thay đổi này là cải thiện tổng thể.

- Tool mới là [`research_notes`](../../starter_v0/tools/research_notes/TOOL.md): chỉ dùng khi người dùng yêu cầu lưu ghi chú nghiên cứu; yêu cầu `confirmed=true`, kiểm tra title/content và trả error dict nếu input hoặc thao tác file lỗi.
- Các thay đổi và giới hạn của prompt/tool declaration được phân tích thêm tại mục B1 và B6. Bằng chứng đo được là các run có liên kết ở B1; không suy luận rằng một thay đổi đơn lẻ chắc chắn gây ra mọi biến động điểm.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hiệu năng ban đầu làm mốc so sánh | N/A | case_accuracy: 70%; tool_routing: 75%; argument: 70%; multiturn: 100% | [v0 run](../../starter_v0/runs/v0_B_base_openai_20261110T191208297808.json) |
| v1 | system_prompt.md | Loại bỏ chỉ dẫn đoán account và URL sẽ giảm gọi tool sai khi thiếu thông tin | case_accuracy: 70%; tool_routing: 75%; argument: 70%; multiturn: 100% | case_accuracy: 80%; tool_routing: 85%; argument: 80%; multiturn: 100% | [v1 run](../../starter_v0/runs/v1_B_base_openai_20261110T192032611274.json) |
| v2 | system_prompt.md | Chỉ định phải gọi clarify và cấm tạo giá trị thay thế để giúp model hỏi lại đúng khi thiếu thông tin hoặc URL | case_accuracy: 80%; tool_routing: 85%; argument: 80%; multiturn: 100% | case_accuracy: 95%; tool_routing: 100%; argument: 95%; multiturn: 100% | [v2 run](../../starter_v0/runs/v2_B_base_openai_20261110T200841226626.json) |
| v3 | tools.yaml - description của clarify | Làm rõ cách dùng text và yes_no sẽ giúp model chọn đúng kiểu xác nhận trước khi gửi hoặc đăng | case_accuracy: 95%; tool_routing: 100%; argument: 95%; multiturn: 100% | case_accuracy: 85%; tool_routing: 95%; argument: 85%; multiturn: 100% | [v3 run](../../starter_v0/runs/v3_B_base_openai_20261110T202011032782.json) |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope (v0) | out_of_scope | `send` | Expected no tool call nhưng model dùng send để trả lời bài toán. Đây là gọi tool sai, không chứng minh đã gửi thành công. | Đề xuất: trả lời/định hướng ngoài phạm vi bằng text; không dùng send để trả lời thông thường. Case PASS ở v1–v3, nhưng chưa đủ bằng chứng quy cải thiện cho một rule riêng. |
| R10_missing_handle (v0) | missing_info | `timeline` | Tự chọn tài khoản khi user chưa cung cấp; thiếu clarify và gọi thừa timeline. | V1 bỏ chỉ dẫn đoán nhưng case vẫn FAIL. V2 yêu cầu gọi clarify và cấm placeholder; case PASS ở v2 và v3. |
| R11_missing_url (v0) | missing_info | `fetch` | Tự tạo URL thay vì gọi clarify để xin link. | V2 bổ sung rule clarify và cấm URL giả; case PASS ở v2 nhưng tái lỗi ở v3. Cần kiểm chứng lại tính ổn định. |
| R12_confirm_before_send (v0) | wrong_boundary | `send` | Gọi send khi chưa xác nhận; expected clarify với response_type=yes_no. | V2 chuyển sang clarify nhưng sai response_type. V3 sửa description vẫn chưa PASS. Đề xuất bỏ chỉ dẫn gửi ngay trong system prompt. |
| R13_parallel_web_and_tweets (v0) | wrong_tool | `lookup`; `social_search` | Đã chọn đủ hai tool nhưng lookup sai query so với expected AI và thiếu topic=news; mismatch thực tế là arguments. | Đề xuất làm rõ convention query và topic của lookup. Case PASS ở v2 nhưng FAIL lại ở v3; chưa có thay đổi riêng cho lookup được kiểm chứng. |
| R14_out_of_scope_coding (v0) | out_of_scope | `send` | Expected no tool call nhưng model gọi send để trả lời yêu cầu coding. | Đề xuất giới hạn send cho yêu cầu gửi đã xác nhận. Case PASS ở v1–v3; không kết luận nguyên nhân chỉ từ thay đổi điểm. |
| R10_missing_handle (v1) | missing_info | `timeline` | Dùng placeholder thay vì hỏi account qua clarify. | Đã bổ sung rule gọi clarify và cấm placeholder ở v2; case PASS ở v2 và v3. |
| R11_missing_url (v1) | missing_info | `fetch` | Vẫn tự tạo URL; thiếu clarify và gọi thừa fetch. | Đã sửa rule ở v2; PASS ở v2 nhưng tái lỗi v3. Đề xuất kiểm tra lại trên nhiều run trước khi kết luận ổn định. |
| R12_confirm_before_send (v1) | wrong_boundary | `send` | Chưa hỏi xác nhận qua clarify trước khi gọi send. | V3 làm rõ description của clarify nhưng case vẫn FAIL. Đề xuất xử lý chỉ dẫn gửi ngay còn mâu thuẫn trong prompt. |
| R13_parallel_web_and_tweets (v1) | wrong_tool | `lookup`; `social_search` | Lookup thiếu topic=news dù user yêu cầu tin tức; routing đúng nhưng arguments sai. | Đề xuất mô tả rõ topic=news cho tin tức trong tools.yaml; chưa kiểm chứng riêng. |
| R12_confirm_before_send (v2) | wrong_boundary | `clarify` | Model hỏi nội dung bản tin; evaluator yêu cầu response_type=yes_no. Chưa có hành động gửi. | V3 phân biệt text/yes_no trong description của clarify, nhưng lỗi vẫn còn. Cần review thủ công vì nội dung gửi chưa được cung cấp nên hỏi bổ sung cũng có cơ sở. |
| R11_missing_url (v3) | missing_info | `fetch` | Tái xuất hiện việc tạo URL giả thay vì clarify. | Đề xuất giữ rule cấm URL giả và kiểm tra lại sự tương tác với description mới; chưa kiểm chứng nguyên nhân tái lỗi. |
| R12_confirm_before_send (v3) | wrong_boundary | `clarify` | Vẫn hỏi nội dung thay vì xác nhận yes/no theo expected; thay đổi description chưa giải quyết lỗi chấm này. | Đề xuất bỏ chỉ dẫn gửi ngay và review tiêu chí hỏi nội dung/xác nhận khi user chưa cung cấp bản tin; chưa chạy vòng kiểm chứng mới. |
| R13_parallel_web_and_tweets (v3) | wrong_tool | `lookup`; `social_search` | Lookup tiếp tục thiếu topic=news; không phải thiếu tool. | Đề xuất sửa riêng description/parameter topic của lookup ở vòng tiếp theo và đo lại; chưa kiểm chứng. |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_handle_without_at | Single turn: Bỏ ký tự @ khỏi handle và trích đúng số lượng 4. | `timeline` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G02_latest_social_results | Single turn: Chọn tìm theo từ khóa với Latest và limit=3 thay vì Top hoặc timeline. | `social_search` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G03_cancel_send | Single turn: Không gọi send hoặc tool khác khi người dùng hủy hành động. | Không gọi tool | [v2: FAIL](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: FAIL](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) - cả hai gọi send dù user hủy; tool trả needs_confirmation, chưa gửi. |
| G04_no_tool_explanation | Single turn: Trả lời câu hỏi về cách sử dụng agent mà không thực hiện tìm kiếm. | Không gọi tool | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G05_save_research_note | Single turn: Chọn research_notes và truyền đúng nội dung cùng confirmed=true khi người dùng xác nhận rõ việc lưu ghi chú. | `research_notes` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) - tool trả status=saved ở cả hai run. |
| G06_switch_to_account | Multi turn: Chuyển từ tìm từ khóa sang timeline và giữ tài khoản từ lượt trước. | `timeline` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G07_change_social_order | Multi turn: Ghi đè Top thành Latest và limit từ 6 thành 2 trong khi giữ query. | `social_search` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G08_still_missing_account | Multi turn: Bổ sung số lượng chưa giải quyết việc thiếu account; vẫn phải gọi clarify. | `clarify` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G09_replace_url | Multi turn: Dùng URL đã sửa và không gọi thêm fetch cho URL cũ hoặc lookup; chỉ chấm routing và args. | `fetch` | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |
| G10_draft_without_permission | Multi turn: Không coi việc cung cấp bản nháp là đồng ý gửi; tôn trọng việc chưa xác nhận. | Không gọi tool | [v2: PASS](../../starter_v0/runs/v2_B_group_openai_20261110T215856877837.json); [v3: PASS](../../starter_v0/runs/v3_B_group_openai_20261110T215102418828.json) |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| [v1 T1](../../starter_v0/transcripts/v1_openai_20261110T195916417164.transcript.json) | “Can you scrape some recent research for me” | Không gọi tool | v1; OpenAI `gpt-4o-mini`; artifact `v1+p6139f40723ba+te69bc53ed884` | Hỏi thêm topic/keywords trước khi tìm kiếm. |
| [v3 T1](../../starter_v0/transcripts/v3_openrouter_20261110T222436366854.transcript.json) | Tác động của AI đến thói quen làm việc và tư duy đến năm 2026 | `lookup` (topic=general, timeframe=week, max_results=5) | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Lookup trả 5 kết quả; assistant tổng hợp và dẫn nguồn trong câu trả lời. |
| [v3 T1](../../starter_v0/transcripts/v3_openrouter_20261110T222905881214.transcript.json) | Nhờ phân tích tương tác và khán giả của “trang này” | Không gọi tool | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Hỏi URL vì yêu cầu chưa nêu trang cần phân tích. |
| [v3 T2](../../starter_v0/transcripts/v3_openrouter_20261110T222905881214.transcript.json) | Cung cấp URL trang Facebook | `fetch(url=…)` | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Fetch lỗi HTTP 403; assistant báo không truy cập được và xin thêm thông tin. |
| [v3 T3](../../starter_v0/transcripts/v3_openrouter_20261110T222905881214.transcript.json) | Cung cấp “11K người theo dõi • 3 đang theo dõi” | `timeline(screenname=…, limit=5)`; `social_search(query=…, limit=5)` | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Timeline lỗi JSON; social search trả danh sách rỗng. Assistant nêu không lấy được bài đăng và đưa hướng phân tích chung dựa trên số liệu user cung cấp. |
| [v3 T1](../../starter_v0/transcripts/v3_openrouter_20261110T223332316291.transcript.json) | Yêu cầu đăng “bản tin này” lên Telegram, chưa có nội dung | Không gọi tool | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Hỏi user cung cấp nội dung bản tin. |
| [v3 T2](../../starter_v0/transcripts/v3_openrouter_20261110T223332316291.transcript.json) | Cung cấp nội dung “I love you. I love you 3000.” | `clarify(response_type=yes_no)` | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Hỏi xác nhận đăng và chuyển trạng thái chờ user. |
| [v3 T3](../../starter_v0/transcripts/v3_openrouter_20261110T223332316291.transcript.json) | Xác nhận “Có.” | `send(text=…, confirmed=true)` | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Gửi không thành công: thiếu `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`; assistant báo lỗi cấu hình. |
| [v3 T4](../../starter_v0/transcripts/v3_openrouter_20261110T223332316291.transcript.json) | Cung cấp `@my_newsletter` | `send(text=…)` | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Tool trả `needs_confirmation`; assistant hỏi xác nhận rõ ràng trước khi gửi. |
| [v3 T5](../../starter_v0/transcripts/v3_openrouter_20261110T223332316291.transcript.json) | Xác nhận “Có.” lần nữa | `send(text=…)` | v3; OpenRouter `openai/gpt-4o-mini`; artifact `v3+p1e2a00d00d33+tf75dc423d71d` | Vẫn `needs_confirmation` vì lần gọi này không truyền `confirmed`; assistant lặp lại câu hỏi, chưa gửi. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | starter_v0/tools/research_notes/tool.py, TOOL.md  | Tạo tool lưu ghi chú nghiên cứu vào file JSON cục bộ.  | Chỉ ghi file khi confirmed=True; kiểm tra title/content không rỗng. |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) starter_v0/tests/test_tools_todo.py | 3 test: happy path, bad input, failure path. Toàn bộ project đạt 84 passed. | Kiểm tra input không hợp lệ và lỗi JSON, đảm bảo tool trả về error dict thay vì crash. |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
