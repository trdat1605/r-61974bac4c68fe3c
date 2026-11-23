# Pilot sản phẩm và kiểm thử Chatwoot

Ngày **23/11/2026**, [QA-001 / issue #9](https://github.com/trdat1605/chatwoot-vn/issues/9), phụ thuộc [source/reproduction #8](https://github.com/trdat1605/chatwoot-vn/issues/8). Owner kỹ thuật: coordinator và implementer nhiệm vụ app; reviewer khác; chủ sản phẩm chấp nhận phạm vi.

**FLOW-001 chưa có pilot ứng dụng; COMPLETE-001 đang thực hiện pilot Docker metadata thật.** Xem [issue app2](https://github.com/trdat1605/s-251521f7e9131fb0/issues/2), [PR app3](https://github.com/trdat1605/s-251521f7e9131fb0/pull/3) và [trạng thái](completion.md). Source app và control SHA riêng, các lần FAIL và sửa/review giữ trong evidence. Tooling fixtures hoặc kế hoạch hợp lệ không thay pilot sản phẩm. Không chọn một thay đổi cosmetic để tạo cảm giác quy trình đã được thử.

## Điều kiện bắt đầu

App source/delta không bí mật có thể lấy lại; checkout đúng ref; môi trường test có project/ports/DB/Redis/volumes riêng hoặc quyền rõ; không dùng development DB hiện tại để chạy lệnh tạo/reset schema của CI. Có bug tái hiện chắc hoặc yêu cầu feature nhỏ được chốt, acceptance cụ thể và rollback phù hợp. Thiếu thì ghi `BLOCKED_SOURCE_REPRO` hoặc `BLOCKED_TEST_ENV` tại issue, không nới tiêu chí để đi tiếp.

Hai ứng viên khảo sát đã biết: lỗi build metadata Git khi Docker đọc worktree pointer (source audit có căn cứ), và F5 chậm (đã có đo nhưng chưa causal A/B). Chưa hứa performance fix nhỏ; phải chọn ca sau khi xác minh reproduction. Nhiệm vụ thực sẽ ghi issue/app base/subject và focused regression rõ; [record ví dụ](product-record.example.json) chưa là nhiệm vụ đủ để giao sửa code.

## Kiểm thử/CI theo ảnh hưởng

| Thay đổi | Checks cần chọn có lý do |
| --- | --- |
| Ruby/API/job/schema | Rubocop, RSpec focused/regression và quyền/account/data migration khi ảnh hưởng; mở rộng regression theo dependency |
| JS/Vue | ESLint, frontend tests/build phù hợp và kiểm trình duyệt cho hành vi UI; API/mobile nếu payload đổi |
| Docker/bootstrap | Cấu hình parse với env giả, build đúng source ref, mount/service identity, chuẩn bị DB/test riêng và restart/cleanup đúng namespace |
| Kênh ngoài | Hợp đồng/quyền API, mock lỗi có căn cứ, test live với tài khoản được cấp; mock PASS không chứng minh Zalo thật |

[CE workflow đúng app pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/workflows/run_foss_spec.yml) có lint/frontend/RSpec, bỏ enterprise ở lượt CE và Brakeman đang non-blocking. Dùng làm đầu vào chọn checks, không sao chép toàn pipeline/publish hoặc gọi CE xanh là full Enterprise/security đạt. COMPLETE-001 đã tắt 17 workflow kế thừa, bật riêng workflow foundation sau review với action allowlist/token đọc; không bật pipeline publish upstream.

## Hồ sơ đủ để đánh giá pilot

- Issue có reproduce/use case, scope và AC-xx; app base/subject thật, đường tệp và lý do.
- Regression/baseline chứng minh điều kiện cần sửa và checks sau sửa; command/output/env/hash đã làm sạch, không chỉ JSON tự khai PASS.
- Reviewer mới đọc source/diff/test; findings được xử lý và đúng final app SHA.
- App PR liên kết issue/control task, kết quả checks và product How to test. Sau đổi base phải kiểm tổ hợp.
- Owner acceptance, merge/release/post-change checks chỉ ghi đã làm khi có quyền và bằng chứng. Nếu dừng ở Draft PR thì chỉ nghiệm thu đến mốc đó.

FLOW-001 chỉ tạo nền móng/checker. COMPLETE-001 đã có lỗi build thật, regression và [CI vòng đời PASS](../../tasks/COMPLETE-001/evidence/app-ci-lifecycle-success.json) ở apphead27e1669, mergecheckout8d953fd có tree giống hệt. [Product record](../../tasks/COMPLETE-001/evidence/product-record.json) đã liên kết [review app cuối PASS](../../tasks/COMPLETE-001/evidence/app-final-review.json) tại đúng27e1669; kiểm consistency trên control commit và review tích hợp còn chờ. UI tương tác, Zalo/mobile, nâng cấp sản phẩm và production release vẫn NOT_RUN. Không có giới hạn tải hoặc bảo đảm ổn định toàn sản phẩm mới.
