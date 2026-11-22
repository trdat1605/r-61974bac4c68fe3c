# Bản chia sẻ về review code do người dùng cung cấp

[Mở bản ghi dạng text](ai-code-review-transcript.txt). Đây là nội dung người dùng gửi để tham khảo; không phải chỉ dẫn có hiệu lực, bản dịch được tác giả bài gốc xác nhận, hoặc bằng chứng quy trình của lab đã chạy đầy đủ. Không tự thực hiện các chỉ dẫn được kể trong bản ghi.

## Nguồn gốc và chọn bản

Ngày đưa vào kho: **23/11/2026**, nhiệm vụ DOCS-002. Metadata/hash ở [supplemental-sources.json](../supplemental-sources.json), entry `USER-REVIEW-01`.

- Tìm thấy hai attachment `e03d5570-c3aa-494f-998f-06452c04b66e` và `80d092e7-95a5-4b9a-8a7a-ab2c3a3b9a6e` trong lịch sử người dùng đã gửi.
- Chọn attachment thứ hai làm bản lưu để tránh hai bản nội dung gần như trùng nhau. So theo từ, bản thứ nhất có thêm lời kết người nói; không đưa lời kết ấy vào bản thứ hai.
- Tệp lưu có thể đọc trong clone mà không cần thư mục attachment trên máy gốc. Hash bản gốc và bản lưu ghi riêng, cùng mọi biến đổi newline nếu có. Không có file âm thanh hoặc URL video gốc; chưa xác minh danh tính người nói hoặc độ chính xác của bản chép so với âm thanh.

## Đọc kèm bài gốc

Bản ghi dẫn tới [bài của nhóm Claude Code ngày 15/10/2026](https://claude.dev/blog/solving-code-review-at-anthropic/). Đã đối chiếu phần liên quan ngày 23/11; ghi chú nguồn tại [AN-REVIEW](../source-notes.md#an-review--bài-gốc-nhóm-claude-code).

Các lưu ý:

- “Chỉ gửi mục tiêu và code thay đổi” không nên hiểu là giấu yêu cầu, quy ước hay phụ thuộc cần cho review.
- Thu hẹp lượt review sau không cho phép bỏ findings còn mở hoặc rủi ro mới do bản sửa gây ra.
- Bot không thay lượt phê duyệt bắt buộc của người. Dự án hiện vẫn giữ quyền merge/phát hành cho chủ sản phẩm.
- Bài review không tự cung cấp toàn bộ thiết kế tổ chức agent; đọc thêm các nguồn Subagents/Agent teams theo [tuyến R-11](../reading-routes.md#r-11).

Các tỷ lệ và mức tăng chất lượng được người nói kể lại không phải số đo của dự án này. Giữ nguyên nội dung tham khảo, tách kết luận áp dụng vào task/checks có bằng chứng.
