# Independent pre-execution review record

Reviewer: `/root/storage_review`, fresh context; read-only. Subject f4ad98d589f0c4f5759ddfbf5d2e9990dbf960bf; maintain.py SHA256 0f38a89d6c147edd85386f7017b80c736780d3435b38d9b8c52b2abcdb4a7be6.

Reviewer verdict: APPROVED for operator-driven stages with explicit gates, not relocation acceptance. Independently checked Python AST, role fallback SELECT 1 on four PostgreSQL containers, full container IDs, guarded fixed-path backups, same-disk capacity, WSL 3.0.5 source export/move and offline known-good restore route. No runtime mutation performed by reviewer.

Required operator gates: inspect clean PostgreSQL/Redis shutdown, allow only the two known `always` datastore IDs after backend restart, verify writer fence before after-digest/resume, separately verify backend stopped/UI path/registry/source/binds, and stop on mismatches. No full isolated restore rehearsal required as a separate blocker, but NOT_RUN must remain recorded. Same physical disk means no hardware-failure resilience. Snapshot limits: public-schema PostgreSQL tables/sequences, persistent Redis DB0 keys, HTTP checks not full UI/security.

Official references read by reviewer:
- https://docs.docker.com/engine/containers/start-containers-automatically/
- https://docs.docker.com/reference/cli/docker/container/stop/
- https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/
- https://raw.githubusercontent.com/microsoft/WSL/3.0.5/src/windows/service/exe/LxssUserSession.cpp

Runtime attempt: quiesce PASS. The first before-datastore snapshot FAIL because Redis requires authentication and redis-cli returned NOAUTH with process exit 0. Snapshot parser raised IndexError; datastores were not stopped and no relocation attempted. Fix at c8810b739f2db344986057e30e2819a217866c51 authenticates inside the Redis container environment and validates probe structure, never prints credentials. Targeted independent delta review requested before retry.

Targeted review at c8810b739f2db344986057e30e2819a217866c51: APPROVED by same independent reviewer. New script SHA256 fe9e7967d5dd3006bc696925752b8ce4fd32bfce33c171223d56fd05b8a0d60b. Password expands only inside container environment, Lua quoted positional argument, strict output validation. AST PASS; actual authenticated Redis probe NOT_RUN by reviewer. Root subsequently reran before snapshot PASS (31 datasets / 967 public tables); all five datastores stopped exit 0, OOM false, Desktop backend/process absent, Ubuntu terminate succeeded. Offline VHD exclusive access checked. Shutdown markers will be inspected before UI move on next startup; no assertion of full restore rehearsal.
