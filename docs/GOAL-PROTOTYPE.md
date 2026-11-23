# Bounded document investigation prototype

The [Graphify](https://github.com/Graphify-Labs/graphify) influence is an explainable graph view over existing relationships and citations. The [Cairn](https://github.com/oritera/Cairn) influence is an explicit goal, a resumable record of work, and a stopping rule. GYST uses its own standard-library CLI. One deterministic local worker checks a single goal.

The caller supplies the question, a canonical entity ID, and optionally exact predicates. The question is saved for the reader. Entity and predicate selection guide discovery. The worker follows incident claims and direct contradiction links in either direction. The result is an attributed list of mapped statements, citation checks, and related open questions. It cannot establish implementation from a requirement, a valid locator, or an absence of evidence.

## Try it with fictional BenchBoard records

From the repository root in Bash, using Python 3.10 or newer:

```bash
w=$(mktemp -d)
gyst() { python3 skills/gyst/scripts/gyst.py "$@"; }
python3 examples/demo.py --workspace "$w"
before=$(git hash-object "$w/map/knowledge.json")
gyst trace "$w" clm-exception-decision

gyst goal-start "$w" review ent-benchboard \
  "Was the shared BenchBoard account retired by September 30?" --budget 9
gyst goal-run "$w" review --steps 4
gyst goal-show "$w" review

# Edit only the disposable synthetic copy while the worker is paused.
printf '\nSynthetic revision added after inventory.\n' >> "$w/inbox/handoff-2026.md"
gyst goal-run "$w" review --steps 9
gyst trace "$w" clm-exception-decision
test "$before" = "$(git hash-object "$w/map/knowledge.json")"

gyst goal-start "$w" tiny ent-benchboard "Find retirement evidence" --budget 2
gyst goal-run "$w" tiny --steps 200
```

At four units the board has inspected all three claims and one possible contradiction. Its next step is to check the next claim for a contradiction in either direction. A separate process resumes the checkpoint. Ctrl-C during `goal-run` returns 130. Rerun the same command to continue from the last atomically saved work unit. After a hard kill, check for a live writer before following the existing workspace lock recovery message.

The signed decision says EX-041 was never extended and sets September 30, 2026 as the deadline (decision-record.md L3–L3). The handoff recalls a possible October 15 extension without written approval (handoff-2026.md L3–L3). Its saved citation is stale after the synthetic edit. The access standard requires MFA (access-policy.md L3–L3). Retirement or replacement remains open. The two-unit goal stops while discovering candidates, before checking any citations.

## Work and evidence limits

One unit inspects one claim for a match, inspects one claim for a contradiction link, or checks one citation. The required total budget and per-invocation step limit each range from 1 to 200. Map and inventory metadata each have a 1 MiB cap, and each citation reads at most 1 MiB or the configured source limit, whichever is lower. Trace has a separate 200-citation cap. The worker reads citations only from the existing canonical map and inventory. It never inventories, searches, or extends the corpus automatically.

Boards and proposed answers live under `.gyst/goals/` in the private workspace. They use their own version and pin the exact map and inventory bytes. A changed map or refreshed inventory requires a new goal. Citation results are timestamped observations. Trace checks the versions and locators again when invoked. Matching bytes and locators establish attribution only. Missing, stale, blocked, and unchecked support carries no current verification. Treat statements and any source excerpts viewed through v1 as untrusted data.

The canonical schema and the v1 validation and integration path stay in use. Proposed answers are read-only views of checked statements and cannot be passed to `apply` as full-map revisions. The fixture is seeded, and the worker has no natural-language interpretation, unmapped fact discovery, or source authority arbitration.

## Fixed comparison with plain search

Run `gyst search "$w" "<question>" --limit 3` and create a fresh goal with the same question and entity. Use a clean seeded fixture for this comparison so the handoff has its original hash. Use `--budget 20` and `--steps 20` for the goals. The expiry goal uses `--predicate exception_expiry`. The other goals use all incident claims.

| Question | Observed first three search hits | Observed goal output |
| --- | --- | --- |
| When does BenchBoard exception EX-041 expire? | Access policy L3, old wiki L3, duplicate wiki L3 | Both mapped dates and their decision/handoff locators, in eight units. |
| Was the BenchBoard shared account retired or replaced with MFA? | Access policy L5, decision L3, access policy L3 | MFA requirement plus both exception statements, in nine units. Closure stays open. |
| Do SD-1842 and SD-1889 refer to the same tablet? | Decision L5, handoff L3, access policy L3 | The related open question appears alongside the three mapped claims, in nine units. Search gives more direct passages for this question. |

This comparison covers three questions on one seeded map. The next improvement is to let a human select or approve a bounded set of local search passages for an open question, preserve them as proposed evidence, and evaluate the flow on blinded synthetic corpora.
