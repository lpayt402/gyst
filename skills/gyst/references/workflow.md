# Mapping workflow

## 1. Scope and inventory

Record the authorized root, output workspace, intended question/audience, model boundary, exclusions, and run time. Default to read-only sources and a restricted workspace. Never infer permission from technical accessibility. Keep company data outside the framework repository.

Run inventory before reading. A `ready` status means readable text, not reviewed content or trustworthy evidence. `needs_extraction` means only bytes/metadata were inventoried. `missing` means not observed, not proven deleted. A directory permission error or file-count cap aborts rather than replacing the manifest with partial results. Inspect exclusions and report them.

Prioritize foundational architecture, responsibilities, policy, and current procedures, then targeted evidence. Avoid loading an entire corpus into one context. Work in batches of at most 20 sources; reduce the batch for large documents. Record source ID plus SHA-256 after each completed batch so a resumed session can identify changed files.

## 2. Extract with scope

Extract entities (systems, roles, processes, vendors, data, products, requirements) and claims about them. Names are not identities. Alias resolution must account for business unit, tenant, environment, location, and time. Prefer stable readable IDs such as `ent-corporate-ad`; maintain IDs through naming changes.

Relationships are claims: subject ID, predicate, entity/literal object, scope, date, basis, state, confidence/rationale, contradictory claim IDs, and evidence. Separate normative statements (must/shall) from reported practices and tested observations. Capture contradictory sources before attempting reconciliation.

## 3. Reconcile instead of flattening

Compare authority, effective date, scope, independence, and directness. File modification time is not an effective date. A recent informal note may be useful without superseding an approved policy. Two copied wiki exports are one evidentiary lineage, not two confirmations.

Keep both sides of material contradictions as `disputed` with reciprocal `contradicts` references. Explain plausible scope/time differences. Prioritize questions that unlock multiple uncertainties or affect important decisions. Ask no more than three at once; include what was found, the precise ambiguity, and the best respondent role.

If a human answers, create a dated, minimal note in the approved source root only when adding new source material is explicitly authorized. Otherwise ask the owner to place the note there. Do not edit original records. Identify the respondent's role and scope without collecting unnecessary personal data. Inventory the note, cite it, and distinguish a reported assertion from independently verified implementation.

## 4. Publish safely

Read current `map/knowledge.json`. Build a proposal with its byte-level SHA-256 as `base_revision` and a full next `knowledge` object. Keep existing records. Do not change a claim's meaning or evidence under its existing ID; create a successor and mark the old claim superseded. `apply` enforces the immutable fields and rejects stale revisions.

Validate then apply. Structural errors block integration. Stale/missing and native-locator warnings must be disclosed and reviewed: `valid: true` does not mean current or semantically correct evidence. Render `reports/overview.md`; additional domain reports should cite the same claims rather than invent new ones.

Save a private checkpoint in `.gyst/runs/` (use a unique descriptive filename) containing scope, processed versions, deferred formats, changes, unresolved IDs, the next bounded batch, and any approvals. Never log credentials or full raw documents. This checkpoint is agent-maintained; the helper does not autonomously manage a queue.

## 5. Refresh and query

On refresh, inventory again and compare version hashes to the checkpoint. Reread changed sources and affected claims. Preserve history; mark unsupported current conclusions for review. No daemon/watch job is included.

For queries, retrieve candidate claims and source passages, verify relevance and version, then follow `answering.md`. Refuse to reveal knowledge beyond the authorized audience. v0.1 has no per-user access-control engine: keep separate workspaces for separate access boundaries.

## Optional organizational output

Produce a proposed folder taxonomy, glossary, owner register, dependency view, stale-document queue, and evidence-gap register only when useful to the user's goal. This is a proposal layer; applying physical moves, retention changes, deletions, or permission changes requires separate authorization and tooling.
