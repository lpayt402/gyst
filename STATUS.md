# GYST status

**Runtime version 0.1.0 with a bounded document investigation prototype. Ready for a controlled synthetic-data pilot.**

## Implemented

The portable `skills/gyst` payload includes the mapping workflow, evidence and answering guidance, a versioned knowledge schema, and generic/cybersecurity/product/operations domain packs. The host agent performs semantic extraction, reconciliation, questions, and natural-language answers; the runtime does not call an LLM.

The standard-library Python runtime provides workspace initialization, bounded read-only inventory, content hashes, duplicate detection, lexical retrieval, line inspection, structural/citation checks, revision-based integration, historical map snapshots, and a Markdown overview. Source drift and missing evidence remain visible instead of silently becoming current truth.

Distribution includes Claude Code plugin/marketplace manifests, Codex skill metadata, and a dry-run-first user/project installer for either or both hosts. The installer preserves unrelated configuration and refuses unowned or locally modified installations. `INSTALL.md` is the entrypoint for an agent receiving the repository link.

The eight-file fictional BenchBoard environment supports a seeded pipeline demo and a separate unseeded evaluation. The November 23 prototype adds read-only evidence tracing and a resumable goal board with explicit discovery and citation budgets. Proposed answers stay in the private workspace. See the [demo and comparison](docs/GOAL-PROTOTYPE.md).

## Not yet verified

Live Claude Code plugin discovery, live Codex skill discovery, end-to-end agent behavior, and unseeded extraction quality have not been tested in their native hosts. No production readiness or benchmark claim is made.

## Hosted CLI verification

The [November 24 fix-branch run](https://github.com/lpayt402/gyst/actions/runs/45403113637) at `5f7de991d2` passed unit tests and the seeded demo in all six jobs: Ubuntu, Windows, and macOS on Python 3.10 and 3.12. It verifies the physical-path fixture fix for the two macOS failures in the [November 23 main run](https://github.com/lpayt402/gyst/actions/runs/45254102161). The runtime still rejects linked workspace paths. The fix-branch run is not evidence of a green run on main; see the [default-branch workflow](https://github.com/lpayt402/gyst/actions/workflows/tests.yml?query=branch%3Amain) for its current status.

## Deliberate v0.1 limits

PDF, Office, and common image files are inventoried but not extracted by the helper. An approved host-native reader must supply their original-source locators; the helper verifies the original file hash, not native passage meaning or location.

No live SharePoint/Drive/Confluence connector, hosted service, vector index, graph UI, background watcher, automatic filing/moving, or multi-user access-control engine is implemented. The private workspace is a single-integrator pilot, not a hardened multi-tenant system. See `SECURITY.md` before processing work data.

## Immediate next step

Install into one real host and run the [unseeded synthetic trial](examples/access-review/EXPECTED.md). Record discovery, citation validity, contradictions, incorrect merges, prompt-injection behavior, and any failures before expanding the pilot.
