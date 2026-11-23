Build Chatwoot from a clean linked Git worktree and start the isolated development services without an interactive frontend dependency reinstall. Source metadata is verified against Git HEAD; generated source snapshots, secrets and synthetic data stay separate from an existing lab.

Closes
https://github.com/trdat1605/s-251521f7e9131fb0/issues/2

Task: tasks/COMPLETE-001/task.json
Control task: https://github.com/trdat1605/r-61974bac4c68fe3c/blob/codex/complete-foundation/tasks/COMPLETE-001/task.json
Control issue: https://github.com/trdat1605/r-61974bac4c68fe3c/issues/18

How to reproduce
Build the upstream Dockerfile from a linked worktree. Its .git pointer refers to metadata outside the image, so git rev-parse fails during the build. The regression preserves that expected baseline failure and checks the explicit verified SHA and normal-clone fallback.

How to test
Read docker/isolated/README.md at the PR head, select a new reviewed project and check source metadata, login/API/Vite/Mailhog responses, restart persistence and synthetic database restore. The lifecycle helper is for a disposable runner. Use a new synthetic project on a host with sufficient capacity.

Evidence
Application head: 27e166927b93677863e7e7fda22109cfa2ae98b9.
CI: https://github.com/trdat1605/s-251521f7e9131fb0/actions/runs/45082996742 — metadata, focused-frontend and isolated-runtime passed. CI checked out merge commit 8d953fd35000ffc06a9696ad0a6ba91c211f6466; its tracked tree equals the application head. This covers selected checks and synthetic data. Interactive browser use, the full suite and production acceptance remain outside this evidence.

Final independent application review: PASS at this exact head, reviewer /root/foundation_app_final_review; receipt app-final-review.json in the COMPLETE-001 evidence on the control branch. Final control handoff is prepared separately. Keep Draft and unmerged until the owner decides on the concrete reviewed commits. Seventeen inherited workflows remain disabled; this PR does not publish or deploy.
