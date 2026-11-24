# Seeded BenchBoard demo output

Selected fields from the [full walkthrough](../docs/GOAL-PROTOTYPE.md), using fictional fixtures. The walkthrough appends a synthetic line to the handoff between the two goal runs. Both `goal-show` calls returned the saved results, and the canonical map hash stayed the same.

```json
{
  "inventory": {
    "ready": 8
  },
  "validate": {
    "valid": true,
    "warnings": []
  },
  "report": "overview.md",
  "search": [
    "access-policy.md L3-L3",
    "decision-record.md L3-L3",
    "wiki-2024.md L3-L3"
  ],
  "paused": {
    "spent": 4,
    "next": {
      "action": "link",
      "claim_id": "clm-exception-decision",
      "why": "Check both directions of contradiction links to retain competing statements."
    }
  },
  "resumed": {
    "status": "completed",
    "spent": 9,
    "findings": [
      {
        "claim": "clm-exception-recollection",
        "interpretation": "source_statement",
        "source": "handoff-2026.md",
        "locator": "L3-L3",
        "status": "stale"
      },
      {
        "claim": "clm-exception-decision",
        "interpretation": "source_statement",
        "source": "decision-record.md",
        "locator": "L3-L3",
        "status": "citation_verified"
      },
      {
        "claim": "clm-mfa-required",
        "interpretation": "requirement",
        "source": "access-policy.md",
        "locator": "L3-L3",
        "status": "citation_verified"
      }
    ],
    "unresolved": "Was the shared BenchBoard account retired or replaced with named MFA accounts by 2026-09-30, and what evidence shows that?"
  },
  "small_budget": {
    "status": "budget_exhausted",
    "spent": 2
  }
}
```
