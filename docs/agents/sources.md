# Nguồn, phiên bản và phạm vi áp dụng

Ngày đọc/kiểm: **18/11/2026**. Đã mở và đọc nội dung các URL, không chỉ dựa search snippets. Docs live không có ngày cập nhật phải hiểu là nội dung tại ngày đọc, không snapshot của phiên bản CLI.

## Chatwoot: yêu cầu ở source ứng dụng

Server v4.19.1 / `caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82`.

- [AGENTS build/test](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L1-L23), [worktree](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L72-L77), [Enterprise](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md#L119-L135).
- [CONTRIBUTING](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/CONTRIBUTING.md), [CI](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/workflows/run_foss_spec.yml), [Playwright](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/tests/playwright/README.md).

Giữ branch/worktree theo task, tests/lint theo phần ảnh hưởng, tương thích core/Enterprise. Không cài Rails vào repo điều phối chỉ để có tên command. Adapter Compose hiện khác mô tả Overmind; chưa chứng minh parallel runtime. Không sửa cấu trúc app trong nhiệm vụ này.

[PR guidelines](https://www.chatwoot.com/hc/handbook/articles/pull-request-guidelines-32), [upgrade](https://developers.chatwoot.com/self-hosted/deployment/upgrade), [backup](https://developers.chatwoot.com/self-hosted/deployment/backup) là docs live, không cùng snapshot source. Chúng hỗ trợ self-review/QA, đọc release notes và bảo toàn code/config/data/storage; không chứng minh dự án đã thử upgrade. Không pull/update server.

## Anthropic: nguyên tắc có thể học và tính năng riêng của Claude

| Nguồn / mục đã đọc | Nguồn thực sự nói | Điều chỉnh dự án và giới hạn |
| --- | --- | --- |
| [Large codebases](https://claude.com/resources/articles/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start), 14/05/2026; harness/configuration patterns/ownership | Chỉ dẫn ngắn, phân tầng và workflow theo nhu cầu, trách nhiệm cấu hình rõ | Root AGENTS + index/briefs; không suy hiệu quả Codex từ quan sát Claude |
| [Admin setup](https://code.claude.com/docs/en/admin-setup); settings reach devices/enforce/data handling | Claude có managed settings, tools, sandbox, MCP, hooks và precedence | Phân biệt prompt với quyền thực; không áp cú pháp Claude sang Codex |
| [Subagents](https://code.claude.com/docs/en/sub-agents); main vs subagent/permissions/context | Việc khép kín phù hợp giao subagent; công cụ, memory và permissions là của Claude; docs hiện có một số subagents nhắn nhau | Kiểm Codex theo công cụ thật; không khẳng định subagent chỉ báo caller hoặc có cùng quyền |
| [Agent teams](https://code.claude.com/docs/en/agent-teams); compare/claim tasks/conflicts/limitations | Experimental, tắt mặc định; task-claim locking không khóa code/runtime | Không triển khai Claude Team; exact file/runtime claims là cơ chế riêng của dự án |
| [Best practices](https://code.claude.com/docs/en/best-practices); deterministic instructions/check to run/review against spec | Prompt không bảo đảm tuân thủ; review theo spec với context riêng và evidence | Chuyển phần cơ học sang validator/tests/CI; slash commands/hooks Claude không tự có ở đây |
| [Long-running harnesses](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), 26/11/2025; environment/progress/testing/getting up to speed | Thí nghiệm initializer/coding sessions, task list/progress/Git để bàn giao | Phiếu/ref/state và nhiệm vụ thật; không gọi bài là benchmark lab này |
| [Demystifying evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), 09/01/2026; task/trial/transcript/outcome/first evals | Chấm trạng thái thật; deterministic graders khi phù hợp, đọc transcript | Negative tests cho sai source/stale review/claims; số lượng test không thay chất lượng |

Cả bảy URL đọc được, không thấy redirect trong lượt khảo sát. Docs không hiển thị ngày cập nhật thì không tự đặt ngày. Chưa thử Claude features. Mô hình trách nhiệm/trạng thái là quyết định dự án, không là tiêu chuẩn doanh nghiệp được nguồn chứng nhận.

## Codex: kiểm theo công cụ thật

CLI hiện `codex-cli 0.169.0-alpha.11.1`, binary WindowsApps desktop26.1111.2228.0. WSL command codex cũng trỏ binary Windows qua /mnt/c, không là Linux native. Python Windows3.13.5; Git/GitHub CLI có thật. Không thấy Claude CLI trong PATH. Antigravity file metadata2.32.1 nhưng chưa thử chức năng, không mặc định tham gia đội.

Collaboration tools của phiên: spawn/followup/send/wait/list; bốn slot tổng theo môi trường. Fresh-context readers/implementer đã được gọi; đó không là sandbox riêng. Parser config allowlist chỉ thấy features js_repl=false/fast_mode=true, không thấy agents/profiles/hooks khai báo ở config đã kiểm. Không đọc/in auth.json, endpoint credentials hoặc toàn config.

Đã đọc skill openai-docs và lấy manual chính thức vào cache tạm ngày18/11. Các URL developers.openai.com được dùng chuyển sang ChatGPT Learn. [AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) mô tả global/repo/cwd, override và giới hạn kích thước. [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) hỗ trợ phân công theo brief. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) có hooks/roles, nhưng docs live và actual alpha không mặc định tương đương.

CLI help xác nhận exec --ephemeral, --sandbox read-only và --json. Probe loading/sandbox phải có evidence riêng; không dùng --trust hoặc bỏ sandbox để ép thành công. Role briefs của dự án được đọc rõ, không tự giả native role discovery. Git hook và GitHub CI là cơ chế khác native Codex hooks.

[actions/checkout](https://github.com/actions/checkout) và [setup-python](https://github.com/actions/setup-python) được đọc từ nguồn chính thức; CI pin commit refs đã tra API và fetch history để kiểm handoff theo commit. Không tự bật required checks, cấp quyền hoặc merge.
