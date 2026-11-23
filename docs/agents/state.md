# Checkpoint vận hành agent ngày 18/11/2026

**Nhãn bổ sung 23/11:** đây là checkpoint lịch sử theo các revision nêu dưới. Trạng thái tổng thể mới xem [status.md](../status.md); nơi lưu bản chính xem [project-map.md](../project-map.md). Giữ nội dung cũ để truy vết, không suy toàn bộ vẫn là hiện trạng hôm nay.

Ngày: 18/11/2026. Coordinator: phiên Codex hiện tại. Đây là repo quản lý agent và bằng chứng, chưa chứa source ứng dụng.

- Baseline: PR1 head4f8ff1c24dedc926d3e24197728b5d92de8a61f3, còn Draft/open; không sửa báo cáo đó.
- App: v4.19.1/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82, codex/wsl-migration, source Linux và Docker Desktop trong profile; recheck Git sạch, sáu services chạy. Chưa có bằng chứng môi trường hay UI performance gaps của PR1 đã được xử lý.
- Agent tools: Codex CLI0.169.0-alpha.11.1; collaboration có trong phiên. Chưa thấy Claude CLI trong PATH; Antigravity file tồn tại nhưng chưa kiểm chức năng. Không triển khai Claude Team.
- Công việc agent-ops: chỉ dẫn ngắn, role briefs, phiếu, ownership và checks trên nhánh riêng. CLI loading và nhiệm vụ thật đã kiểm; PASS tooling tại059aef12 bị thay bằng BLOCK khi positive hook thật lộ Git-local env tác động nhầm kho điều phối; đã phục hồi, sửa ranh giới Git environment và review độc lập PASS tại af22b139 bằng actual positive/negative hook trong clone tạm, xem evidence/system-review.json và hook-incident-recovery.json. Metadata70a0df6 được review riêng; CI thực đã đạt tại revision đó, không suy từ YAML.
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
| repository_check + hook | Checker có content/contract/tests; hook chỉ theo lệnh git -c | Negative/clone proof giữ trong hook-portability.json và hook-positive-isolated.json. Root positive hook đã tạo đúng metadata commit70a0df6 với40tests, config bytes/parent/tree đúng, không fixture paths: evidence/hook-positive-root.json. Giữ cả failure/recovery cũ. Không cài shared/global hook |
| GitHub workflow | File CI pin actions, quyền contents:read, không runtime access | PR và push runs tại70a0df6 đều success: evidence/ci-initial.json. Ubuntu40cases,1 Windows-only skip. Chưa là required check; kết quả revision mới hơn xem PR |

Tests: Windows40/40; reviewer tự chạy actual commit hook trong clone tại af22b139 cũng40/40. CI Ubuntu24.04/Python3.13 tại70a0df6 chạy40cases,1 Windows-specific skip, success; không gọi case skip là đã chạy. Không dùng số lượng làm điểm chất lượng. Reviewer task ban đầu chạy15 doctor tests. Review toàn gói giữ các vòng BLOCK, PASS059 bị supersede bởi lỗi actual hook; sau xem lại ranh giới và recovery, PASS độc lập đúng af22b139. Không xóa lỗi cũ. Chưa có kết luận full product hoặc hiệu năng mới.

Fresh-context handover ở commit050c6ac đã tìm đúng mục tiêu/source/quyền/lệnh/trạng thái, tự chạy handoff READY_FOR_OWNER; evidence/fresh-handover.json giữ giới hạn lịch sử ấy. Không dùng lượt đó chứng minh gate sửa sau này. Thiếu URL PR/CI lúc thử nay bổ sung dưới đây. Recheck hiện trạng tạic2fdd64: doctor HEALTHY, source Linux và Windows cũ sạch, profile hash giữ nguyên; evidence/environment-check.json. Không là phép đo UI mới.

Các tài liệu lịch sử11/11 nói chưa có kho/chưa chạy app đã bị checkpoint hiện tại và PR1 thay thế trong phạm vi agent-ops. Không sửa hoặc xóa lịch sử ấy. Repo canonical mới là trdat1605/chatwoot-vn; runtime source vẫn có remote upstream riêng. Phiên mở riêng app chưa được chứng minh tự nạp policy control repo, nên điều phối phải truyền brief/context rõ.

Sau recovery và commit af22b139, coordinator chạy lại doctor HEALTHY, cả source Linux và Windows cũ sạch; shared core.hooksPath unset. Known local config phục hồi có giới hạn trong receipt, không tác động app/runtime. Kiểm trước publish không thấy path ngoài phạm vi, broken relative links hoặc selected secret patterns; evidence/prepublish-check.json.

## Nơi bàn giao

- [Draft PR #2](https://github.com/trdat1605/chatwoot-vn/pull/2), base `review/project-foundation`, liên kết PR #1; cả hai còn Draft/open, chưa merge.
- [PR CI tại70a0df6](https://github.com/trdat1605/chatwoot-vn/actions/runs/44165473970) và [push CI cùng head](https://github.com/trdat1605/chatwoot-vn/actions/runs/44165446555) đã success. Receipt phân biệt headSha với commit checkout thực của PR merge ref.
- Bản cập nhật URL/chứng cứ cuối là metadata; kiểm kết quả mới nhất trong checks của PR. Không liên tục commit receipt của chính commit chứa nó: mỗi receipt ghi revision đã thực chạy, tránh vòng tự tham chiếu.
- Chờ chủ sản phẩm review/chấp nhận quy trình; quyền required checks/merge/phát hành và backlog workspace/adapters/UI/Zalo chưa tự quyết.
