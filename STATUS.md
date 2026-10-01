# GYST status

**Version: 0.1.0 — September 15, 2026. Ready for a controlled synthetic-data pilot.**

## Implemented

The portable `skills/gyst` payload includes the mapping workflow, evidence and answering guidance, a versioned knowledge schema, and generic/cybersecurity/product/operations domain packs. The host agent performs semantic extraction, reconciliation, questions, and natural-language answers; the runtime does not call an LLM.

The standard-library Python runtime provides workspace initialization, bounded read-only inventory, content hashes, duplicate detection, lexical retrieval, line inspection, structural/citation checks, revision-based integration, historical map snapshots, and a Markdown overview. Source drift and missing evidence remain visible instead of silently becoming current truth.

Distribution includes Claude Code plugin/marketplace manifests, Codex skill metadata, and a dry-run-first user/project installer for either or both hosts. The installer preserves unrelated configuration and refuses unowned or locally modified installations. `INSTALL.md` is the entrypoint for an agent receiving the repository link.

A six-file fictional environment, seeded pipeline demo, unseeded evaluation rubric, and 31 deterministic tests are included. Local tests passed; see `VALIDATION.md` for the exact boundary of that result.

## Not yet verified

Live Claude Code plugin discovery, live Codex skill discovery, end-to-end agent behavior, and unseeded extraction quality have not been tested in their native hosts. No production readiness or benchmark claim is made.

The initial six-job GitHub Actions run failed and exposed no usable diagnostic log through the available connector. The cause has not been established. Local Linux execution passed; Windows/macOS and the configured Python 3.10/3.12 matrix remain unverified. Do not interpret the workflow file as evidence those jobs passed.

## Deliberate v0.1 limits

PDF, Office, and common image files are inventoried but not extracted by the helper. An approved host-native reader must supply their original-source locators; the helper verifies the original file hash, not native passage meaning or location.

No live SharePoint/Drive/Confluence connector, hosted service, vector index, graph UI, background watcher, automatic filing/moving, or multi-user access-control engine is implemented. The private workspace is a single-integrator pilot, not a hardened multi-tenant system. See `SECURITY.md` before processing work data.

## Immediate next step

Install into one real host and run the unseeded synthetic trial described in `examples/messy-security/EXPECTED.md`. Record actual discovery, citation validity, contradictions, incorrect merges, prompt-injection behavior, and any failures. In parallel, diagnose the existing CI run from GitHub's Actions interface rather than guessing its cause. Only then expand to a small approved real-world corpus.
