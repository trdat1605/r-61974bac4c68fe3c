# Bằng chứng, phương pháp và giới hạn

Ngày khảo sát: **18/11/2026, UTC+07**. Source ứng dụng: `chatwoot/chatwoot`, `v4.19.1`, `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, nhánh local `codex/wsl-migration`. Bộ báo cáo thuộc kho private `trdat1605/chatwoot-vn`, nhánh `review/project-foundation`; commit chứa báo cáo xem lịch sử Git/PR, khác commit source. [README](README.md).

## Cách đọc bằng chứng

- **O — quan sát:** kiểm trực tiếp hoặc đọc một artifact xác định.
- **H — lịch sử:** bằng chứng đã lưu từ lượt trước, không phải vừa thực chạy lại.
- **I — suy luận:** có điều kiện từ source/cơ chế, chưa thay cho phép chạy.
- **P — đề xuất:** việc cho lượt sau, chưa áp dụng vào ứng dụng.
- **U — chưa xác minh / NOT_RUN:** thiếu phép thử hoặc dữ kiện.

Có nhiều file, tests từng chạy, agent nhận chức danh hoặc Git sạch không tự chứng minh chất lượng toàn hệ thống. Lượt đóng gói tận dụng số đo ngày 18/11 và receipts ngày 17/11; chỉ kiểm thêm Git, runtime, quyền GitHub và các khoảng trống về source/tài liệu. Không chạy lại toàn bộ đo/test để tạo vẻ có bằng chứng mới.

Chỉ xuất các trường cho phép. Không publish toàn bộ Env/inspect, dữ liệu khách hàng, secrets, DB dump, uploads, ảnh chụp có nội dung hội thoại hoặc log thô. Tên biến được nhắc để giải thích, không kèm giá trị bí mật.

## Inventory bằng chứng

| ID | Loại/ngày | Nội dung và phương pháp | Giới hạn |
| --- | --- | --- | --- |
| E01 | O, 18/11, kiểm lại khi soạn | Git HEAD, tag, branch, status, số commit riêng, history và remote: đúng pin, nhánh wsl-migration, Git sạch, 0 commit riêng | Không audit mọi repo trên máy hoặc mọi tài khoản GitHub |
| E02 | O, 18/11 00:04–00:16 | CIM Windows, phiên bản WSL, selected settings, Docker version/info/context, df/findmnt/free/swapon | Snapshot, không phải capacity test; không in toàn bộ settings/env |
| E03 | O, 18/11 | Compose resolved trong bộ nhớ; chọn mounts/ports; checksum bốn tệp trong ba app containers; PG data_directory và Redis dir/persistence | Không hash toàn cây; không tạo probe trong khảo sát này; probe lịch sử 17/11 là phép khác |
| E04 | O, 18/11 và kiểm lại | Container images/state/restart/OOM, image IDs, sáu service running, phiên bản Ruby/Node/pnpm/PG | Không build/pull; chưa chứng minh build tái lập |
| E05 | O và I, 18/11 | BUNDLE_PATH=/gems, bundle config/show; gems khoảng 1.1 GiB, /usr/local/bundle khoảng 3.2 MiB; đối chiếu mount | Không cài gem/recreate; hậu quả vòng đời được suy từ source và Docker |
| E06 | O, 18/11 00:07–00:13 | curl Windows/WSL ba lần; CDP Navigation/Paint Timing và Network events; lấy mẫu containers; tổng hợp log | Số liệu mới trích từ tool output trong chat; không có raw trace được upload; trace truncated |
| E07 | H, 17/11; đọc lại 18/11 | Kế hoạch, review từng pha, backup/restore, audit runtime/HTTP/browser và review cuối | Artifact gốc còn local; reviewer lịch sử không tự chạy lại toàn bộ browser |
| E08 | O, 18/11 | diff local Dockerfiles so với pin; ignored rules, cấu hình local; Compose project/port/DB cố định | Không sửa adapter; drift tương lai là nguy cơ, chưa phải lỗi nâng cấp đã tái hiện |
| E09 | O trong tài liệu/phạm vi đã nêu, 18/11 | Tìm quyết định/backlog Zalo, kế hoạch nâng cấp và repo riêng | Không khẳng định không có ở mọi nơi; hợp đồng/thiết kế chưa chốt |
| E10 | O, 18/11 | Đọc chỉ mục, quyết định, mẫu, runbook và results; repo hồ sơ cũ chưa commit, ls-files=0, không remote; xác định các dòng trạng thái cũ | Kho báo cáo mới chưa chuyển toàn bộ hồ sơ; người chỉ truy cập GitHub không mở được các đường dẫn local |
| E11 | H, 11/11; đọc lại 18/11 | Receipts ghi 18 RSpec, 4 frontend tests/3 files và một lượt 82 feature specs đạt | Các bộ chọn lọc khác nhau; không cộng coverage; không chạy lại trên Desktop trong khảo sát |
| E12 | O, lượt xuất bản 18/11 | API danh sách repo ban đầu trả []; người dùng cho phép tạo kho private; API xác nhận private=true và ADMIN; main khởi tạo rỗng, branch báo cáo riêng | Không upload ứng dụng; không tự cấp collaborator; chỉ push sau review và làm sạch |

## Artifact gốc còn local

Gốc: `C:/Users/MFLAT-ADS-010/Documents/ChatGPT/tôi`. Đây là hồ sơ ngoài Git sản phẩm; các tệp kiểm mẫu còn untracked trong một repo local chưa có commit lúc khảo sát.

| Thư mục | Tệp tiêu biểu |
| --- | --- |
| buoc-2/chuyen-docker-desktop-2026-11-17 | PHUONG-AN.md, STAGED.json, REVIEW-PHA-A-V3.md, REVIEW-PHA-B.md, REVIEW-INTEGRATION.md, REVIEW-PHA-C.md, REVIEW-LEGACY-GUARD.md, REVIEW-KET-QUA.md |
| Cùng thư mục trên | BACKUP-VERIFIED.json, TARGET-RESTORED.json, RUNTIME-AUDIT.json, SOURCE-BIND-VERIFIED.json, HTTP-SMOKE*.json, BROWSER-SMOKE.json, CURRENT-HEALTH.json, KET-QUA.md, CACH-CHAY.md |
| buoc-2/chuan-bi-moi-truong/logs | rspec-messages-RESULT.json, frontend-tests-final-RESULT.json và stdout tương ứng |
| buoc-2/mo-tinh-nang-lab | full-feature-specs-RESULT.json và stdout; FULL-78.md, DANH-MUC.md |
| buoc-1 | 01-HO-SO-CHATWOOT.md, 02-TO-CHUC-VA-QUAN-LY-AGENT.md, 03-CONG-VIEC-VA-DIEU-KIEN.md |
| buoc-1/kien-thuc | BAT-DAU.md, THEO-CONG-VIEC.md, NGUON.json, KIEM-CHUNG.md, QUYET-DINH-VA-VUONG-MAC.md, QUY-TAC-SU-DUNG.md |
| buoc-1/mau | GIAO-VIEC.md, BAN-GIAO.md, REVIEW.md, GOI-NGU-CANH.md |

Hai hash lịch sử đã khớp bản review cuối, **không phải hash báo cáo mới**:

```text
KET-QUA.md  CB711284C2D004B18E80AABBB3537F08E5E0BF3EF99FCFB44E45E7EBA12E0F2F
CACH-CHAY.md 5197F8E73708D1A5841A3256A8856332FD509601E5BD24065A7C080C0FAFF41A
```

Không sao chép cả các thư mục trên lên GitHub. Người review từ xa có bộ trích và nguồn cố định, nhưng không thể tự xác minh toàn bộ lịch sử chỉ bằng hash khi không có artifact gốc. Nếu cần thêm bằng chứng, chọn riêng và làm sạch trong nhiệm vụ phù hợp; không publish backup nhạy cảm để lấp thiếu chứng cứ.

## Các lệnh đã dùng

```text
Get-CimInstance Win32_OperatingSystem / Win32_Processor / Win32_ComputerSystem
wsl.exe --version
wsl.exe --list --verbose

git -C /root/code/chatwoot-worktrees/wsl-preflight status --porcelain
git ... rev-parse HEAD / branch --show-current / rev-list --count <pin>..HEAD
# Git sạch; source pin caab07a...2d82; branch codex/wsl-migration; 0 commit riêng

docker context show / context ls
docker version / docker compose version
docker info --format <selected-fields>
docker inspect <project-containers>    # capture trong bộ nhớ, chỉ xuất fields cần thiết
docker stats --no-stream
docker diff <container>                # không bao gồm nội dung mounts
findmnt -T /root/code/chatwoot-worktrees/wsl-preflight
bundle config get path
bundle show rails
# /gems; /gems/ruby/3.4.0/gems/rails-7.2.3.1
```

Không lưu output xác thực chứa token, kể cả đã mask. Quyền và visibility của kho được lấy bằng selected API fields, không phải sao chép credential/config.

### Phương pháp HTTP

Khoảng 00:07:35, ba lần liên tiếp cho mỗi endpoint `/health`, `/api`, `/app/login`, `/vite-dev/@vite/client`. Windows và WSL dùng cùng URL, IPv4 và no-proxy; hai nhóm gần đồng thời. Mỗi mẫu là curl process mới. Không restart, cold reset hoặc thay cache-control.

Ví dụ Windows:

```powershell
curl.exe --noproxy '*' -4 --max-time 30 --silent --show-error -o NUL -w '%{http_code} %{time_namelookup} %{time_connect} %{time_starttransfer} %{time_total} %{size_download}' http://localhost:44330/health
```

Ubuntu dùng cùng flags/endpoint, đổi output thành `/dev/null`. Số đo ba lần ghi trong [local-environment.md](local-environment.md). TTFB và total khác UI render. `/api` gốc không phải mọi API nghiệp vụ. Không dùng vài mẫu này làm benchmark tổng quát giữa hai OS.

### Phương pháp browser và lấy mẫu

Trình duyệt trong ứng dụng chạy trên Windows, session đã có. CDP đọc Navigation/Paint Timing, bật Network observation và reload thông thường. Không throttle, đổi cache, tăng resource timing buffer hoặc tạo cold start. Không submit login/message mới. Chỉ đọc DOM/editor visibility; không đưa nội dung hội thoại vào báo cáo.

Resource Timing giới hạn 250 entries; thu CDP theo cursor vẫn truncated. Không công bố tổng request/module duy nhất hoặc waterfall đầy đủ. Một số selector timeout; lần quan sát sau xác nhận editor hiện, không chuyển timeout thành PASS. Chưa định lượng overhead của browser/công cụ quan sát.

Docker sampling 00:10:20–00:11:07 bao phủ reload đầu. CPU container có thể vượt 100% trên nhiều lõi. Log chỉ lấy cửa sổ và tổng hợp status/timing/error patterns, không đưa raw lines/payloads lên GitHub. Các mẫu không chứng minh không có spike ngoài cửa sổ quan sát.

## Kết quả không đạt hoặc chưa giải thích

| Kết quả | Diễn giải được giữ trong báo cáo |
| --- | --- |
| FCP khoảng 12 giây, load 14–17 giây | UI chậm trong browser khảo sát; chưa biết nguyên nhân gốc hoặc so production |
| Selector deadline | Không báo selector đạt; quan sát tiếp có editor nhưng thời gian ready chưa chính xác |
| CDP trace truncated / buffer 250 | Không báo waterfall đầy đủ hoặc tổng module chính xác |
| InvokeWebRequest timeout 20 giây lịch sử 17/11 | Direct curl Windows/WSL trả 200; nguyên nhân default client chưa rõ, không gán proxy/IPv6/Chatwoot |
| detail BadRequest người dùng báo | Chưa có request/bề mặt/thời điểm để tái hiện hoặc quy lỗi |
| HTTP smoke lúc boot 17/11 connection reset | Phép thử trước readiness; giữ receipt lỗi và kết quả sau đó, không xóa lịch sử |
| Smoke chọn account đầu trống | Sửa phép kiểm chọn đúng tài khoản lab; không sửa dữ liệu để pass |
| limits 404 | Source pin cố ý trả 404 ngoài Cloud; frontend silent catch; không sửa gate trong nhiệm vụ |
| Redis DUMP mismatch khi restore 17/11 | Giữ receipt mismatch; review V3 chuyển sang so dữ liệu logic và expiry thay serialization bytes; không chỉ so số keys |

## Phạm vi PostgreSQL, Redis và phục hồi

PG thực chạy 16.15, `data_directory=/data/postgres`. Snapshot hoạt động chỉ tổng hợp: 9 idle/ClientRead, 1 active/không wait tại thời điểm đọc. Không đọc query hoặc dữ liệu nghiệp vụ. Snapshot này không chứng minh database không bao giờ nghẽn.

Redis: dir `/data`, dump.rdb, appendonly=no, save `3600 1 300 100 60 10000`; loading=0, last background save OK lúc quan sát. Không gọi SAVE/restore trong khảo sát.

Restore lịch sử 17/11 bao phủ 5 DB public tables bằng counts/canonical checksums và các trường sequence chọn lọc (`last_value`, increment, cycle, cache_size; không có `is_called`). Redis 47 keys ở mốc restore, so giá trị logic và absolute expiry trên 16 DB; kiểm persistence stop/start trước app writers. Chưa replay globals ACL, chưa có upload blob thật, chưa full Engine rollback. 78 flags bật là trạng thái tài khoản lab trong audit 17/11, không phải mọi account hoặc mọi chức năng; không chạy lại feature tests ngày 18/11.

## Nguồn kiểm theo phiên bản

| ID | Nguồn | Điều kiện áp dụng |
| --- | --- | --- |
| S01 | [AGENTS pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L1-L23), [worktree](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L72-L77), [Enterprise](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L119-L135) | Source đúng pin, không phải yêu cầu tự cài mọi công cụ vào repo báo cáo |
| S02 | [Enterprise injection](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/config/initializers/01_inject_enterprise_edition_module.rb#L23-L48), [API inbox](https://www.chatwoot.com/hc/user-guide/articles/1677839703-how-to-create-an-api-channel-inbox) | Source pin và guide live; chưa là hợp đồng Zalo |
| S03 | [BUNDLE_PATH](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/Dockerfile#L121), [copy gems](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/Dockerfile#L147), [bundle mount](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker-compose.yaml#L29), [entrypoint](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/entrypoints/rails.sh#L24) | Sự lệch đã có upstream; không gán toàn bộ cho adapter local |
| S04 | [Docker dev Windows](https://developers.chatwoot.com/contributing-guide/environment-setup/docker#install-docker), [WSL backend](https://docs.docker.com/desktop/features/wsl/), [Linux bind/inotify](https://docs.docker.com/desktop/features/wsl/best-practices/) | Docs live đọc 18/11; chưa có snapshot v4.19.1 |
| S05 | [Production Compose pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker-compose.production.yaml), [guide](https://developers.chatwoot.com/self-hosted/deployment/docker), [requirements](https://developers.chatwoot.com/self-hosted/deployment/requirements) | File production pin dùng image, không có build; không chép lệnh build/reset mù |
| S06 | [CI pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/workflows/run_foss_spec.yml), [Playwright README pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/tests/playwright/README.md), [PR guidance](https://www.chatwoot.com/hc/handbook/articles/pull-request-guidelines-32) | CI/source đúng pin; handbook live; không chứng minh CI riêng đã chạy |
| S07 | [Upgrade](https://developers.chatwoot.com/self-hosted/deployment/upgrade), [Backup](https://developers.chatwoot.com/self-hosted/deployment/backup), [Docker backup](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) | Đọc hướng dẫn; không thử upgrade/rollback ngày 18/11 |
| S08 | [Cloud guard](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/enterprise/app/controllers/enterprise/api/v1/accounts_controller.rb#L119-L120), [frontend catch](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/javascript/dashboard/store/modules/accounts.js#L180-L186) | Source đúng pin |
| S09 | [Mobile release](https://github.com/chatwoot/chatwoot-mobile-app/releases/tag/v4.11.4), pinned links trong báo cáo mobile, [custom mobile](https://developers.chatwoot.com/self-hosted/custom-mobile-app) | Release không tự xác định binary config trên store hoặc compatibility |

[Why Vite](https://vite.dev/guide/why.html) live đã đọc mô tả source modules phục vụ theo yêu cầu. Trang v6.vite.dev không truy cập được qua web tool, nên không gọi tài liệu live là snapshot Vite 6. Gem Vite Ruby 3.10.6 trong image được đọc để xác nhận proxy, không sửa gem.

## Chưa kiểm chứng

| Phép kiểm tra | Trạng thái và lý do |
| --- | --- |
| HMR bằng sửa source | NOT_RUN: cần thay đổi tệp ngoài phạm vi |
| Build sạch/recreate với dependency mới | NOT_RUN: thay image/container/cache |
| Browser profile đầy đủ, Chrome thường, cold start | NOT_RUN: trace hiện có thiếu; không restart hoặc đổi cache |
| Full tests, load test, production build | NOT_RUN; không thay kết quả chọn lọc lịch sử thành full suite hiện tại |
| Feature PR → checks → review → acceptance | NOT_RUN; mới có workflow môi trường và bộ báo cáo |
| Upgrade target release và rollback code+dữ liệu | NOT_RUN; chưa chốt target/acceptance, phải bảo toàn dữ liệu |
| Upload restore/globals ACL/đủ sequence state | Chưa đủ phạm vi lịch sử, không thử thêm |
| Mobile thiết bị/HTTPS/WSS/push/phiên bản/Zalo | NOT_RUN; chưa có endpoint/connector/acceptance đã kiểm |
| IDE/Git panel hoặc AI mới tiếp quản đầy đủ | NOT_RUN; chỉ đánh giá tài liệu và lệnh WSL tường minh |
| Reviewer khác truy cập private GitHub | NOT_VERIFIED; không tự cấp collaborator/quyền |
| Merge hoặc branch protection enforcement | NOT_RUN; Draft PR là artifact review, không tự là gate kỹ thuật |

## Kiểm tra trước publish và review bộ báo cáo

Chỉ năm file Markdown trong thư mục yêu cầu được đưa vào commit. Kiểm allowlist staged paths, đọc diff, quét secret patterns/URL credentials/contact material, xác minh private visibility và Git source không đổi. Scanner không thay việc đọc nội dung. Reviewer nhận yêu cầu, pin, hashes của năm file và giới hạn bằng chứng; kết quả thực được ghi trong phần bàn giao/PR. Đoạn mô tả quy trình này tự nó không chứng minh review đã chạy.
