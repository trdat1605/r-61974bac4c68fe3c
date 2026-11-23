# Chatwoot Việt Nam — bắt đầu ở đây

Kho GitHub **công khai** này là nơi dùng chung để quản lý tài liệu dự án, cấu hình không bí mật và công cụ điều phối agent. Source ứng dụng đang chạy vẫn ở Linux, được nhận diện trong [profile runtime](config/agents/runtime.json). Clone kho này **chưa đủ** để dựng lại Chatwoot trên máy mới.

| Anh muốn biết gì? | Mở tài liệu nào? |
| --- | --- |
| Đã làm tới đâu, còn việc gì? | [Trạng thái dự án](docs/status.md) |
| Tài liệu, code và dữ liệu nằm đâu; bản nào là bản chính? | [Bản đồ dự án](docs/project-map.md) |
| Chạy và kiểm tra Chatwoot trên máy hiện có | [Hướng dẫn local development](docs/runbooks/local-development.md) |
| Tìm tài liệu gốc Chatwoot: kiến trúc, backend, frontend, host, mobile | [Thư viện nguồn có thể bấm đọc](docs/knowledge/README.md); [tuyến đọc theo việc](docs/knowledge/reading-routes.md) |
| Tìm lại đoạn chia sẻ cách tin tưởng code AI | [Bản ghi dạng text và nguồn bài gốc](docs/knowledge/user-materials/README.md) |
| Giao việc, quản lý agent và review code | [Lối vào agent](docs/agents/README.md) và [nguồn khảo sát agent/review](docs/agents/sources.md) |
| Bảy cải tiến và luồng issue → task → PR → merge/phát hành | [Theo dõi cải tiến](docs/development/improvement-tracker.md), [quy trình sản phẩm](docs/development/product-workflow.md) |
| Source ứng dụng dùng chung và việc dựng lại môi trường | [Source/reproduction](docs/development/source-reproduction.md); kho ứng dụng riêng, chưa dựng app chỉ từ clone |
| Đọc đánh giá nền móng và phép đo F5 | [Review ngày 18/11](docs/reviews/project-foundation/README.md), [chẩn đoán F5 ngày 23/11](docs/reviews/performance/2026-11-23-f5.md) |

**Công việc hiện hành:** [COMPLETE-001 — hoàn thiện bảy cải tiến](docs/development/completion.md), nhánh `codex/complete-foundation`, [issue18](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/18). [App Draft PR3](https://github.com/trdat1605/s-251521f7e9131fb0/pull/3) ở repo source riêng; main hai kho chưa nhận thay đổi này.

[Bảo vệ nhánh](docs/development/branch-protection.md), [quyết định công khai](docs/development/repository-publication.md) và các tasks/PR trước giữ lịch sử. Bộ mới nối tiếp GOV/PUB/FLOW/DOCS; chưa merge. Chọn đúng nhánh khi đọc trên GitHub. [Phương án chuyển Docker data sang D](docs/runbooks/docker-storage-migration.md) chỉ chuẩn bị/review, chưa thực hiện.

AI đọc [AGENTS.md](AGENTS.md), trang này và tuyến liên quan đến phiếu việc; mở nguồn/bằng chứng chi tiết khi cần. Không nạp toàn bộ kho vào mọi nhiệm vụ. Chưa có phép đo chứng minh tiết kiệm token. Không lưu thông tin đăng nhập, dữ liệu khách hàng hoặc bản sao database trong Git.
