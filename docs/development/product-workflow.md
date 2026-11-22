# Quy trình cho công việc sản phẩm Chatwoot

Áp dụng đề xuất của dự án ngày **23/11/2026**, [issue đầu mối #5](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/5), task `FLOW-001`. Tài liệu và tooling trên nhánh đang review; chưa được chủ sản phẩm chấp nhận trên main. Đây là quy trình cho app ở repo riêng; CI kho điều phối không chứng minh app đã đạt.

## Từ yêu cầu tới bàn giao

| Cổng | Owner / đầu vào | Đầu ra cần có để đi tiếp |
| --- | --- | --- |
| G1 — Yêu cầu → issue | Coordinator dùng quyết định đã có của chủ sản phẩm | Issue thật: hành vi hiện tại/mong muốn, use case hoặc reproduce, scope/ngoài scope, acceptance có ID và rủi ro. Chỉ hỏi lại phần thiếu ảnh hưởng quyết định |
| G2 — Issue → khảo sát | Agent nhận brief đúng repo/ref, chỉ dẫn và tuyến đọc | Nguồn chính thức đã đọc, code/file:dòng theo commit, phụ thuộc, điều chưa xác minh. Chưa đủ API/quyền thì ghi thiếu, không hứa khả năng |
| G3 — Khảo sát → phương án/task | Coordinator và người thực hiện; reviewer khác khi thiết kế/runtime ảnh hưởng đáng kể | Phương án, lý do/đánh đổi, task phạm vi rõ, từng acceptance gắn checks, quyền runtime, ownership và kế hoạch rollback. Chưa đạt source/test prerequisites thì dừng ghi code |
| G4 — Task → implementation | Một owner ghi mỗi scope, nhánh/worktree theo việc | Đúng app checkout, nhận diện delta, môi trường tách hoặc quyền dùng chung đã chốt; commit ứng dụng riêng với commit control |
| G5 — Implementation → evidence | Implementer chạy checks theo ảnh hưởng | Command/bước thao tác, app subject SHA, environment, PASS/FAIL/NOT_RUN và artifact đã làm sạch cho từng acceptance. Bug cần regression bắt được lỗi; UI/API/mobile/integration thử theo vùng ảnh hưởng |
| G6 — Evidence → review | Reviewer ngữ cảnh mới nhận yêu cầu/base/subject/diff/input hashes và nguồn | Review đúng app commit, finding có trigger/impact/location/căn cứ/cách xác minh. Sửa hoặc phản hồi có căn cứ; sau ba vòng chưa hội tụ xem lại hướng |
| G7 — Review → PR | Coordinator giữ source/handoff đồng nhất | Full issue URL, `Task: tasks/ID/task.json`, app repo/SHA, product How to test, risk/rollback, review và evidence. PR mới đầu có thể Draft/CI đỏ khi chưa đủ hồ sơ; không nới strict gate để giả xanh |
| G8 — PR → chấp nhận | Reviewer kiểm bản cuối; chủ sản phẩm có quyền quyết định | CI sản phẩm/checks áp dụng thực chạy, source head đúng bản review, phụ thuộc/base được kiểm tổ hợp, findings được xử lý. Required checks phía GitHub có trạng thái thực riêng |
| G9 — Chấp nhận → merge/phát hành | Nhiệm vụ có quyền riêng | Nhánh đích và merge/release SHA, môi trường, kiểm sau triển khai và người chịu trách nhiệm. Merge không tự đồng nghĩa đã phát hành; chưa được phép thì ghi NOT_RUN |
| G10 — Đóng việc/tiếp quản | Owner và coordinator | Issue có kết quả/giới hạn, tài liệu cập nhật, quyết định và việc còn mở. Không đóng issue chỉ vì code đã viết hoặc tooling xanh |

## Agent đọc và làm việc với nhau

Đọc AGENTS thực tại nơi làm, README/trạng thái/task, rồi chọn [tuyến R-xx](../knowledge/reading-routes.md) và điền [gói ngữ cảnh](../knowledge/context-packet.md). Khảo sát Zalo có thể tách API nhà cung cấp và điểm mở rộng Chatwoot; implementer chỉ bắt đầu khi đầu vào cần thiết đã bàn giao. Backend/frontend chỉ ghi song song khi scope và hợp đồng đủ tách. Reviewer tự lần phụ thuộc, không chỉ lặp danh sách implementer.

Thông điệp quan trọng phải nối về issue/task/commit hoặc quyết định trong PR. Chat không là bản lưu duy nhất. File claim là phối hợp tự nguyện, không phải OS sandbox; worktree không tách DB/Redis/volume. [Mô hình agent hiện có](../agents/operating-model.md), [căn cứ và eval cần có](agent-selection.md).

## Hai repo và ba loại kiểm

- **Control repo:** `trdat1605/r-61974bac4c68fe3c` lưu task/handoff/review và công cụ; `workflow.py` xác minh commit của repo này.
- **App repo:** [source Chatwoot](https://github.com/trdat1605/s-251521f7e9131fb0) giữ source ứng dụng; app base/subject phải được kiểm bằng Git của app. Không thay app SHA bằng control SHA.
- **Governance CI:** kiểm hợp đồng/hashes/tools của control. **Product evidence checker:** kiểm tính nhất quán app Git và hồ sơ. **Product CI/runtime tests:** chạy ứng dụng/tests thật. Ba loại không thay nhau.

Tên kho hiện hành theo [PUB-001](repository-publication.md); công cụ dùng map ID/alias đã khai báo để đọc hồ sơ tên cũ. Tài liệu/task/evidence lịch sử không được viết lại.

## Công cụ và giới hạn

```text
python -B tools/agents/product_check.py plan --record docs/development/product-record.example.json
python -B tools/agents/product_check.py verify --record RECORD.json --repo CONTROL_ROOT --source-repo APP_ROOT
python -B tools/agents/product_check.py pr --repo . --expected-repository trdat1605/r-61974bac4c68fe3c
```

`plan` chỉ trả `PLAN_VALID`; mẫu là ví dụ, chưa đủ nội dung nghiệp vụ để giao code. `verify` yêu cầu app origin/ref/HEAD/tracked bytes phù hợp, không dùng assume-unchanged/skip-worktree hoặc sparse checkout để che kiểm tra; receipts đã commit đúng app repo/subject/criteria/hash/command, checks PASS và review khác implementer. Đây là kiểm current checkout và tính nhất quán, không attestation danh tính hoặc sự thật của mọi receipt. Không kiểm toàn bộ untracked/ignored files. Chưa có product task thật đạt verify thì ghi NOT_RUN; tests fixture không tính là pilot app.

`pr` dùng API GET cố định `api.github.com` để kiểm issue thật, không nhầm `/pull/`, và task link trong checkout. Nó không kiểm đầy đủ nội dung yêu cầu/nghiệp vụ, không tự cấp quyền merge. Với app PR ở repo khác, phải thiết lập đường kiểm riêng phù hợp; job của control không tự kiểm app PR.

Legacy task/handoff/review giữ nguyên. Phiếu dự kiến có thể nằm ở issue trước khi có reviewed implementation; strict repository handoff gate vẫn chặn thiếu hồ sơ khi được gọi. Không hạ status để bỏ review.

## Căn cứ và điều chỉnh

[Chatwoot PR guidelines](https://www.chatwoot.com/hc/handbook/articles/pull-request-guidelines-32), trang cập nhật 17/04/2023, hỗ trợ issue/owner/tests/docs. [AGENTS ở app pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md) và [PR template cùng pin](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/PULL_REQUEST_TEMPLATE.md) có khác biệt về test/format: dự án giao rõ regression/checks cần thiết, giữ product How to test, dẫn automated outputs sang evidence. Các cổng G1–G10 là điều chỉnh của dự án, chưa là kết quả hoàn thành.

[Bài nhóm Claude Code ngày 15/10/2026](https://claude.dev/blog/solving-code-review-at-anthropic/) là căn cứ cho executable verification, fresh review và trách nhiệm theo rủi ro; không chuyển kết quả nội bộ của họ sang lab. [GitHub issue–PR](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) chỉ áp closing keywords ở default branch: PR stack hiện tại dùng full links để theo dõi, chưa tự đóng issue.
