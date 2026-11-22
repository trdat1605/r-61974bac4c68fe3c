# Đọc theo việc để thực hiện và review

Cập nhật **23/11/2026** từ bảng R-01–R-11 đã lập ngày 11/11. Đây là cách áp dụng riêng cho dự án; giữ ID để nối lịch sử, thay đường dẫn local bằng nguồn dùng được từ clone. Không cần một agent thường trực cho mỗi hàng.

Trước hết đọc AGENTS đang áp dụng, [trạng thái](../status.md) và phiếu việc. Chọn tuyến, đọc mục liên quan rồi source/test đúng ref. [Mục lục nguồn](README.md) cho URL, ref/ngày và công năng; [gói ngữ cảnh](context-packet.md) ghi tuyến đã chọn và lý do. Reviewer tự xét phụ thuộc, không bị danh sách implementer giới hạn.

## R-01

**Backend/service/job.** Bắt đầu [CW-01](README.md#cw-01) General Guidelines/Code Style và [CW-02](README.md#cw-02) Project Structure, Design Principles; Background Jobs nếu sửa job. Mục đích: đặt thay đổi đúng lớp và quy ước. Mở thêm R-02 nếu đổi API, R-03 nếu đổi dữ liệu, R-04 nếu gửi/nhận tin, CW-04 nếu dùng chung enterprise. Đầu ra: source paths/ref, điều kiện lỗi, hành vi mong đợi và checks phù hợp; không đoán retry/idempotency từ tên lớp.

## R-02

**API, quyền và cách ly account.** Đọc [CW-06](README.md#cw-06) loại API liên quan, CW-02 API Design/Security; [CW-26](README.md#cw-26) chỉ làm điểm lần theo đường hội thoại. Mục đích: chọn đúng API và kiểm phạm vi dữ liệu. CW-07 chỉ khi thao tác account/user qua nền tảng; thêm R-05/R-06 nếu client bị ảnh hưởng. Đầu ra: routes/controller/policy thật, payload, ca đúng quyền/sai quyền/cross-account. Ví dụ controller không là kiểm toán toàn hệ thống.

## R-03

**Schema/migration/dữ liệu.** Đọc CW-01 migration/SQL, CW-02 Database/Testing, [CW-04](README.md#cw-04) khi liên quan edition. Mục đích: hiểu đường đọc/ghi và dữ liệu cũ. Mở R-10 khi lập chuyển đổi/khôi phục, R-02/R-06 khi hợp đồng thay đổi. Đầu ra: migration/schema, khóa, thứ tự chuyển đổi và phép kiểm dữ liệu. Hoàn tác commit không tự phục hồi dữ liệu; cần task có quyền runtime, không chạy migration trong nhiệm vụ tài liệu.

## R-04

**Tích hợp kênh/gửi nhận tin.** Đọc CW-06, [CW-22](README.md#cw-22), [CW-27](README.md#cw-27)/[CW-28](README.md#cw-28) làm điểm vào Message/SendReplyJob, rồi lần theo source. Mục đích: xác định hợp đồng kênh và luồng tin. Thêm CW-23 nếu TikTok, R-06 nếu mobile dùng payload, R-07 nếu quyền/cờ bị ảnh hưởng; kênh mới cần tài liệu nhà cung cấp. Đầu ra: API/quyền xác minh, định danh, chữ ký, media, trùng/retry/echo và test toàn tuyến theo scope. Chưa có hợp đồng Zalo OA/cá nhân, Shopee hoặc Lazada được chốt trong kho.

## R-05

**Web/component/nội dung.** Đọc CW-01 Vue/Styling/i18n theo thay đổi và [CW-03](README.md#cw-03) đúng mục. Mục đích: giữ convention frontend hiện tại. Handbook cũ có quy ước khác tag khảo sát: ưu tiên yêu cầu người dùng và AGENTS/convention thực tại ref; không áp máy móc ví dụ frontend cũ. Thêm R-02 nếu đổi payload, R-07 nếu điều kiện tính năng, R-09 khi thử UI. Đầu ra: component/ref, lint/test thích hợp, bằng chứng trình duyệt cho hành vi bị ảnh hưởng. Nhãn UI đơn lẻ không mặc định cần toàn bộ mobile/deployment.

## R-06

**Mobile/realtime/push.** Đọc [CW-08](README.md#cw-08), [CW-21](README.md#cw-21), [CW-29](README.md#cw-29) theo vùng ảnh hưởng. Mục đích: hiểu API/account và cách chạy app mobile. CW-09 chỉ mục push/deep link nếu liên quan; CW-30 khi thêm nhận diện kênh; R-02/R-04 khi hợp đồng đổi. Đầu ra: cặp ref server/mobile, auth/account/realtime và checks theo nền tảng. Mobile v4.10.6 chỉ là mốc tham khảo, chưa thử tương thích. README và env ví dụ cũ từng ghi ngưỡng server khác nhau; phải kiểm source/binary thực, không suy từ một số phiên bản.

## R-07

**Feature flags/edition/quyền dùng tính năng.** Đọc CW-01 Enterprise, CW-04, [CW-16](README.md#cw-16)/[CW-17](README.md#cw-17). Mục đích: truy đủ lớp điều kiện. Mở CW-18 về cấu hình sản phẩm, CW-31 nếu có plan reconciliation; R-02/R-06 theo đường client. Đầu ra: điều kiện code/cờ/quyền/dịch vụ đã kiểm và phần chưa thử. Không bật hàng loạt rồi coi đã nghiệm thu; không dùng tuyến này làm quyền thay edition hoặc runtime ngoài phiếu.

## R-08

**Host/môi trường phát triển.** Mở [runbook local](../runbooks/local-development.md), [profile](../../config/agents/runtime.json) và [CW-13](README.md#cw-13); CW-11/CW-12 theo hệ điều hành, CW-20 theo scripts. Mục đích: thao tác đúng source/engine và lệnh. CW-10 dùng để hiểu production architecture, không thay cấu hình dev. Đầu ra: ref, services, mounts/ports/dữ liệu và checks. Source app cùng adapter chưa nằm trong kho này; clone chưa dựng app trên máy mới. Không chạy start/stop/build nếu task read-only.

## R-09

**Kiểm thử/review/CI.** Đọc yêu cầu/task, [brief reviewer](../../agents/codex/reviewer.md), [workflow](../agents/README.md), CW-01 Build/Test/Lint và vùng code theo tuyến trên. [Bài gốc/ghi chú review](source-notes.md#an-review--bài-gốc-nhóm-claude-code), [bản ghi người dùng](user-materials/README.md) cung cấp căn cứ, không thay source. Mở CW-19 khi E2E web, CW-24/25 khi CI CE/MFA, CW-21 khi mobile. Đầu ra: finding có điều kiện lỗi/ảnh hưởng/file:dòng/căn cứ/cách kiểm; lệnh/output/ref, PASS/FAIL/NOT_RUN và giới hạn. Câu “avoid specs” upstream không bỏ yêu cầu kiểm chứng cần thiết của người dùng. Reviewer khác implementer, review đúng commit; sau ba vòng chưa hội tụ phải xem lại hướng. Phân biệt CI tooling của repo này với test sản phẩm Chatwoot.

## R-10

**Nâng cấp/khôi phục.** Đọc [CW-14](README.md#cw-14)/[CW-15](README.md#cw-15), [review nâng cấp](../reviews/project-foundation/upgrades-and-integrations.md), release notes đúng phiên bản/kiểu triển khai. Mục đích: bảo toàn phần riêng và dữ liệu. Thêm R-03 khi schema đổi, R-06 khi hợp đồng mobile đổi. Đầu ra: delta code/config và mốc image/data/uploads, tiêu chí tương thích và rollback có phép thử. Chưa diễn tập đầy đủ trên dự án; không biến việc tải hướng dẫn thành kết quả đã nâng cấp.

## R-11

**Tổ chức agent/ngữ cảnh/bàn giao.** Đọc [operating-model](../agents/operating-model.md), [source-notes](source-notes.md), [context-packet](context-packet.md) và role brief/phiếu thực tế. Mục đích: giao đủ thông tin, một owner cho một phạm vi và thu đúng bằng chứng. [Claude Subagents/Agent teams](source-notes.md#an-subagents--ngữ-cảnh-và-đầu-vào-được-giao) là nguồn học; công cụ đang dùng là Codex và cấu hình riêng đã mô tả, chưa triển khai Claude Team hoặc Antigravity. Đầu ra: mục tiêu/ref/phạm vi/checks/receiver, quyền đã kiểm, handoff và review đúng bản. Đọc catalog TOOL-xx chỉ khi cần đối chiếu công cụ tương ứng; không nạp mọi nhà cung cấp.

## Khi phát hiện tài liệu thiếu hoặc mâu thuẫn

Không có tuyến phù hợp: tìm nguồn chính thức trước khi đề xuất, ghi thiếu gì và ảnh hưởng; không tự đặt quy ước từ tên tệp. Source phát hiện phụ thuộc mới thì mở rộng đọc và ghi lý do. Handbook/live docs phải đối chiếu ref; pinned snapshot chỉ áp dụng phạm vi đã nêu. Thông tin không có trong clone và URL nguồn phải được đánh dấu cần bàn giao, không lấp bằng suy đoán hoặc nhớ từ chat cũ.
