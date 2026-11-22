# Bảo vệ main — GOV-001

Ngày 23/11/2026. [Issue15](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/15), [task](../../tasks/GOV-001/task.json). Trạng thái: **đã áp dụng main rules và kiểm các phép thử bên dưới**. [Receipt thực thi](../../tasks/GOV-001/evidence/execution.json) giữ ID, effective rules, phép thử, kiểm tra sau dọn dẹp. Tài liệu/config trên nhánh đang review, chưa merge.

## Chính sách dự án

| Phạm vi | Control | Source app |
| --- | --- | --- |
| Target thật | Default branch `main` | Default branch `main` |
| PR trước thay đổi | Có, 0 approval GitHub | Có, 0 approval GitHub |
| Chặn xóa / non-fast-forward | Có / có | Có / có |
| Giải quyết review threads | Có | Có |
| Required checks | `contracts-and-tests`, `issue-and-product-record`; nguồn GitHub Actions App ID15368 | Chưa có CI sản phẩm; không yêu cầu check hư cấu |
| Nhánh phải cập nhật base | Có với hai checks | Chưa áp dụng vì chưa có checks |
| Bypass | Danh sách rỗng | Danh sách rỗng |

Payload đích: [control](../../config/github/control-main.ruleset.json) và [app](../../config/github/app-main.ruleset.json). ID repo và preflight giữ ở [bằng chứng](../../tasks/GOV-001/evidence/preflight.json). Chỉ có owner `trdat1605` trong danh sách collaborator kiểm ngày này; không yêu cầu approval của một người chưa có. Review agent vẫn bắt buộc theo quy trình nội bộ, nhưng chưa được GitHub xác minh tự động là human approval. Admin có thể sửa policy; đây không là sandbox không thể vượt.

## Kiểm thực thi

[Kế hoạch](../../tasks/GOV-001/evidence/ruleset-plan.json) phải được reviewer khác kiểm trước thao tác. Dùng cùng actual ruleset đang bảo vệ main, tạm thêm **chỉ** exact random ref thử. Không gửi request ghi/force/xóa vào main. Sau từng thao tác lưu receipt ngay.

Các thử: direct fast-forward bị chặn, forced non-fast-forward bị chặn, xóa bị chặn; kiểm message hoặc rule-suite để không nhầm lỗi mạng/quyền với policy. Control có head commit mới cùng tree với bản PUB-001 đã review để bảo đảm chưa có check từ trước. Trước PR phải quan sát missing checks; PR metadata sai làm job thật FAIL; metadata hợp lệ chạy lại hai job để kiểm readiness. Đây là **synthetic enforcement probe**, không là bàn giao PUB-001 mới, GOV-001 product acceptance hoặc feature app. Không gọi merge endpoint. App dùng same-tree commit, không sửa source; nếu GitHub từ chối empty-diff PR thì ghi NOT_RUN.

Sau thử bỏ exact probe targets khỏi rulesets, đóng PR thử unmerged và xóa chỉ refs thử đã ghi đúng SHA. Giữ main protections nguyên, kiểm tất cả nhánh gốc vẫn đúng SHA và Actions app vẫn tắt. Kết quả FAIL/NOT_RUN cũng giữ trong receipt; chưa quan sát thì chưa ghi PASS.

## Kết quả quan sát

| Phép thử | Kết quả | Bằng chứng / giới hạn |
| --- | --- | --- |
| Effective rules | PASS cả hai kho | Control ruleset27859154; app27859157, active/no bypass; đọc rules áp main |
| Direct fast-forward | Bị chặn cả hai | HTTP422 nêu yêu cầu pull request; control còn nêu 2 checks expected |
| Forced non-fast-forward | Bị chặn cả hai | HTTP422 nêu Cannot force-push và PR requirement |
| Delete branch | Bị chặn cả hai | HTTP422 nêu Cannot delete this branch |
| Fresh head chưa có check | Quan sát check_count0, bị chặn bởi PR rule | Suite5294561172 báo status rule PASS; không lấy phép này chứng minh missing-check enforcement |
| Missing required checks thực sự bị chặn | PASS trên directFF probe riêng | Suite5294561671 ghi required_status_checks FAIL và 2 checks expected |
| Metadata PR thiếu Task | Expected FAIL; PR blocked | [Run45073259804](https://github.com/trdat1605/r-61974bac4c68fe3c/actions/runs/45073259804): issue-and-product-record failure, contracts success; nondraft PR vẫn blocked |
| Metadata hợp lệ, cùng head control | PASS readiness | [Run45073330723](https://github.com/trdat1605/r-61974bac4c68fe3c/actions/runs/45073330723): cả2jobs success từ App15368; PR16 clean/mergeable true |
| App same-tree PR | PASS readiness, không có checks | PR1 clean/mergeable true; Actions app disabled; không là productCI/test |
| Merge thật | NOT_RUN | Không gửi merge endpoint, kể cả PR thử |

Giữ cả job cố ý FAIL và lần quan sát cũ trong receipt. Một stdout ghi Six negative probes bị sai nhãn; thực tế có 7 denial entries, gồm phép fresh-head bổ sung. Không xóa kết quả không thuận lợi.

## Giới hạn và việc còn lại

Chỉ default main được bảo vệ, feature/stack branches vẫn ghi bình thường. Check nguồn App15368 không chứng minh mọi workflow là đáng tin; sửa workflow cần review và app tests khác governance tests. GitHub có thể chấp nhận một số check skipped/neutral theo cơ chế của họ; gate hồ sơ không là bảo đảm nghiệp vụ.

PR1 nhắm main còn là bản cũ chưa có hai job mới; required checks có thể chặn tích hợp nó. Cần kế hoạch tích hợp stack riêng, kiểm đầy đủ và quyền merge riêng. Không hạ policy/bypass để làm xanh hoặc merge trong GOV-001.

App chưa có product CI, clone chưa dựng lại được runtime hoàn chỉnh, chưa có pilot bugfix/feature, upgrade/rollback/Zalo/mobile chưa nghiệm thu. Xem [bảy cải tiến](improvement-tracker.md) và [source/reproduction](source-reproduction.md).

## Nguồn đã đọc

[GitHub tạo ruleset](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) mô tả target, bypass, active state. [Các rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) phân biệt yêu cầu PR, approvals, nguồn check và strict policy. [REST rules](https://docs.github.com/en/rest/repos/rules) cung cấp POST/PUT và effective rules; [rule suites](https://docs.github.com/en/rest/repos/rule-suites) hỗ trợ xem kết quả đánh giá. Việc chọn main/0approvals/hai control jobs và probe là điều chỉnh cho dự án, không là khuyến nghị rằng mọi doanh nghiệp nên dùng cùng cấu hình.
