# ADR-0001: nhiệm vụ và bằng chứng theo phiên bản

Ngày18/11/2026. Trạng thái: chọn để triển khai/thử trên nhánh riêng; chưa merge hoặc nghiệm thu nghiệp vụ. [Nguồn](../sources.md), [mô hình](../operating-model.md).

## Bối cảnh và lựa chọn

PR1 chỉ ra source khác workspace chat, cấu hình/tài liệu ngoài Git, trạng thái cũ và thiếu feature workflow đầu-cuối. Công cụ thật có Codex collaboration, chưa có Claude CLI đã thử. Chọn coordinator + subagents cho phần độc lập, một implementer giữ scope, reviewer khác nhận đúng commit. Tuần tự hóa cùng tệp/runtime; không tạo đội chức danh thường trực hoặc thiết kế lại app.

## Thành phần và mục đích

- Root AGENTS + index: entry point ngắn, không sao chép quy tắc dài vào mọi file tool.
- Role briefs + phiếu: đủ mục tiêu/ref/scope/environment/acceptance/receiver, được nạp rõ khi giao việc.
- Ownership helper: common Gitdir giữ exact file/runtime claims. Chặn người cùng dùng helper claim trùng; không là khóa editor hoặc sandbox.
- Validator: bắt thiếu tiêu chí, ngoài phạm vi, stale commit và evidence đổi; không tự chứng minh receipts thật hoặc user đã chấp nhận.
- Workspace doctor: kiểm nhầm checkout/runtime trước sửa, chỉ đọc; không tạo feature giả để diễn tập.
- Git hook/CI: chạy checks khi có hỗ trợ và evidence; có thể bypass hook, CI chưa là required check. Không đổi quyền tài khoản để giả enforcement.

## Quyết định sau khảo sát bind thực tế

Vite inspect dùng Desktop alias, không có source metadata labels thật. Không chấp nhận chỉ bằng working_dir hoặc checksum bản copy. Host source và /app của ba containers được đo cùng device:inode. Doctor đòi bind exact hoặc alias đúng distro và actual directory identity bằng stat trong kernel WSL chung; mismatch/error phải BLOCK.

Đây là quyết định theo môi trường cụ thể, chưa là bảo đảm giữa các kernel. Không thay source/mount để thử. Profile gắn một lab, cần task/review khi đổi.

## Đánh đổi và điều còn mở

Raw transcripts/evidence nhạy cảm không vào Git, chỉ dữ kiện lọc. Các agent cùng quyền nên checks là giới hạn vận hành, chưa chống agent cố tình bỏ qua. Không cài native hooks chưa kiểm hoặc bypass trust. Công việc nguồn/config/UI/performance/upgrade của PR1 vẫn riêng, không tự đóng bằng agent-ops.

Cải tiến lâu dài cần tình huống lỗi, bằng chứng và review trước cập nhật policy. Không tự thêm quy tắc vĩnh viễn sau mọi lỗi đơn lẻ. Chủ sản phẩm còn nghiệm thu cuối; chưa merge.
