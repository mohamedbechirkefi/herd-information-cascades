<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# experiments/

Runnable configurations (schema `src/herd/schemas/config-v1.json`). Protocols and reports live in `research/experiments/EXP-NNN/`.

- `EXP-001-R001.json`: the EXP-001 smoke matrix (exploratory; `herd.cli smoke`).
- `EXP-001-R002.json`, `EXP-001-R003.json`: exploratory throughput and seed-spread probes on the EXP-002 and EXP-003 matrix shapes, one fifth of the episodes, seeds 100 to 109 (disjoint from the confirmatory seeds).
- `EXP-001-R004.json`: exploratory `window-2` cells (amendment proposal P-1).
- `EXP-002.json`, `EXP-003.json`: confirmatory configurations of the frozen protocols v1.0 (owner-approved 2026-11-24). `herd.cli run` accepts them only while their canonical SHA-256 and the protocol hashes match `research/freeze.json` and the registry; never edit them (a change is a new study version).
