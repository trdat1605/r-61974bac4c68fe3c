# Quy tắc vận hành agent của dự án Chatwoot Việt Nam

Policy ID: CHATWOOT_AGENT_POLICY_V1

Đọc [README.md](README.md) để định vị trạng thái và bản chính tài liệu, rồi [docs/agents/README.md](docs/agents/README.md) và chỉ mở tuyến cần cho nhiệm vụ. Đây là repo điều phối/cấu hình/bằng chứng; source ứng dụng là một repo khác được xác định trong `config/agents/runtime.json` và từng phiếu việc. Không coi cwd của repo này là source app. Kho local lịch sử chỉ là tham khảo; chưa có bằng chứng mọi chat ở source app tự nạp chỉ dẫn repo này.

- Nguồn trước đề xuất: đọc tài liệu/source chính thức đúng phiên bản; tách quan sát, suy luận, đề xuất và NOT_RUN. Ưu tiên đúng đắn, ổn định, bảo trì và bàn giao; không bỏ kiểm chứng để giảm token.
- Giữ quy ước upstream khi làm ở source Chatwoot: đọc AGENTS/override thực tại checkout đó; kiểm app/enterprise khi liên quan. Không áp dụng cú pháp Claude vào Codex.
- Trước sửa phải có phiếu trong `tasks/<id>/task.json`: mục tiêu/ref, acceptance, scope, phụ thuộc, môi trường/quyền, checks, receiver và escalation. Mỗi phạm vi chỉ một implementer ghi tại một thời điểm; claim qua công cụ ownership sau khi nó được kiểm chứng.
- Tách worktree không tách DB/Redis/container/port. Runtime dùng chung mặc định chỉ đọc; restart/migration/cấu hình nền tảng cần nhiệm vụ và người được giao rõ. Không reset DB, xóa volume/data, nâng runtime, mở quyền, merge PR hoặc phát hành trong nhiệm vụ agent-ops này.
- Người thực hiện không tự review/chấp nhận thay đổi mình. Reviewer nhận brief/ngữ cảnh riêng, đúng commit và bằng chứng; không tự sửa đối tượng review. Agent hiện chia sẻ quyền máy, nên fresh context và claim không phải sandbox bảo mật.
- Lưu PASS/FAIL/NOT_RUN với command, ref và bằng chứng đã làm sạch. Code đổi sau review cần kiểm lại phần ảnh hưởng. Validator chỉ kiểm những quan hệ máy có thể kiểm, không xác nhận nghiệp vụ hay tính trung thực của mọi receipt.
- Điều phối được tích hợp local sau review/kiểm tra, chưa được merge PR. Chỉ chủ sản phẩm quyết định nghiệm thu nghiệp vụ, thay phạm vi/ưu tiên và bước merge/phát hành.
- Không đưa secrets, env thực, thông tin khách hàng, dumps hoặc log nhạy cảm vào Git. Chỉ stage phạm vi được giao, đọc diff và quét nội dung trước push.
- Khi probe chỉ dẫn yêu cầu nêu policy ID, trả ID phía trên từ chỉ dẫn đang có; không đoán nếu không thấy. Không coi việc trả ID là chứng minh tuân thủ toàn bộ chính sách.

Kiểm tra tooling: `python -B -m unittest discover -s tests -v`; đọc thêm lệnh chính xác trong README theo giai đoạn đang thực hiện. Không mặc định CLI, hooks hoặc CI đã được nạp chỉ vì file tồn tại.
