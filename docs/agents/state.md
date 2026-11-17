# Trạng thái hiện hành

Ngày: 18/11/2026. Coordinator: phiên Codex hiện tại. Đây là repo quản lý agent và bằng chứng, chưa chứa source ứng dụng.

- Baseline: PR1 head4f8ff1c24dedc926d3e24197728b5d92de8a61f3, còn Draft/open; không sửa báo cáo đó.
- App: v4.19.1/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82, codex/wsl-migration, source Linux và Docker Desktop trong profile; recheck Git sạch, sáu services chạy. Chưa có bằng chứng môi trường hay UI performance gaps của PR1 đã được xử lý.
- Agent tools: Codex CLI0.169.0-alpha.11.1; collaboration có trong phiên. Chưa thấy Claude CLI trong PATH; Antigravity file tồn tại nhưng chưa kiểm chức năng. Không triển khai Claude Team.
- Công việc agent-ops: đã có chỉ dẫn ngắn, role briefs, phiếu, ownership và checks trên nhánh riêng. CLI loading và nhiệm vụ thật đã kiểm; review toàn gói/hook/CI ở giai đoạn riêng, không suy từ file tồn tại.
- Runtime chung: read-only cho nhiệm vụ này; không restart/migration/tách DB/Redis hoặc đổi source bind.
- Nhiệm vụ thật AGENT-001 là workspace doctor đọc Git/Docker. Worker commit c10c00ad9a299d92d1a48eb43d5f8d37640d8bdd, reviewer khác đã chạy unit/live/negative và PASS đúng commit. [Handoff](../../tasks/AGENT-001/handoff.json), [review](../../tasks/AGENT-001/review.json). Spec giữ baseline; trạng thái tiếp tục nằm trong handoff, chưa chủ sản phẩm chấp nhận.
- Còn mở: source workspace của chat Windows khác appLinux; adapters runtime phần lớn ignored; đầy đủ upgrade/rollback/HMR/mobile/hiệu năng còn chưa nghiệm thu. Agent-ops chỉ phối hợp và chặn nhầm theo profile, không tự hoàn tất các việc đó.

## Cấu hình và bằng chứng hiệu lực

| Cấu hình | Cách được dùng | Bằng chứng / giới hạn |
| --- | --- | --- |
| AGENTS.md | Codex CLI mới ở root control repo tự nạp | evidence/codex-loading.json: đúng policy ID/entrypoint, chỉ agent_message, không gọi tool; chưa là thử write denial |
| roles.json + briefs | workflow.py brief đọc map/file, coordinator truyền rõ trong giao việc | Worker/reviewer đọc brief; rendering tiếng Việt đã chạy/test; không native auto-discovery |
| runtime.json | Doctor nhận --profile | Windows live HEALTHY và wrong-source BLOCKED/2; coordinator thêm live Ubuntu WSL, evidence/linux-doctor.json |
| ownership.py | Common Gitdir, claims hai file trước worker ghi | Unit tranh claim/cross-worktree/runtime/wrong-owner; cooperative, không OS enforcement |
| workflow.py | validate task và handoff exact commit/scope/receipt | Thật trả VALID/READY_FOR_OWNER; negative tests stale/self-review/changed evidence/FAIL/NOT_RUN |
| repository_check + hook | Checker có content/contract/tests; hook chỉ theo lệnh git -c | Chưa cài hook global/shared Git config. Kết quả lệnh commit có hook phải ghi riêng khi thực hiện |
| GitHub workflow | File CI pin actions, quyền contents:read, không runtime access | Trước publish chưa có run; kết quả live xem Draft PR/checks và bằng chứng cập nhật, không tự là required check |

Tests coordinator đã chạy: Windows33/33, Ubuntu33 cases với1 Windows-specific skip; không dùng số lượng làm điểm chất lượng. Reviewer task ban đầu chạy15 doctor tests, không gắn nhãn họ đã chạy toàn framework. Chưa có kết luận full product hoặc hiệu năng mới.

Các tài liệu lịch sử11/11 nói chưa có kho/chưa chạy app đã bị checkpoint hiện tại và PR1 thay thế trong phạm vi agent-ops. Không sửa hoặc xóa lịch sử ấy. Repo canonical mới là trdat1605/chatwoot-vn; runtime source vẫn có remote upstream riêng. Phiên mở riêng app chưa được chứng minh tự nạp policy control repo, nên điều phối phải truyền brief/context rõ.
