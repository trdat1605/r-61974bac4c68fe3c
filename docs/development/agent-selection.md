# Lựa chọn mô hình agent có bằng chứng

Ngày **23/11/2026**, [Lựa chọn agent / issue #6](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/6). Quyết định hiện tại: dùng coordinator + subagents theo nhiệm vụ; đây là lựa chọn đã thử ở phạm vi docs/tooling, **chưa chứng minh tối ưu cho Chatwoot**. Chưa triển khai hoặc A/B native Claude Agent Teams.

## Nguồn và điều không được suy rộng

| Nguồn đã đọc ngày 23/11 | Nội dung liên quan / giới hạn |
| --- | --- |
| [Towards a Science of Scaling Agent Systems, v3, 08/04/2026](https://arxiv.org/html/2512.08296v3) | Preprint, 260 cấu hình/sáu benchmark. Lợi ích phụ thuộc nhiệm vụ và phối hợp; SWE-bench/Terminal-Bench dùng tập con 20 bài. Không trực tiếp so tính năng Claude Teams với cấu hình Codex dự án |
| [Worse Together, v1, 30/09/2026](https://arxiv.org/abs/2610.00583) | Preprint, môi trường nhiều người dùng/mục tiêu riêng. Cho thấy rủi ro phối hợp tài nguyên; khác một chủ sản phẩm và một mục tiêu chung của lab |
| [Anthropic multi-agent Research, 13/06/2025](https://www.anthropic.com/research/multi-agent-research-system) | Bài kỹ thuật dùng lead + subagents; kết quả eval nghiên cứu thông tin không là bảo đảm chất lượng code |
| [Claude Agent Teams](https://code.claude.com/docs/en/agent-teams) và [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Hướng dẫn sản phẩm về cơ chế phối hợp, không phải so sánh thực nghiệm của dự án. Tính năng/permissions phải kiểm trên công cụ thật |
| [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices#multi-agent-architectures) | Hướng dẫn chọn kiến trúc theo evals; không chứng nhận mô hình nào của lab |

## Khi chọn và khi xem lại

Chia khảo sát độc lập, giữ một writer cho mỗi phạm vi, reviewer khác người viết. Nếu cần nhiều thành viên liên tục thương lượng hợp đồng, đầu mối trở thành chỗ nghẽn, quyết định bị thất lạc hoặc tích hợp thất bại lặp lại, thử cơ chế team phù hợp sau khi kiểm công cụ/quyền/tài nguyên. Có messaging không tự chứng minh phối hợp tốt.

Không thêm agent chỉ để đặt chức danh; không bỏ review/test cần thiết để giảm token. Khi chưa khảo sát nguồn hoặc chưa đo, ghi “đề xuất/chưa đủ bằng chứng” thay vì “tối ưu/không cần Teams”.

## COMPLETE-001 — kết quả Codex đã kiểm chứng

Người dùng xác nhận chưa có Claude Code và chấp nhận thử các cách phối hợp Codex hiện có. Native Claude Agent Teams **NOT_RUN**. [Protocol V3](../../tasks/COMPLETE-001/evidence/agent-eval/protocol.json), oracle và review được giữ nguyên; 12 lượt = 3 bài đọc source/đối chiếu API/thiết kế regression × 2 cách liên lạc × 2 lần lặp, mỗi lượt ba agent ngữ cảnh mới cùng ref/nguồn/công cụ/tiêu chí. Đây là phép thử riêng của dự án, không là quy mô chuẩn do Anthropic/OpenAI quy định.

Đã giữ 36 outputs gốc, packets, tool traces chọn lọc và bản đồ mẫu. Reviewer độc lập chấm source/trích dẫn/phụ thuộc/phạm vi; [review thứ hai](../../tasks/COMPLETE-001/evidence/agent-eval/grading/material-second-check.json) giữ các finding quan trọng. [Kết quả và đầy đủ 12 dòng](../../tasks/COMPLETE-001/evidence/agent-eval/results.json) liên kết hashes và judgments; không sửa outputs để làm xanh.

| Bài | Qua coordinator: lần 1 / 2 | Worker trao đổi trực tiếp: lần 1 / 2 |
| --- | --- | --- |
| T1 — labels/API | FAIL phạm vi đọc kết quả / PASS | PASS / PASS |
| T2 — canned response/cache | FAIL thiếu chi tiết bàn giao / PASS | PASS / FAIL thiếu nội dung/trích dẫn |
| T3 — thiết kế regression toggle status | PARTIAL_FAIL / PARTIAL_FAIL | PARTIAL_FAIL / PARTIAL_FAIL |

Theo tiêu chí đã đóng băng: **5/12 lượt đạt đầy đủ**, 7 lượt fail/partial; 87/100 tiêu chí dữ kiện PASS và 13 thiếu, 57/60 tiêu chí chung PASS và 3 FAIL. Các reviewers không xác định phát biểu sai thực chất hoặc defect bịa trong phạm vi đã đọc; điều này không xóa lỗi thiếu nội dung/trích dẫn. T1 có một lượt đọc chính tệp kết quả gốc ngoài allowlist, được giữ như lỗi phạm vi hẹp của protocol; dấu vết không cho thấy thao tác app/runtime/secret ở lượt đó. Không suy rằng mọi hành vi ngoài dấu vết đều được kiểm soát.

Ví dụ mất thông tin: coordinator bỏ một số chi tiết cache contract, account/display_id/authorization hoặc ảnh hưởng Enterprise khi tổng hợp. IDs và đường link có chứa dữ kiện chưa thay phần giải thích cần có trong bàn giao. Một citation sai đã được sửa trong trao đổi vẫn giữ trong ledger. Các reviewers dùng đơn vị đếm citations khác nhau nên không cộng tổng hoặc dùng chúng để xếp hạng hai cách.

**Quyết định tạm:** giữ coordinator + subagents và một writer cho mỗi phạm vi; cho phép trao đổi peer ở phụ thuộc được giao rõ. Hai cách đều có lỗi; 12 lượt hẹp không xác lập ưu thế thống kê, mô hình tối ưu hoặc kết luận có/không cần native Teams. Pilot app PR3 là phép viết/build/test/review riêng, không phải A/B implementation.

Brief coordinator/reviewer hiện có đã bổ sung đối chiếu từng acceptance với kết luận/nguồn/bằng chứng, kiểm chi tiết còn thiếu và quyền đọc/ghi/hash/gửi artifact. [CLI đã nạp brief mới](../../tasks/COMPLETE-001/evidence/brief-loading.json); **chưa đo hành vi cải thiện** sau thay đổi. Áp dụng cho việc tiếp theo, giữ nguyên tiêu chí và kết quả V3. Khi công việc sản phẩm tiếp theo bắt đầu, kiểm coverage bằng acceptance thực và verifier khác; không mở thêm agent chỉ vì có nhãn vai trò.

V2 shakedown bị loại nguyên lượt vì harness lưu bản gốc; giữ lịch sử, không dùng trong so sánh V3. Các can thiệp procedural và start/transport đều có trong dispatch. Timestamps là quan sát dispatch/capture, không kiểm soát để so tốc độ; token/model identity/hidden context **NOT_EXPOSED**. Đây là kiểm đọc source và bàn giao, chưa là bằng chứng hệ thống AI thay được toàn bộ năng lực đội phần mềm.

## Thiết kế mở rộng chưa thực hiện

Dùng một bộ công việc có acceptance và ref cố định: khảo sát API, sửa bug với regression, thay đổi có backend/frontend phụ thuộc. So coordinator+subagents với cơ chế team thực có; giữ đầu vào và kiểm kết quả cuối tương đương, lặp đủ để tránh kết luận từ một lượt may mắn. Không tự đặt số lần chạy hoặc mục tiêu tiết kiệm khi chưa chốt thiết kế đo.

Đo hành vi đúng/lỗi còn sót, findings sai, xung đột/ghi ngoài scope, quyết định bị mất, tiếp quản, thời gian và sự can thiệp cần thiết. Ghi actual tool/model/context/ref và giới hạn; số agent/token không là điểm chất lượng. Những lỗi workflow/claim/env đã có trong tests là nguồn ca đánh giá tooling; chúng chưa là benchmark feature Chatwoot.

Owner: coordinator chuẩn bị ca, reviewer kiểm dữ kiện và cách chấm; chủ sản phẩm quyết định phạm vi/chấp nhận. Kết quả chẩn đoán đã có; issue chưa tự đóng vì owner còn quyết định chấp nhận và tích hợp.
