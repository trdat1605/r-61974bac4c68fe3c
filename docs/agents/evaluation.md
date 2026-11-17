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
6. Review toàn gói tại commit050c6ac bị BLOCK với ba fixture thật: staged deletion còn file working bị bỏ lọt, task cũ chặn task mới sửa cùng tệp, scanner bỏ lọt .env.production. Đã sửa kiểm toàn index/deletion, review lịch sử với owner mới nhất theo tệp, và họ env files; thêm regression tests. Kết quả review lại xem evidence/system-review.json, không coi test cũ xanh là đủ.
7. Review cũng chỉ ra profile dependency chưa bind bytes. Phiếu/handoff/review hiện khai báo input hashes; đổi profile ngoài task review mới bị chặn. Đây là bổ sung theo rủi ro cấu hình thực, không tuyên bố xác thực mọi input ngoài danh sách.
8. Probe hook đầu chỉ phân tích stdout, trong khi Git đưa output hook vào stderr; sửa phép thu và xác nhận commit fixture bị chặn, không thay hook hoặc làm sai kết quả để pass.
9. Fresh clone Windows ở commit9bf đổi .gitattributes/.gitignore thành CRLF do thiếu quy định LF cho chính hai tệp này. Checker chặn cả checkout sạch, nên kết quả negative khi ấy không chứng minh chặn thiếu acceptance. Đã thêm hai quy định LF; clone mới kiểm sạch đạt và hook chặn đúng missing acceptance. Giữ lỗi đo trong receipt mới, không thay global autocrlf.
10. Review vòng2 phát hiện handoff staged có thể đọc receipt untracked; commit sẽ thiếu bằng chứng và CI checkout sạch sẽ lỗi. Đã xem lại ranh giới gate: kiểm toàn index chưa đủ, phải đóng tập artifact được đọc. Bổ sung index membership cho task/handoff/review/receipts, cùng ca untracked bị chặn và staged hợp lệ. Không mở rộng thành tuyên bố test hermetic hay xác thực mọi lời khai.

## Mở / NOT_RUN

- Reviewer nhiệm vụ ban đầu chỉ kiểm nhánh Linux bằng mock; coordinator sau đó đã chạy thật doctor trong Ubuntu WSL qua Linux CLI, xem evidence/linux-doctor.json. Chưa thử máy Linux/kernel khác; không mở rộng bảo đảm device:inode ra ngoài kernel chung.
- Không thử ghi phá sandbox để chứng minh write denial; CLI loading probe dùng read-only option và không gọi tools, chỉ chứng minh chỉ dẫn hiện diện.
- Chưa cô lập OS/account của reviewer; chưa branch protection/required checks; không tự cấp quyền hoặc merge.
- Không thử UI thay đổi rồi hoàn nguyên, HMR thực, đo hiệu năng mới, Zalo, mobile hoặc upstream upgrade. Doctor được chọn thay một nhiệm vụ UI để không chiếm runtime chung và vì lỗi nhầm source đã có bằng chứng; không tự đóng backlog UI/performance.
- Chưa thử toàn bộ vòng feature sản phẩm ngoài nhiệm vụ tooling thật; không gọi AGENT-001 là bảo đảm đội AI thay doanh nghiệp CNTT.
- Token chưa được đo như chỉ tiêu hiệu quả; không ước lượng tiết kiệm. Cải tiến policy cần tình huống lặp/căn cứ và review trước khi thay rules chung.

## Quyết định còn cần chủ sản phẩm

Review Draft PR và chấp nhận quy trình trong phạm vi thử; có cho phép cấu hình required checks/quyền review riêng trong lượt sau; thứ tự xử lý source workspace/adapters/UI-performance và hợp đồng Zalo. Không hỏi lại source pin/cách chạy đã có. Merge/phát hành chưa được tự thực hiện.
