# Architecture

## Three responsibilities, one evidence contract

**The host agent reasons.** It interprets documents, proposes entities and scoped aliases, reconciles claims, asks questions, and writes cited answers. This behavior lives in the skill and focused references. It is not a hidden model call in the CLI.

**The runtime records and checks.** Standard-library Python inventories authorized local files, hashes versions, identifies identical duplicates, retrieves text, validates record structure/citation mechanics, applies revision-checked proposals, and renders a Markdown view.

**The workspace persists understanding.** JSON stores the canonical map and source manifest. Hash-addressed history preserves prior map bytes. Run records/checkpoints let agents resume and review source changes. The runtime records inventory/apply events; semantic work checkpoints are maintained by the agent.

The framework repository is software. The workspace is private organizational data. They must remain separate.

## Current model

A source has a root-relative identity, path, observed version hash, format/readability status, and inventory metadata. A root/path change is not automatically resolved as the same identity. Identical hashes identify duplicate bytes, not independent authority.

An entity has an ID, type, scope, name, aliases, and source evidence. A relationship is a claim with an entity subject, predicate, entity/literal object, human-readable statement, scope, as-of value, basis, lifecycle, confidence rationale, contradiction links, and evidence. Questions link back to affected records and carry priority, respondent role, state, and resolution.

The distinction between `documented`, `reported`, and `inferred` is separate from lifecycle and confidence. Conflicting claims can both be well-documented. A high-confidence policy requirement does not establish high-confidence implementation.

Every entity/claim cites original source IDs, version hashes, and locators. Text ranges and supplied quotes can be mechanically checked. Native locators need the host or human to verify meaning/location. Validation cannot establish semantic entailment or completeness.

`apply` uses an exclusive writer lock, expected base revision, atomic replacement of the canonical file, and prior-map snapshots. One integrator owns canonical writes. It is not a multi-user transactional database or a hardened defense against an attacker who can write the workspace.

## Portability decisions

The installed payload is entirely inside `skills/gyst`. No runtime database, provider API, or network service is required. JSON is canonical because it supports deterministic tooling; Markdown is a human-readable view. Schema version `0.1` is explicit. Future migrations must preserve source/claim identity and history or declare a breaking change.

Domain packs are declarative vocabularies and interview guidance, not code-loaded plugins or licensed control catalogs. Generic, cybersecurity, product, and operations packs reuse the same claim model. Do not reproduce proprietary requirements or assign external control IDs without an authorized versioned source.

## Connector boundary — planned, not implemented

A future connector should provide bounded enumeration, authorized fetches, original resource IDs/URLs, versions/ETags, modified and observed timestamps, deletion/tombstone state, original locators, classification, and effective audience/permission metadata. It must distinguish inaccessible from deleted and preserve partial-result warnings.

Before enabling a connector: define allowlisted roots/resources, delegated read-only access, the model boundary, rate limits, pagination/checkpoint behavior, retention, and how permission revocation invalidates derived views and cached answers. Credential material stays in the host's approved secret store, never map records or Git.

Exported documents can lose ACLs. Until real authorization-aware retrieval exists, separate workspaces are the boundary; do not mix corpora with different permitted audiences and call it secure because the output is local.

Do not couple source identity to a temporary download path. Future extractor records should link the original resource/version to derived text and its extraction method/version, preserving page/cell/slide mapping. Derived text is not independent evidence.

## Indexes and graph views — planned

SQLite/FTS, embeddings, graph exports, and visual maps should be replaceable projections of the canonical records. They must preserve citations and lifecycle/permission filters, and must be rebuildable. Retrieval scores are not confidence scores. A vector database is not required for v0.1's pilot.

The next bottleneck should determine the next component: measured retrieval misses justify better indexing; demonstrated native-format coverage gaps justify extraction; controlled workflow trials justify more automation. Do not start with a distributed service or agent swarm before the evidence loop works.
