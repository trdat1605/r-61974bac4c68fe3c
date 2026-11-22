# Trạng thái dự án

Cập nhật khảo sát **23/11/2026, Asia/Saigon**. [Điểm bắt đầu](../README.md), [nơi lưu bản chính](project-map.md). Nội dung này thay vai trò trạng thái tổng thể của các ghi chép trước; không thay kết quả lịch sử tại đúng revision.

## Đã quan sát / đã có bằng chứng

- Source ứng dụng đang chạy: Chatwoot v4.19.1, commit `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, branch `codex/wsl-migration`. Kiểm lại ngày 23/11: HEAD/branch đúng profile và `git status --short` rỗng. Vị trí/môi trường: [profile](../config/agents/runtime.json), [runbook](runbooks/local-development.md).
- Docker Desktop + WSL2, source Linux, chế độ development. Lượt chẩn đoán 23/11 ghi sáu dịch vụ đang chạy và health HTTP200; không phải nghiệm thu đầy đủ ứng dụng.
- [F5 ngày 23/11](reviews/performance/2026-11-23-f5.md): hai lượt load khoảng 13,12s và 11,02s trong trình duyệt đã quan sát, trong khi HTML khoảng 186ms và 161ms. Bằng chứng mạnh chỉ về chờ tải frontend module development trước khi API bắt đầu; chưa cô lập hết nguyên nhân, chưa có đối chiếu production hoặc sửa hiệu năng. Load event không phải thời điểm app dùng được.
- [Báo cáo nền móng 18/11](reviews/project-foundation/README.md) và [checkpoint agent 18/11](agents/state.md) giữ các kết quả đạt/không đạt/NOT_RUN theo ngày và commit. Đã có thử nghiệm giao việc/review/tooling; không suy ra hệ thống sản phẩm ổn định hoặc mọi phiên AI tự đọc đúng.

## Tài liệu dùng chung đang thay đổi

Kho riêng tư `trdat1605/chatwoot-vn` hiện chứa hồ sơ/công cụ, **chưa chứa source ứng dụng**. DOCS-001 thiết lập README, bản đồ, catalog gốc và trạng thái trên `codex/docs-home`; [review](../tasks/DOCS-001/review.json) PASS đúng subject và [PR #3](https://github.com/trdat1605/chatwoot-vn/pull/3) có [CI đạt](https://github.com/trdat1605/chatwoot-vn/actions/runs/45056629726) tại bản bàn giao. Không mở rộng kết quả ấy sang revision khác hoặc sản phẩm.

DOCS-002 nối tiếp trên `codex/knowledge-handoff`: [thư viện nguồn cho người đọc](knowledge/README.md), [tuyến R-01–R-11](knowledge/reading-routes.md), [gói ngữ cảnh](knowledge/context-packet.md), bản ghi âm dạng text và nguồn bổ sung. Phép thử reviewer từ clone GitHub mới sẽ ghi đúng subject/đường tìm thông tin/giới hạn trong hồ sơ [DOCS-002](../tasks/DOCS-002/task.json) và review/handoff khi có; không suy đã PASS từ việc tài liệu tồn tại.

Kiểm GitHub trong lượt DOCS-001 ngày 23/11: [PR #1](https://github.com/trdat1605/chatwoot-vn/pull/1), [PR #2](https://github.com/trdat1605/chatwoot-vn/pull/2) và PR #3 còn Draft/open. Nhánh DOCS-002 phụ thuộc #3, #3 phụ thuộc #2, #2 phụ thuộc #1. Chưa merge, chưa nghiệm thu sản phẩm; trạng thái PR/checks có thể đổi sau ngày ghi, kiểm trực tiếp tại PR.

## Chưa hoàn tất và việc tiếp theo

| Phần việc | Giới hạn / bước tối thiểu tiếp theo |
| --- | --- |
| Tài liệu và bàn giao | Đã bổ sung bản ghi âm dạng text và bản AGENTS tham khảo; còn các snapshots cũ ngoài Git. DOCS-001 đã thử đọc cùng máy; DOCS-002 thử từ clone GitHub mới. Cả hai không tự chứng minh auto-loading ở chat app hoặc dựng app trên máy mới |
| Quản lý source/cấu hình | Runtime adapters còn local/ignored; clone repo điều phối không tái lập app. Lập việc riêng để quản lý delta không bí mật và source, giữ quy ước upstream |
| Hiệu năng/UI | Chưa có A/B và production comparison; chưa sửa F5. Chốt phép đo app-ready và cấu hình đối chứng trước sửa |
| Quy trình thực tế | Tooling đã có các thử nghiệm lịch sử; chưa chứng minh trọn vòng một feature sản phẩm từ yêu cầu tới nghiệm thu. Không tự bật required checks hoặc merge |
| Zalo và mobile | Chưa triển khai connector; cần chốt loại Zalo/API, scope và test toàn tuyến. Mobile chỉ là bản tham khảo, chưa thử cặp tương thích |
| Nâng cấp/hoàn tác | Có các bằng chứng phục hồi trước đây nhưng chưa diễn tập cập nhật toàn bộ code + cấu hình + dữ liệu + uploads. Không nâng runtime trong DOCS-001 |

Nhiệm vụ hiện tại chỉ bổ sung nguồn/tuyến đọc và thử bàn giao tài liệu; quy tắc LF cho `.txt` trong Git giúp clone giữ đúng bytes tham khảo. Không đổi code Chatwoot, feature flags, database, container hoặc cấu hình agent hệ thống. Không có số đo tiết kiệm token và không dùng số lượng tài liệu làm bằng chứng chất lượng.
