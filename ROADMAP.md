# GYST roadmap

Ship the evidence loop before a platform. Everything below is planned unless explicitly identified as implemented in `STATUS.md`.

## 1. Prove the real-host workflow

Run the unseeded synthetic environment in Claude Code and Codex. Confirm link-based installation, actual skill discovery, complete installed references, scoped source approval, safe checkpoint/resume, cited answers, contradiction retention, and refusal to obey the injected note. Diagnose the GitHub Actions failure and obtain observed results across the configured OS/Python matrix.

Acceptance: reproducible records of the host/version/model/commit, passing discovery and invocation, unchanged source bytes, valid original-source citations, no unsupported implementation claims, no cross-scope identity merges, and a useful bounded clarification queue. Failures stay in the evaluation record; do not tune the rubric after seeing results.

## 2. Native document extraction with trustworthy locators

Add optional bounded local extractors for PDF, DOCX, XLSX, and PPTX. Preserve original source identity/version, extractor identity/version, extraction status, and page/paragraph/sheet-cell/slide locators. Support partial/unreadable sections explicitly. No macros, embedded script execution, automatic external conversion, or silent parser installation. Scan extracted text for sensitive content without claiming comprehensive DLP.

Acceptance: fixtures covering tables, empty/image-only pages, malformed documents, oversized/zip-bomb inputs, formulas/cached values, embedded links, and extraction failures. Every derived passage maps back to the original. Document supported and unsupported behavior separately. OCR requires explicit approval and uncertainty labels.

## 3. Permission-preserving connector contracts

Start with read-only SharePoint or another demonstrated source need. Use delegated access, explicit allowed roots, original resource IDs/URLs, versions/ETags, pagination/cursors, bounded fetches, deletion-versus-inaccessibility handling, and audience metadata. Do not import credentials into the knowledge model. Plan revocation/retention before shared retrieval.

Acceptance: duplicate/retry idempotence, interrupted-run recovery, partial-permission behavior, no traversal outside approved scope, no answer from inaccessible evidence, and invalidation of derived views after permission withdrawal. Until that exists, keep separate private workspaces rather than pretending exported ACLs are enforced.

## 4. Measured retrieval and map exploration

Add an optional rebuildable SQLite/FTS index when lexical retrieval misses demonstrate the need. Add graph exports and a local read-only explorer after the relationship model is stable. Consider embeddings only after measuring value against simpler retrieval.

Acceptance: canonical JSON remains authoritative; indexes are rebuildable; source citations, lifecycle, date, scope, and access boundaries survive retrieval; ranking scores never become claim confidence. Compare retrieval coverage against a fixed question set.

## 5. Knowledge lifecycle and practical scale

Introduce explicit schema migrations, source relocation/rename reconciliation, typed temporal assertions, richer evidence lineage, materialized impact views, and reviewed organization proposals. Improve large-corpus batching and incremental extraction based on measured bottlenecks. Add refresh scheduling only with explicit user opt-in.

Acceptance: no silent loss of IDs/history, no auto-merge from name similarity alone, no silent deletion or physical filing changes, bounded resumable runs, deterministic migrations with rollback/review, and tests showing stale evidence cannot be presented as verified current support.

## Not on the critical path

A mandatory vector database, hosted SaaS, autonomous cross-company crawler, elaborate agent swarm, compliance-certification claims, and provider-specific model routing. Add complexity only when a validated user workflow justifies it.
