# STORAGE-001 — chuyển môi trường sang D

Ngày thực hiện: 26/11/2026, Asia/Saigon. [Issue 20](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/20). Chủ sản phẩm đã cho phép chuyển và yêu cầu dọn sau. Đây là bảo trì máy local dùng chung, không phải thay đổi tính năng hoặc merge/phát hành Chatwoot.

**Trạng thái: đã chuyển và kiểm tra runtime; đang review bàn giao.** Xem [phương án](maintenance-plan.md), [script đúng phạm vi](maintain.py), [review trước thực hiện](evidence/preflight-review.md) và các receipt trong `evidence/`. Không dùng việc có tệp làm bằng chứng bước đã chạy; chỉ đọc receipt có kết quả tương ứng.

## Bố trí đích

| Thành phần | Vị trí |
| --- | --- |
| Dữ liệu Docker Desktop | `D:/Dev/Runtime/Docker/DockerDesktopWSL/disk/docker_data.vhdx` |
| Ubuntu-22.04 | `D:/Dev/Runtime/Ubuntu/ext4.vhdx` |
| Source Chatwoot đang dùng, đường dẫn Linux giữ nguyên | `/root/code/chatwoot-worktrees/wsl-preflight` |
| Source pilot nền móng, đường dẫn Linux giữ nguyên | `/root/code/chatwoot-foundation-worktrees/complete-001` |
| Worktree hồ sơ bảo trì, Git Windows | `D:/Dev/Projects/Chatwoot-StorageOps` |
| Backup Docker mới, riêng tư ngoài Git | `C:/Users/MFLAT-ADS-010/.codex/private-backups/STORAGE-001/docker/docker_data.vhdx` |
| Backup Ubuntu mới, riêng tư ngoài Git | `D:/Dev/Backups/STORAGE-001/ubuntu/ext4.vhdx` |

Windows/VS Code có thể tìm source Linux qua `\\wsl.localhost\Ubuntu-22.04\root\code\chatwoot-worktrees\wsl-preflight`. Thay vị trí VHD vật lý không biến source thành thư mục NTFS `/mnt/d`; giữ Linux filesystem. Các cấu hình agent/source dùng đường dẫn Linux cũ không cần đổi chỉ vì chuyển ổ chứa VHD. Kho điều phối hiện tại vẫn khác kho ứng dụng; metadata common Gitdir của worktree Windows có thể còn ở C, không được xóa tùy tiện.

## Quyền và giới hạn

Không dọn cache/image/volume/backup cũ, không reset DB, không nâng Docker/WSL, không sửa source của Chatwoot hoặc website khóa học. Dữ liệu Docker và Ubuntu dùng chung nên cả hai website tạm dừng trong cửa sổ bảo trì. Khóa, env, database, raw container inspect và logs chỉ lưu riêng tư ngoài Git, có ACL hạn chế.

C/D cùng một ổ vật lý; backup phục vụ khôi phục khi di chuyển lỗi, không chống hỏng ổ vật lý. Backup Docker được chuyển tạm về C để đủ chỗ cho Ubuntu và bản sao trên D; đây là giữ backup, không phải đã dọn C tối đa. Dung lượng thực sau cùng phải đọc receipt, không suy từ tổng kích thước VHD.

## Kiểm tra và điều chưa kiểm

Trước dừng: 20 container, 15 running, 50 image riêng, 33 volume. Mốc dữ liệu: 31 dataset/967 bảng public PostgreSQL và persistent Redis DB0; key có TTL không so digest. Full VHD giữ cả volume/writable layers và phạm vi ngoài các digest được chọn. Năm datastore đã ghi nhận shutdown sạch exit 0/OOM false và đủ log markers riêng tư. Không coi đây là restore rehearsal hoặc full security test.

Sau chuyển: source ref/tracked bytes và selected bind-file hashes giữ nguyên; 20 container gốc/images/volumes/mounts giữ nguyên. HTTP khớp mốc trước. PostgreSQL 30 dataset khớp. Redis opaque DUMP digest ban đầu FAIL được giữ; hai parser đọc cùng 360525 bytes RDB từ backup, CRC/load Redis-only fixture đạt, 49 persistent keys của 5 kiểu dữ liệu canonical giống nhau và fresh recheck đạt. Fixture network none/read-only không gắn volume gốc; đã dừng và giữ, tổng container hiện 21 (20 gốc + 1 diagnostic). Không có full application/whole-VM restore rehearsal hoặc kiểm thử toàn bộ UI/tính năng/bảo mật.

Dung lượng tại kiểm tra sau: C khoảng 39,66 GiB, D khoảng 17,34 GiB. Đây là snapshot có hoạt động Windows, không gán mọi byte chênh lệch cho di chuyển. Backup Docker mới khoảng 31,86 GiB còn ở C, backup Ubuntu mới 16,54 GiB ở D, bản Ubuntu cũ 16,19 GiB vẫn ở C. Chưa dọn cache/old images/volumes/backups; không tự cam kết D đủ cho build lớn tiếp theo.

HTTP trước chuyển: Chatwoot login/Vite/Mailhog và course 44400/44403/44405 trả 200; HTTPS trial 44406 đã UNREACHABLE trước chuyển, phải ghi riêng nếu còn lỗi, không quy thành regression do chuyển ổ hoặc giả toàn bộ UI đạt.

Source Chatwoot lab khảo sát: `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`; pilot: `27e166927b93677863e7e7fda22109cfa2ae98b9`. Các commit hồ sơ bảo trì khác hai commit ứng dụng. Không sửa source trong nhiệm vụ này.
