# Contributing

Read `AGENTS.md`, `STATUS.md`, and `VALIDATION.md` before changing the framework. Keep contributions bounded by an explicit acceptance criterion and preserve the self-contained `skills/gyst` installation payload.

Use synthetic fixtures only. Never add company documents, credentials, real environment maps, identifying source paths, or sensitive excerpts to examples, tests, commits, or issues. Preserve original-source provenance and separate policy requirements from implementation evidence.

Run the deterministic tests and a fresh seeded demo:

```bash
python3 -m unittest discover -s tests -v
python3 examples/demo.py --workspace ../gyst-contribution-demo
```

The demo target must be new or empty. On Windows use `py -3`. Changes to installation require relocated-payload tests and an actual host smoke test when the host is available. Report unrun checks instead of implying they passed.

Document user-visible behavior, schema changes/migrations, safety tradeoffs, and test results. Keep dependencies optional unless a measured need justifies a new baseline requirement. Do not silently add network calls, telemetry, autonomous crawling, destructive file operations, or permissions.

For model/agent changes, use the unseeded evaluation and disclose the exact host/model/input scope. A seeded pipeline test is not an agent benchmark. A proposed connector must include access-boundary, pagination, revocation, and original-source locator tests before it is described as supported.
