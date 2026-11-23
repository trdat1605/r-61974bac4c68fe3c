# Nâng cấp Chatwoot, Zalo và mobile

Ngày: **18/11/2026, UTC+07**. Server được khảo sát: v4.19.1 / `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, local branch `codex/wsl-migration`. Commit báo cáo xem Git/PR của kho private, không phải source pin. [README](README.md) · [Bằng chứng](evidence.md).

## Nhận upstream và phục hồi

**Quan sát E01/E07:** giữ upstream history/tag, 0 private feature commits; có rollback artifacts và isolated restore trước migration, rồi restore sang Desktop. Hồ sơ 17/11 so public tables/canonical checksums và một số sequence fields; Redis logical values/absolute expiry, restart persistence trước app writers. Chưa replay globals ACL; không có upload blob thật; chưa diễn tập quay lại Engine cũ. Đây không là lần nâng cấp Chatwoot.

**Nguồn chính thức:** [Upgrade](https://developers.chatwoot.com/self-hosted/deployment/upgrade) yêu cầu đối chiếu release notes và quy trình của hình thức triển khai; [Backup](https://developers.chatwoot.com/self-hosted/deployment/backup) bao gồm dữ liệu/storage/config/custom code. Là docs live18/11, chưa có snapshot gắn riêngv4.19.1. Không chuyển các lệnh chuẩn bị DB/reset development thành thao tác an toàn cho mọi dữ liệu.

**Kế hoạch có điều kiện, chưa thực thi:**

1. Chọn target release và commit, đọc release notes/migrations/toolchain; so delta source, Dockerfile copies, config và dependencies.
2. Xác định tiêu chí tương thích phần riêng/API/mobile và các luồng nghiệp vụ cần regression. Hiện chưa có feature connector để đánh giá diff.
3. Giữ source/config/image identities và backup nhất quán DB/Redis/uploads/cấu hình cần thiết bằng quy trình đã review; secrets không vào Git. Xác định ai có quyền khôi phục và RPO/RTO được người dùng chấp nhận.
4. Thử trên môi trường riêng, dữ liệu mẫu phù hợp, không dùng chung project/ports/DB/Redis hiện tại một cách ngầm định.
5. Kiểm app/worker/assets/API/integrations/mobile theo ảnh hưởng; kiểm migration và uploads; review đúng ref/config.
6. Diễn tập rollback cả code/image/config và dữ liệu. Đổi image về bản cũ không tự đảo schema/data migration; không hứa rollback không mất dữ liệu trước phép thử.

Đây là điều chỉnh tối thiểu đề xuất dựa trên hướng dẫn/source và khoảng trống thực tế, không phải tuyên bố đã có enterprise pipeline. Không merge/rebase/pull/upgrade/restore runtime trong nhiệm vụ báo cáo.

### Điểm làm nâng cấp khó hơn

- Local Dockerfiles copy upstream có delta nhỏ nhưng toàn file không tự nhận sửa bảo mật/build mới.
- Configuration adapters ignored và dependency volumes chưa đủ version history để tái lập.
- BUNDLE_PATH=/gems khác volume /usr/local/bundle; runtime additions có lifecycle riêng mỗi container.
- Vite cache/node_modules có thể che nội dung image; thay image không tự bảo đảm dependencies cache khớp lockfile.
- Chưa có connector feature code, nên chưa có bằng chứng coupling thực tế hoặc phần riêng đã tách thành công.
- Tài liệu cũ/current có status drift, dễ chọn nhầm hướng upgrade/runbook.

## Zalo: mục tiêu có, thiết kế chưa chốt

**Mục tiêu người dùng:** phát triển sản phẩm Việt Nam, tích hợp Zalo và ưu tiên tách phần tích hợp để dễ nhận Chatwoot updates. Mục tiêu không tự là quyết định đã thực hiện.

**Quan sát E09:** hồ sơ01 §5.4/7 và backlog TH-02/03/06 ghi API-channel/webhook hoặc native là hai hướng; G-03 còn mở. Chưa tìm thấy repo connector/code tùy chỉnh hoặc acceptance đã chốt trong phạm vi source và hồ sơ đã khảo sát. Không suy tài khoản Zalo cá nhân có hợp đồng API được hỗ trợ chỉ vì có thư viện cộng đồng.

[API inbox của Chatwoot](https://www.chatwoot.com/hc/user-guide/articles/1677839703-how-to-create-an-api-channel-inbox) mô tả contact/conversation/message và callback. [Channel support](https://developers.chatwoot.com/self-hosted/supported-features) là khả năng Chatwoot công bố, không chứng minh bridge Zalo hoặc kênh marketplace cụ thể.

**Suy luận để review:** API channel có thể giảm nhu cầu sửa luồng core nếu hợp đồng nghiệp vụ ánh xạ đủ. Nếu thiếu media/status/identity/delivery/retry cần thiết, phải phân tích extension points hoặc native; chưa chọn phương án chính trước khi khảo sát hợp đồng Zalo. Việc tạo một repo riêng không chứng minh đã tách coupling.

**Cần trước khi code:** chốt OA/cá nhân, quyền và tài liệu API chính thức áp dụng; mapping contact/conversation/message, idempotency/order/retry/error, media và trạng thái; đường callback trong dev; tiêu chí user chấp nhận. Không mở port, xin/gửi tokens, tạo bridge hoặc gửi tin thật ở lượt này.

## Mobile chính thức

Repo: [chatwoot-mobile-app](https://github.com/chatwoot/chatwoot-mobile-app), React Native + Expo. Mốc nghiên cứu cũ v4.10.6 commit `a7b5deb2db6a3cb13a6c72205d53079ee89e4611`; latest repo khi khảo sát 18/11 là [v4.11.4](https://github.com/chatwoot/chatwoot-mobile-app/releases/tag/v4.11.4), commit `cbfad0be59aba1f94a1fdda7ebc9885dfbeb80f0`, release 16/11. Không update/build/cài mobile trong nhiệm vụ này.

| Điều đã đọc | Nguồn cố định / giới hạn |
| --- | --- |
| REST API/auth và account routes | [APIService v4.10.6](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/src/services/APIService.ts), [authService](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/src/store/auth/authService.ts) |
| ActionCable/events | [base connector](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/src/utils/baseActionCableConnector.ts), [events](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/src/utils/actionCable.ts) |
| HTTPS/WSS | [URL constants latest surveyed](https://github.com/chatwoot/chatwoot-mobile-app/blob/cbfad0be59aba1f94a1fdda7ebc9885dfbeb80f0/src/constants/url.js), [settingsUtils](https://github.com/chatwoot/chatwoot-mobile-app/blob/cbfad0be59aba1f94a1fdda7ebc9885dfbeb80f0/src/store/settings/settingsUtils.ts) |
| Minimum version không đồng nhất | README ghi server 3.13.0+; [.env.example](https://github.com/chatwoot/chatwoot-mobile-app/blob/cbfad0be59aba1f94a1fdda7ebc9885dfbeb80f0/.env.example) ghi minimum 4.1.0; không suy env binary store từ template |
| Store | [App Store](https://apps.apple.com/us/app/chatwoot/id1495796682) lúc khảo sát hiện 4.11.4 / iOS 16.4+; README cũ nói13.4+ nên không dùng README làm yêu cầu cài hiện tại. [Google Play](https://play.google.com/store/apps/details?id=com.chatwoot.app&hl=en) cập nhật 16/11, output chưa có version/minAndroid |

Server4.19.1 cao hơn hai minimum đã thấy nhưng không chứng minh cặp mobile nào tương thích mọi chức năng. Cặpv4.10.6 và v4.11.4 với server lab đều NOT_RUN.

### App chính thức khác custom build

[Custom mobile guide](https://developers.chatwoot.com/self-hosted/custom-mobile-app) mô tả relay cho official app và Firebase/directFCM cho custom build, cần nhận diện app/config/build/phân phối. Không mặc định phải custom-build vì server self-hosted. [Server push source pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/services/notification/push_notification_service.rb) chọn direct hoặc relay theo cấu hình và preferences; đây là đọc source, chưa xác minh effective push config hay thiết bị.

### Đường mạng và các phép thử còn thiếu

Ports hiện publish127.0.0.1. Localhost trên điện thoại là chính điện thoại; chưa có endpoint từ điện thoại vào PC được kiểm. [Docker publishing](https://docs.docker.com/engine/network/port-publishing/) mô tả loopback binding. Cần đường mạng thực, HTTPS được thiết bị tin cậy và WSS/cable; không mặc định public Vite/Mailhog. Chưa mở firewall, bindLAN/tunnel/certificate.

Trước khi cam kết Zalo trên mobile: inbound đúng inbox/identity/order/idempotency; outbound tới Zalo thực nhận; private note không ra ngoài; media URLs truy cập được; status/error/retry; foreground realtime, reconnect/background; push đúng agent và deep link đúng hội thoại. Toàn bộ end-to-end mobile/Zalo NOT_RUN. Handshake101 trên browser không thay các phép thử này.
