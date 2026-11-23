# Bắt đầu vận hành AI coding agent

**Công việc hiện hành:** [COMPLETE-001](../development/completion.md),
[checkpoint máy đọc](../../tasks/COMPLETE-001/evidence/checkpoint.json).
Đọc trạng thái này trước các kết quả lịch sử dưới đây. Bài so sánh Codex và pilot
app là hai phép kiểm khác nhau; nguồn ứng dụng vẫn ở repo riêng. Runtime lab/course
chỉ đọc; không chạy ví dụ build local khi C dưới ngưỡng 15 GiB. Docker sang D mới
là [phương án chuẩn bị](../runbooks/docker-storage-migration.md).

Ngày thiết lập: 18/11/2026. [README dự án](../../README.md) là cửa vào chung; [trạng thái dự án](../status.md) là bản tóm tắt hiện hành. [state.md](state.md) giữ checkpoint agent ngày 18/11 và bằng chứng theo revision, không suy từ việc có các file.

1. Đọc AGENTS.md của repo điều phối và [operating-model.md](operating-model.md).
2. Định vị source/runtime bằng `config/agents/runtime.json` và phiếu việc. Repo app đang chạy khác repo này. Khi làm ở app đọc AGENTS/override tại app.
3. Chọn [tuyến theo việc](../knowledge/reading-routes.md) và điền [gói ngữ cảnh](../knowledge/context-packet.md). Nguồn khảo sát ngày 18/11 tại [sources.md](sources.md), nguồn bổ sung/tài liệu người dùng tại [thư viện](../knowledge/README.md). Giao việc tại `tasks/<id>/task.json`; roles Codex tại `agents/codex/roles.json` và các brief. Các brief được đọc rõ trong giao việc, không là native role tự phát hiện của Claude hoặc Codex.
4. Kiểm script/commands và bằng chứng ở từng phiếu; dùng PASS/FAIL/NOT_RUN. Không tự thao tác runtime dùng chung.
5. Handoff ghi đúng commit, checks, reviewer và next step; chủ sản phẩm còn quyết định cuối. Chưa merge.

Công việc sản phẩm dùng [G1–G10](../development/product-workflow.md), [tracker bảy cải tiến](../development/improvement-tracker.md) và [pilot](../development/pilot.md). Issue là nơi giữ yêu cầu; task giữ brief/phạm vi/checks, PR giữ diff và bằng chứng đúng bản. Công cụ `product_check.py plan|verify|pr` bổ sung traceability; không thay test app, quyền GitHub hoặc core handoff gate. Giới hạn rulesets private đã được ghi tại FLOW-001; PUB-001 chuyển hai kho sang public theo quyết định riêng, GOV-001 xử lý [main rules và kiểm chứng](../development/branch-protection.md). Xem [publication](../development/repository-publication.md) và [review/merge](../development/review-and-merge.md).

[PR nền móng #1](https://github.com/trdat1605/r-61974bac4c68fe3c/pull/1) là baseline. Nhánh agent-ops dựa trên head PR1 để tái dùng báo cáo, không sửa năm báo cáo lịch sử đó. Draft PR mới phụ thuộc PR1, không merge PR1 trong nhiệm vụ này.

[Draft PR agent-ops #2](https://github.com/trdat1605/r-61974bac4c68fe3c/pull/2) dùng base `review/project-foundation`. [CI đầu tiên của PR](https://github.com/trdat1605/r-61974bac4c68fe3c/actions/runs/44165473970) đã đạt tại head70a0df6; bản chứng cứ ghi riêng commit checkout thực. Kết quả các revision mới hơn xem checks trong PR, không suy từ kết quả cũ.

## Lệnh dùng từ root repo điều phối

Yêu cầu Python 3.10+ và Git; máy đã thử dùng Python Windows3.13.5. Không cần cài package Python ngoài standard library. Repo này dùng Git Windows, không dùng Git Linux để đọc metadata worktree trỏ đường dẫn Windows.

```text
python -B tools/agents/workflow.py validate --task tasks/AGENT-001/task.json
python -B tools/agents/workflow.py brief --role implementer --task tasks/AGENT-001/task.json
python -B tools/agents/ownership.py status --repo .
python -B tools/agents/workspace_doctor.py --profile config/agents/runtime.json
python -B tools/agents/workflow.py handoff --task tasks/AGENT-001/task.json --handoff tasks/AGENT-001/handoff.json --review tasks/AGENT-001/review.json
python -B tools/agents/repository_check.py --require-handoffs
```

Để giao việc: coordinator đọc output brief và truyền cho công cụ collaboration đang có; reviewer dùng context mới và nhận exact commit. Script brief không tự gọi model/tạo agent và không cấp quyền. Role definitions được nạp rõ qua cách này, không giả auto-discovery.

Claim ví dụ cho một việc mới (đổi owner và exact path cho đúng phiếu):

```text
python -B tools/agents/ownership.py claim --repo . --owner TASK-ID --resource file:relative/file.py
python -B tools/agents/ownership.py release --repo . --owner TASK-ID --resource file:relative/file.py
```

Chỉ dùng file paths chính xác, không glob/subtree; các phiên phải dùng cùng common Gitdir để thấy cùng claims. Không có lease tự hết hạn: nếu gián đoạn, coordinator kiểm người thực hiện/process/worktree rồi mới release đúng owner; không xóa lock vì thấy lâu. Runtime write dùng key `runtime:<project>` chỉ khi phiếu và quyền cho phép. Claims không tách hoặc cấp tài nguyên.

Git hook được version-control và có thể gọi theo từng lệnh, không sửa cấu hình chung của các worktree khác:

```text
git -c core.hooksPath=.githooks commit -m "type(scope): description"
```

Hook này dành cho commit bàn giao/tích hợp đã có review, không phải commit implementation đầu tiên chưa thể có review exact commit. Implementation tạo commit trên nhánh riêng sau checks; bước bàn giao sau đó mới dùng hook có --require-handoffs.

Hook kiểm toàn index so với các file working được tests đọc, gồm deletion; chặn snapshot khác nhau hoặc contract/checks không đạt. Dùng Git trực tiếp/no-verify có thể bỏ qua; CI chưa là required check. Không gọi đây là chính sách quản trị không thể vượt. Trạng thái hook/CI thực chạy xem state/evidence.

Repository checker còn yêu cầu task/handoff/review và mọi receipt được dùng phải có trong index. Một tệp bằng chứng chỉ có trên máy sẽ bị chặn. Lệnh handoff riêng là phép chẩn đoán hồ sơ; để bàn giao phải chạy repository checker. Gate chưa tạo môi trường test kín hoàn toàn hoặc xác thực lời khai trong receipt.

Hook truyền các biến Git-local vào tiến trình con. Checker giữ chúng để đọc đúng index đang commit, nhưng loại danh sách từ `git rev-parse --local-env-vars` khỏi môi trường unit tests; Git fixtures cũng dùng bản môi trường đã làm sạch trước lệnh Git đầu tiên. Không gọi Git tại kho thử chỉ bằng `git -C` mà vẫn giữ các biến của kho gọi hook. Đây là xử lý ngữ cảnh Git, không là sandbox hệ điều hành.

Phiếu khai báo `bound_inputs` cho cấu hình/tệp ảnh hưởng kết quả. Handoff và review cùng ghi SHA256 các input tại subject commit. Gate toàn repo giữ review lịch sử, rồi chọn owner review mới nhất theo Git ancestry cho từng code/input path; bytes hiện tại phải khớp. Sau này sửa cùng tệp cần task/review mới, không sửa receipt cũ hoặc khóa nó mãi ở HEAD cũ. Lệnh handoff có `--historical` chỉ trả REVIEW_RECORD_VALID cho hồ sơ cũ, không READY_FOR_OWNER.

## Bàn giao và tiếp tục

- [Phiếu thật](../../tasks/AGENT-001/task.json), [handoff](../../tasks/AGENT-001/handoff.json), [review](../../tasks/AGENT-001/review.json) và `tasks/AGENT-001/evidence/` dùng đường dẫn từ root repo; các link tương đối chính xác nằm dưới.
- [Task AGENT-001](../../tasks/AGENT-001/task.json) mô tả đầy đủ các trường cần có; không thay giá trị/ref của việc cũ để dùng cho việc mới.
- [Đánh giá và giới hạn](evaluation.md); [quyết định vận hành](decisions/0001-agent-operation.md).

Profile hiện tại gắn lab máy gốc. Máy khác phải khảo sát/profile riêng, không coi doctor BLOCKED là lý do bỏ guard. Từ một chat mở riêng ở source app, chính sách repo điều phối chưa được chứng minh tự nạp; coordinator phải truyền brief và chỉ dẫn rõ. Không thay global config hoặc override upstream để giả việc này đã hoàn tất.
