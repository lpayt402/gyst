# Evidence, identity, and uncertainty

The canonical contract is `assets/knowledge.schema.json`. All IDs share one namespace. Entity IDs, claim IDs, and question IDs must be unique. Every entity/claim must have at least one evidence item; do not create free-floating facts.

## Evidence item

```json
{
  "source_id": "src-example",
  "sha256": "<64 lowercase hexadecimal characters from the inventory>",
  "method": "text",
  "locator": "L5-L8",
  "quote": "An optional short exact excerpt"
}
```

The placeholder hash is explanatory, not valid sample data. Get actual IDs/hashes from `.gyst/manifest.json`. `text` locators refer to physical UTF-8 text lines after BOM handling. CSV locators are file lines, not logical record numbers when cells contain embedded newlines. HTML is text, not a browser view. No regex-based extraction is a substitute for semantic review.

`native` evidence uses an original PDF/Office/image hash and a precise locator such as `page 3, Access Reviews` or `sheet Owners!B12:D12`. The CLI checks the file version but cannot validate that a native passage exists or supports the claim. Record this as a verification limit. Keep OCR/extraction uncertainty visible and do not let derived text masquerade as an independent original.

## Claim dimensions

- **Basis:** `documented` means a source explicitly says it; `reported` means a human/source report; `inferred` means a deduction. None alone means verified in production.
- **Lifecycle:** `active`, `disputed`, `needs_review`, `superseded`, `retracted`. Historical claims remain visible and must not be answered as current truth.
- **Confidence:** `low`, `medium`, `high` plus a rationale describing source authority, recency, specificity, conflicts, and verification limits. These are judgments, not calibrated probabilities.

Use `as_of` as the source-supported effective/observation date, or `unknown`. Do not substitute file mtime or today's date. Explain mixed dates in `rationale`; separate different scopes into different claims. A policy requiring MFA and an export showing one exception are not necessarily contradictory: requirement and implementation are different predicates.

## What validation can and cannot establish

The helper validates the shipped JSON Schema subset, required evidence, ID/reference integrity, text range bounds and supplied exact quotes, and source version availability. It does not prove semantic entailment, authority, policy compliance, organizational completeness, or that a human response is accurate.

Source drift/missing files create warnings, not automatic erasure. Native locators also warn. Reports must expose these warnings; an agent must not call warning-bearing evidence verified/current. Historic source bytes are not copied automatically, so unavailable historical passages may no longer be independently readable.

Original claims remain immutable in subject, predicate, object, statement, basis, scope, as_of, and evidence. Add a successor ID instead of silently editing meaning. Confidence/state/rationale/contradiction links can evolve with recorded review. Questions become resolved only with a recorded resolution, ideally linking the successor claims and evidence IDs.

## Information hygiene

Do not store credentials, payment data, personal identifiers, or unnecessary excerpts. Secret detection is heuristic and incomplete, especially for native files. Paths, hashes, entity names, inferred relationships, and saved questions may themselves disclose confidential information. Workspace gitignore is a convenience, not access control or a security boundary.
