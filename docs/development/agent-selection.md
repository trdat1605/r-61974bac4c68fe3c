# Lựa chọn mô hình agent có bằng chứng

Ngày **23/11/2026**, [GOV-001 / issue #6](https://github.com/trdat1605/chatwoot-vn/issues/6). Quyết định hiện tại: dùng coordinator + subagents theo nhiệm vụ; đây là lựa chọn đã thử ở phạm vi docs/tooling, **chưa chứng minh tối ưu cho Chatwoot**. Chưa triển khai hoặc A/B native Claude Agent Teams.

## Nguồn và điều không được suy rộng

| Nguồn đã đọc ngày 23/11 | Nội dung liên quan / giới hạn |
| --- | --- |
| [Towards a Science of Scaling Agent Systems, v3, 08/04/2026](https://arxiv.org/html/2512.08296v3) | Preprint, 260 cấu hình/sáu benchmark. Lợi ích phụ thuộc nhiệm vụ và phối hợp; SWE-bench/Terminal-Bench dùng tập con 20 bài. Không trực tiếp so tính năng Claude Teams với cấu hình Codex dự án |
| [Worse Together, v1, 30/09/2026](https://arxiv.org/abs/2610.00583) | Preprint, môi trường nhiều người dùng/mục tiêu riêng. Cho thấy rủi ro phối hợp tài nguyên; khác một chủ sản phẩm và một mục tiêu chung của lab |
| [Anthropic multi-agent Research, 13/06/2025](https://www.anthropic.com/research/multi-agent-research-system) | Bài kỹ thuật dùng lead + subagents; kết quả eval nghiên cứu thông tin không là bảo đảm chất lượng code |
| [Claude Agent Teams](https://code.claude.com/docs/en/agent-teams) và [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Hướng dẫn sản phẩm về cơ chế phối hợp, không phải so sánh thực nghiệm của dự án. Tính năng/permissions phải kiểm trên công cụ thật |
| [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices#multi-agent-architectures) | Hướng dẫn chọn kiến trúc theo evals; không chứng nhận mô hình nào của lab |

## Khi chọn và khi xem lại

Chia khảo sát độc lập, giữ một writer cho mỗi phạm vi, reviewer khác người viết. Nếu cần nhiều thành viên liên tục thương lượng hợp đồng, đầu mối trở thành chỗ nghẽn, quyết định bị thất lạc hoặc tích hợp thất bại lặp lại, thử cơ chế team phù hợp sau khi kiểm công cụ/quyền/tài nguyên. Có messaging không tự chứng minh phối hợp tốt.

Không thêm agent chỉ để đặt chức danh; không bỏ review/test cần thiết để giảm token. Khi chưa khảo sát nguồn hoặc chưa đo, ghi “đề xuất/chưa đủ bằng chứng” thay vì “tối ưu/không cần Teams”.

## Phép so sánh cần thực hiện — NOT_RUN

Dùng một bộ công việc có acceptance và ref cố định: khảo sát API, sửa bug với regression, thay đổi có backend/frontend phụ thuộc. So coordinator+subagents với cơ chế team thực có; giữ đầu vào và kiểm kết quả cuối tương đương, lặp đủ để tránh kết luận từ một lượt may mắn. Không tự đặt số lần chạy hoặc mục tiêu tiết kiệm khi chưa chốt thiết kế đo.

Đo hành vi đúng/lỗi còn sót, findings sai, xung đột/ghi ngoài scope, quyết định bị mất, tiếp quản, thời gian và sự can thiệp cần thiết. Ghi actual tool/model/context/ref và giới hạn; số agent/token không là điểm chất lượng. Những lỗi workflow/claim/env đã có trong tests là nguồn ca đánh giá tooling; chúng chưa là benchmark feature Chatwoot.

Owner: coordinator chuẩn bị ca, reviewer kiểm dữ kiện và cách chấm; chủ sản phẩm quyết định phạm vi/chấp nhận. Chưa có kết quả A/B thì issue còn mở.
