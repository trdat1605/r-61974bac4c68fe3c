# Mô hình vận hành

Ngày quyết định: 18/11/2026. [Nguồn](sources.md), [baseline PR1](https://github.com/trdat1605/chatwoot-vn/pull/1). Đây là áp dụng riêng trên Codex, không cài nguyên hệ thống Claude.

## So sánh và lựa chọn

| Mô hình | Khi phù hợp | Giới hạn |
| --- | --- | --- |
| Một implementer tuần tự, review ở ngữ cảnh riêng | Cùng tệp/runtime hoặc nhiều phụ thuộc | Người thực hiện không tự ký review độc lập |
| Coordinator + subagents theo nhiệm vụ | Khảo sát độc lập, implementer sở hữu phạm vi, reviewer nhận bản ổn định | Phải giao đủ brief/ref và thu bằng chứng; không tăng agent chỉ để đặt chức danh |
| Nhiều phiên/team | Các phần độc lập, cần đối thoại và tài nguyên đã kiểm | Claude Agent teams là tính năng thử nghiệm của Claude, chưa triển khai ở đây; worktrees không tách runtime |

Chọn coordinator + subagents, tuần tự hóa ghi cùng phạm vi/runtime. Chọn theo phụ thuộc và khả năng kiểm chứng, không tối ưu số token hoặc số agent. Bốn slot là giới hạn của phiên, không quy mô tối ưu.

## Trách nhiệm và quyết định

| Trách nhiệm | Có thể làm | Không tự quyết |
| --- | --- | --- |
| Chủ sản phẩm | Nhu cầu, ưu tiên, tiêu chí nghiệp vụ, chấp nhận cuối | Chấp nhận nghiệp vụ không thay bằng chứng kỹ thuật còn thiếu |
| Điều phối | Phân việc, kiểm phụ thuộc/claims, tổng hợp, tích hợp local đã review | Không tự merge PR/phát hành, mở quyền hoặc thay tiêu chí |
| Khảo sát/kiến trúc | Nguồn đúng ref, phương án và tác động | Không gọi đề xuất là đã triển khai/đo kiểm |
| Implementer | Ghi đúng scope/worktree, kiểm tra, bàn giao commit | Không tự review độc lập hoặc thao tác runtime khác phiếu |
| Verifier/reviewer | Đối chiếu spec/diff/ref và kết quả, báo lỗi có căn cứ | Không sửa đối tượng review rồi tự chấp nhận |
| Tích hợp/phát hành | Tích hợp local, kiểm tổ hợp, chuẩn bị PR | Merge/phát hành cần quyết định riêng của chủ sản phẩm |

`READY_FOR_OWNER` chỉ là sẵn sàng để người dùng quyết định khi đủ checks/review áp dụng. Không dùng Done hoặc tests pass đơn lẻ. PR nhiệm vụ này vẫn Draft, chưa merge.

## Trình tự

1. Đọc state/task và nguồn theo tuyến; kiểm repo/ref/runtime. Không giả định các việc source/config/UI/performance của PR1 đã xong.
2. Phiếu JSON ghi mục tiêu, repo/branch/base, application ref, acceptance, scope/ảnh hưởng, phụ thuộc/điều kiện bắt đầu, môi trường/quyền, checks/evidence, điều kiện dừng và receiver. Task AGENT-001 là mẫu thực, không sao chép nguyên giá trị cho việc khác.
3. Một implementer trên worktree/branch riêng, giữ exact file claims qua common Git directory. Claims là phối hợp tự nguyện có kiểm tra, không khóa editor không sử dụng helper.
4. Runtime là tài nguyên riêng. Nhiệm vụ này read-only. Việc tương lai cần ghi runtime phải có người phụ trách/quyền/exclusive claim; chạy song song phải kiểm project/port/DB/Redis riêng, không ngầm dùng chung lab.
5. Lưu commit và PASS/FAIL/NOT_RUN; không sửa dữ liệu/test để hợp thức hóa kết quả.
6. Reviewer ngữ cảnh riêng nhận spec/base/subject và hashes; tự đọc diff/nguồn, chạy kiểm tra hoặc ghi rõ giới hạn receipts.
7. Finding cần điều kiện lỗi, ảnh hưởng, vị trí, căn cứ và phép xác minh. Sửa rồi review commit mới. Sau ba vòng chưa hội tụ xem lại hướng, không tự cho qua.
8. Tích hợp local sau review và kiểm tổ hợp. Code thay sau review phải kiểm lại phần ảnh hưởng. Bàn giao next step/open issues/receiver rồi tạo Draft PR.

## Cấu hình được nạp và giới hạn

- Root AGENTS.md: Codex hỗ trợ khám phá theo repo/cwd và override precedence; cần probe phiên mới. File tồn tại không chứng minh chat cũ đã nạp.
- `agents/codex/roles.json` và briefs: cấu hình harness dự án, được `workflow.py brief` đọc/đưa rõ vào giao việc. Không phải native auto-discovered Codex TOML hoặc Claude YAML.
- `config/agents/runtime.json`: doctor đọc profile nhận diện không bí mật; không là Compose/credentials, không đổi container.
- ownership/workflow/repository checks thực thi các quan hệ máy có thể kiểm. Kết quả thực xem evidence/state.
- Git hook/CI chỉ gọi active khi có cài/chạy và evidence. Hook có thể bypass; CI không tự thành required check nếu chưa có bảo vệ nhánh.
- Chưa cài native Codex hooks/managed settings, Claude hooks/Agent teams hoặc Antigravity definitions; không mở trust/bypass để ép thử.

Snapshot danh sách chats/subagents không chứng minh không có tiến trình ngoài phạm vi. Lượt này không thấy agent khác sửa môi trường trong danh sách được cung cấp; chỉ sở hữu control-repo paths, không thay source/runtime chung. Trước việc sau phải kiểm lại.

Các agent cùng quyền máy không là các bên độc lập bảo mật. Claim owner ID không có chữ ký, receipts không tự chứng minh thật, và chủ quyền có thể sửa/bỏ qua gates. Thay đổi quyền/required checks phải đề xuất riêng.
