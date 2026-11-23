# Review hiện trạng và nền móng dự án Chatwoot

Ngày khảo sát: **18/11/2026, Asia/Ho_Chi_Minh (UTC+07)**. Báo cáo phục vụ review độc lập, chưa phải quyết định triển khai hoặc nghiệm thu sản phẩm.

> Hiện trạng: Chatwoot đang chạy theo mô hình development trên Docker Desktop + WSL2, với source nằm trong filesystem Linux. Bố trí này phù hợp cho phát triển, nhưng quản lý cấu hình, tài liệu và quy trình nhận cập nhật còn thiếu. Giao diện vẫn tải chậm dù HTML/API phản hồi tương đối nhanh.

Phạm vi của câu trên: các endpoint và trình duyệt đã đo, không phải mọi API hoặc mọi trình duyệt. Chưa xác định nguyên nhân gốc của độ chậm.

## Hai repository và hai loại commit

| Đối tượng | Repository / nhánh / mốc |
| --- | --- |
| Source ứng dụng được khảo sát | `https://github.com/chatwoot/chatwoot`, tag `v4.19.1`, commit `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82` |
| Checkout ứng dụng đang chạy | `/root/code/chatwoot-worktrees/wsl-preflight`, nhánh `codex/wsl-migration` |
| Kho nhận bộ báo cáo | `https://github.com/trdat1605/chatwoot-vn`, **private**, nhánh `review/project-foundation` |
| Commit chứa báo cáo | Xác định bằng commit của nhánh/PR này và lịch sử Git; không dùng commit Chatwoot phía trên làm commit báo cáo |
| Nhánh main của kho báo cáo | Chỉ có commit khởi tạo rỗng làm base cho Draft PR; không có mã ứng dụng hoặc bộ báo cáo trên main tại bàn giao |

Kho riêng tư được tạo theo ủy quyền của người dùng trong lượt này. Đây là kho mới chứa báo cáo; chưa phải fork/mirror có source ứng dụng, chưa thay remote của checkout chạy thật. Không push mã Chatwoot hay dữ liệu runtime để dựng base cho PR.

## Đọc theo công việc

1. [Môi trường local](local-environment.md): máy, Docker/WSL, source, mounts, image IDs, đo tốc độ và giới hạn.
2. [Nền móng phát triển](development-foundation.md): cấu trúc, quản lý thay đổi, tài liệu, bàn giao AI và quy trình.
3. [Nâng cấp và tích hợp](upgrades-and-integrations.md): nhận upstream, rollback, Zalo và mobile.
4. [Bằng chứng](evidence.md): ID bằng chứng, nguồn cố định, lệnh chọn lọc, kết quả không đạt và NOT_RUN.

Không cần nạp cả bộ vào context cho mọi nhiệm vụ: đọc trang này, chọn báo cáo liên quan, rồi mở bằng chứng/nguồn cần dùng. Đây là hướng dẫn đọc bộ review, không thay runbook vận hành hoặc AGENTS của ứng dụng.

## Bảng bàn giao tám tiêu chí

Các trạng thái áp dụng đúng phạm vi chứng cứ; không cộng thành điểm chất lượng tổng.

| Tiêu chí | Đạt/Một phần/Chưa đạt/Chưa đủ bằng chứng | Bằng chứng cụ thể | Hậu quả | Đề xuất tối thiểu |
| --- | --- | --- | --- | --- |
| 1. Cấu trúc code | **Đạt** trong phạm vi lõi chưa sửa | E01: HEAD đúng pin, Git sạch, 0 commit riêng; S01 quy ước upstream; E08 local Dockerfiles nằm .codex | Giữ cấu trúc gốc; chưa có feature diff để đánh giá chất lượng code tùy chỉnh | Tiếp tục theo cấu trúc và extension points upstream; quản lý các delta local có phiên bản |
| 2. Ranh giới mở rộng | **Chưa đủ bằng chứng** | E09: API channel/native mới là hướng khảo sát; chưa tìm thấy connector hoặc feature code trong phạm vi đã kiểm; S02 | Chưa thể nói tách Zalo đã thành công hoặc dễ nâng cấp | Chốt loại Zalo, hợp đồng API, tiêu chí toàn tuyến và bản quyết định trước code |
| 3. Quản lý thay đổi | **Một phần** | E01 có pin/branch; E07 có hash/receipts; E08 cấu hình bị ignore; E10 hồ sơ chưa commit | Nhận diện được runtime hiện tại nhưng chưa tái lập toàn bộ bằng clone repo | Version-control cấu hình không bí mật, lý do và phép kiểm tra; giữ secrets ngoài Git |
| 4. Chất lượng tài liệu | **Một phần** | E10 có BAT-DAU/index/decision log; nhiều trạng thái 11/11 đã cũ; báo cáo 17/11 còn dòng đang review | Có đầu mối, nhưng dễ chọn nhầm trạng thái hoặc runbook | Chỉ định bản hiện hành, gắn nhãn lịch sử và cập nhật trạng thái ở lượt được phép |
| 5. Bàn giao AI khác | **Một phần** | E10 có AGENTS/override, mục tiêu, runbook, review; E01 chat cwd Windows khác source Linux | AI trên cùng máy có thể tiếp tục khi chọn đúng tài liệu; clone kho báo cáo trên máy mới chưa đủ | Bàn giao đúng source/ref, đường chạy, scope sửa, test, next task và quyền cần có |
| 6. Quy trình phát triển | **Một phần** | E07 thực có review trước từng pha và kết quả; E11 có tests lịch sử; chưa có luồng feature PR/required checks | Đã thử quản lý thay đổi môi trường; chưa chứng minh quy trình phần mềm đầu-cuối | Thực nghiệm một thay đổi nhỏ được chốt yêu cầu với branch/test/review/chấp nhận |
| 7. Bảo trì và nâng cấp | **Một phần** | E07 có isolated restore/data restore; E09 hướng BT-01–04; chưa diễn tập nâng cấp/rollback đầy đủ | Chưa cam kết nhận bản mới không lỗi hoặc hoàn tác đủ code+dữ liệu | Thử nâng cấp trong môi trường riêng với bản sao dữ liệu đã làm sạch và tiêu chí rollback |
| 8. Nguy cơ lãng phí công sức/token | **Một phần** về khả năng tìm và dùng lại kiến thức | E10 index theo việc đã có; status drift và source/config ngoài Git gây tìm lại; S01 AGENTS/CLAUDE giống nhau từ upstream | Có nguy cơ đọc lại/suy lại hoặc theo hướng dẫn cũ; chưa đo chi phí | Dùng một điểm bắt đầu và trạng thái chuẩn; không tự xóa duplication upstream; không ước lượng token tiết kiệm |

## Kết luận để người review quyết định

**Đã phù hợp:** lựa chọn development có tài liệu chính thức; source bind từ ext4; có web/worker/data/frontend dev server; pin, image IDs và lịch sử kiểm tra có thể đối chiếu; lõi ứng dụng chưa có delta riêng.

**Cần xử lý trước khi phát triển Zalo:** chốt Zalo OA/cá nhân và khả năng API có căn cứ; chọn ranh giới tích hợp sau khi khảo sát hợp đồng; ghi yêu cầu/tiêu chí nghiệm thu; chọn đúng checkout; quản lý cấu hình và quyết định không bí mật bằng Git; chốt cách test toàn tuyến/không gửi private note ra ngoài. Quyền và tài khoản dịch vụ do người dùng cấp qua cơ chế an toàn, không ghi vào báo cáo.

**Có thể để sau trong phạm vi tìm hiểu local:** custom mobile build, production HA/capacity, sơ đồ nhiều agent thường trực. Cần đưa trở lại kế hoạch trước khi nhận khách hàng hoặc cam kết chức năng tương ứng. Không bắt buộc custom mobile chỉ để bắt đầu Zalo.

**Cần review thêm:** nguyên nhân UI chậm; build/recreate dependencies; thử HMR thật; khả năng tương thích connector/mobile; upgrade/rollback bao gồm uploads, schema, ACL và globals; hiệu lực CI/branch protection. Không coi số lượng thư mục, báo cáo hoặc agent là chứng minh các mục này đạt.

## Nhãn bằng chứng và giới hạn

- **Quan sát:** kiểm trực tiếp hoặc đọc artifact xác định; ghi ngày và phạm vi.
- **Suy luận:** kết luận có điều kiện từ source/cơ chế, chưa thay cho phép chạy.
- **Đề xuất:** hành động tối thiểu cho lượt sau, chưa áp dụng vào ứng dụng.
- **Chưa xác minh / NOT_RUN:** thiếu phép thử hoặc quyền/dữ kiện.

Bộ review chỉ thêm năm báo cáo Markdown. Không chứa env, token, dump DB, uploads, screenshots, log thô hay script thao tác runtime. Các chi tiết khách hàng/nội dung hội thoại được loại bỏ. Bằng chứng lịch sử không bị đổi thành kiểm thử mới. Xem [evidence.md](evidence.md) để biết phần nào chỉ có số liệu từ cuộc chat và chưa có trace gốc đi kèm.
