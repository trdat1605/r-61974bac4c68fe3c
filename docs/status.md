# Trạng thái dự án

Cập nhật **23/11/2026, Asia/Saigon**. [Điểm bắt đầu](../README.md), [bản đồ](project-map.md), [công việc COMPLETE-001](development/completion.md). Đây là trạng thái kỹ thuật đang thực hiện trên `codex/complete-foundation`, chưa merge hoặc nghiệm thu toàn bộ bảy mục.

## Hai môi trường cần phân biệt

**Lab hiện có** dùng Chatwoot v4.19.1 tại `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, branch `codex/wsl-migration`, Docker Desktop + WSL2, source Linux, development. [Profile](../config/agents/runtime.json) và [cách chạy](runbooks/local-development.md). COMPLETE-001 giữ lab Chatwoot và website khóa học ở phạm vi chỉ đọc, không đổi code/runtime/dữ liệu của hai ứng dụng này.

**Môi trường thử COMPLETE-001** dùng clone/worktree và nhánh app `codex/portable-foundation` riêng. [App task](../tasks/COMPLETE-001/evidence/app-task.json) giữ SHA hiện hành. [Draft app PR3](https://github.com/trdat1605/s-251521f7e9131fb0/pull/3) sửa lỗi Docker build từ linked worktree và cung cấp bootstrap/CI tách biệt. Nó chưa được đưa vào lab hoặc main. Không dùng control commit làm app commit.

## Bằng chứng đã có và giới hạn

- Regression Docker thực: baseline upstream lỗi Git metadata, bản sửa PASS. Full development image build đã PASS tại `0768677`; đó không phải bằng chứng build ở mọi commit sau. [Các receipt](../tasks/COMPLETE-001/evidence/) giữ cả lỗi và giới hạn.
- Runtime thử local lần đầu FAIL vì Vite đợi cài dependency tương tác. Có sửa và review riêng; không đổi FAIL cũ thành PASS. Do C dưới ngưỡng 15 GiB, không tạo thêm runtime local. Chỉ tài nguyên tổng hợp do task tạo đã được dọn sau backup/review; Postgres volume thử vẫn giữ. Chín container được bảo vệ giữ nguyên identity/start time tại lần đối chiếu.
- CI ứng dụng đã chạy metadata và focused frontend thật; lifecycle build/setup/test/restart/restore trên runner dùng một lần đã PASS tại apphead27e1669, mergecheckout8d953fd có tree giống hệt. Xem đúng run/SHA trong [completion](development/completion.md), không suy từ CI cũ.
- Bộ công cụ điều phối local: 80 unit tests PASS; đây là test fixtures của tooling, không chứng minh sản phẩm Chatwoot ổn định.
- Phép so sánh Codex theo protocol V3 đã đủ 12 lượt, có chấm độc lập và second check (5 PASS, 7 fail/partial); coordinator-routed và peer đều là cơ chế Codex hiện có. Claude Agent Teams NOT_RUN theo phạm vi người dùng đã xác nhận. Giữ lựa chọn tạm và cải thiện brief sau các lỗi thực; chưa có kết luận mô hình tối ưu hoặc số đo tiết kiệm token.
- [F5 ngày 23/11](reviews/performance/2026-11-23-f5.md): hai lượt load khoảng 13,12s/11,02s; HTML khoảng 186ms/161ms. Chờ module development trước khi API bắt đầu là quan sát, chưa cô lập mọi nguyên nhân hoặc có production comparison. Load event không đồng nghĩa app dùng được. Chưa sửa hiệu năng F5.

## Quản trị và nơi lưu kết quả

Hai kho [control](https://github.com/trdat1605/r-61974bac4c68fe3c) và [app](https://github.com/trdat1605/s-251521f7e9131fb0) công khai theo PUB-001. Tên ngẫu nhiên không giữ bí mật. Control chứa tài liệu/cấu hình/công cụ/bằng chứng sạch; app chứa source ứng dụng. Secrets, dumps và dữ liệu khách hàng không đưa vào Git.

GOV-001 đã bật rules yêu cầu PR, chặn deletion/non-fast-forward trên main hai kho; control có hai required jobs. [Bằng chứng quản trị](development/branch-protection.md) bao gồm phép thử fail → blocked, pass → clean; chưa merge thật, agent review không là GitHub human approval. COMPLETE-001 đã bổ sung CI app và ba required checks sau review, tắt toàn bộ 17 workflow kế thừa; chỉ workflow đã review được bật với action allowlist và token đọc. Xem receipt hiện hành thay vì dùng trạng thái Actions-disabled lịch sử.

Main control còn gần bản khởi tạo; bộ tài liệu mới nằm trên nhánh làm việc và PR stack chưa merge. PR tích hợp phải giữ ancestry của reviews bằng merge commit. Không coi file templates có trên nhánh là đã active trên default branch.

## Việc còn mở

| Phần | Bước cần hoàn tất |
| --- | --- |
| Bảy cải tiến | Theo [tracker](development/improvement-tracker.md), eval và lifecycle CI đã có kết quả; còn source handover tổng thể và final exact-commit control review; chuẩn bị PR để owner quyết định |
| Dung lượng Docker | [Phương án sang D](runbooks/docker-storage-migration.md) đã có review vòng đầu; execution BLOCKED vì cần backup/capacity/maintenance/rollback/postchecks cụ thể. Chưa chuyển hoặc restart Docker |
| Giao diện/hiệu năng | Chưa kiểm đầy đủ thao tác trình duyệt ở môi trường mới; chưa có production comparison |
| Zalo/mobile | Chưa triển khai connector hoặc kiểm cặp tương thích mobile; cần task/API/scope riêng |
| Nâng cấp | Diễn tập dữ liệu tổng hợp không thay thử nâng Chatwoot cùng code/config/dữ liệu/uploads thật |
| Nghiệm thu | Owner quyết định theo PR/SHA cụ thể sau checks/review; chưa merge/phát hành hoặc chấp nhận nghiệp vụ |

Hồ sơ nền móng [18/11](reviews/project-foundation/README.md), [agent state lịch sử](agents/state.md) và tasks AGENT/DOCS/FLOW/PUB/GOV giữ nguyên theo revision. Nội dung lịch sử không thay trạng thái hiện hành; không sửa receipt cũ để làm xanh.
