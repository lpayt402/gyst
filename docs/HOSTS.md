# Host compatibility and primary references

Documentation checked September 15, 2026. These are distribution targets, not a claim that end-to-end sessions were run in every host. See `VALIDATION.md` for observed tests.

| Target | Distribution | Explicit invocation | Status |
| --- | --- | --- | --- |
| Claude Code | Native plugin/marketplace or `.claude/skills/gyst` | `/gyst:gyst` for plugin; `/gyst` standalone | Packaged; live host discovery/smoke test pending |
| Codex local hosts | Native skill installer or `.agents/skills/gyst` | `$gyst` / host skill picker | Packaged; live host discovery/smoke test pending |
| Other Agent Skills hosts | Entire `skills/gyst` directory in a documented host location | Host-specific | Portable format; adapters not tested |
| ChatGPT / Claude chat products | Requires product-specific plugin/skill/tool support | Product-specific | No claim that an arbitrary URL installs a local skill |

## Authoritative references

- Agent Skills specification: https://agentskills.io/specification — skill frontmatter, portable directory structure, and progressive disclosure.
- Claude Code skills: https://code.claude.com/docs/en/skills — standalone locations, explicit invocation, and `disable-model-invocation`.
- Claude Code plugins: https://code.claude.com/docs/en/plugins — plugin layout and namespaced skills.
- Claude Code marketplaces: https://code.claude.com/docs/en/plugin-marketplaces — GitHub catalogs, local sources, private repository authentication, and validation.
- Claude Code plugin installation: https://code.claude.com/docs/en/discover-plugins — installation scope and reload behavior.
- OpenAI skill authoring: https://developers.openai.com/codex/skills/ (redirects to https://learn.chatgpt.com/docs/build-skills) — `.agents/skills` discovery, built-in skill installer, explicit invocation, and `agents/openai.yaml`.

GYST disables implicit invocation through Claude's frontmatter and Codex's `policy.allow_implicit_invocation: false`. This helps prevent accidental mapping, but it is not a sandbox or an authorization mechanism. Other hosts may interpret extensions differently; verify their behavior.

Native plugin systems can provide their own update lifecycle. The standalone copy installer is deliberately conservative: it tracks exact files, refuses local modifications, and does not change host permissions or install network tools. A private GitHub repository remains private after packaging; users still need access.

For future unified plugin distribution, follow the current host's published packaging/registry contract rather than inventing a manifest. Keep the core skill independent of any one registry, provider, model, or orchestration harness.
