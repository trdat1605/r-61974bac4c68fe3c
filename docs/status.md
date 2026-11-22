# Trạng thái dự án

Cập nhật khảo sát **23/11/2026, Asia/Saigon**. [Điểm bắt đầu](../README.md), [nơi lưu bản chính](project-map.md). Nội dung này thay vai trò trạng thái tổng thể của các ghi chép trước; không thay kết quả lịch sử tại đúng revision.

## Đã quan sát / đã có bằng chứng

- Source ứng dụng đang chạy: Chatwoot v4.19.1, commit `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, branch `codex/wsl-migration`. Kiểm lại ngày 23/11: HEAD/branch đúng profile và `git status --short` rỗng. Vị trí/môi trường: [profile](../config/agents/runtime.json), [runbook](runbooks/local-development.md).
- Docker Desktop + WSL2, source Linux, chế độ development. Lượt chẩn đoán 23/11 ghi sáu dịch vụ đang chạy và health HTTP200; không phải nghiệm thu đầy đủ ứng dụng.
- [F5 ngày 23/11](reviews/performance/2026-11-23-f5.md): hai lượt load khoảng 13,12s và 11,02s trong trình duyệt đã quan sát, trong khi HTML khoảng 186ms và 161ms. Bằng chứng mạnh chỉ về chờ tải frontend module development trước khi API bắt đầu; chưa cô lập hết nguyên nhân, chưa có đối chiếu production hoặc sửa hiệu năng. Load event không phải thời điểm app dùng được.
- [Báo cáo nền móng 18/11](reviews/project-foundation/README.md) và [checkpoint agent 18/11](agents/state.md) giữ các kết quả đạt/không đạt/NOT_RUN theo ngày và commit. Đã có thử nghiệm giao việc/review/tooling; không suy ra hệ thống sản phẩm ổn định hoặc mọi phiên AI tự đọc đúng.

## Tài liệu dùng chung đang thay đổi

Kho riêng tư `trdat1605/chatwoot-vn` hiện chứa hồ sơ/công cụ, **chưa chứa source ứng dụng**. DOCS-001 thiết lập README, bản đồ, catalog gốc và trạng thái trên `codex/docs-home`; kết quả kiểm/review xem [hồ sơ nhiệm vụ](../tasks/DOCS-001/task.json) và evidence bàn giao khi có. Việc có tệp này không chứng minh kiểm/review đã PASS.

Kiểm GitHub ngày 23/11: [PR #1](https://github.com/trdat1605/chatwoot-vn/pull/1) và [PR #2](https://github.com/trdat1605/chatwoot-vn/pull/2) còn Draft/open. Nhánh docs phụ thuộc #2, #2 phụ thuộc #1. Chưa merge, chưa nghiệm thu sản phẩm; trạng thái PR/checks có thể đổi sau ngày ghi, kiểm trực tiếp tại PR.

## Chưa hoàn tất và việc tiếp theo

| Phần việc | Giới hạn / bước tối thiểu tiếp theo |
| --- | --- |
| Tài liệu và bàn giao | Chưa chia sẻ snapshots cũ/bản ghi âm review qua Git; chưa kiểm auto-loading ở chat app mới. Thử tiếp quản từ README bằng reviewer ngữ cảnh riêng trong DOCS-001; giới hạn và kết quả ghi trong review |
| Quản lý source/cấu hình | Runtime adapters còn local/ignored; clone repo điều phối không tái lập app. Lập việc riêng để quản lý delta không bí mật và source, giữ quy ước upstream |
| Hiệu năng/UI | Chưa có A/B và production comparison; chưa sửa F5. Chốt phép đo app-ready và cấu hình đối chứng trước sửa |
| Quy trình thực tế | Tooling đã có các thử nghiệm lịch sử; chưa chứng minh trọn vòng một feature sản phẩm từ yêu cầu tới nghiệm thu. Không tự bật required checks hoặc merge |
| Zalo và mobile | Chưa triển khai connector; cần chốt loại Zalo/API, scope và test toàn tuyến. Mobile chỉ là bản tham khảo, chưa thử cặp tương thích |
| Nâng cấp/hoàn tác | Có các bằng chứng phục hồi trước đây nhưng chưa diễn tập cập nhật toàn bộ code + cấu hình + dữ liệu + uploads. Không nâng runtime trong DOCS-001 |

Nhiệm vụ hiện tại chỉ sắp xếp lối vào/bản chính tài liệu. Không đổi code Chatwoot, feature flags, database, container hoặc cấu hình agent hệ thống. Không có số đo tiết kiệm token và không dùng số lượng tài liệu làm bằng chứng chất lượng.
