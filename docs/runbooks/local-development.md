# Dùng Chatwoot development trên máy hiện có

Tổng hợp ngày **23/11/2026** từ runbook local `buoc-2/chuyen-docker-desktop-2026-11-17/CACH-CHAY.md` trong [kho lịch sử](../project-map.md). Đây là hướng dẫn của bố trí đã có; DOCS-001 chỉ đọc, không thực hiện start/stop/build. Chưa là quy trình cài đặt sạch trên máy khác.

## Chọn đúng nơi làm việc

Danh tính source, branch/commit, Docker engine/project và cổng nằm trong [runtime.json](../../config/agents/runtime.json). Source ứng dụng ở Ubuntu-22.04: `/root/code/chatwoot-worktrees/wsl-preflight`. Trước sửa, đọc AGENTS.md/AGENTS.override.md đang áp dụng tại source đó và nhận phiếu việc có phạm vi/quyền. Checkout Windows cũ không phải source container đang đọc.

Docker Desktop trên Windows dùng backend WSL2. Rails/Vite/Sidekiq bind source Linux; dữ liệu và dependencies dùng volumes. Chưa thể khôi phục đầy đủ chỉ bằng clone kho tài liệu vì `.codex/desktop.sh` và overrides đang nằm tại source local, chưa được quản lý trong repo này.

## Kiểm tra an toàn từ PowerShell

```powershell
wsl.exe -d Ubuntu-22.04 --exec git -C /root/code/chatwoot-worktrees/wsl-preflight status --short
wsl.exe -d Ubuntu-22.04 --exec git -C /root/code/chatwoot-worktrees/wsl-preflight rev-parse HEAD
wsl.exe -d Ubuntu-22.04 --cd /root/code/chatwoot-worktrees/wsl-preflight --exec bash .codex/desktop.sh ps
```

So kết quả với profile; nếu khác, khảo sát trước thao tác. Có thể chạy doctor từ root repo tài liệu:

```text
python -B tools/agents/workspace_doctor.py --profile config/agents/runtime.json
```

Doctor HEALTHY chỉ kiểm danh tính/guard theo profile, không chứng minh UI hoặc nghiệp vụ đạt. Cần Python 3.10+ và các CLI theo [agent guide](../agents/README.md).

## Vận hành khi nhiệm vụ có quyền

Mở Docker Desktop trước. Trong terminal Ubuntu-22.04:

```bash
cd /root/code/chatwoot-worktrees/wsl-preflight
./.codex/desktop.sh up -d --no-build --pull never rails
./.codex/desktop.sh ps
```

Truy cập [Chatwoot local](http://localhost:44330/app/login) và [Mailhog local](http://localhost:44332). Các link localhost chỉ hoạt động trên máy host, không phải website chia sẻ cho người ngoài. Thông tin đăng nhập thực lấy qua kênh riêng, không đưa vào Git.

Dừng trong nhiệm vụ được giao quyền runtime:

```bash
./.codex/desktop.sh stop
```

Không reset DB/xóa volume để chạy lại thường ngày. Không chạy đồng thời Engine cũ và Desktop. Task/worktree riêng không tự tách DB/Redis/container. Không đọc/in `.env` hoặc log thô để chia sẻ bằng chứng. VS Code WSL có thể mở source Linux; UI VS Code chưa được kiểm trong nhiệm vụ này.

## Căn cứ và giới hạn

[Chatwoot Docker development](https://developers.chatwoot.com/contributing-guide/environment-setup/docker) là nguồn setup phát triển; [Docker WSL best practices](https://docs.docker.com/desktop/features/wsl/best-practices/) là căn cứ giữ source bind mount trong Linux. Ports, adapter `.codex` và giữ nguyên dữ liệu là điều chỉnh local, không phải nguyên mẫu upstream. [Đánh giá môi trường ngày 18/11](../reviews/project-foundation/local-environment.md) giữ các image/mount đã khảo sát; không coi đó là kiểm lại image hôm nay. Hiệu năng hiện quan sát và NOT_RUN xem [F5 ngày 23/11](../reviews/performance/2026-11-23-f5.md).
