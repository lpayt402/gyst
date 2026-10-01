# Validation record

Date: September 15, 2026. Version: 0.1.0.

## Observed local execution

Environment: Linux, Python 3.13.5.

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 31 tests passed; 1.380 seconds |
| `python examples/demo.py --workspace <new-temporary-directory>` | Completed; six ready synthetic sources, valid seeded map, no validation warnings |
| `python -m compileall -q install.py skills/gyst/scripts examples tests` | Completed successfully |
| Independent JSON Schema Draft 2020-12 check of the schema and seeded map | Passed using `jsonschema` available in the verification environment; it is not a runtime dependency |

The local verification copy's runtime, installer, schema, test file, skill file, demo, and synthetic inputs were checked against the corresponding Git blob identities. This was not an authenticated local clone of the entire repository. Some documentation/distribution files were not present in that local test copy, so the installer tests demonstrate copy/update/relocation behavior, not native host discovery or a complete packaged-host certification.

Tested runtime blob: `b71e77810d77d2e81e6580d0a1b87b8625ab7107`.
Tested installer blob: `48bca0fad9e9d0178c3190a8011036de4ed3dd7a`.
Tested tests blob: `49958c6ddc23f1ce0647483b9e7e070f4c17c585`.
Tested schema blob: `be5851fa7c3831dfffad09b892adad0c16113051`.

## What the tests cover

Read-only source preservation; stable path-based IDs; duplicate bytes; bounded search/show; changed-source reporting; valid integration/history; invalid quotes and line ranges; unknown references; duplicate IDs; required/unknown schema fields; optimistic revision conflicts; immutable claim meaning; no silent record deletion; lifecycle updates; stale/missing evidence warnings; heuristic secret handling; native-format limitations; inventory limits; unsupported/sensitive files; traversal/link checks; writer locks; disjoint roots; seeded demo behavior; installation scope; dry runs; idempotence; preservation of existing instruction files; refusal of unowned/modified installs; update backups; user-scope and relocated-script behavior.

Some filesystem checks are platform-dependent. A symlink creation check may be skipped by returning early when the platform denies permission to create the fixture. No Windows/macOS execution is claimed from the Linux result.

## Seeded demo result

The demo deliberately creates a reference map: three entities, three claims (including two disputed responsibility claims), and two open questions. It integrates and renders that map against six synthetic source files. The policy claim remains a requirement, not a claim that MFA deployment was observed.

**This is a plumbing test, not evidence that a model independently discovered the correct map.** The separate unseeded evaluation must be performed with the chosen host/model; do not show the expected-answer document or seeded map to the agent before evaluating extraction.

## GitHub Actions status

The initial run for implementation commit `bb8610530003da7fc4cda88ac6dfbc0f73601f40` was:

https://github.com/lpayt402/gyst/actions/runs/34999927250

It reported failure for all six configured OS/Python combinations. Fetching an available job's logs returned `BlobNotFound`; no usable diagnostic output was obtained. The cause was not determined. Do not label this a code failure, quota failure, billing failure, or successful cross-platform validation without further evidence.

The committed workflow targets Ubuntu, Windows, and macOS with Python 3.10 and 3.12. Later pushes may trigger additional runs; inspect their actual outcomes. This record does not predict or claim their success.

## Not performed

No live Claude Code or Codex installation/discovery session; no native host plugin validator execution; no unseeded LLM extraction/answering evaluation; no actual SharePoint/Drive access; no native PDF/Office extraction; no real organizational data test; no adversarial security audit; no performance benchmark on large corpora; no calibrated confidence study; no multi-user authorization test.

The CLI's `valid: true` is structural and citation-mechanical validation, not semantic truth, coverage, source authority, implementation assurance, or safety certification. Stale/native warnings require explicit review even when structure passes.

## Next validation record

Record date, framework commit, host and host version, model/provider, approved input scope, exact prompts, installation route, observed outputs, source preservation, unsupported-claim count, citation checks, contradiction retention, aliases/scopes, injection behavior, costs when available, and unresolved failures. Use only synthetic or explicitly approved/redacted material in a public result.
