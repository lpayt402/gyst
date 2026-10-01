# Changelog

## 0.1.0 — 2026-09-15

Initial functional baseline for an evidence-first environment-mapping skill/framework.

### Added

- Portable self-contained GYST skill with bounded mapping, source preservation, provenance, scoped identity resolution, contradiction handling, targeted questions, checkpoint/resume guidance, and cited-answer instructions.
- Versioned JSON knowledge schema for entities, claims/relationships, evidence, and questions; generic, cybersecurity, product, and operations domain packs.
- Standard-library Python helpers for initialization, inventory, lexical retrieval, line inspection, validation, revision-checked integration, map history, and Markdown reporting.
- Claude Code plugin/marketplace packaging, Codex skill metadata, and user/project copy installer with dry runs, receipts, idempotence, modification checks, and reviewed update backups.
- Agent-readable link-to-install guide, development instructions, architecture/usage/security documentation, and an acceptance-driven roadmap.
- Six-file fictional environment, seeded reference-map demo, unseeded evaluation rubric, 31 deterministic tests, and a cross-platform CI definition.

### Validation and limitations

Local Linux/Python 3.13.5 tests passed. Initial remote CI reported failure without usable logs; its cause and cross-platform results remain unresolved. Live Claude/Codex discovery and actual unseeded agent performance have not been tested. Native document extraction, live connectors, automatic organization/moves, multi-user access control, and background monitoring are not included.
