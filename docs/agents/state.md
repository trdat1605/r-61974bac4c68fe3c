# Trạng thái hiện hành

Ngày: 18/11/2026. Coordinator: phiên Codex hiện tại. Đây là repo quản lý agent và bằng chứng, chưa chứa source ứng dụng.

- Baseline: PR1 head4f8ff1c24dedc926d3e24197728b5d92de8a61f3, còn Draft/open; không sửa báo cáo đó.
- App: v4.19.1/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82, codex/wsl-migration, source Linux và Docker Desktop trong profile; recheck Git sạch, sáu services chạy. Chưa có bằng chứng môi trường hay UI performance gaps của PR1 đã được xử lý.
- Agent tools: Codex CLI0.169.0-alpha.11.1; collaboration có trong phiên. Chưa thấy Claude CLI trong PATH; Antigravity file tồn tại nhưng chưa kiểm chức năng. Không triển khai Claude Team.
- Công việc agent-ops: chỉ dẫn ngắn, role briefs, phiếu, ownership và checks trên nhánh riêng. CLI loading và nhiệm vụ thật đã kiểm; PASS tooling tại059aef12 bị thay bằng BLOCK khi positive hook thật lộ Git-local env tác động nhầm kho điều phối; đã phục hồi, sửa ranh giới Git environment và review độc lập PASS tại af22b139 bằng actual positive/negative hook trong clone tạm, xem evidence/system-review.json và hook-incident-recovery.json. CI chưa chạy trước publish; không suy từ YAML.
- Runtime chung: read-only cho nhiệm vụ này; không restart/migration/tách DB/Redis hoặc đổi source bind.
- Nhiệm vụ thật AGENT-001 là workspace doctor đọc Git/Docker. Worker commit c10c00ad9a299d92d1a48eb43d5f8d37640d8bdd, reviewer khác đã chạy unit/live/negative và PASS đúng commit. [Handoff](../../tasks/AGENT-001/handoff.json), [review](../../tasks/AGENT-001/review.json). Spec giữ baseline; trạng thái tiếp tục nằm trong handoff, chưa chủ sản phẩm chấp nhận.
- Còn mở: source workspace của chat Windows khác appLinux; adapters runtime phần lớn ignored; đầy đủ upgrade/rollback/HMR/mobile/hiệu năng còn chưa nghiệm thu. Agent-ops chỉ phối hợp và chặn nhầm theo profile, không tự hoàn tất các việc đó.

## Cấu hình và bằng chứng hiệu lực

| Cấu hình | Cách được dùng | Bằng chứng / giới hạn |
| --- | --- | --- |
| AGENTS.md | Codex CLI mới ở root control repo tự nạp | evidence/codex-loading.json: đúng policy ID/entrypoint, chỉ agent_message, không gọi tool; chưa là thử write denial |
| roles.json + briefs | workflow.py brief đọc map/file, coordinator truyền rõ trong giao việc | Worker/reviewer đọc brief; rendering tiếng Việt đã chạy/test; không native auto-discovery |
| runtime.json | Doctor nhận --profile | Windows live HEALTHY và wrong-source BLOCKED/2; coordinator thêm live Ubuntu WSL, evidence/linux-doctor.json |
| ownership.py | Common Gitdir, claims hai file trước worker ghi | Unit tranh claim/cross-worktree/runtime/wrong-owner; đã release sau tích hợp/review, evidence/ownership-release.json; không OS enforcement |
| workflow.py | validate task và handoff exact commit/scope/receipt | Thật trả VALID/READY_FOR_OWNER; negative tests stale/self-review/changed evidence/FAIL/NOT_RUN |
| repository_check + hook | Checker có content/contract/tests; hook chỉ theo lệnh git -c | Negative commit bị chặn đúng missing acceptance, clean clone PASS tạic2fdd64: evidence/hook-portability.json. Không cài hook global/shared; positive commit đầu FAIL và đã recovery; bản sửa af22b139 qua actual clone positive/negative, config/index/tree/ngoại vi giữ đúng; evidence/hook-positive-isolated.json. Root positive commit ghi riêng sau thực hiện |
| GitHub workflow | File CI pin actions, quyền contents:read, không runtime access | Trước publish chưa có run; kết quả live xem Draft PR/checks và bằng chứng cập nhật, không tự là required check |

Tests mới nhất: Windows40/40; reviewer tự chạy actual commit hook trong clone tại af22b139 cũng40/40. Ubuntu trước đó37 cases với1 Windows-specific skip; bản40 còn chờ CI thực. Không dùng số lượng làm điểm chất lượng. Reviewer task ban đầu chạy15 doctor tests. Review toàn gói giữ các vòng BLOCK, PASS059 bị supersede bởi lỗi actual hook; sau xem lại ranh giới và recovery, PASS độc lập đúng af22b139. Không xóa lỗi cũ. Chưa có kết luận full product hoặc hiệu năng mới.

Fresh-context handover ở commit050c6ac đã tìm đúng mục tiêu/source/quyền/lệnh/trạng thái, tự chạy handoff READY_FOR_OWNER; evidence/fresh-handover.json giữ giới hạn lịch sử ấy. Không dùng lượt đó chứng minh gate sửa sau này. Thiếu URL PR/CI lúc thử được bổ sung sau publish. Recheck hiện trạng tạic2fdd64: doctor HEALTHY, source Linux và Windows cũ sạch, profile hash giữ nguyên; evidence/environment-check.json. Không là phép đo UI mới.

Các tài liệu lịch sử11/11 nói chưa có kho/chưa chạy app đã bị checkpoint hiện tại và PR1 thay thế trong phạm vi agent-ops. Không sửa hoặc xóa lịch sử ấy. Repo canonical mới là trdat1605/chatwoot-vn; runtime source vẫn có remote upstream riêng. Phiên mở riêng app chưa được chứng minh tự nạp policy control repo, nên điều phối phải truyền brief/context rõ.

Sau recovery và commit af22b139, coordinator chạy lại doctor HEALTHY, cả source Linux và Windows cũ sạch; shared core.hooksPath unset. Known local config phục hồi có giới hạn trong receipt, không tác động app/runtime. Kiểm trước publish không thấy path ngoài phạm vi, broken relative links hoặc selected secret patterns; evidence/prepublish-check.json.
