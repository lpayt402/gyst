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

The original seeded demo integrated and rendered three entities, three claims, and two open questions against six synthetic source files. The current BenchBoard fixture has eight files and two disputed exception-expiry claims. The policy claim remains a requirement, not a claim that MFA deployment was observed.

**This is a plumbing test, not evidence that a model independently discovered the correct map.** The separate unseeded evaluation must be performed with the chosen host/model; do not show the expected-answer document or seeded map to the agent before evaluating extraction.

## GitHub Actions status

The initial run for implementation commit `bb8610530003da7fc4cda88ac6dfbc0f73601f40` was:

https://github.com/lpayt402/gyst/actions/runs/34999927250

It reported failure for all six configured OS/Python combinations. Fetching an available job's logs returned `BlobNotFound`; no usable diagnostic output was obtained. The cause was not determined. Do not label this a code failure, quota failure, billing failure, or successful cross-platform validation without further evidence.

The committed workflow targets Ubuntu, Windows, and macOS with Python 3.10 and 3.12. The November 23 main run and the local verification of the follow-up are recorded below.

## Not performed

No live Claude Code or Codex installation/discovery session; no native host plugin validator execution; no unseeded LLM extraction/answering evaluation; no actual SharePoint/Drive access; no native PDF/Office extraction; no real organizational data test; no adversarial security audit; no performance benchmark on large corpora; no calibrated confidence study; no multi-user authorization test.

The CLI's `valid: true` is structural and citation-mechanical validation, not semantic truth, coverage, source authority, implementation assurance, or safety certification. Stale/native warnings require explicit review even when structure passes.

## Next validation record

Record date, framework commit, host and host version, model/provider, approved input scope, exact prompts, installation route, observed outputs, source preservation, unsupported-claim count, citation checks, contradiction retention, aliases/scopes, injection behavior, costs when available, and unresolved failures. Use only synthetic or explicitly approved/redacted material in a public result.

## GYST 2.0 prototype validation

Linux cloud workspace, Python 3.12.14, starting from main at `29a84d0b5a8285e470575a302c68a763f21eae98`. All 31 v1 and four prototype tests passed. A fresh v1 demo inventoried eight ready files and reported a valid seeded map with zero warnings. The prototype CLI tests cover pause/resume, discovery budget exhaustion, contradiction links, policy handling, changed source support, map preservation, and inventory revision drift.

A separate CLI subprocess received SIGINT after completing ten work units on a synthetic fixture with 100 citations. It exited 130, and a new process resumed the ten-unit checkpoint and completed at 108 units. Canonical map bytes were identical before and after goal execution. The three-question plain search comparison is recorded in [the prototype demo](docs/GOAL-PROTOTYPE.md).

## November 24 demo and CI follow-up

Baseline main: `88cfe4de85f1f0018c47b3bfb490e2f34dda08ac`. On Linux with Python 3.12.14, `python3 -m unittest discover -s tests -v` passed all 35 baseline tests. [The main workflow run](https://github.com/lpayt402/gyst/actions/runs/45254102161) passed both Python versions on Ubuntu and Windows. The [macOS 3.10 job](https://github.com/lpayt402/gyst/actions/runs/45254102161/job/137971193550) and [macOS 3.12 job](https://github.com/lpayt402/gyst/actions/runs/45254102161/job/137971194234) each failed the four goal CLI tests with `Link/junction paths are not allowed: /var`.

On Linux, setting `TMPDIR` to a symlink reproduced all four failures on baseline main. After resolving the test-owned workspace path, the same full test command passed all 37 tests with ordinary and symlinked temporary parents. The new tests cover the complete seeded CLI workflow and verify that the runtime still rejects an explicitly linked workspace. The README quickstart and the full [goal walkthrough](docs/GOAL-PROTOTYPE.md) passed with the symlinked temporary parent. The [sample output](examples/goal-demo-output.md) records the fixture results. Hosted verification of the follow-up and native host discovery are pending.
