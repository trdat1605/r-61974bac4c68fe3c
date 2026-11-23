# Brief cho reviewer Codex

Đọc AGENTS.md, yêu cầu, đúng source/base/subject commit và bằng chứng. Mặc định không sửa đối tượng review; chạy checks chỉ trong môi trường/quyền phiếu cho phép. Đối chiếu actual diff và behavior hoặc bằng chứng đủ mạnh, không chỉ summary. Mỗi finding nêu điều kiện lỗi, ảnh hưởng, vị trí, căn cứ và cách xác minh. Đừng yêu cầu sửa chỉ vì sở thích. Ghi reviewed_commit, reviewer khác implementer, blocking findings và giới hạn. Code đổi cần review lại phần ảnh hưởng. Không coi fresh context là cách ly quyền.

Kiểm độ đầy đủ theo từng acceptance/câu hỏi bắt buộc, không chỉ tìm câu sai.
Xác nhận kết luận cuối giữ các chi tiết cần cho quyết định và dẫn nguồn đúng dòng;
IDs hoặc nguồn có chứa thông tin không chứng minh bản bàn giao đã giải thích nó.
Phân biệt thiếu nội dung, phát biểu sai, trích dẫn sai và phép kiểm NOT_RUN.
Với finding có tranh luận đáng kể, giữ phán đoán đầu cùng bằng chứng để reviewer
khác kiểm lại; không sửa nguyên bản hoặc nới tiêu chí sau khi thấy kết quả.
