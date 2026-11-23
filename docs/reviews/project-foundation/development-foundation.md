# Chất lượng nền móng phát triển

Ngày: **18/11/2026, UTC+07**. Source được đánh giá: Chatwoot v4.19.1 / `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`, local branch `codex/wsl-migration`. Kho/commit bộ review khác source, xem [README](README.md). Không sửa code, runtime hoặc tài liệu vận hành cũ.

## 1. Cấu trúc và delta riêng

**Quan sát E01:** source Linux Git sạch, 0 commit riêng so pin. Cây tracked giữ upstream; chưa có feature Zalo/mobile tùy chỉnh được tìm thấy trong phạm vi source/hồ sơ đã kiểm. Không dùng Git sạch để kết luận không có cấu hình ignored hoặc thay đổi trong volumes.

**Nguồn S01/S02:** [AGENTS:119–135](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L119-L135) yêu cầu kiểm cả app/enterprise, giữ tương thích và dùng extension/config thay hardcode instance. [config/application.rb:42–53](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/config/application.rb#L42-L53) nạp enterprise; [injection:23–48](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/config/initializers/01_inject_enterprise_edition_module.rb#L23-L48) cung cấp prepend/extend/include hooks. [Account:247–251](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/models/account.rb#L247-L251) có cách dùng thực. Đây là quy ước cho thay đổi tương lai, không phải bằng chứng custom code đã đạt.

**Quan sát E08:** ba Dockerfile riêng ở `.codex/dockerfiles` là copy upstream với delta hẹp:

| Local file / dòng | Delta so pin upstream | Lý do có thể nhận diện / rủi ro |
| --- | --- | --- |
| base.Dockerfile:90–91 | Thay `git rev-parse HEAD` bằng ARG CHATWOOT_SOURCE_COMMIT và kiểm không rỗng trước ghi .git_sha | Hỗ trợ build worktree không dựa Git metadata trong context; bản copy không tự nhận sửa upstream |
| rails.Dockerfile:1–2 | ARG CHATWOOT_BASE_IMAGE rồi FROM biến đó | Dùng image lab riêng; cần so lại khi upstream đổi |
| vite.Dockerfile:1–2 | Tương tự Rails | Cùng rủi ro drift bản copy |

Đối chiếu [base upstream:89–90](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/Dockerfile#L89-L90), [Rails:1](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/dockerfiles/rails.Dockerfile#L1), [Vite:1](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/docker/dockerfiles/vite.Dockerfile#L1). Vite entrypoint local còn điều chỉnh install/start, không coi toàn bộ adapter chỉ gồm ba delta trên.

**Đánh giá:** cấu trúc lõi đạt trong phạm vi chưa sửa; adapters runtime dễ nhận diện nhưng chưa được version-control trong repo sản phẩm. Không đề xuất đổi layout Rails/Vue hoặc xóa file upstream vì sở thích.

## 2. Ranh giới mở rộng

**Quan sát E09:** hồ sơ đề cập API channel/webhook và native channel như các lựa chọn; chưa tìm thấy quyết định chốt connector riêng, repo connector hoặc feature code. Chỉ khảo sát trong source/hồ sơ đã chỉ định, không khẳng định không có repo ở mọi nơi khác.

**Suy luận:** nếu chọn API channel, có thể tận dụng hợp đồng message/conversation thay sửa nhiều controller/model; nhưng còn phải đọc hợp đồng Zalo và đo các luồng nghiệp vụ. Native channel hoặc sửa gate/contract dùng chung có thể tăng delta khi nâng cấp. Chưa có diff nên chưa định lượng phụ thuộc lõi hoặc kết luận tách thành công.

**Đề xuất tối thiểu:** chọn loại tích hợp, ghi contract và acceptance criteria; với mỗi file dự kiến đổi nêu upstream hook/extension phù hợp, các edition/mobile/API bị ảnh hưởng và cách kiểm. Chi tiết ở [upgrades-and-integrations](upgrades-and-integrations.md).

## 3. Quản lý thay đổi

| Câu hỏi | Quan sát | Giới hạn |
| --- | --- | --- |
| Bản gốc? | Có tag/commit exact, full Git history | Không có nghĩa tự cập nhật upstream |
| Thay đổi ứng dụng riêng? | 0 commit/diff tracked | Cấu hình ignored vẫn hiện hữu |
| Runtime/config? | Có STAGED hashes, image IDs, source probe/checksums và receipts review 17/11 | Không được clone lại đầy đủ từ repo báo cáo |
| Lý do? | Có plans, mẫu giao việc, review theo pha | Lý do ban đầu chọn Engine/source Windows chưa có đủ đánh giá trước quyết định |
| Mọi thay đổi đều truy vết được? | Chưa: .codex/env/override bị ignore, hồ sơ cũ untracked | Không suy mọi file ngoài Git được bảo toàn bằng lịch sử |

Upstream [.gitignore:93–99](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.gitignore#L93-L99) ignore .codex; đây là quy ước có sẵn. Nó không cấm dự án quản lý adapter không bí mật bằng một cơ chế riêng sau quyết định rõ. Không tự force-add .env hoặc cả .codex để giải quyết truy vết.

**Đề xuất:** một inventory delta có nguồn pin, lý do, hash/commit, phạm vi tác động và phép kiểm; source và config không bí mật có version history thích hợp; secrets tiếp tục ngoài Git. Bộ review này chỉ lưu mô tả và bằng chứng đã làm sạch.

## 4. Chất lượng tài liệu và bản chính

E10: thư mục `C:/Users/MFLAT-ADS-010/Documents/ChatGPT/tôi` có repo local nhưng chưa commit, ls-files=0, không remote lúc kiểm; hồ sơ tiêu biểu untracked. Không đồng nghĩa hoàn toàn không có .git. Kho private mới tạo trong lượt này chứa bộ báo cáo, chưa chuyển toàn bộ tài liệu cũ vào Git.

| Tài liệu hiện có | Vai trò / đường dẫn tương đối từ thư mục tôi | Quan sát chất lượng |
| --- | --- | --- |
| BAT-DAU.md | buoc-1/kien-thuc/BAT-DAU.md:7–16 | Có định tuyến theo việc và chỉ runtime mới; đã gắn nhãn lịch sử11/11 |
| THEO-CONG-VIEC/NGUON/KIEM-CHUNG | cùng kien-thuc | Có tra cứu nguồn và trạng thái; không chứng minh mọi agent dùng đúng |
| 01-HO-SO-CHATWOOT | buoc-1/01-HO-SO-CHATWOOT.md | Kiến thức/source survey có ích; mở đầu chưa clone và restore status đã cũ |
| 02-TO-CHUC-VA-QUAN-LY-AGENT | buoc-1/... | Có mẫu/chu trình/khác biệt chỉ dẫn và gate; phần trạng thái ban đầu còn cũ |
| QUYET-DINH-VA-VUONG-MAC | kien-thuc/...:13,24,42 | Còn branch dev-environment và trạng thái chưa build/Ubuntu/Docker chưa chạy; khác runtime mới |
| CACH-CHAY17/11 | buoc-2/chuyen-docker-desktop-2026-11-17/CACH-CHAY.md:7–20,55–64 | Runbook hiện tại, nêu cwd Windows và Linux commands |
| KET-QUA17/11 / REVIEW-KET-QUA | cùng folder:3 | Một file còn đang review, file review đã kết luận đủ bằng chứng phạm vi |
| Backlog03 | buoc-1/03-CONG-VIEC-VA-DIEU-KIEN.md | Có công việc/vướng mắc; không là GitHub issues và có trạng thái cũ |
| Upstream README/AGENTS/CLAUDE/CONTRIBUTING/tests | trong source Linux tracked | Quy ước/source, không phải phép chạy riêng dự án |

Nhật ký quyết định **chưa đạt cho việc đại diện trạng thái hiện hành**; chất lượng tài liệu tổng thể là một phần, vì entry point mới đã giảm rủi ro. Không gọi tất cả tài liệu cũ sai hoặc vô dụng. Không sửa các file cũ trong nhiệm vụ này.

AGENTS.md và CLAUDE.md đúng pin byte-identical; đây là duplication có sẵn từ upstream. Không tự xóa/merge hai file hoặc gọi đó là lỗi thiết kế của dự án. Phân biệt tài liệu lịch sử cần giữ với sao chép trạng thái có thể lệch.

## 5. Bàn giao một phiên AI mới

**Có thể tìm được trên cùng máy nếu đọc đúng tuyến:** mục tiêu dev/test, pin, giới hạn chưa production, nơi source thực, launcher, ports, các hành động phá dữ liệu cần tránh, mẫu giao việc và bằng chứng test/review. Đây là đánh giá tài liệu, **chưa là một phép thử AI mới tiếp quản runtime hoàn chỉnh**.

**Chưa self-contained khi chỉ clone kho báo cáo trên máy khác:** không có source ứng dụng hoặc adapter build/run đã version-control; các runbook cũ trỏ đường dẫn tuyệt đối local; credentials không nằm trong repo theo chủ đích; hướng kiến trúc connector chưa chốt. Bộ năm báo cáo không thay bộ hướng dẫn tái lập môi trường.

AI mới không cần hỏi lại những điều đã có: source pin, mục tiêu dev/test, sự khác biệt source Windows/Linux, không mặc định Antigravity, không reset dữ liệu, report branch chưa merge. Nó cần đọc trước thay vì hỏi lại.

**Thông tin thực sự còn cần người dùng quyết định/cấp qua kênh phù hợp:**

- Zalo OA hay cá nhân, tài khoản/quyền API hợp lệ nào có sẵn, chức năng và tiêu chí nghiệm thu ưu tiên; không hỏi gửi token trong chat/repo.
- Chuẩn nghiệm thu nghiệp vụ: ai review/chấp nhận, phạm vi dữ liệu mẫu được dùng, có cho phép gửi tin thật ở lượt thử sau không.
- Khi nâng cấp: target release, thời gian gián đoạn chấp nhận, mức mất dữ liệu/khôi phục chấp nhận, dữ liệu cần bảo toàn và nơi backup phù hợp.
- Nếu mobile thành mục tiêu thực thi: thiết bị/OS, official hay custom app, push/distribution/branding và cặp server/mobile cần hỗ trợ.
- Phạm vi quyền cho thao tác hệ thống tiếp theo nếu chưa được cho phép trong nhiệm vụ cụ thể.

Repo đích đã được người dùng cho phép tạo ở lượt này: `trdat1605/chatwoot-vn`, private; không còn là câu hỏi đang chờ. Source runtime vẫn chỉ có remote upstream, không tự đổi thành repo private mới.

## 6. Quy trình: đã làm và mới viết

| Bước | Đã thực hiện có chứng cứ | Phần còn ở mức hướng dẫn/kế hoạch |
| --- | --- | --- |
| Yêu cầu/tiêu chí | Plans và tiêu chí môi trường/agent experiments | PRD/acceptance của Zalo chưa chốt |
| Nhánh/worktree | codex/wsl-migration và dev-environment có thật | Runtime project/ports/DB hiện cố định; không chứng minh parallel runtimes an toàn |
| Kiểm tra | Tests chọn lọc11/11, restore và HTTP/UI17/11, khảo sát 18/11 | Full suite, production regression, HMR edit, mobile/Zalo NOT_RUN |
| Review | Fresh-context reviews trước pha A/B/integration/C/legacyguard và review kết quả17/11 | Reviewer browser lịch sử chủ yếu xem ảnh/receipt, không tự chạy cùng toàn bộ UI |
| Chấp nhận/tích hợp | Có báo trạng thái và giới hạn cho migration | Chưa có một feature product đi qua GitHub PR + required checks + nghiệm thu nghiệp vụ |
| Bộ báo cáo hiện tại | Nhánh review/project-foundation, review docs và Draft PR khi bàn giao | Không merge trong nhiệm vụ này; không coi Draft PR là gate CI đã bảo vệ |

[AGENTS:72–77](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L72-L77) nêu worktree/branch/task, port/DB động và Overmind. Runtime này dùng Compose adapter có điều chỉnh; không có Procfile.worktree hoặc .codex/environments/environment.toml trên source Linux. Thiếu chúng không tự là lỗi runtime; cấu hình hiện chỉ được kiểm cho một project. Khi cần chạy task song song, phải chứng minh tách runtime/dữ liệu chứ không chỉ tách source.

[AGENTS build/test](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L1-L23), [CI CE pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/workflows/run_foss_spec.yml), [PR guidance](https://developers.chatwoot.com/contributing-guide) là quy ước tham chiếu. Không coi CE test hoặc prompt reviewer là bằng chứng Enterprise/UI đạt hay quyền reviewer bị cách ly. Các agent chia sẻ quyền máy; fresh context không bảo đảm lỗi độc lập.

## 7. Bảo trì và khôi phục

Có pin/history/hashes/backup và restore giới hạn. Chưa có diễn tập nâng cấp upstream hoặc rollback đủ source/config/schema/data/uploads/globals. [Báo cáo nâng cấp và tích hợp](upgrades-and-integrations.md) mô tả điều kiện và phần NOT_RUN, không áp dụng lệnh upgrade/reset trong lượt này.

## 8. Nguy cơ lãng phí công sức/token

| Nguy cơ có bằng chứng | Hệ quả có thể xảy ra | Điều chỉnh tối thiểu đề xuất |
| --- | --- | --- |
| Nhiều đoạn trạng thái khác ngày không supersede đồng bộ | AI lặp việc đã xong, suy lại quyết định hoặc dùng runbook cũ | Một trạng thái hiện hành, liên kết lịch sử và ngày thay thế |
| Hồ sơ ngoài Git, config ignored, đường tuyệt đối | Máy/AI mới phải tìm lại file hoặc xin người dùng nhắc lại | Entry point versioned, inventory phần local-only và context bàn giao |
| Copy nguyên Dockerfiles rồi sửa ít dòng | Khi upstream đổi phải so thủ công, dễ bỏ delta | Ghi baseline/delta và so trước đổi pin |
| Nhiều báo cáo dài/receipts cùng chủ đề | Nạp quá nhiều context hoặc bỏ sót giới hạn | Đọc theo nhiệm vụ, tham chiếu ID bằng chứng thay chép log |
| Quyết định Zalo chỉ mới lựa chọn trong chat/backlog | Code sai mục tiêu rồi phải làm lại | Chốt requirement/contract/acceptance trước triển khai |

Không có phép đo token/cost/time saved; không ước lượng phần trăm tiết kiệm. Không dùng ít file/agent hơn làm mục tiêu thay chất lượng. Bộ năm report là gói review theo yêu cầu, không phải đề xuất thay cấu trúc source hoặc chứng nhận nền móng đã hoàn thiện.
