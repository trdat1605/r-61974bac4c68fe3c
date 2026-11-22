# Review, CI và quyền merge thực tế

Ngày **23/11/2026**, [GOV-003 / issue #10](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/10). Owner quyết định quyền: chủ sản phẩm. Coordinator chuẩn bị, reviewer khác kiểm; không tự merge/phát hành.

## Trạng thái quan sát

**Lịch sử FLOW-001 trước chuyển đổi:** kho control là private; API xác nhận quyền admin của tài khoản nhưng GET rulesets trả **HTTP403: Upgrade to GitHub Pro or make this repository public**. Đây là giới hạn gói GitHub quan sát được, không phải lý do đổi public hoặc mua gói. Không có server enforcement được nghiệm thu trong lượt này.

**PUB-001:** chủ sản phẩm sau đó yêu cầu công khai cả hai kho, chấp nhận discoverability. Kho đã đổi tên; [publication](repository-publication.md) giữ bằng chứng riêng. GET rulesets sau chuyển đổi trả HTTP200 ở cả hai kho và danh sách rỗng; có khả năng sử dụng không tự là đã cài/enforce. Không mua gói hoặc tự merge.

Local hook chỉ chạy khi gọi/cài đúng và có thể bỏ qua. Governance CI kiểm hợp đồng/tools; job PR issue kiểm traceability; cả hai chưa là required checks phía server và chưa là CI sản phẩm. Review JSON khác implementer không tự là GitHub approval của người khác hoặc cách ly quyền máy.

## Chính sách chuẩn bị để owner xem — chưa áp dụng server

- Nhánh đích được chọn rõ, yêu cầu PR/checks theo risk, conversation resolution và xét lại approval khi head/base đổi.
- Danh sách required checks dùng tên job duy nhất, xác định nguồn check và không dùng job tổng hợp xanh để che product checks FAIL/NOT_RUN/skipped. Ngoại lệ phải ghi lý do.
- Review app nhận exact app repo/base/subject, acceptance/evidence. Thay đổi app sau review cần kiểm lại vùng ảnh hưởng; metadata và app SHA không được trộn.
- Người phê duyệt kỹ thuật cần quyền/năng lực phù hợp. Bot/subagent không thay lượt người nếu policy cần người. Hiện chưa xác nhận có một reviewer người thứ hai trên GitHub; không cài yêu cầu khiến owner tự approve PR của mình rồi gọi độc lập.
- Merge queue, deployment gates, security review tự động và rollback production chưa thiết lập. Chỉ bật khi có phạm vi/quyền và khả năng vận hành đã kiểm.

## Cách nghiệm thu enforcement sau này

Khi có tính năng/gói và quyết định quyền phù hợp: reviewer đọc target settings/Active state, actor/bypass, expected checks và stale approval; thử có kiểm soát một PR thiếu check hoặc review phải bị chặn, rồi positive case đúng bản. Ghi API/settings và kết quả, không suy từ file cấu hình. Không thực hiện thử merge vào nhánh thật trong lượt FLOW-001.

Điểm cần owner quyết sau khi có cấu hình cụ thể: ai là reviewer người có quyền và nhánh bảo vệ nào. Quyết định public đã có ở PUB-001; không cần hỏi lại hoặc mua gói trong nhiệm vụ này. Không cần quyết các việc này để tiếp tục khảo sát/branch/CI/Draft PR hiện tại.

## Nguồn

[GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) mô tả availability/private plans, stale review, checks và bypass. [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) hỗ trợ quyền tối thiểu, tránh chạy PR input như shell và pin dependencies. [Claude Code review](https://claude.dev/blog/solving-code-review-at-anthropic/) là căn cứ tham khảo trách nhiệm, không cấp quyền hoặc bảo đảm thực thi cho repo này.
