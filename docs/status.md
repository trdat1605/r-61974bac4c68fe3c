# Trạng thái dự án

Cập nhật khảo sát **23/11/2026, Asia/Saigon**. [Điểm bắt đầu](../README.md), [nơi lưu bản chính](project-map.md). Nội dung này thay vai trò trạng thái tổng thể của các ghi chép trước; không thay kết quả lịch sử tại đúng revision.

## Đã quan sát / đã có bằng chứng

- Source ứng dụng đang chạy: Chatwoot v4.19.1, commit `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, branch `codex/wsl-migration`. Kiểm lại ngày 23/11: HEAD/branch đúng profile và `git status --short` rỗng. Vị trí/môi trường: [profile](../config/agents/runtime.json), [runbook](runbooks/local-development.md).
- Docker Desktop + WSL2, source Linux, chế độ development. Lượt chẩn đoán 23/11 ghi sáu dịch vụ đang chạy và health HTTP200; không phải nghiệm thu đầy đủ ứng dụng.
- [F5 ngày 23/11](reviews/performance/2026-11-23-f5.md): hai lượt load khoảng 13,12s và 11,02s trong trình duyệt đã quan sát, trong khi HTML khoảng 186ms và 161ms. Bằng chứng mạnh chỉ về chờ tải frontend module development trước khi API bắt đầu; chưa cô lập hết nguyên nhân, chưa có đối chiếu production hoặc sửa hiệu năng. Load event không phải thời điểm app dùng được.
- [Báo cáo nền móng 18/11](reviews/project-foundation/README.md) và [checkpoint agent 18/11](agents/state.md) giữ các kết quả đạt/không đạt/NOT_RUN theo ngày và commit. Đã có thử nghiệm giao việc/review/tooling; không suy ra hệ thống sản phẩm ổn định hoặc mọi phiên AI tự đọc đúng.

## Tài liệu dùng chung đang thay đổi

Kho riêng tư `trdat1605/chatwoot-vn` hiện chứa hồ sơ/công cụ, **chưa chứa source ứng dụng**. DOCS-001 thiết lập README, bản đồ, catalog gốc và trạng thái trên `codex/docs-home`; [review](../tasks/DOCS-001/review.json) PASS đúng subject và [PR #3](https://github.com/trdat1605/chatwoot-vn/pull/3) có [CI đạt](https://github.com/trdat1605/chatwoot-vn/actions/runs/45056629726) tại bản bàn giao. Không mở rộng kết quả ấy sang revision khác hoặc sản phẩm.

DOCS-002 trên `codex/knowledge-handoff` đã có [review PASS](../tasks/DOCS-002/review.json) tại app-independent documentation subject `a2f8fcf45bc5479a0a5f8548784e03a309f7a1b1`, bản bàn giao control `c7c884151d8baaa6d95312846b6ee4db3a6d5016`, [Draft PR #4](https://github.com/trdat1605/chatwoot-vn/pull/4) và [CI đạt tại bản đó](https://github.com/trdat1605/chatwoot-vn/actions/runs/45058938525). Reviewer tiếp quản từ clone GitHub trên cùng máy; chưa là dựng app máy khác hoặc app-chat auto-loading. Giữ cả ngoại lệ whitespace nguyên gốc và các gate chưa đạt trước metadata trong hồ sơ.

FLOW-001 trên `codex/product-foundation` triển khai nền móng [bảy cải tiến](development/improvement-tracker.md), liên kết issue5–11, [quy trình sản phẩm](development/product-workflow.md), checker và nguồn/reproduction. Kết quả review cuối và CI của bản mới xem task/PR; tài liệu có mặt không chứng minh mọi cổng đã đạt. Source app baseline đã có ở private [chatwoot-vn-app](https://github.com/trdat1605/chatwoot-vn-app) đúng `caab07a8...`, Actions tắt trước first push và vẫn tắt; [bằng chứng](../tasks/FLOW-001/evidence/source-seeded.json). Chưa có adapter portable hoặc product CI.

Kiểm GitHub ngày 23/11 trước FLOW-001: PR1–4 còn Draft/open. Nhánh FLOW-001 phụ thuộc #4, rồi #3 → #2 → #1. Chưa merge, chưa nghiệm thu sản phẩm; trạng thái PR/checks có thể đổi sau ngày ghi, kiểm trực tiếp tại PR. GET rulesets private trả403 yêu cầuPro; [giới hạn và điều kiện review/merge](development/review-and-merge.md), không gọi localhook/CI là server enforcement.

## Chưa hoàn tất và việc tiếp theo

| Phần việc | Giới hạn / bước tối thiểu tiếp theo |
| --- | --- |
| Tài liệu và bàn giao | Đã bổ sung bản ghi âm dạng text và bản AGENTS tham khảo; còn các snapshots cũ ngoài Git. DOCS-001 đã thử đọc cùng máy; DOCS-002 thử từ clone GitHub mới. Cả hai không tự chứng minh auto-loading ở chat app hoặc dựng app trên máy mới |
| Quản lý source/cấu hình | Source baseline private đã có; runtime adapters còn local/ignored. [Issue #8 và kế hoạch](development/source-reproduction.md), fresh setup/build/test app chưa thực hiện |
| Hiệu năng/UI | Chưa có A/B và production comparison; chưa sửa F5. Chốt phép đo app-ready và cấu hình đối chứng trước sửa |
| Quy trình thực tế | [Issue #5/quy trình G1–G10](development/product-workflow.md) và tooling mới có phạm vi rõ; chưa chứng minh trọn vòng một feature app. [Pilot #9](development/pilot.md) chờ đủ source/test prerequisites; không tự merge |
| Zalo và mobile | Chưa triển khai connector; cần chốt loại Zalo/API, scope và test toàn tuyến. Mobile chỉ là bản tham khảo, chưa thử cặp tương thích |
| Nâng cấp/hoàn tác | Có các bằng chứng phục hồi trước đây nhưng chưa diễn tập cập nhật toàn bộ code + cấu hình + dữ liệu + uploads. Không nâng runtime trong DOCS-001 |

FLOW-001 chỉ thay control docs/tooling/templates/CI và chia sẻ source app baseline upstream có review kế hoạch. Không đổi code runtime Chatwoot, feature flags, database, container hoặc cấu hình agent hệ thống. Chưa claim product verify/build/UI PASS. Không có số đo tiết kiệm token và không dùng số lượng tài liệu làm bằng chứng chất lượng.
