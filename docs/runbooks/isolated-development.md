# Dựng Chatwoot trong môi trường thử riêng

Ngày 23/11/2026, COMPLETE-001. Đây là hướng dẫn đang được kiểm chứng; xem receipt của task trước khi coi bước nào đạt. Source ứng dụng và control là hai repo khác nhau. Không dùng Compose/script của lab cũ để chạy phép thử này.

## Đầu vào

- Docker Desktop với WSL2, source trong filesystem Linux.
- Repo app: https://github.com/trdat1605/s-251521f7e9131fb0 ; nhánh `codex/portable-foundation` đang review, chưa có trên main.
- App commit được thử phải đúng `app-task.json`; không thay bằng control commit.
- Python3, Git, Docker Compose; đọc AGENTS thực ở app checkout.
- Dung lượng host C trên ngưỡng dừng15GiB, cổng44440–44442 còn trống. WSL free logical không thay dung lượng ổ host.

## Những tệp có công năng gì

| Tệp app | Công năng |
| --- | --- |
| `docker/Dockerfile` | Build image Chatwoot từ dependency và source; nhận SHA đã được wrapper kiểm, vẫn hỗ trợ Git clone thường |
| `docker/isolated/bootstrap.py` | Kiểm source sạch/ref thật, tạo snapshot từ Git, sinh bí mật riêng, cố định project/file/ports và gọi các lệnh cho môi trường mới |
| `docker/isolated/compose.yaml` | Khai báo Rails, Sidekiq, Vite, Postgres, Redis, Mailhog và service test; dữ liệu riêng theo project |
| `docker/isolated/entrypoint.sh` | Kiểm dependency, không xóa cache/PID dùng chung kiểu entrypoint development upstream |
| `docker/isolated/test_bootstrap.py` | Kiểm ranh giới project/secret/source/archive/image; không thay test ứng dụng |
| `docker/isolated/verify_runtime.py` | Bài lifecycle dành cho runner dùng một lần, ghi ref và kết quả JSON, dừng project riêng; không chạy trên lab dùng chung |
| `.github/workflows/foundation-ci.yml` | Chạy regression Docker, focused frontend và lifecycle trên runner dùng một lần; không publish/deploy |

Các tệp `.codex/isolated/<project>/` được sinh local và ignored: build context riêng, runtime source snapshot riêng, state và `secrets.env` mode600. Không đưa chúng vào Git. Build context không chứa `.git`, `.codex`, env thực hoặc adapters lab. Chỉ bỏ exact symlink chỉ dẫn Windsurf đã xác định để tương thích tar-filter Python3.10 trên máy; AGENTS giữ nguyên và liên kết khác vẫn bị kiểm an toàn.

## Trình tự theo hướng dẫn app

Trong app checkout sạch, sau khi review đúng commit: chạy boundary tests → metadata-regression → prepare → config → build → prepare-db → up → smoke → test → restart → smoke. Lệnh cụ thể và quyền runtime xem `docker/isolated/README.md` của chính app commit. Project local đầu là `cwdev-complete001`, successor `cwdev-complete002` chưa được tạo do thiếu dung lượng; helper hosted dùng riêng `cwdev-ci-runtime`. không đổi tên thành `cwlab-9200023e` hoặc `course-platform-local`.

`prepare` lặp lại giữ secrets/config khi source và tham số không đổi; source HEAD đổi thì dừng để tạo project mới. `build` mặc định FULL_BUILD; nếu dùng image dependency có sẵn bằng ID thì phải ghi CACHE_REUSE, không gọi đó là build sạch. Bản image mới phải có `.git_sha` khớp sourceHEAD.

`test` dùng database/Redis-index/storage/tmp riêng với development. Trước khi chạy lệnh thêm ngoài wrapper, reviewer phải kiểm lại namespace và cấu hình; không truyền CLI tùy ý để thay project/file. Không chạy reset/prune/down-v lên môi trường đang có dữ liệu.

## Phục hồi và tiếp quản

Chỉ backup dữ liệu tổng hợp của project mới vào vị trí local ignored. Lưu riêng code SHA, cấu hình không bí mật và đường quản lý secret. Restore vào database thử mới, kiểm record đã biết, rồi giữ/làm sạch đúng tài nguyên được giao. Đây là diễn tập local, chưa là rollback production.

Không tạo thêm môi trường local khi C dưới 15 GiB; Linux báo free logical không thay ngưỡng host. [Phương án sang D](docker-storage-migration.md) mới chuẩn bị/review, chưa áp dụng.

Agent tiếp quản đọc task/control README trước, xác định app commit, mở đúng README app, kiểm state/ref/resource và receipt; không coi việc có file hoặc HTTP200 là sản phẩm đã ổn định.

Nguồn: [Chatwoot Docker development](https://developers.chatwoot.com/contributing-guide/environment-setup/docker), [Docker project isolation](https://docs.docker.com/compose/how-tos/project-name/), [Git worktree metadata](https://git-scm.com/docs/git-worktree). Cổng/project/helper ở trên là điều chỉnh có kiểm chứng riêng của dự án, không trình bày như nguyên mẫu upstream.
