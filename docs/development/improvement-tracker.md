# Bảy cải tiến: kết quả và việc còn mở

Ngày **23/11/2026**, task [FLOW-001](../../tasks/FLOW-001/task.json), [issue đầu mối #5](https://github.com/trdat1605/chatwoot-vn/issues/5). Nhánh `codex/product-foundation` còn review/Draft, chưa merge. Không đánh dấu hoàn tất toàn bộ từ việc tạo issue, docs hoặc test fixtures.

| Điểm / issue thật | Đã làm trong phạm vi foundation | Còn thiếu / điều kiện hoàn tất |
| --- | --- | --- |
| 1 — [Lựa chọn agent #6](https://github.com/trdat1605/chatwoot-vn/issues/6) | [Nguồn/giới hạn/rubric](agent-selection.md); giữ lựa chọn tạm coordinator+subagents | A/B công việc đại diện trên tool thật NOT_RUN; không gọi tối ưu hoặc không cần Teams |
| 2 — [Issue → task → PR #7](https://github.com/trdat1605/chatwoot-vn/issues/7) | Issue5–11, task có issue_url; templates và API PR checker; source/app record checker riêng | Job cần CI thực trên PR này; chưa có app feature PR. Templates chưa ở default main nên issue chooser/default PR template chưa được chứng minh active |
| 3 — [Source/reproduction #8](https://github.com/trdat1605/chatwoot-vn/issues/8) | Private app source baseline, Actions disabled trước push, review plan và SHA readback | Templates bootstrap/isolated fresh setup/build/runtime chưa làm; [chi tiết](source-reproduction.md) |
| 4 — [CI sản phẩm/pilot #9](https://github.com/trdat1605/chatwoot-vn/issues/9) | Tool kiểm app commit và acceptance/evidence, negative tests; [tiêu chí pilot](pilot.md) | Product CI và bugfix/feature runtime thật NOT_RUN. Tool fixtures không thay app tests |
| 5 — [Review/merge #10](https://github.com/trdat1605/chatwoot-vn/issues/10) | [Policy và phép kiểm cần có](review-and-merge.md), ghi đúng giới hạn | Rulesets API403 yêu cầuPro; chưa có server enforcement/reviewer người thứ hai. Không đổipublic/muagói/merge |
| 6 — [Trạng thái #11](https://github.com/trdat1605/chatwoot-vn/issues/11) | [status](../status.md) nối kết quả DOCS-002/CI đã chạy và FLOW-001; hồ sơ lịch sử giữ nguyên | Review cuối/CI của revision mới xem task/PR; owner acceptance chưa có. Tiếp tục cập nhật theo task thực |
| 7 — [Quy trình sản phẩm #5](https://github.com/trdat1605/chatwoot-vn/issues/5) | [G1–G10](product-workflow.md), owner/criteria/đường docs/code/tài nguyên; mẫu record và checker | Chưa có pilot app đi toàn tuyến, chưa merge/release/rollback sản phẩm. Không gọi viết quy trình là đã kiểm chứng quy trình |

## Owner và cách tiếp tục

Coordinator giữ liên kết issue/task/PR và tách công việc theo phụ thuộc. Implementer mỗi scope khác reviewer; chủ sản phẩm chốt phạm vi/acceptance/merge/release. Tên vai trò không chứng minh năng lực chuyên gia. Chưa assign issue cho một người khác hoặc gửi thông báo ngoài dự án; owner trách nhiệm kỹ thuật ở bảng/task, không giả có đội nhân sự đã nhận.

Thứ tự hiện tại: review foundation/tooling → hoàn thiện source/bootstrap không bí mật và môi trường tách → chọn bug có reproduce → app task/regression/review/PR → nghiệm thu các chặng được cấp quyền. Giới hạn GitHub private không ngăn khảo sát/branch/checks/Draft PR, nhưng phải xử lý trước khi hứa required checks server.

## Bằng chứng và trạng thái theo phiên bản

[Task](../../tasks/FLOW-001/task.json), evidence trong `tasks/FLOW-001/evidence/`, review/handoff khi có ghi subject kiểm khác commit chứa báo cáo. Không sửa bytes evidence cũ để làm xanh. Tool plan chỉ báo cấu trúc hợp lệ; verify records chỉ kiểm nhất quán và Git hiện tại, không xác nhận lời khai test hoặc reviewer identity. Local hook và CI không tự có quyền chặn server merge.
