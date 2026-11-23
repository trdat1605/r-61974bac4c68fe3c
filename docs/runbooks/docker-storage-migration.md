# Phương án chuyển dữ liệu Docker Desktop sang D

Ngày 23/11/2026. **Chỉ là kế hoạch, chưa áp dụng.** Chủ sản phẩm yêu cầu chuẩn bị và review trước khi thực hiện. Không thay đổi Docker Desktop hoặc dừng ứng dụng trong bước khảo sát này.

## Hiện trạng quan sát

- Docker Desktop Windows 4.99.0.245822, WSL2, engine 29.9.3.
- Data VHD ở `C:/Users/MFLAT-ADS-010/AppData/Local/Docker/wsl/disk/docker_data.vhdx`, khoảng 26,9 GiB tại lần đo. Tệp `main/ext4.vhdx` khoảng 0,09 GiB là thành phần khác.
- C còn khoảng 14,9 GiB, D còn khoảng 72 GiB tại lần khảo sát; phải đo lại trước thực hiện.
- Chín container Chatwoot và website khóa học cần được bảo toàn. [Inventory](../../tasks/COMPLETE-001/evidence/docker-storage-inventory.json) chỉ chứa thông tin không bí mật.

## Căn cứ và phương án chính

[Docker WSL backend](https://docs.docker.com/desktop/features/wsl/) chỉ dẫn đổi vị trí dữ liệu qua Settings → Resources → Advanced. Ưu tiên chức năng Disk image location của Docker Desktop. Trang [settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/) có bảng platform chưa liệt kê WSL2 ở dòng này; cần kiểm UI thật của bản đang dùng trước khi chốt khả năng hỗ trợ.

Đích dự kiến là thư mục mới, rỗng `D:/DockerDesktopData/`. Cần xác minh filesystem, quyền, đường tuyệt đối, dung lượng và không có VHD khác tại đó. Đây chưa phải quyết định đã di chuyển dữ liệu.

## Kiểm tra bổ sung đã thực hiện

UI bản 4.99.0 hiển thị **Settings → VM resources → Disk image location**, backend
WSL 2, vị trí hiện hành trên C, nút Browse và trạng thái **No unsaved changes**.
Đây là tên mục trong UI mới; đường dẫn Resources → Advanced ở tài liệu là giao
diện tài liệu mô tả. Chưa chọn thư mục, chưa Apply. [Receipt UI](../../tasks/COMPLETE-001/evidence/docker-storage-ui.json).

[Metadata mounts](../../tasks/COMPLETE-001/evidence/docker-storage-mounts.json)
phân biệt named/anonymous volumes với bind mounts. Đặc biệt Postgres Chatwoot có
cả `/data/postgres` và `/var/lib/postgresql/data`: chưa được phép đoán volume nào
chứa dữ liệu đang dùng. Nhiệm vụ backup phải xác định PGDATA thực trước khi chọn
nguồn. Khóa Google, video và các bind source của website khóa học nằm ngoài VHD;
chuyển VHD không sao lưu hoặc di chuyển chúng. Source Ubuntu cũng tách khỏi VHD này.

## Các cổng cần đạt trước và sau thực hiện

1. Inventory container/image/volume/bind paths và các kiểm tra ứng dụng trước thay đổi; không in môi trường hoặc bí mật.
2. Backup nhất quán Postgres, Redis, uploads và cấu hình của cả hai ứng dụng trong nhiệm vụ bảo trì riêng. Backup dữ liệu tổng hợp COMPLETE-001 không thay thế backup ứng dụng đang dùng.
3. Reviewer xác nhận đủ dung lượng cho dữ liệu đích và backup, phương án khôi phục và phạm vi gián đoạn. Chủ sản phẩm quyết định cửa sổ bảo trì với ảnh hưởng cụ thể.
4. Dùng chức năng UI được hỗ trợ để thay vị trí sau khi thực hiện các bước dừng nhất quán theo hướng dẫn chính thức. [Docker backup](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) yêu cầu Desktop dừng hẳn khi sao lưu data VHD.
5. Sau chuyển: đối chiếu vị trí, backend, image/container/volume, bind paths, source SHA và kiểm tra DB/uploads/login cùng chức năng liên quan của cả hai ứng dụng.
6. Giữ bản backup và nguồn cũ đến khi kiểm chứng khôi phục và nghiệm thu. Nếu UI không hỗ trợ hoặc dữ liệu đích xung đột, dừng để khảo sát lại, không tự thay cơ chế lưu trữ.

## Khôi phục và giới hạn

Phương án chi tiết cần chỉ rõ bản dữ liệu tốt để quay lại qua cơ chế Docker hỗ trợ, điều kiện dừng và cách kiểm sau khôi phục. Không cho hai bản database cùng nhận ghi trong lúc xác minh.

Chuyển Docker data không tự chuyển distro Ubuntu hoặc source trong Linux. Docker yêu cầu backup các distro riêng khi cần. Chưa đo hiệu năng sau chuyển; không kết luận ổ D nhanh hơn C.

**Trước áp dụng:** cần review độc lập, xác minh UI/đích thực, backup hai ứng dụng và quyết định cửa sổ gián đoạn. Kế hoạch này chưa cho phép tự khởi động lại Docker Desktop hoặc thay đổi dữ liệu đang chạy.

## Kết quả review và bảng chuẩn bị bảo trì

[Review vòng 1](../../tasks/COMPLETE-001/evidence/docker-storage-plan-review.json)
đã kiểm bản kế hoạch theo SHA256 và kết luận **BLOCKED_FOR_EXECUTION**, gồm năm
thiếu sót về backup, ngân sách dung lượng, cửa sổ bảo trì, rollback và postchecks.
Bổ sung UI/mounts ở trên chưa tự giải quyết các thiếu sót đó. Kế hoạch này là hồ sơ
chuẩn bị được review, **chưa là runbook có thể chạy**. Không yêu cầu người dùng phê
duyệt di chuyển khi chưa có đủ đầu vào dưới đây.

| Hạng mục | Quyết định chuẩn bị / thông tin phải hoàn tất trước khi chạy |
| --- | --- |
| Người thao tác | Một runtime owner của nhiệm vụ bảo trì mới, reviewer khác; không cho agent eval hoặc implementer app tự restart Docker |
| Dữ liệu cần bảo toàn | Hai Postgres; Redis/queue Chatwoot; uploads/storage; source/config/secrets riêng tư; video và khóa Google ngoài VHD. Chọn nguồn theo mounts và PGDATA thực, không chỉ theo tên volume |
| Backup | Backup nhất quán khi đã chặn ghi ứng dụng/worker; dump DB và manifest/hash lưu riêng tư ngoài Git. Sau khi Desktop dừng hẳn, sao chép/hash VHD offline đến thư mục backup riêng, không đặt trong thư mục đích đang chuyển |
| Kiểm backup | Restore logical DB vào môi trường cách ly đã được cấp quyền, đối chiếu dữ liệu tổng hợp/quan hệ và uploads; kiểm VHD backup theo quy trình phục hồi được hỗ trợ. Backup COMPLETE-001 không thay backup hai ứng dụng |
| Dung lượng | [Số đo bytes](../../tasks/COMPLETE-001/evidence/docker-storage-capacity.json): hai lần chiều dài VHD chỉ là ngân sách thô cho một backup và một đích. Cộng backup ứng dụng, chỗ copy tạm, phục hồi và dự phòng tăng trưởng; chưa xác định đủ các số này nên chưa kết luận D đủ. Không tạo đích/copy thử khi chưa đạt |
| Cửa sổ gián đoạn | Chốt giờ bắt đầu, hạn abort và thời gian phục hồi sau khi đo tốc độ copy/restore. Cả Chatwoot và website khóa học sẽ gián đoạn; hiện chưa có số đo để cam kết số phút |
| Dừng/khởi động | Nhiệm vụ bảo trì phải chỉ rõ cách chặn request và Sheet sync/Sidekiq, dừng app/worker trước datastore, dừng Desktop hoàn toàn cho offline backup; kiểm restart policy. Sau chuyển khởi động datastore trước app/worker, chỉ mở ghi khi đã kiểm dữ liệu. Không dùng `wsl --shutdown` mặc định vì ảnh hưởng Ubuntu khác |
| Rollback | Trước move: không đổi cấu hình nếu preflight/backup FAIL. Trong/sau move: giữ ghi bị chặn, dừng Desktop, giữ cả target dở dang và backup tốt; xác định vị trí hiện hành, dùng quy trình Docker hỗ trợ để phục hồi từ bản offline đã hash. Không giả rằng UI giữ VHD gốc trên C; không overwrite/xóa bản tốt cuối cùng. Nếu chưa đủ chỗ giữ partial và bản phục hồi thì dừng, không tự dọn |
| Sau cutover | Kiểm backend/data location, image IDs, container/volume/mount identities và thay đổi nào được phép. Start time phải đổi do restart, không dùng tiêu chí “start time không đổi” của lượt bảo vệ trước đây. Kiểm login, uploads/video, quyền khóa học/Sheet sync, API/UI Chatwoot và worker/queue với dữ liệu đúng. Chỉ ghi aggregate không nhạy cảm vào Git |
| Phát sinh ghi sau cutover | Chưa mở ghi trước nghiệm thu. Nếu sau đó cần rollback, phải quyết định mốc dữ liệu và xử lý ghi mới; không khôi phục backup cũ âm thầm |
| Giữ backup | Giữ đến khi đã kiểm khôi phục và chủ sản phẩm nghiệm thu; xóa là quyết định riêng. Backup trên cùng D không bảo vệ khỏi hỏng ổ D; hiện chưa chọn đích dự phòng độc lập |

Những mục còn UNKNOWN cần khảo sát read-only hoặc nhiệm vụ bảo trì có phạm vi/quyền
cụ thể, rồi review lại bản runbook theo commit. Không thực hiện backup, restore,
stop/start, tạo đích, move hoặc dọn dữ liệu trong phần chuẩn bị này.
