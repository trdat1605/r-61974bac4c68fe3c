# Thư viện nguồn — dành cho người và AI

Cập nhật tổ chức **23/11/2026**. [README dự án](../../README.md) → chọn [tuyến đọc theo việc](reading-routes.md) → mở nguồn/code liên quan. Muốn đọc cách hosting, mở **CW-13 Docker development** bên dưới và [runbook local](../runbooks/local-development.md). Production architecture CW-10 là phạm vi khác.

## Cách dùng và bản chính

- [sources.json](sources.json) giữ metadata gốc của 36 nguồn khảo sát ngày 11/11: URL/ref/ngày lấy/hash/phạm vi. Mục lục dưới trình bày lại các ID để anh bấm đọc; không coi mọi URL đã được kiểm lại hôm nay. Mốc thiếu ngày lấy hiển thị rõ bên dưới.
- [supplemental-sources.json](supplemental-sources.json) ghi nguồn bổ sung ngày 23/11, provenance bản chép lời và bản upstream đã chọn lưu. [source-notes.md](source-notes.md) giải thích nguồn nói gì và dự án áp dụng gì; [khảo sát agent ngày 18/11](../agents/sources.md) giữ kết quả theo ngày.
- [Bản chép lời người dùng gửi](user-materials/README.md) đã có trong Git; dài nên chỉ mở khi cần đối chiếu. Không tự nạp vào mọi task hoặc coi mọi nhận định là quy định dự án.
- [Bản AGENTS upstream tham khảo](references/chatwoot-v4.19.1-AGENTS.txt) lưu đúng ref; [license kèm theo](references/chatwoot-v4.19.1-LICENSE.txt). Đuôi `.txt` để tránh trở thành AGENTS được nạp tại thư mục này. Chỉ dẫn có hiệu lực là AGENTS/override ở checkout thực.
- Bản website có ngày lấy nhưng không pin commit không tự tương ứng server v4.19.1. Các snapshot lịch sử khác vẫn ngoài repo; đường `legacy_local_snapshot` không phải file trong clone. Thư viện này chưa là kho đọc offline toàn bộ tài liệu.

## Tổ chức agent và review

| Cần tìm | Nơi đọc / công năng |
| --- | --- |
| Cách nhóm Claude Code review | [Bài gốc và ghi chú](source-notes.md#an-review--bài-gốc-nhóm-claude-code); [bản ghi âm dạng text](user-materials/README.md) để đối chiếu |
| Chọn chỉ dẫn/context | [Memory và context](source-notes.md#an-memory--chia-chỉ-dẫn-theo-phạm-vi) |
| Subagent/team là gì, khi nào dùng | [Subagents và Teams](source-notes.md#an-subagents--ngữ-cảnh-và-đầu-vào-được-giao) |
| Phiên mới tiếp quản | [Harness](source-notes.md#an-harness--tiếp-tục-sau-khi-mất-ngữ-cảnh) và [gói ngữ cảnh](context-packet.md) |
| Cách dự án đang giao việc và review | [Agent guide](../agents/README.md); đây là quy trình riêng trên Codex, khác tính năng Claude |

## Chatwoot: kiến trúc và quy ước

| ID | Mở nguồn gốc | Công năng | Mốc trong catalog |
| --- | --- | --- | --- |
| <a id="cw-01"></a>CW-01 | [Chatwoot AGENTS.md](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/AGENTS.md) | Quy ước tại commit server | caab07a8f000 |
| <a id="cw-02"></a>CW-02 | [Backend Guidelines](https://www.chatwoot.com/hc/handbook/articles/1743728412-backend-guidelines) | Tổ chức backend/API/jobs/dữ liệu | 2026-11-10 (web) |
| <a id="cw-03"></a>CW-03 | [Frontend Guidelines](https://www.chatwoot.com/hc/handbook/articles/frontend-guidelines-30) | Quy ước frontend; đối chiếu source mới | 2026-11-10 (web) |
| <a id="cw-04"></a>CW-04 | [Developing Enterprise Edition Features](https://www.chatwoot.com/hc/handbook/articles/developing-enterprise-edition-features-38) | Mở rộng Enterprise | 2026-11-10 (web) |
| <a id="cw-05"></a>CW-05 | [Contributing Guide](https://developers.chatwoot.com/contributing-guide) | Lối vào đóng góp | 2026-11-10 (web) |
| <a id="cw-06"></a>CW-06 | [Chatwoot APIs](https://developers.chatwoot.com/contributing-guide/chatwoot-apis) | Chọn loại API | 2026-11-10 (web) |
| <a id="cw-07"></a>CW-07 | [Platform APIs](https://developers.chatwoot.com/contributing-guide/chatwoot-platform-apis) | API quản lý nền tảng | 2026-11-10 (web) |
| <a id="cw-10"></a>CW-10 | [Production architecture](https://developers.chatwoot.com/self-hosted/deployment/architecture) | Kiến trúc production | 2026-11-10 (web) |

## Chatwoot: host, nâng cấp, sao lưu

| ID | Mở nguồn gốc | Công năng | Mốc trong catalog |
| --- | --- | --- | --- |
| <a id="cw-11"></a>CW-11 | [Project setup](https://developers.chatwoot.com/contributing-guide/setup-guide) | Thiết lập dependencies | 2026-11-10 (web) |
| <a id="cw-12"></a>CW-12 | [Windows setup](https://developers.chatwoot.com/contributing-guide/environment-setup/windows) | Thiết lập trên Windows | 2026-11-10 (web) |
| <a id="cw-13"></a>CW-13 | [Docker development](https://developers.chatwoot.com/contributing-guide/environment-setup/docker) | Docker phát triển | 2026-11-10 (web) |
| <a id="cw-14"></a>CW-14 | [Upgrade](https://developers.chatwoot.com/self-hosted/deployment/upgrade) | Cập nhật phiên bản | 2026-11-10 (web) |
| <a id="cw-15"></a>CW-15 | [Backup](https://developers.chatwoot.com/self-hosted/deployment/backup) | Sao lưu/khôi phục | 2026-11-10 (web) |

## Chatwoot: mobile

| ID | Mở nguồn gốc | Công năng | Mốc trong catalog |
| --- | --- | --- | --- |
| <a id="cw-08"></a>CW-08 | [Mobile development setup](https://developers.chatwoot.com/contributing-guide/mobile-app/setup-guide) | Thiết lập mobile | 2026-11-10 (web) |
| <a id="cw-09"></a>CW-09 | [Custom Mobile App](https://developers.chatwoot.com/self-hosted/custom-mobile-app) | Mobile tùy chỉnh/push/deep link | 2026-11-10 (web) |
| <a id="cw-21"></a>CW-21 | [Mobile package scripts](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/package.json) | Scripts mobile tham khảo | a7b5deb2db6a |
| <a id="cw-29"></a>CW-29 | [Mobile APIService](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/src/services/APIService.ts) | API client mobile | a7b5deb2db6a |
| <a id="cw-30"></a>CW-30 | [Mobile channel icon](https://github.com/chatwoot/chatwoot-mobile-app/blob/a7b5deb2db6a3cb13a6c72205d53079ee89e4611/src/utils/getChannelIcon.tsx) | Nhận diện kênh mobile | a7b5deb2db6a |

## Chatwoot: tính năng, edition, kênh

| ID | Mở nguồn gốc | Công năng | Mốc trong catalog |
| --- | --- | --- | --- |
| <a id="cw-16"></a>CW-16 | [Feature flags](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/config/features.yml) | Danh mục cờ | caab07a8f000 |
| <a id="cw-17"></a>CW-17 | [Featurable](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/models/concerns/featurable.rb) | Logic cờ | caab07a8f000 |
| <a id="cw-18"></a>CW-18 | [Managing Enterprise Features](https://developers.chatwoot.com/self-hosted/enterprise-edition) | Cấu hình Enterprise | 2026-11-10 (web) |
| <a id="cw-22"></a>CW-22 | [Supported features by channel](https://developers.chatwoot.com/self-hosted/supported-features) | Khả năng theo kênh | 2026-11-10 (web) |
| <a id="cw-23"></a>CW-23 | [TikTok setup](https://developers.chatwoot.com/self-hosted/configuration/features/integrations/tiktok) | Thiết lập TikTok | 2026-11-10 (web) |
| <a id="cw-31"></a>CW-31 | [Plan feature reconciliation](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/enterprise/app/services/enterprise/billing/reconcile_plan_features_service.rb) | Tính năng theo plan | caab07a8f000 |

## Chatwoot: kiểm thử và điểm vào source

| ID | Mở nguồn gốc | Công năng | Mốc trong catalog |
| --- | --- | --- | --- |
| <a id="cw-19"></a>CW-19 | [Playwright E2E](https://developers.chatwoot.com/contributing-guide/tests/playwright) | E2E web | 2026-11-10 (web) |
| <a id="cw-20"></a>CW-20 | [Server package scripts](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/package.json) | Scripts server | caab07a8f000 |
| <a id="cw-24"></a>CW-24 | [CE workflow](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/workflows/run_foss_spec.yml) | CI Community | caab07a8f000 |
| <a id="cw-25"></a>CW-25 | [MFA workflow](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/.github/workflows/run_mfa_spec.yml) | CI/MFA và điều kiện chạy | caab07a8f000 |
| <a id="cw-26"></a>CW-26 | [Conversation account boundary](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/controllers/api/v1/accounts/conversations/base_controller.rb) | Controller hội thoại/account | caab07a8f000 |
| <a id="cw-27"></a>CW-27 | [Message model](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/models/message.rb) | Model tin nhắn | caab07a8f000 |
| <a id="cw-28"></a>CW-28 | [SendReplyJob](https://github.com/chatwoot/chatwoot/blob/caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82/app/jobs/send_reply_job.rb) | Job gửi trả lời | caab07a8f000 |

## Công cụ: tài liệu đã thu thập

| ID | Mở nguồn gốc | Công năng | Mốc trong catalog |
| --- | --- | --- | --- |
| <a id="tool-01"></a>TOOL-01 | [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Chỉ dẫn Codex; kiểm bản công cụ thật | Không ghi ngày lấy riêng |
| <a id="tool-02"></a>TOOL-02 | [Codex skills](https://learn.chatgpt.com/docs/build-skills) | Skills Codex | Không ghi ngày lấy riêng |
| <a id="tool-03"></a>TOOL-03 | [Claude memory and scoped rules](https://code.claude.com/docs/en/memory) | Chỉ dẫn/memory Claude | Không ghi ngày lấy riêng |
| <a id="tool-04"></a>TOOL-04 | [Claude skills](https://code.claude.com/docs/en/skills) | Skills Claude | Không ghi ngày lấy riêng |
| <a id="tool-05"></a>TOOL-05 | [Antigravity rules](https://antigravity.google/docs/rules/) | Rules Antigravity; chưa tham gia mặc định | Không ghi ngày lấy riêng |

Bảng mục lục không thay việc mở nguồn liên quan. Nếu URL đổi, tra retrieved_url trong catalog hoặc nguồn chính thức, ghi rõ khác biệt. Khi chưa truy cập được nguồn cần thiết, ghi NOT_RUN/thiếu nguồn và ảnh hưởng; không dùng cache như tài liệu luôn mới.
