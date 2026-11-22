# Đổi tên và công khai hai kho

Ngày 23/11/2026, task PUB-001. Chủ sản phẩm yêu cầu công khai cả hai kho, đồng thời chấp nhận tên ngẫu nhiên không giữ bí mật hoặc ngăn tìm kiếm. Đây là quyết định riêng, thay giới hạn không đổi visibility trong task FLOW-001; hồ sơ cũ giữ nguyên tại đúng thời điểm.

## Nhận diện kho

| Vai trò | Repository ID | Tên cũ | Tên mới |
| --- | --- | --- | --- |
| Điều phối, tài liệu, bằng chứng | 1461752107 | trdat1605/chatwoot-vn | [trdat1605/r-61974bac4c68fe3c](https://github.com/trdat1605/r-61974bac4c68fe3c) |
| Source ứng dụng | 1467945011 | trdat1605/chatwoot-vn-app | [trdat1605/s-251521f7e9131fb0](https://github.com/trdat1605/s-251521f7e9131fb0) |

**Đã quan sát:** cả hai kho public qua API không có Authorization; ID và tất cả branch/tag heads giữ nguyên, app Actions tắt. GET rulesets trả200 và danh sách rỗng ở cả hai kho. Control common origin và clone kiểm bàn giao đã chuyển sang URL mới; source runtime tiếp tục dùng upstream. Readback cuối được lưu trong [hồ sơ thực hiện](../../tasks/PUB-001/evidence/publication-executed.json). Nhánh tài liệu/tooling còn Draft; không merge hoặc nghiệm thu sản phẩm trong nhiệm vụ này.

## Phạm vi kiểm tra và giới hạn

[Audit trước thay đổi](../../tasks/PUB-001/evidence/publication-audit-prechange.json) quét mẫu credential ở lịch sử control reachable, thông điệp commit, issue/PR/review/comments và toàn bộ 7 archive log Actions. Không có artifacts/release assets để kiểm. App chỉ có main đúng commit public upstream `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82` / tree `2979093d6c3f6c545fff930744e685ff3773f5d8`; không nhận kết quả ấy là đã scan từng blob trong 7013 commit app.

Không phát hiện mẫu không có nghĩa bảo đảm không có bí mật. Metadata tác giả Git, đường dẫn máy, tài liệu kế hoạch và bản ghi chia sẻ của người dùng có thể đọc công khai. Quay lại private không thu hồi được bản sao hoặc fork đã phát sinh. Không lưu env, credential, database hoặc dữ liệu khách hàng trong repo.

## Lần dừng kiểm tra và phục hồi

[Lần thử đầu](../../tasks/PUB-001/evidence/publication-attempt-1.json) dừng sau khi control đổi public vì dấu vân tay metadata không khớp. Chưa khôi phục được trường khác biệt, nên **nguyên nhân chưa xác minh**; không quy cho GitHub hoặc khẳng định nội dung cũ không đổi. Thuật toán cũ có cả toàn bộ user object và thứ tự mảng.

Đã [khảo sát lại nội dung hiện tại](../../tasks/PUB-001/evidence/publication-recovery-audit.json) và reviewer kiểm độc lập trước tiếp tục. [Kế hoạch phục hồi](../../tasks/PUB-001/evidence/publication-recovery-plan.json) dùng danh sách sắp theo ID, title/body và user ID/login; lưu hashes theo mục và kết quả ngay sau từng thao tác. Giữ cả hồ sơ FAIL; không đổi guard thành luôn PASS. Phép khảo sát lại chứng minh phạm vi nội dung hiện tại được kiểm, không tái tạo bằng chứng đã mất trước chuyển đổi.

## Công cụ và tài liệu sau đổi tên

`config/agents/repositories.json` giữ canonical URL, stable ID và alias được khai báo rõ. Checker chuẩn hóa alias cũ trước khi gọi endpoint GitHub cố định; không tự đi theo redirect có credential. Event của repo được map phải khớp ID. Việc này giữ task/evidence lịch sử byte-identical; không sửa link cũ trong các báo cáo lịch sử để giả chúng được viết sau đổi tên. Không tái sử dụng tên kho cũ vì có thể làm mất redirect.

README và tài liệu điều hướng hiện hành chuyển sang tên mới. Local control origin cập nhật; remote upstream của source runtime giữ nguyên. Clone mới vẫn chưa đủ dựng lại lab: xem [source/reproduction](source-reproduction.md). Các PR stack cũ chưa được merge, và HEAD cũ chưa tự có checker mới; không gọi kết quả CI cũ là bằng chứng kiểm tên mới.

App Actions tiếp tục tắt để tránh chạy workflow publish/schedule kế thừa upstream. Công khai chỉ giải quyết điều kiện availability của một số tính năng GitHub; không tự bật rulesets, required checks, human approval hoặc nghiệm thu sản phẩm. Không đổi code Chatwoot, runtime, DB, container hoặc feature flags.

## Căn cứ

[GitHub visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility) mô tả tác động của đổi public. [Đổi tên](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository) giải thích redirect và khuyến nghị đổi local remotes; redirect không làm nội dung bí mật. [Update repository API](https://docs.github.com/en/rest/repos/repos#update-a-repository) là API sử dụng để đổi name/private. Các guard, kiểm và alias map ở đây là điều chỉnh của dự án, không phải chứng nhận GitHub về chất lượng phần mềm.
