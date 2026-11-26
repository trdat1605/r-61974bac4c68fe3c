# Giảm dung lượng backup — STORAGE-002

Ngày 26/11/2026. [Issue 22](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/22). Người dùng yêu cầu sắp xếp tránh lãng phí dung lượng sau khi chuyển ổ. Chỉ nén ba bản VHD offline, không xóa một mốc backup nào. Đĩa runtime trên D, source/database/container/cache không sửa, không cần dừng website.

**Đã thực hiện và kiểm tra đạt:** [receipt tổng hợp](evidence/summary.json). Ba tệp backup giảm từ64,60GiB xuống26,89GiB, chênh37,71GiB theo kích thước tệp. C trống khoảng120,47GiB, D20,17GiB tại snapshot cuối; chênh dung lượng volume có hoạt động Windows khác, không gán toàn bộ cho nhiệm vụ. 21 container giữ nguyên ID/image/trạng thái/start time/mount/port; sáu HTTP200 và một endpoint trial đã unreachable từ trước giữ baseline.

| Backup | Trước | Sau | Nơi lưu |
| --- | --- | --- | --- |
| Ubuntu26/11 |16,54GiB|6,96GiB|Private archives trên C |
| Docker26/11 |31,86GiB|13,69GiB|`D:/Dev/Backups/archives/` |
| Ubuntu11/11 |16,19GiB|6,24GiB|Private archives trên C |

Nguồn Ubuntu chạy script1497c7b, Docker dùng d4684cf; các commit task/report khác commit app. Archive và manifest riêng tư được đối chiếu full decompressed SHA256+CRC/size trước xóa bản chưa nén; 3 mốc vẫn đầy đủ. Runtime không restart, cache/images/volumes không prune. Giới hạn: không diễn tập boot cả VM, không chứng minh bảo mật/hiệu năng toàn ứng dụng, backup cùng ổ vật lý. Review độc lập trước thực hiện tại [receipt review](evidence/independent-review.json); review bàn giao riêng sau khi có đủ kết quả.

Trình tự: Ubuntu backup mới D -> archive riêng tư C; kiểm toàn bộ giải nén CRC/SHA256/size rồi bỏ đúng VHD offline gốc để D đủ chỗ. Docker backup C -> archive riêng tư D, kiểm tương tự; cuối cùng Ubuntu cũ C -> archive C. Gzip level1 ưu tiên tốc độ với dữ liệu lớn; không hứa tỷ lệ nén. Đích mới exclusive-create, từ chối conflict/reparse/active distro paths, dự phòng10GiB và giữ source nếu bất kỳ lỗi nào. SHA hai backup mới phải khớp receipt STORAGE-001; backup cũ dùng hash thực đọc được. Giữ log tiến độ chỉ số byte, không in dữ liệu bên trong.

Điều chỉnh trình tự được reviewer khác cho phép: hai Ubuntu backup có thể nén song song bằng cùng script đã review, source/archive/receipt tách riêng. Trước khởi động job thứ hai, C trống trừ tối đa phần còn lại của Ubuntu mới trừ toàn bộ kích thước Ubuntu cũ phải còn ít nhất10.5GiB. Lần kiểm đầu chỉ9.13GiB nên chưa chạy; lần kiểm sau11.05GiB đạt mới chạy job thứ hai. Docker vẫn chờ Ubuntu mới hoàn tất và trả chỗ trên D. Một implementer thao tác; không chạy hai writer trên cùng tệp. Không coi thay trình tự là bằng chứng đã tăng tốc trước khi đo.

Nguồn đã đọc: [Python gzip](https://docs.python.org/3.13/library/gzip.html), [hashlib](https://docs.python.org/3.13/library/hashlib.html). Nén giữ nội dung binary; cách sắp xếp/giới hạn dung lượng là điều chỉnh cho máy này. Gzip không mã hóa: thư mục private ACL chỉ user/SYSTEM/Admin, không Git/GitHub. C/D cùng ổ vật lý; không bảo vệ hỏng ổ.

## Đọc kết quả và phục hồi

Kết quả thực từng tệp nằm ở `evidence/<backup>.json`. Các manifest riêng tư cạnh archive ghi SHA256 của VHD chưa nén và kích thước cần khi phục hồi. Khi cần, giải nén ra **tệp mới** đủ chỗ, đối chiếu SHA256/size với manifest, rồi mới dùng hướng dẫn phục hồi Docker/WSL đã review; không giải nén đè đĩa runtime đang chạy. Kiểm CRC/giải nén hash không thay diễn tập boot toàn VM.

Sau thành công, đường dẫn backup chưa nén trong STORAGE-001 là lịch sử; đường dẫn hiện hành ở receipt STORAGE-002. Không chạy lại script STORAGE-001 vì nó tham chiếu VHD cũ. Không chuyển tất cả backup về D khi chưa đủ dung lượng. Giữ bản đồ và lịch sao lưu; đề xuất về sau giữ hai mốc đầy đủ gần nhất sau khi có bản sao dữ liệu nhỏ và kiểm phục hồi, chỉ loại mốc cũ trong nhiệm vụ riêng được cho phép. Lượt này giữ đủ cả ba mốc.

## Quy ước tránh tích lũy tiếp

Áp dụng cho việc tiếp theo của dự án: sửa code thường ngày dùng nhánh/commit Git, không tự tạo một VHD backup mới cho mỗi lần sửa. Backup dữ liệu thật cần tách khỏi Git; thay đổi DB và thay đổi môi trường lớn phải có phương án backup phù hợp. Nếu cần snapshot toàn Docker/Ubuntu, ghi ngày/lý do/đích/chi phí dung lượng/mốc có thể bỏ và kiểm phục hồi. Nén backup offline sau khi đối chiếu; không để cả gzip và VHD trùng nhau sau khi đã kiểm hoàn chỉnh. Không tự prune volumes hoặc chạm runtime của dự án khác. Đo dung lượng trước build lớn, không coi Linux hiển thị đĩa 1TB là ổ Windows còn đủ chỗ. Đây là quy ước vận hành riêng đã chọn cho máy này, không phải khẳng định mọi dự án phải giữ cùng số backup.

Các archive Ubuntu nằm ở thư mục private C và Docker ở D; có một lối vào chung `D:/Dev/Backups/README.md`. Nén là lossless, không phải mất một phần snapshot. Khi phục hồi Docker32GiB mà D không đủ chỗ giải nén thêm, chọn staging C đủ dung lượng rồi theo runbook phục hồi offline; không tự xóa volume hoặc giải nén đè đĩa đang chạy.
