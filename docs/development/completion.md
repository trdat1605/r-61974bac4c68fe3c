# Hoàn thiện bảy cải tiến — COMPLETE-001

Ngày 23/11/2026. [Issue18](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/18), [phiếu việc](../../tasks/COMPLETE-001/task.json). Đây là trang theo dõi công việc đang thực hiện; **chưa phải báo cáo nghiệm thu**. Giữ nguyên task/review/evidence lịch sử.

## Tiêu chí và phụ thuộc

| Mục | Bằng chứng cần có để chấp nhận trong phạm vi này |
| --- | --- |
| 1. Phối hợp agent | Protocol cố định, các lượt Codex routing/peer thật, reviewer chấm theo source, quyết định tạm có giới hạn. Chủ sản phẩm xác nhận chưa có Claude Code; Claude Agent Teams NOT_RUN, không đổi tên phép thử Codex thành Claude Teams |
| 2. Traceability | Issue ứng dụng thật, task và app SHA riêng control SHA, regression/review/PR có liên kết; template ở default branch chỉ kiểm sau khi merge được cho phép |
| 3. Dựng lại môi trường | Source clone từ GitHub, cấu hình có version, secret sinh riêng, build và môi trường mới không phụ thuộc adapter/volume lab; lặp setup/restart và kiểm source ref |
| 4. Kiểm thử và CI | Lỗi Docker metadata có baseline FAIL, fix PASS; CI thực trên app SHA đã review, focused app tests; phạm vi test và phần chưa chạy ghi rõ |
| 5. Review/quyền tích hợp | Review agent ngữ cảnh riêng đúng commit; main rules giữ nguyên; merge cần quyết định với PR/SHA cụ thể, không giả human approval |
| 6. Trạng thái/bàn giao | Một điểm bắt đầu, receipt command/ref/hash, PASS/FAIL/NOT_RUN và kiểm tiếp quản; không dùng số lượng tài liệu làm chất lượng |
| 7. Pilot quy trình | Lỗi thật đi qua issue→task→source→regression→review→PR và kiểm bàn giao; diễn tập phục hồi chỉ trên dữ liệu tổng hợp mới. Không đồng nghĩa phát hành sản phẩm hoặc tích hợp Zalo |

## Những quyết định đã có

- Chỉ thao tác project thử mới `cwdev-complete001`, các cổng dự kiến 44440–44442. Lab `cwlab-9200023e` và website khóa học `course-platform-local` giữ nguyên. Tên project không tự chứng minh an toàn: cần đọc cấu hình render và so volumes/mounts/ports thực.
- Phép sửa ứng dụng nhắm lỗi build Git metadata từ linked worktree; [issue app2](https://github.com/trdat1605/s-251521f7e9131fb0/issues/2). Build context dùng source đã commit, không chép env/adapter ignored trên máy.
- Có thể dùng image cache đã chọn bằng ID để kiểm setup, nhưng phải ghi CACHE_REUSE; đó không thay bằng chứng full Dockerfile build. Không hứa build bit-identical khi dependency mạng chưa pin đầy đủ.
- Kho app có 17 workflow kế thừa. Phải tắt và đọc lại từng workflow khi Actions toàn kho còn tắt, review CI mới rồi mới bật. Không dùng việc thiếu secrets làm cơ chế ngăn workflow publish.
- PR tích hợp control phải giữ lịch sử bằng merge commit: core checker dùng ancestry của reviewed subjects. Không squash/rebase hoặc sửa receipt cũ để hợp thức hóa.

## Đọc bằng chứng

Kế hoạch và review nằm trong `tasks/COMPLETE-001/evidence/`; app task xác định checkout/ref/scope riêng. Kết quả runtime/CI/agent eval chỉ được ghi đạt sau khi có dữ liệu tương ứng. Phần đang chờ review hoặc quyền phải giữ trạng thái chưa hoàn tất.

## Checkpoint đã kiểm chứng — 23/11/2026

[CI45082996742](https://github.com/trdat1605/s-251521f7e9131fb0/actions/runs/45082996742)
đạt cả `metadata`, `focused-frontend`, `isolated-runtime` tại app head
`27e166927b93677863e7e7fda22109cfa2ae98b9`. Runner thực checkout merge commit
`8d953fd35000ffc06a9696ad0a6ba91c211f6466`, tree
`65705962f43b3c1a3b35920b66436d3c210c4db6` giống app head; không nhầm hai SHA.
[Receipt chọn lọc](../../tasks/COMPLETE-001/evidence/app-ci-lifecycle-success.json)
ghi 23 boundary tests, 14 frontend tests trong job riêng và lifecycle:
full build/SHA, DB tổng hợp, HTTP API/login/Vite/Mailhog, focused RSpec/Vitest,
restart, pg_dump → DB restore mới với counts 2 accounts/1 user/129 configs,
prepare lặp và stop project. Không đưa dump/secrets/log thô lên Git.

Kết quả local FAIL và run bị hủy do push tài liệu vẫn giữ nguyên. Không dùng PASS
hosted để nói lab đã được thay hoặc sửa F5. Chưa kiểm tương tác trình duyệt,
toàn bộ suite, dữ liệu thật hoặc production.

Đánh giá Codex hoàn tất 12 lượt/36 outputs, có chấm source độc lập và kiểm lại
findings bởi reviewer thứ hai: 5 lượt đạt đầy đủ, 7 fail/partial. [Kết quả](agent-selection.md)
giữ lỗi thiếu chi tiết bàn giao/trích dẫn và một own-result read ngoài allowlist;
không chọn mô hình thắng hoặc gọi native Claude Teams đã thử. Brief đã cải thiện
cho việc sau; CLI loading PASS, hiệu quả hành vi của brief mới chưa đo.

Review app cuối PASS tại27e1669 và app PR3 đã cập nhật đúng SHA/CI. Product record
đã gắn review thật; bước verify trên control commit sẽ kiểm sau commit.
[Phương án Docker sang D](../runbooks/docker-storage-migration.md) đã review bổ sung:
chuẩn bị bàn giao PASS, thực hiện vẫn BLOCKED_FOR_EXECUTION do các cổng backup,
capacity, maintenance, rollback và postchecks chưa được phép/chưa kiểm xong.
Không chuyển hoặc restart Docker. Ba required app checks đã apply/readback sau review, main giữ nguyên. Còn
final control review/handoff/CI và PR tích hợp để owner quyết định. Templates trên
main chỉ kiểm active sau merge được cho phép; chưa đánh dấu cả bảy hoàn tất.
