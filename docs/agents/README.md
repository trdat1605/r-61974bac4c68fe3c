# Bắt đầu vận hành AI coding agent

Ngày thiết lập: 18/11/2026. Trạng thái triển khai/kiểm chứng hiện tại xem [state.md](state.md), không suy từ việc có các file.

1. Đọc AGENTS.md của repo điều phối và [operating-model.md](operating-model.md).
2. Định vị source/runtime bằng `config/agents/runtime.json` và phiếu việc. Repo app đang chạy khác repo này. Khi làm ở app đọc AGENTS/override tại app.
3. Chọn tuyến: khảo sát và quyết định tại [sources.md](sources.md); giao việc tại `tasks/<id>/task.json`; roles Codex tại `agents/codex/roles.json` và các brief. Các brief được đọc rõ trong giao việc, không là native role tự phát hiện của Claude hoặc Codex.
4. Kiểm script/commands và bằng chứng ở từng phiếu; dùng PASS/FAIL/NOT_RUN. Không tự thao tác runtime dùng chung.
5. Handoff ghi đúng commit, checks, reviewer và next step; chủ sản phẩm còn quyết định cuối. Chưa merge.

[PR nền móng #1](https://github.com/trdat1605/chatwoot-vn/pull/1) là baseline. Nhánh agent-ops dựa trên head PR1 để tái dùng báo cáo, không sửa năm báo cáo lịch sử đó. Draft PR mới phụ thuộc PR1, không merge PR1 trong nhiệm vụ này.

Các lệnh sử dụng và kết quả sẽ được chốt sau khi script được review/kiểm chứng; state phân biệt phần đã chạy và dự kiến. Không dùng đoạn đang triển khai làm hướng dẫn rằng mọi gate đã active.
