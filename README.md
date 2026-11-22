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

**Đổi tên/công khai:** xem [PUB-001](docs/development/repository-publication.md). Kho điều phối và app công khai; tên ngẫu nhiên không giữ bí mật. Bản mới đang ở `codex/repository-publication`, Draft PR dựa trên `codex/product-foundation`; chưa merge.

Nền trước đó là `FLOW-001` trên nhánh `codex/product-foundation`, liên kết [issue #5](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/5), nối tiếp [Draft PR #4 — DOCS-002](https://github.com/trdat1605/r-61974bac4c68fe3c/pull/4), rồi [PR #3](https://github.com/trdat1605/r-61974bac4c68fe3c/pull/3), [PR #2](https://github.com/trdat1605/r-61974bac4c68fe3c/pull/2), [PR #1](https://github.com/trdat1605/r-61974bac4c68fe3c/pull/1). Chưa merge; muốn đọc bộ mới hãy chọn đúng nhánh. Không coi nội dung trên nhánh này đã được chấp nhận trên `main`.

AI đọc [AGENTS.md](AGENTS.md), trang này và tuyến liên quan đến phiếu việc; mở nguồn/bằng chứng chi tiết khi cần. Không nạp toàn bộ kho vào mọi nhiệm vụ. Chưa có phép đo chứng minh tiết kiệm token. Không lưu thông tin đăng nhập, dữ liệu khách hàng hoặc bản sao database trong Git.
