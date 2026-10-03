# Answer from the map without inventing certainty

Start with the requested answer, not a description of the workflow. Keep paragraphs short. Use no more than three prioritized findings unless the user requests more detail.

## Retrieval

Read relevant entities/claims, check lifecycle, then retrieve original passages. Search lexical variants and aliases in scope. A keyword miss is not evidence of absence. A generated report is a view of the map, not an independent source. Do not cite earlier AI answers as corroboration.

Refresh or check relevant source hashes before current-state answers. Read surrounding text to distinguish requirements, plans, examples, implementation, and historical notes. For dependency questions, explain whether the link is explicit or inferred; do not infer complete outage impact from a partial map.

## Answer contract

1. **Answer:** the strongest supported conclusion, with a clear date/scope when material.
2. **Evidence and uncertainty:** source path/ID plus locator and version; show important conflicting evidence beside the claim it qualifies.
3. **Next action:** one concrete verification or clarification when uncertainty prevents a decision.

Use citations such as `[wiki-2024.md, L2-L4; src-…; sha256:…]` in local Markdown. Use the host's native citation system when it provides stable original-source references. Do not invent clickable SharePoint links from export filenames.

Say “I found no owner documented in the reviewed sources” rather than “there is no owner.” Say “The policy requires MFA; implementation has not been verified” rather than “MFA is enabled.” Say “Two sources disagree” rather than choosing the most recent-looking file.

## Confidence and coverage

Mention unreadable, unreviewed, missing, inaccessible, or extraction-required sources when they could change the answer. Do not claim an exhaustive inventory of the company when the scope is one export. Native locators need host/human verification. Stop rather than answer from evidence unavailable to the authorized audience.

A reported answer can resolve a documentation ambiguity while leaving implementation assurance open. Inferences must state their premises and a credible alternative explanation. Do not present risk/compliance classifications as certification or professional sign-off.

## Examples

These are hypothetical response patterns. Use the dates, roles, and findings from the actual reviewed sources; do not treat this wording as evidence about an environment.

**Who owns remediation?** “Unresolved. The 2024 wiki assigns Security, while the 2026 handoff note says Infrastructure handles execution. A split between accountability and execution is plausible but not established. Ask for the approved RACI and effective date.” Cite both originals.

**Which systems rely on AD?** List only explicitly supported relationships, separate possible aliases, and name the corpus boundary. Do not conflate Entra ID, an on-premises AD domain, and a separate cloud tenant because they share a vendor.

**What changed?** Compare source versions and claim lifecycle transitions. Show new evidence and remaining contradictions. Absence from an export does not prove removal from production.
