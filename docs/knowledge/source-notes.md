# Ghi chú nguồn về tài liệu, agent và review

Đọc lại ngày **23/11/2026**. Metadata ở [supplemental-sources.json](supplemental-sources.json). Ghi chú dưới đây do dự án viết; không phải bản sao toàn văn, cấu hình đã chạy hay bằng chứng năng lực của Codex. [Khảo sát ngày 18/11](../agents/sources.md) vẫn giữ nguyên ngày và giới hạn lịch sử.

## AN-REVIEW — bài gốc nhóm Claude Code

[How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/), Addy Osmani, Morgan Westlee Lunt, Qing Wang; đăng **15/10/2026**.

**Nguồn nói:** dùng nhiều lớp kiểm, bằng chứng thực chạy, review ngữ cảnh mới, xử lý findings và phê duyệt theo rủi ro; có cơ chế khôi phục. Đây là kinh nghiệm của đội tác giả tại thời điểm công bố.

**Áp dụng dự án:** quy trình hiện có yêu cầu task, commit, checks và reviewer khác. Các lớp security review tự động, merge queue, phát hành dần và diễn tập rollback sản phẩm chưa được chứng minh đã thiết lập. [Bản ghi âm người dùng và các lưu ý khi đọc](user-materials/README.md) bổ sung ngữ cảnh, không thay bài gốc.

## AN-MEMORY — chia chỉ dẫn theo phạm vi

[Claude memory](https://code.claude.com/docs/en/memory), tài liệu live, không thấy mốc cập nhật ổn định để pin theo CLI dự án.

**Nguồn nói:** giữ thông tin cần cho nhiều phiên trong chỉ dẫn dự án; đưa quy trình nhiều bước hoặc chỉ liên quan một vùng sang tài liệu có phạm vi phù hợp. Nội dung chỉ dẫn là context, không phải cơ chế chặn hành động.

**Áp dụng dự án:** giữ AGENTS và cửa vào ngắn, chi tiết trong tuyến đọc/gói ngữ cảnh. Cách nạp Claude không tự thành cách nạp Codex. Chưa kiểm auto-loading từ mọi chat tại source app.

## AN-SUBAGENTS — ngữ cảnh và đầu vào được giao

[Claude subagents](https://code.claude.com/docs/en/sub-agents), tài liệu live.

**Nguồn nói:** subagents xử lý nhiệm vụ chuyên biệt trong context riêng, có cấu hình và quyền theo công cụ Claude. Đầu vào khởi tạo khác nhau theo loại agent.

**Áp dụng dự án:** giao mục tiêu/ref/nguồn/phạm vi/đầu ra rõ bằng brief Codex. Reviewer mới nhận yêu cầu và phiên bản cần kiểm. Đây là phối hợp trên công cụ thực có; các agent của lab chia sẻ quyền máy, chưa phải sandbox độc lập.

## AN-TEAMS — chọn khi có việc độc lập

[Claude Agent teams](https://code.claude.com/docs/en/agent-teams), tài liệu live ghi tính năng thử nghiệm và tắt mặc định.

**Nguồn nói:** có lead, tasks và liên lạc giữa teammates; phù hợp công việc có thể làm độc lập. Phối hợp cũng tạo overhead, nhất là việc phụ thuộc hoặc cùng sửa tệp.

**Áp dụng dự án:** không dựng đội cố định theo chức danh. Người điều phối phân việc theo phạm vi; một nơi ghi có một owner. Đã có công cụ claims riêng của repo; chưa cài Claude Team.

## AN-HARNESS — tiếp tục sau khi mất ngữ cảnh

[Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), đăng **26/11/2025**.

**Nguồn nói:** thí nghiệm dùng chuẩn bị môi trường, danh sách công việc, ghi tiến độ, Git và kiểm tra để phiên sau tiếp tục được.

**Áp dụng dự án:** thử một reviewer mới bắt đầu từ README trong clone GitHub, ghi đường tìm thông tin và các khoảng trống. Đây là phép thử tài liệu, chưa chứng minh dựng lại app hoặc toàn bộ quy trình sản phẩm.

## AN-CONTEXT — tìm thông tin theo việc

[Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), đăng **29/09/2025**.

**Nguồn nói:** context cần được chọn và duy trì theo nhiệm vụ; dùng tìm kiếm để lấy thông tin phù hợp khi cần.

**Áp dụng dự án:** [mục lục](README.md) dẫn đến [tuyến đọc](reading-routes.md), rồi mở nguồn/code chi tiết. Không đặt mức token tiết kiệm hoặc bỏ kiểm chứng để rút ngắn context. Chưa đo hiệu quả/token của bố trí này.
