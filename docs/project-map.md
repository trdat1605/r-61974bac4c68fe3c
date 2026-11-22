# Bản đồ nơi lưu và cách tìm tài liệu

Quyết định dự án ngày **23/11/2026** trong nhiệm vụ [DOCS-001](../tasks/DOCS-001/task.json), bổ sung nguồn/tuyến đọc trong [DOCS-002](../tasks/DOCS-002/task.json). Đây là bố trí áp dụng cho hiện trạng; chưa chứng minh là phương án tối ưu bằng benchmark.

## Bản chính của từng loại thông tin

| Loại thông tin | Nơi dùng làm bản chính | Cách sử dụng / giới hạn |
| --- | --- | --- |
| Điểm bắt đầu | [README gốc](../README.md) của kho riêng tư [trdat1605/chatwoot-vn](https://github.com/trdat1605/chatwoot-vn) | Người có quyền truy cập đọc trên web hoặc clone. Bộ mới ở nhánh `codex/knowledge-handoff`, nối tiếp `codex/docs-home`; chưa có trên main |
| Trạng thái dự án | [status.md](status.md) | Người bàn giao cập nhật khi có kết quả mới, dẫn tới bằng chứng có ngày; không dùng báo cáo cũ như trạng thái hôm nay |
| Danh tính source/runtime | [runtime.json](../config/agents/runtime.json) | Là profile máy hiện có, không là template triển khai. Source app ở Linux; kho tài liệu chưa chứa source app |
| Cách chạy local | [local-development.md](runbooks/local-development.md) | Dùng trên máy hiện có; thiếu adapter local trong Git nên chưa là hướng dẫn cài máy mới |
| Nguồn tham khảo đã thu thập | [Thư viện](knowledge/README.md), [catalog gốc](knowledge/sources.json), [nguồn bổ sung](knowledge/supplemental-sources.json) | Thư viện là cửa tra cứu cho người; catalog giữ metadata. Đã có bản chép lời và AGENTS/license tham khảo, chưa chuyển toàn bộ snapshots |
| Quy trình và nguồn agent | [agents/README.md](agents/README.md), [agents/sources.md](agents/sources.md) | Mở quy trình, brief, phiếu và evidence theo việc; không đồng nghĩa mọi cơ chế Claude đã chạy trên Codex |
| Yêu cầu / phạm vi / kết quả từng việc | `tasks/<id>/task.json`, handoff, review và evidence cùng thư mục | Người thực hiện và reviewer khác nhau; subject commit của review khác commit chứa metadata bàn giao |
| Báo cáo lịch sử | [project-foundation](reviews/project-foundation/README.md), [checkpoint agent ngày 18/11](agents/state.md) | Giữ để truy vết; kết quả mới ghi ở báo cáo có ngày và nối từ trạng thái dự án |
| Bí mật, dữ liệu vận hành, backups | Ngoài Git | Không đính kèm `.env`, khóa, database hoặc log khách hàng vào tài liệu; quyền đọc kho riêng tư không phải quyền đọc bí mật |

GitHub là nơi chia sẻ/lưu lịch sử. Worktree là bản làm việc trên máy, được commit và push qua nhánh/PR. Linux hay Windows là nơi tệp nằm và lệnh thực thi. Đây là các lựa chọn khác nhau: lưu tài liệu trên GitHub không bắt source runtime chuyển khỏi Linux.

## Đọc đúng nguồn theo công việc

Mở [thư viện nguồn](knowledge/README.md) để bấm URL theo ID dưới đây; [reading-routes.md](knowledge/reading-routes.md) ghi cụ thể tài liệu/mục nào cần đọc, lý do và điều kiện mở thêm. Metadata đầy đủ giữ ở [sources.json](knowledge/sources.json). Không cần tải/nạp tất cả. Mục có `source_ref` là commit đã khảo sát; tài liệu web live phải kiểm lại nội dung/phiên bản khi dùng cho thay đổi mới.

| Việc cần làm | Nguồn / công năng |
| --- | --- |
| Hiểu kiến trúc và quy ước Chatwoot | CW-10: production architecture; CW-01: AGENTS đúng commit. Kiến trúc production không tự mô tả cấu hình dev local |
| Sửa backend hoặc frontend | CW-02 / CW-03: guidelines tương ứng; CW-01: lệnh và quy ước. Đọc thêm source thực tại ref của phiếu |
| Host để phát triển trên máy | CW-13: Docker development; CW-11/CW-12: setup; [runbook dự án](runbooks/local-development.md): khác biệt local |
| Triển khai thật / nâng cấp / phục hồi | CW-10/CW-14/CW-15: kiến trúc, upgrade, backup. Chưa diễn tập nâng cấp toàn bộ code+dữ liệu |
| Tích hợp kênh, API, mobile | CW-06/CW-07/CW-22: API và hỗ trợ kênh; CW-08/CW-09/CW-21/CW-29/CW-30: mobile. Không coi bản mobile tham khảo là cặp tương thích đã thử |
| Tổ chức agent và review | [sources.md](agents/sources.md): Subagents, Agent teams, best practices và nguồn có ngày 18/11; TOOL-03/TOOL-04: memory/skills; [quyết định](agents/decisions/0001-agent-operation.md): điều chỉnh riêng của dự án |

Ví dụ muốn đọc cách host: mở [hướng dẫn Docker development chính thức](https://developers.chatwoot.com/contributing-guide/environment-setup/docker), rồi [runbook local](runbooks/local-development.md). Muốn hiểu cách đưa lên môi trường thật thì đọc [production architecture](https://developers.chatwoot.com/self-hosted/deployment/architecture), không áp nguyên cấu hình dev cho khách hàng.

## Tài liệu local cũ và phần còn thiếu

Kho cũ trên máy gốc: `C:/Users/MFLAT-ADS-010/Documents/ChatGPT/tôi/`, gồm `buoc-1/kien-thuc/BAT-DAU.md`, `NGUON.json`, snapshots và hồ sơ thử nghiệm. Đây là **kho lưu lịch sử/cache local**, chưa phải đầu vào portable bắt buộc của repo mới. Không xóa hoặc sửa kho cũ trong nhiệm vụ này.

Đã chuyển danh mục nguồn vào Git và chọn lưu [bản chép lời người dùng](knowledge/user-materials/README.md), [AGENTS upstream](knowledge/references/chatwoot-v4.19.1-AGENTS.txt) cùng license; provenance/hash ở [nguồn bổ sung](knowledge/supplemental-sources.json). Chưa chuyển toàn bộ snapshots. `legacy_local_snapshot` trong catalog là đường dẫn tương đối với kho local cũ, **không** phải liên kết tới tệp có trong repo. Người ở máy khác dùng URL nguồn; nếu cần đúng snapshot chưa được chia sẻ phải bổ sung bản đã làm sạch và kiểm SHA256. Chưa có audio/video gốc của bản chép lời. Nguồn agent ngày 18/11 giữ riêng ngày khảo sát ở `docs/agents/sources.md`, nguồn đọc lại ngày 23/11 ở `source-notes.md`; không gán lùi chúng vào catalog ngày 11/11.

AGENTS ở checkout app cũ còn trỏ vào kho local. Lượt này chưa sửa các chỉ dẫn ấy hoặc kiểm auto-loading từ chat mở riêng tại source app. Điều phối phải truyền lối vào repo/nhánh và brief rõ. Chưa gọi việc hợp nhất tài liệu/đầu vào agent là hoàn tất.

## Giữ bản chính không bị lệch

Người thực hiện thay đổi cập nhật tài liệu đúng chủ đề trong cùng phiếu/PR; reviewer kiểm tài liệu khớp bản bàn giao. Trạng thái dự án chỉ tóm tắt và dẫn đến evidence; chi tiết runtime đặt ở profile/runbook, chi tiết từng phép đo đặt trong báo cáo có ngày. Đổi cấu hình thật sau này phải cập nhật profile và runbook bằng nhiệm vụ có review, không sửa bản lịch sử để che khác biệt. Tài liệu tham khảo tải về không tự thành chỉ dẫn có hiệu lực.

## Căn cứ và điều chỉnh

- [GitHub về README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), đọc 23/11: README là nơi bắt đầu và relative links hoạt động theo nhánh/clone. Áp dụng riêng: chọn README gốc làm cửa vào, giữ chi tiết ở tài liệu theo việc.
- [Docker WSL best practices](https://docs.docker.com/desktop/features/wsl/best-practices/), đọc 23/11: source bind mount nên nằm trong Linux filesystem để có hiệu năng và sự kiện thay đổi tệp. Áp dụng: giữ source runtime hiện tại, không chuyển sang Windows trong nhiệm vụ tài liệu.
- [Claude memory](https://code.claude.com/docs/en/memory) và [Anthropic context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), đọc 23/11: chỉ dẫn có phạm vi, chọn ngữ cảnh phù hợp và tìm thông tin khi cần. Áp dụng riêng: mục lục ngắn và tuyến đọc theo việc; chưa có phép đo hiệu quả/token trên dự án này. Không suy cơ chế nạp Claude sang Codex.
