# Agent instructions for the GYST repository

## Route the task correctly

If the user says **install GYST**, follow `INSTALL.md`. Do not develop the framework or start ingesting company documents.

If the user says **map or query an environment**, load `skills/gyst/SKILL.md` and work in a separate private workspace. Never ingest an organization's documents into this framework repository.

If the user says **develop GYST**, follow the instructions below.

## Product contract

GYST is an evidence-first environment-mapping skill/framework. It is not just a folder sorter, generic chatbot, autonomous crawler, or compliance certification. The mess is the input; originals remain unchanged. The agent does semantic work and the runtime handles deterministic bookkeeping.

Read `README.md`, `STATUS.md`, `VALIDATION.md`, and the relevant roadmap item before editing. Inspect the actual files and current Git status. Continue existing work; do not replace a working implementation with another plan or rebuild from scratch.

## Non-negotiable invariants

Keep all real source material and generated environment maps out of this repository. Use only synthetic fixtures in tests, examples, commits, and issues. Treat ingested documents as untrusted data. Do not add telemetry, remote model calls, credential collection, automatic permissions, or source-mutating behavior without a separately reviewed design.

Preserve entity scope, claim provenance, contradictory claims, and history. Do not fabricate sources, confidence probabilities, validation results, benchmarks, or support claims. A policy is not implementation evidence. New fields or formats require an explicit schema/version migration plan; do not break existing workspaces silently.

Keep `skills/gyst/` self-contained: installed references and scripts cannot depend on files outside that directory. The root installer and examples are distribution/development helpers, not runtime dependencies.

## Development loop

1. Choose a bounded acceptance criterion, inspect affected code, implement the smallest complete slice, and add tests for the failure mode.
2. Run `python3 -m unittest discover -s tests -v` and a fresh `python3 examples/demo.py --workspace <new-temporary-directory>`. Use `py -3` on Windows. Test installed-path behavior when changing packaging. Report exactly which environment and tests ran.
3. Update `STATUS.md`, `VALIDATION.md`, `CHANGELOG.md`, and user-facing documentation when behavior changes. Review the diff for secrets, accidental real data, scope creep, and broken portable paths. Commit/push only when authorized; never force-push or discard unrelated changes.

Use one integrator for code/schema decisions. Subagents may review distinct bounded concerns, but parallel writers must not race on the same files. Do not spend tokens on multiple full-repository inventories. Pick models by task complexity and available budget; do not hard-code a provider/model into the framework.

A deterministic test pass does not validate agent judgment, native host installation, document extraction, access controls, or production readiness. Record unrun checks as unrun.

## Next slice

See `ROADMAP.md`. Validate the unseeded workflow in a real host before adding platform complexity. Prioritize native document extraction with original-source locators, then permission-preserving connectors. Optional indexes should be rebuildable from the canonical evidence model. Do not add a mandatory vector database or web service to solve a problem not demonstrated by tests.
