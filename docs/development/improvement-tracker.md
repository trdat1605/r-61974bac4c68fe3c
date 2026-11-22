# Bảy cải tiến: kết quả và việc còn mở

Cập nhật **23/11/2026** qua PUB-001 và GOV-001; bản mới đang trên `codex/branch-protection`, chưa merge. Nền ban đầu: task [FLOW-001](../../tasks/FLOW-001/task.json), [issue đầu mối #5](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/5). FLOW-001 đã review PASS tại `48f8a14`, bàn giao `f8e5822`, CI đạt; PUB-001 review PASS tại `802091d`, bàn giao `3feef9b`, [CI đạt](https://github.com/trdat1605/r-61974bac4c68fe3c/actions/runs/45071862054). PR stack còn Draft, chưa merge. Không đánh dấu hoàn tất toàn bộ từ việc tạo issue, docs hoặc test fixtures.

| Điểm / issue thật | Đã làm trong phạm vi foundation | Còn thiếu / điều kiện hoàn tất |
| --- | --- | --- |
| 1 — [Lựa chọn agent #6](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/6) | [Nguồn/giới hạn/rubric](agent-selection.md); giữ lựa chọn tạm coordinator+subagents | A/B công việc đại diện trên tool thật NOT_RUN; không gọi tối ưu hoặc không cần Teams |
| 2 — [Issue → task → PR #7](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/7) | Issue5–11, task có issue_url; templates và API PR checker; source/app record checker riêng | Hai job control đã chạy đạt ở PR12 và PR14; chưa có app feature PR. Templates chưa ở default main nên issue chooser/default PR template chưa được chứng minh active |
| 3 — [Source/reproduction #8](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/8) | App source baseline nay công khai theo PUB-001, Actions disabled trước push và vẫn tắt, review plan và SHA readback | Templates bootstrap/isolated fresh setup/build/runtime chưa làm; [chi tiết](source-reproduction.md) |
| 4 — [CI sản phẩm/pilot #9](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/9) | Tool kiểm app commit và acceptance/evidence, negative tests; [tiêu chí pilot](pilot.md) | Product CI và bugfix/feature runtime thật NOT_RUN. Tool fixtures không thay app tests |
| 5 — [Review/merge #10](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/10) | [Policy và phép kiểm cần có](review-and-merge.md), ghi đúng giới hạn | PUB-001 gỡ giới hạn private: rulesets GET200. GOV-001 đã bật main rules và thử direct/force/delete denial, CI fail→blocked rồi pass→clean trên probe; kết quả thực xem [bảo vệ nhánh](branch-protection.md). Chỉ có owner; chưa có reviewer người thứ hai hoặc product CI. Không coi JSON review của agent là GitHub approval |
| 6 — [Trạng thái #11](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/11) | [status](../status.md) nối kết quả DOCS-002/CI đã chạy và FLOW-001; hồ sơ lịch sử giữ nguyên | FLOW/PUB có review và CI theo exact revision; cập nhật GOV theo task/PR. Owner acceptance/merge chưa có. Tiếp tục cập nhật theo task thực |
| 7 — [Quy trình sản phẩm #5](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/5) | [G1–G10](product-workflow.md), owner/criteria/đường docs/code/tài nguyên; mẫu record và checker | Chưa có pilot app đi toàn tuyến, chưa merge/release/rollback sản phẩm. Không gọi viết quy trình là đã kiểm chứng quy trình |

## Owner và cách tiếp tục

Coordinator giữ liên kết issue/task/PR và tách công việc theo phụ thuộc. Implementer mỗi scope khác reviewer; chủ sản phẩm chốt phạm vi/acceptance/merge/release. Tên vai trò không chứng minh năng lực chuyên gia. Chưa assign issue cho một người khác hoặc gửi thông báo ngoài dự án; owner trách nhiệm kỹ thuật ở bảng/task, không giả có đội nhân sự đã nhận.

Thứ tự hiện tại: hoàn tất GOV-001 (main rules và bằng chứng) → source/bootstrap không bí mật và môi trường tách → chọn bug có reproduce → app task/regression/review/PR → nghiệm thu các chặng được cấp quyền. Việc source/app dựng lại chưa hoàn tất; tên public không thay thế kiểm thử hoặc quản trị.

Main control còn gần bản khởi tạo; PR1 chưa có hai job mới nên có thể bị chặn bởi required checks. Cần nhiệm vụ tích hợp stack theo thứ tự phụ thuộc và policy phù hợp, không bypass hoặc merge trong GOV-001. Các nhánh feature/stack không bị khóa ghi bởi policy chỉ nhắm main.

## Bằng chứng và trạng thái theo phiên bản

[Task](../../tasks/FLOW-001/task.json), evidence trong `tasks/FLOW-001/evidence/`, review/handoff khi có ghi subject kiểm khác commit chứa báo cáo. Không sửa bytes evidence cũ để làm xanh. Tool plan chỉ báo cấu trúc hợp lệ; verify records chỉ kiểm nhất quán và Git hiện tại, không xác nhận lời khai test hoặc reviewer identity. Local hook và CI không tự có quyền chặn server merge.
