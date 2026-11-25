Moved existing local Docker Desktop data and Ubuntu-22.04 from C to D using the supported Desktop UI and installed WSL move/export commands. This PR records the maintenance plan, guarded scripts, independent reviews and sanitized evidence; it does not change application source or deploy a new app version. The local relocation has already been performed under the owner's authorization; merging this record is not required to make the moved runtime work.

Refs https://github.com/trdat1605/r-61974bac4c68fe3c/issues/20

Task: tasks/STORAGE-001/task.json

## Result and validation
- Runtime: Docker D:/Dev/Runtime/Docker/DockerDesktopWSL; Ubuntu D:/Dev/Runtime/Ubuntu. Linux source paths retained.
- Preserved 20 original container identities, 15 running states, 50 images, 33 volumes and original mounts/ports. One isolated Redis diagnostic fixture is stopped and retained, without original volumes or network access.
- Full offline Docker and Ubuntu backups verified and retained privately outside Git. Thirty PostgreSQL dataset digests match. Redis first opaque DUMP comparison failed; retained that failure, independently extracted the pre-move RDB using two readers, validated checksum/load in the same-image fixture, and verified canonical equality of 49 persistent keys plus a fresh current recheck before resuming apps.
- Source commits unchanged: Chatwoot lab caab07a8f00032d5205b5a5d7e2eb0ba2f3d2d82; foundation pilot 27e166927b93677863e7e7fda22109cfa2ae98b9. Selected source hashes match Rails/Vite/Sidekiq containers. Maintenance records have separate commits.
- Independent technical handover review PASS at d62c6423d3bdd33bd6c66f165abc8864df312475. Browser smoke observed Chatwoot dashboard and course landing render after restart.

## Limits and recovery
Existing backups/cache/images were not pruned. Full Docker backup is temporarily retained on C; Ubuntu backup is on D. C/D are partitions of one physical disk, so these copies do not protect against hardware loss. Final observed free space C approximately39.66GiB, D17.34GiB.

Redis expiring keys are outside semantic equality; no full application/VM restore rehearsal, full feature suite, security certification or performance improvement is claimed. HTTPS IP probe44406 was unreachable before and after maintenance; six other probes returned200. Initial Chatwoot browser cold load timed out/was blank before eventually rendering; F5 performance remains a separate issue. A 7-Zip filesystem Headers Error warning is retained; the specific RDB bytes were cross-checked with an independent reader and Redis CRC/load.

Recovery uses private known-good copies and the reviewed maintenance plan while writers are stopped; do not run maintenance scripts as routine app commands or overwrite live data. No merge or release performed.
