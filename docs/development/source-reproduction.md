# Source và môi trường có thể lấy lại

Khảo sát **23/11/2026**, [ENV-001 / issue #8](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/8). Phân biệt **đã chia sẻ source baseline** với **chưa tái lập runtime hoàn chỉnh**.

## COMPLETE-001 — cấu hình portable và pilot Docker

Source branch `codex/portable-foundation` bổ sung `docker/isolated/` và sửa Docker metadata. [PR ứng dụng3](https://github.com/trdat1605/s-251521f7e9131fb0/pull/3), [hướng dẫn môi trường riêng](../runbooks/isolated-development.md), [trạng thái công việc](completion.md). Chưa merge; clone main hiện chưa có helper này.

Đã build full Dockerfiledevelopment tại appSHA `0768677`, image `.git_sha` đúng; Docker regression thật có baseline FAIL/fix PASS và normalGit fallback. Sau đó startup Vite phát hiện prompt cài dependency; appSHA `2db109b` sửa entrypoint và CI đạt metadata/frontend. Bài vòng đời trên hosted runner đã PASS apphead27e1669/mergecheckout8d953fd, tracked tree giống hệt: [receipt](../../tasks/COMPLETE-001/evidence/app-ci-lifecycle-success.json). Phạm vi gồm setup/focused tests/restart/synthetic restore, chưa là toàn bộ app hoặc local reproduction. Không gán kết quả076 sang SHA mới mà không đối chiếu phần thay đổi.

C local xuống dưới ngưỡng15GiB sau fullbuild. Chỉ tài nguyên tổng hợp COMPLETE-001 được dọn với reviewer và backup; PGvolume cũ giữ đến khi restore kiểm xong. Không prune toànDocker hoặc thay lab/course. Đây là hạn chế dung lượng host, không phải bằng chứng thiết kế app tối ưu hoặc hoàn tất localreproduction.

## Tiếp quản source hiện hành

Chỉ clone/read trước khi có quyền và đủ tài nguyên chạy. Trong Linux, dùng thư mục mới:

```text
git clone --branch codex/portable-foundation --single-branch https://github.com/trdat1605/s-251521f7e9131fb0.git chatwoot-foundation
git -C chatwoot-foundation checkout --detach 27e166927b93677863e7e7fda22109cfa2ae98b9
git -C chatwoot-foundation rev-parse HEAD
git -C chatwoot-foundation status --short
```

Đọc `AGENTS.md` rồi `docker/isolated/README.md` tại chính app SHA. Clone trên chưa chạy app và không tạo credentials. Nếu dùng shallow clone riêng, hướng dẫn app nêu cách lấy baseline Git object còn thiếu cho regression. Để chạy local phải có task/runtime claim, project/ports riêng, host C đạt ngưỡng và plan đã review. C hiện thiếu dung lượng: không chạy build/start local theo ví dụ.

CI kiểm code trên merge checkout của PR; receipt phải giữ cả app head và checkout SHA/tree thực. Full build076, CI2db và runtime27 là các lượt khác nhau. Không ghép chúng thành một lần chạy giả.

## Lịch sử chia sẻ source

**PUB-001:** kho này hiện công khai sau đổi tên, ID `1467945011` giữ nguyên. Actions từng tắt ở PUB-001; COMPLETE-001 đã bật riêng workflow foundation sau review và tắt 17 workflow kế thừa. Các đoạn về seed private bên dưới là lịch sử đã thực hiện, không mô tả visibility hiện tại. [Bằng chứng chuyển đổi](repository-publication.md).

[Kho source ứng dụng](https://github.com/trdat1605/s-251521f7e9131fb0) có `main` tại đúng Chatwoot v4.19.1 / `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, tree `2979093d6c3f6c545fff930744e685ff3773f5d8`, ancestry upstream 7013 commits theo khảo sát. Giữ LICENSE và enterprise/LICENSE gốc, không trộn history repo tài liệu vào app.

Trước push đầu tiên đã tạo repo rỗng/private, tắt Actions và đọc lại `enabled=false`. Push exact SHA tới main với `--no-follow-tags`, không mirror/all/tags/force, không đổi remote/config/branch của source lab. Readback private=true, remote SHA đúng và Actions vẫn disabled. Plan có reviewer độc lập trước thực hiện; hồ sơ [plan](../../tasks/FLOW-001/evidence/source-seed-plan.json), [review plan](../../tasks/FLOW-001/evidence/source-seed-plan-review.json), [readbacks](../../tasks/FLOW-001/evidence/source-seeded.json).

Tại FLOW/PUB, Actions app repo giữ tắt vì kế thừa workflow publish/schedule upstream. COMPLETE-001 không bật các workflow kế thừa ấy; không coi thiếu secrets là cơ chế ngăn publish đủ. Cảnh báo push: upstream có file model ONNX khoảng 65,78MB vượt mức khuyến nghị GitHub50MB; push vẫn thành công. Không rewrite lịch sử hoặc di chuyển LFS trong lượt này.

## Khoảng trống của bố trí lab lịch sử

Source đang chạy ở [profile lab](../../config/agents/runtime.json), tracked Git sạch. Nhưng `.codex/*` bị upstream `.gitignore:97` bỏ qua, AGENTS.override local bị common exclude. Clone app baseline **không có các adapter lab này**. Kho app mới chưa thay remote/source bind của lab; không sửa ở kho tài liệu rồi kỳ vọng web đổi.

| Thành phần đã khảo sát | Vì sao cần xử lý trước fresh setup |
| --- | --- |
| `.codex/desktop.sh` | Guard Desktop nhưng hardcode project lab; không dùng nguyên cho môi trường mới |
| Compose lab/desktop | Hardcode source/images/ports; desktop overlay để chuyển dữ liệu cũ, không là template fresh setup |
| Base/Rails/Vite Dockerfiles local | Delta nhỏ phục vụ worktree và base image namespace; cần giữ diff với upstream, không copy toàn cây ignored |
| Vite entrypoint local | Khác upstream về pid/cache/install; cần kiểm hành vi khi chia sẻ source mount |
| `.dockerignore` | Chưa loại toàn bộ artifacts/override local; cần allowlist build context |
| Bí mật và dữ liệu | Không nằm trong Git; môi trường mới dùng secrets mới/dữ liệu tổng hợp. Restore dữ liệu thật là nhiệm vụ riêng |

Upstream [Dockerfile tại pin, dòng 89–90](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/Dockerfile#L89-L90) dùng Git metadata trong build; worktree pointer tới host cần được xử lý cho ngữ cảnh image. Chưa thực hiện regression/build đối chứng trong lượt này. Danh sách/hashes adapter local nằm trong [inventory](../../tasks/FLOW-001/evidence/source-inventory.json); không chứa env/khóa/log thật.

## Kế hoạch bootstrap lịch sử của FLOW-001

Đoạn này ghi kế hoạch ở FLOW-001; phần COMPLETE-001 phía trên và receipt mới mô tả việc đã thực hiện.

Tạo clone/nhánh độc lập, giữ templates không bí mật ngoài `.codex` rồi sinh config local theo convention upstream. Mỗi môi trường có project/image/port/DB/Redis/volume riêng, fail-closed nếu đụng `cwlab-9200023e`; không dùng external volume lab. Kiểm source SHA/build context và truyền source ref từ Git thật, không nhận SHA tùy ý.

Review phương án trước build. Sau đó Compose render với env giả → build → DB prepare riêng → focused app tests → UI smoke/restart theo acceptance. Không áp các lệnh reset/prune của hướng dẫn dev lên lab đang có dữ liệu. Cần thử cả fresh và chạy lại; ghi dependencies từ network/image và khác biệt. Không hứa build bit-for-bit reproducible: Dockerfile còn package mạng không pin hết.

Dung lượng host C tại khảo sát còn khoảng29GiB; WSL báo dung lượng logic lớn không phải host disk thật. Chưa quyết vị trí môi trường mới hoặc tải/build thêm image. Không tạo thêm môi trường nặng chỉ để đóng checklist.

## Căn cứ

[Chatwoot Docker development](https://developers.chatwoot.com/contributing-guide/environment-setup/docker) mô tả source/env/build/prepare/run; [AGENTS đúng pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md) yêu cầu worktree và giá trị tránh collision; [backup](https://developers.chatwoot.com/self-hosted/deployment/backup) tách code/data/storage/config; [Git clone](https://git-scm.com/docs/git-clone) giải thích clone/alternates; [GitHub Actions permissions API](https://docs.github.com/en/rest/actions/permissions) hỗ trợ việc tắt workflow trước seed. Đây là căn cứ thiết kế. Bằng chứng thực chạy nằm ở COMPLETE-001 theo từng SHA; không lấy tài liệu làm bằng chứng setup PASS.
