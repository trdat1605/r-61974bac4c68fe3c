# Gói ngữ cảnh cho một nhiệm vụ

Mẫu dự án ngày 23/11/2026, cập nhật từ mẫu local ngày 11/11. Đây là dữ liệu bàn giao được coordinator điền và truyền rõ cho agent; file tồn tại không tự tạo hoặc cấu hình agent.

- **Việc / mục tiêu / acceptance:** liên kết `tasks/<id>/task.json`; nói rõ ngoài phạm vi.
- **Nơi làm:** repo, worktree, baseline, branch, application ref; subject commit khi bàn giao. Phân biệt repo tài liệu và repo app.
- **Chỉ dẫn đang áp dụng:** AGENTS/override thực tại nơi sửa; đừng dùng bản tham khảo lưu trong thư viện thay chỉ dẫn checkout.
- **Tuyến đọc và lý do:** chọn R-xx từ [reading-routes.md](reading-routes.md); mỗi nguồn ghi ID/URL, ref/ngày, mục cần đọc và vì sao liên quan.
- **Mở thêm khi nào:** API, dữ liệu, edition, mobile, dịch vụ ngoài hoặc phụ thuộc khác do source chỉ ra; ghi điều kiện mở rộng và quyền cần thêm.
- **Code/test cần đối chiếu:** paths và dòng theo commit, hành vi mong đợi, ca lỗi cần bắt. Chưa có app source trong clone thì ghi giới hạn, không giả đã khảo sát code.
- **Quyền / ownership / runtime:** tệp được ghi, claim owner, runtime read-only hay exclusive-write; DB/Redis/ports dùng chung hay đã tách bằng chứng nào.
- **Kiểm tra:** command, môi trường, PASS/FAIL/NOT_RUN, output đã làm sạch và commit tương ứng. Chỉ dẫn không thay kết quả chạy.
- **Bàn giao:** đã xong, findings chưa xử lý, quyết định và căn cứ, bước tiếp theo/receiver. Reviewer nhận đúng subject và input hashes, ngữ cảnh mới; không truyền nguyên lập luận implementer để thay yêu cầu.

Định dạng máy kiểm vẫn là [phiếu JSON và workflow](../agents/README.md). Không sao chép nguyên hồ sơ lịch sử vào mỗi gói. Yêu cầu đã có trong task nên liên kết; chỉ ghi thêm phần giúp thực hiện lần này. Người đọc có thể mở rộng source khi phát hiện phụ thuộc, không bị bảng tuyến giới hạn cứng.
