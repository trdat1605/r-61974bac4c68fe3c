# Đọc bằng chứng COMPLETE-001

Không cần nạp toàn bộ thư mục vào mỗi nhiệm vụ. Bắt đầu từ [checkpoint](checkpoint.json),
[app task](app-task.json), [completion](../../../docs/development/completion.md) và
[product record](product-record.json) rồi chỉ mở bằng chứng liên quan.

| Muốn kiểm điều gì? | Điểm vào |
| --- | --- |
| Build lỗi thật và bản sửa | metadata-regression.json/.txt; full-build.json/.txt; app source PR3 |
| Bài CI hiện hành | [app-ci-lifecycle-success.json](app-ci-lifecycle-success.json): head27e1669 khác checkout8d953fd, tree identical |
| Vì sao local chưa đạt | runtime-attempt-1.json, startup-fix-review.json, owned-cleanup-*.json, synthetic-backup.json; không có dump ở Git |
| Phối hợp Codex | [protocol](agent-eval/protocol.json), oracle/review, runs-v3/<id>/dispatch và originals; grading/<case>-review. Các bản V1/V2/shakedown giữ lịch sử, không tính vào V3 |
| Gửi/nhận và phạm vi agent | runs-v3/<id>/observer-tool-traces.json: tool calls theo roster đã chọn, không hidden reasoning/user messages/raw logs. Đây là coverage quan sát được, không sandbox hoặc chứng minh mọi hành vi |
| Docker sang D | docker-storage-*.json và [runbook chuẩn bị](../../../docs/runbooks/docker-storage-migration.md). Review đầu BLOCKED_FOR_EXECUTION; chưa chuyển/restart |
| Quyền và CI app | workflow-quarantine*.json, app-ci-enable*.json, app-required-checks-plan.json và receipt applied nếu có |
| Review và bàn giao cuối | app-docs-review.json; final app/control review và handoff chỉ có giá trị ở đúng SHA được ghi |

Các grading packets lặp bản gốc để che nhãn mẫu khi chấm; không phải bản chính mới.
Originals/hash/frozen packets không sửa sau thực nghiệm. T1 judgment đầu giữ nguyên,
bằng chứng gửi/nhận bổ sung được chấm bằng addendum riêng. Không suy kết quả từ tên
file hoặc từ số lượng tài liệu. Receipt chưa có/đang pending không được xem là PASS.

Chỉ chứa nội dung đã chọn lọc; không đưa env, khóa, dumps, dữ liệu khách hàng hoặc
raw session logs lên Git. Pattern scan hỗ trợ phát hiện một số bí mật, không chứng
minh tuyệt đối rằng mọi nội dung đều an toàn. Mốc nghiệm thu/merge vẫn do owner quyết.

Hai receipt độc lập `app-final-review.json` và
`agent-eval/grading/material-second-check.json` được tác giả lưu CRLF. `.gitattributes`
chỉ đặt `-text` cho đúng hai đường dẫn này để giữ nguyên bytes/hash qua Git;
các tệp khác vẫn theo LF. Không chuẩn hóa lại bản gốc sau khi đã được tham chiếu.
Căn cứ: [Git attributes, text unset](https://git-scm.com/docs/gitattributes#_text).

[Whitespace receipt](whitespace-preservation.json) ghi ngoại lệ đúng ba đường dẫn: CRLF của hai receipt và trailing spaces do tool build sinh. Không sửa bytes/hash gốc hoặc bỏ kiểm whitespace toàn repo.
