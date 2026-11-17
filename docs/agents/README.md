# Bắt đầu vận hành AI coding agent

Ngày thiết lập: 18/11/2026. Trạng thái triển khai/kiểm chứng hiện tại xem [state.md](state.md), không suy từ việc có các file.

1. Đọc AGENTS.md của repo điều phối và [operating-model.md](operating-model.md).
2. Định vị source/runtime bằng `config/agents/runtime.json` và phiếu việc. Repo app đang chạy khác repo này. Khi làm ở app đọc AGENTS/override tại app.
3. Chọn tuyến: khảo sát và quyết định tại [sources.md](sources.md); giao việc tại `tasks/<id>/task.json`; roles Codex tại `agents/codex/roles.json` và các brief. Các brief được đọc rõ trong giao việc, không là native role tự phát hiện của Claude hoặc Codex.
4. Kiểm script/commands và bằng chứng ở từng phiếu; dùng PASS/FAIL/NOT_RUN. Không tự thao tác runtime dùng chung.
5. Handoff ghi đúng commit, checks, reviewer và next step; chủ sản phẩm còn quyết định cuối. Chưa merge.

[PR nền móng #1](https://github.com/trdat1605/chatwoot-vn/pull/1) là baseline. Nhánh agent-ops dựa trên head PR1 để tái dùng báo cáo, không sửa năm báo cáo lịch sử đó. Draft PR mới phụ thuộc PR1, không merge PR1 trong nhiệm vụ này.

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

Hook gọi repository_check, chặn khi staged/working khác hoặc contract/checks không đạt. Dùng Git trực tiếp hoặc no-verify có thể bỏ qua; CI cũng chưa là required check. Không gọi hai cơ chế này là chính sách quản trị không thể vượt. Trạng thái hook/CI đã thực chạy xem state và evidence, không suy từ file tồn tại.

## Bàn giao và tiếp tục

- [Phiếu thật](../../tasks/AGENT-001/task.json), [handoff](../../tasks/AGENT-001/handoff.json), [review](../../tasks/AGENT-001/review.json) và `tasks/AGENT-001/evidence/` dùng đường dẫn từ root repo; các link tương đối chính xác nằm dưới.
- [Task AGENT-001](../../tasks/AGENT-001/task.json) mô tả đầy đủ các trường cần có; không thay giá trị/ref của việc cũ để dùng cho việc mới.
- [Đánh giá và giới hạn](evaluation.md); [quyết định vận hành](decisions/0001-agent-operation.md).

Profile hiện tại gắn lab máy gốc. Máy khác phải khảo sát/profile riêng, không coi doctor BLOCKED là lý do bỏ guard. Từ một chat mở riêng ở source app, chính sách repo điều phối chưa được chứng minh tự nạp; coordinator phải truyền brief và chỉ dẫn rõ. Không thay global config hoặc override upstream để giả việc này đã hoàn tất.
