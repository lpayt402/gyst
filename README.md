# GYST

## Get Your Shit Together.

GYST supports reviewing a policy, an old wiki page, a ticket export, and a handoff note when they do not quite agree. It helps keep those sources intact, map what each one says, and list the questions that still need an answer. It does not decide which source is authoritative on its own.

**v0.1.0 — working skill and local helpers, not an autonomous hosted platform.** Your agent does the reasoning; the included code does inventory, retrieval, evidence checks, revision-controlled integration, and reporting. No database, API key, or additional Python package is required by the helpers.

## Install by giving your agent a link

Paste this into Claude Code, Codex, or another agent with authorized repository and filesystem access:

```text
Install GYST from https://github.com/lpayt402/gyst.
Read INSTALL.md and follow the route for this agent.
Use user scope, preserve my existing configuration, verify installation,
and stop before reading any organizational documents.
```

This candidate is intended for a private repository. The receiving agent needs authorized repository access; a link does not change permissions or install tools into an ordinary chat session. [Full installation instructions](INSTALL.md).

**Claude Code plugin:**

```text
/plugin marketplace add lpayt402/gyst
/plugin install gyst@gyst-marketplace
/reload-plugins
/gyst:gyst
```

**Codex standalone skill:**

```text
$skill-installer install the skill at https://github.com/lpayt402/gyst/tree/main/skills/gyst
```

Then invoke `$gyst`. A cross-platform installer is also included for user or project scope, for either or both hosts. Choose one installation method per host to avoid duplicate skills.

## What you get

| Layer | Included now |
| --- | --- |
| Agent skill | Bounded mapping passes, scoped entity resolution, contradiction handling, targeted interviews, checkpoint/resume guidance, and cited natural-language answers |
| Local runtime | `init`, `inventory`, `search`, `show`, `validate`, `apply`, and `report` commands; source hashes; duplicate detection; historical snapshots; stale-evidence warnings |
| Domain packs | Generic, cybersecurity, software product, and business operations vocabularies and questions |
| Installation | Self-contained Agent Skills directory, Claude Code plugin/marketplace manifests, Codex metadata, safe copy installer, and manual fallback |
| Evaluation | Synthetic messy environment, seeded plumbing demo, unseeded agent evaluation rubric, and 31 deterministic tests |

What is **not** included: a standalone LLM service, live SharePoint/Drive/wiki connectors, automatic Office/PDF extraction, a vector database, an interactive graph UI, per-user authorization, or a background monitor. Those are explicit extension points, not implied capabilities.

## Use it on an approved folder

Open your agent in a **trusted workspace**, not inside the raw dump. Give it an approved source folder and a separate, new output workspace:

```text
Use GYST to map my approved source folder: /path/to/document-dump
Write the map to a new private workspace: /path/to/environment-map
Use the cybersecurity domain pack.
This source scope and this agent/model are approved for the data.

Keep the originals unchanged. Start with a bounded first pass, distinguish
requirements from implementation evidence, retain contradictions, and ask
no more than three high-value questions at a time. Save a checkpoint.
```

For Claude Code use `/gyst:gyst` (plugin) or `/gyst` (standalone); for Codex use `$gyst` in front of the request. Other hosts can explicitly load `skills/gyst/SKILL.md` when their tools and policies permit.

Then ask normal questions:

> Who owns vulnerability remediation, and which sources disagree?
>
> What depends on our on-premises directory?
>
> What do our policies require that we have not found implementation evidence for?
>
> Explain this product to someone joining the team. Show what is uncertain.

GYST should say **"No owner is documented in the reviewed sources"**, not **"There is no owner."** It should say **"The policy requires MFA"**, not **"MFA is definitely deployed."**

## Try the example without real data

From a checkout with Python 3.10 or newer:

```bash
python3 -m unittest discover -s tests -v
python3 examples/demo.py --workspace ../gyst-demo
```

On Windows, use `py -3` instead of `python3`. The demo requires a new or empty output directory. It generates `../gyst-demo/reports/overview.md` from a **seeded reference map**. It tests the pipeline, not an agent's extraction ability. For a separate extraction trial, use the fictional scattered-information example in [the unseeded evaluation](examples/access-review/EXPECTED.md). Do not give the expected findings to the agent before it has made its map.


## Data boundary

The included helper reads and writes local files and does not call a model, connector, or external service. The example uses fictional files only. If a host agent reads real documents, that host may send their contents to its configured model provider; approve the host, provider, and data scope before using real material. GYST does not enforce source-folder permissions or provide per-user access control. On Windows, workspace folders inherit permissions from their parent folder, so choose a parent with the access rules you need.

## Where everything lives

```text
GYST/                         # Framework repository — no real organizational data
├── INSTALL.md                # Link-to-install playbook
├── AGENTS.md                 # Instructions for developing this framework
├── install.py                # Dry-run-first standalone installer
├── skills/gyst/              # Entire portable skill and runtime
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/               # Knowledge schema and domain packs
│   ├── references/           # Mapping, evidence, and answering guidance
│   └── scripts/gyst.py
├── .claude-plugin/           # Claude Code distribution
├── examples/                 # Fictional inputs, demo, evaluation rubric
├── tests/
└── docs/

private-environment-map/      # Separate, private working directory
├── gyst.json
├── inbox/                    # Optional local source drop; external root also supported
├── map/knowledge.json        # Entities, claims/relationships, and questions
├── proposals/                # Candidate full-map revisions
├── reports/overview.md       # Generated readable view
└── .gyst/                    # Source manifest, history, and run checkpoints
```

The canonical map is JSON for predictable validation; readable reports are Markdown. No graph database is necessary to represent relationships. Future indexes must remain rebuildable from evidence-backed records.

## Trust and practical limits

Originals are read-only to the helpers. A claim records its source ID, version hash, locator, scope, date, basis, lifecycle, and confidence rationale. Changed evidence is flagged, not silently replaced. Conflicting claims stay separate.

The helpers search UTF-8 text formats. PDF, Office documents, and common images are inventoried and marked `needs_extraction`; reading them requires an approved host-native reader or a future extractor. Native locators are not automatically verified. Heuristic secret checks are incomplete and are not a DLP system.

**Local files do not mean local inference.** A cloud agent may receive file contents and tool output. Approve that boundary before processing work data. Keep source material and generated maps out of this framework repository. GYST is not an access-control engine or a compliance certification.

[Usage](docs/USAGE.md) · [Host compatibility](docs/HOSTS.md) · [Architecture](docs/ARCHITECTURE.md) · [Security](SECURITY.md) · [Roadmap](ROADMAP.md) · [Validation](VALIDATION.md)

License: MIT. Copyright 2026 GYST contributors.
