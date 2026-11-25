## Request
Move the existing Docker Desktop data and Ubuntu-22.04 distribution from C to D, keeping Linux source inside its Linux filesystem. The owner authorized relocation on 2026-11-26 and explicitly deferred cleanup until after relocation. Preserve old backups, source, containers and data. No product changes, upgrades, merges, payment changes or public exposure.

## Acceptance
- A1: Docker Desktop uses D:/Dev/Runtime/Docker and the original images, containers, volumes and private bind data remain accounted for.
- A2: Ubuntu-22.04 uses D:/Dev/Runtime/Ubuntu; existing Linux absolute paths and source commits remain valid.
- A3: Pre/post datastore and source checks match; Chatwoot and course website public endpoints return their baseline status after controlled restart.
- A4: Backups and rollback instructions remain private outside Git; no cache, image, volume, old backup or application source is pruned.
- A5: Independent review of the exact maintenance plan precedes runtime mutations. Record actual PASS/FAIL/NOT_RUN, capacity and limitations.

## Scope and risks
This is shared local infrastructure maintenance, not application feature work. Docker/Ubuntu maintenance interrupts both local products. Backups on C/D share one physical disk and protect rollback, not physical-disk loss. Capacity must be checked at each stage. Stop before mutation if there is insufficient space, active competing work, destination conflict, missing backup coverage, or unsupported UI behavior.

Task: tasks/STORAGE-001/task.json
