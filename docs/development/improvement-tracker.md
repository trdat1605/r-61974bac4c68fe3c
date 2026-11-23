# Bảy cải tiến: kết quả và việc còn mở

Cập nhật **23/11/2026** trên `codex/complete-foundation`, [COMPLETE-001](completion.md), [issue18](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/18). Chưa merge hoặc nghiệm thu toàn bộ. Bảng này mô tả bằng chứng hiện hành; các task/review lịch sử giữ nguyên theo SHA.

| Điểm / issue | Đã có bằng chứng | Còn thiếu trước chấp nhận |
| --- | --- | --- |
| 1 — [Agent #6](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/6) | Protocol V3 cố định/ref nguồn; đủ 12 lượt/36 outputs, chấm độc lập và second check; 5 PASS, 7 fail/partial, kết luận tạm có giới hạn | Brief đã cập nhật, CLI loading đạt; chưa đo hiệu quả hành vi của brief mới. [Giới hạn/kết quả](agent-selection.md). Claude Teams NOT_RUN theo phạm vi user xác nhận |
| 2 — [Traceability #7](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/7) | Issue control18/app2, task riêng, [Draft app PR3](https://github.com/trdat1605/s-251521f7e9131fb0/pull/3), CI và reviews theo app SHA khác control SHA | PR control tích hợp, final checks; templates/default issue chooser chỉ kiểm active sau owner cho phép merge |
| 3 — [Source #8](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/8) | Source baseline công khai, bootstrap tracked-source/fresh secrets/isolation; full development image build076 PASS, `.git_sha` đúng; clone/handover đã tìm ra thiếu sót docs và có sửa/review | [Lifecycle runner](source-reproduction.md) đã PASS ở apphead27e1669; final fresh reader/ref check còn đang thực hiện. Local runtime lần đầu FAIL, C thiếu dung lượng; không che lỗi hoặc tự chuyển Docker |
| 4 — [CI/pilot #9](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/9) | Regression Docker thật baseline EXPECTED_FAIL → fix PASS, 23 boundary tests và 14 frontend tests đã chạy ở các SHA ghi trong receipts. CI17 workflow kế thừa đã tắt; chỉ bật workflow foundation sau review | Lifecycle/RSpec/restart/restore đã PASS trên hosted runner ở apphead27e1669/mergecheckout8d953fd với tree identical; final independent review vẫn cần. chưa phải full suite/UI/stability certification |
| 5 — [Review #10](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/10) | Main rules đã enforce ở GOV-001; app implementation có nhiều vòng review khác người viết, lỗi cleanup/capacity/startup được giữ và sửa | Review app cuối PASS tại27e1669; ba required app CI checks đã apply/readback sau review; còn final control review; owner quyết định merge riêng. Agent JSON không là GitHub human approval |
| 6 — [Bàn giao #11](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/11) | README/status hiện hành dẫn tới task, app SHA, receipts và điểm còn mở; 80 tooling unit tests PASS | Final machine handoff/hash/index gate/hosted control CI và một fresh reader kiểm tuyến mới. Không có số đo tiết kiệm token |
| 7 — [Quy trình #5](https://github.com/trdat1605/r-61974bac4c68fe3c/issues/5) | Lỗi build thật đi qua issue → task → nhánh app → regression → review → Draft PR, đã chạy CI thực | Hoàn tất [pilot](pilot.md) tới acceptance-ready, final review/PR control. Chưa merge/phát hành, chưa thử nâng cấp sản phẩm hoặc tích hợp Zalo |

## Quyết định và ranh giới

Coordinator quản lý liên kết/phụ thuộc; mỗi phạm vi một implementer; reviewer nhận ngữ cảnh riêng và exact commit. Chủ sản phẩm chốt phạm vi, nghiệp vụ và merge/phát hành. Không dùng số tài liệu, agent hoặc tên chức danh làm bằng chứng chất lượng.

Nguồn nền trước: [FLOW-001](../../tasks/FLOW-001/task.json), [PUB-001](repository-publication.md), [GOV-001](branch-protection.md). Main control còn gần khởi tạo; cần PR tích hợp giữ ancestry bằng merge commit, không squash/rebase hồ sơ review. Các PR cũ giữ lịch sử cho tới quyết định riêng của owner.

[Phương án Docker sang D](../runbooks/docker-storage-migration.md) là chuẩn bị/review theo yêu cầu mới, chưa thực hiện; đây không phải bằng chứng đã giải quyết thiếu dung lượng local. Lab Chatwoot và website khóa học hiện có không bị thay đổi trong COMPLETE-001.
