# Đánh giá vận hành và khoảng trống

Ngày18/11/2026. Không chấm bằng số lượng tài liệu/agent/test. Phân biệt task, trial, transcript và outcome theo nguồn Anthropic trong sources.md.

| Tiêu chí | Phép kiểm / evidence | Kết luận có giới hạn |
| --- | --- | --- |
| Đúng source/runtime | AGENT-001 live doctor HEALTHY và wrong-source BLOCKED/2; reviewer tự chạy lại | Đạt cho profile/kernel hiện tại; không là full tree audit hoặc chống sửa ngoài scope |
| Phạm vi và bảo toàn | Worker commit chỉ hai tệp; source app sạch; claims qua common Gitdir và tests tranh claim/worktree | Đạt phạm vi thử; editor không dùng helper vẫn có thể ghi |
| Yêu cầu thực tế | Doctor chặn nhầm checkout được PR1 xác nhận là nguy cơ thật | Có ích cho preflight, không là một feature Zalo hoặc cải thiện UI |
| Review đúng phiên bản | review.json gắn exact subject; validator/tests stale commit và code thay sau review | Kiểm được quan hệ commit/bytes; không xác thực danh tính reviewer bằng chữ ký |
| Agent mới tiếp tục | Role briefs/task được worker đọc; CLI mới nhận policy ID tự nạp | Có bằng chứng nạp và tiếp nhận giới hạn; chưa thử mọi tình huống mất context hoặc máy khác |
| Cấu hình tái dùng | Root rules/roles/profile/tools versioned; brief đọc role map, tests chạy không cần package ngoài | Profile lab cần thay theo máy/task; không triển khai native Claude/Codex role/hook chưa thử |
| Hỗ trợ cập nhật | Source ref, profile và policy tách khỏi app; ADR yêu cầu kiểm compatibility/delta | Chưa nâng cấp Chatwoot hoặc thử rollback/full integrations |

## Lỗi, việc làm lại và cách xử lý có căn cứ

1. Vite alias không có source metadata labels thật: không bỏ guard hoặc tin working_dir; đọc stat host/container và thêm negative case inode mismatch. Đây là điều chỉnh thiết kế có căn cứ, không một quy tắc vĩnh viễn chống mọi alias.
2. Brief tiếng Việt qua pipeline Windows bị UnicodeEncodeError do cp1252. Đã sửa output CLI sang UTF-8 và thêm regression case với PYTHONIOENCODING=cp1252; không thay global locale.
3. Một lệnh shell ghi nhóm docs bị công cụ chặn. Chuyển sang công cụ sửa tệp chuyên dụng; không đổi permissions hoặc bypass. Không suy đó là lỗi model/runtime của Chatwoot.
4. README bootstrap trỏ docs chưa tạo trong lúc worker bắt đầu. Worker báo rõ thay vì giả đã đọc; coordinator hoàn thiện docs trước bàn giao. Kiểm liên kết cuối để không để lại lỗi bàn giao.
5. JSON bằng chứng ghi trên Windows có CRLF, làm whitespace check không đạt và cần chuẩn hóa trước khi hash. Đã dùng LF và cập nhật digest receipts; gitattributes versioned quy định line endings. Không đổi cấu hình Git/global locale để giấu kết quả không đạt.

## Mở / NOT_RUN

- Reviewer nhiệm vụ ban đầu chỉ kiểm nhánh Linux bằng mock; coordinator sau đó đã chạy thật doctor trong Ubuntu WSL qua Linux CLI, xem evidence/linux-doctor.json. Chưa thử máy Linux/kernel khác; không mở rộng bảo đảm device:inode ra ngoài kernel chung.
- Không thử ghi phá sandbox để chứng minh write denial; CLI loading probe dùng read-only option và không gọi tools, chỉ chứng minh chỉ dẫn hiện diện.
- Chưa cô lập OS/account của reviewer; chưa branch protection/required checks; không tự cấp quyền hoặc merge.
- Không thử UI thay đổi rồi hoàn nguyên, HMR thực, đo hiệu năng mới, Zalo, mobile hoặc upstream upgrade. Doctor được chọn thay một nhiệm vụ UI để không chiếm runtime chung và vì lỗi nhầm source đã có bằng chứng; không tự đóng backlog UI/performance.
- Chưa thử toàn bộ vòng feature sản phẩm ngoài nhiệm vụ tooling thật; không gọi AGENT-001 là bảo đảm đội AI thay doanh nghiệp CNTT.
- Token chưa được đo như chỉ tiêu hiệu quả; không ước lượng tiết kiệm. Cải tiến policy cần tình huống lặp/căn cứ và review trước khi thay rules chung.

## Quyết định còn cần chủ sản phẩm

Review Draft PR và chấp nhận quy trình trong phạm vi thử; có cho phép cấu hình required checks/quyền review riêng trong lượt sau; thứ tự xử lý source workspace/adapters/UI-performance và hợp đồng Zalo. Không hỏi lại source pin/cách chạy đã có. Merge/phát hành chưa được tự thực hiện.
