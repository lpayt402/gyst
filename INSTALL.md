# Install GYST

**For an agent given this repository link: install the skill; do not begin reading a corpus.**

Choose one route for the current host. Preserve existing skills, instructions, permissions, hooks, and configuration. No administrator access, API key, service, daemon, or database is required by GYST. Local helpers require Python 3.10+; use `python3` on macOS/Linux and `py -3` on Windows when available.

## Link-to-install protocol for agents

1. Read this file, `skills/gyst/SKILL.md`, and the relevant manifest/installer before running anything. Confirm the requested scope; an explicit user-scope request is already authorization to install there. When no scope was given, use an identified trusted project directory; ask one question only if no target can be resolved.
2. Obtain an authenticated checkout using the user's existing Git/GitHub connection. Never request that they paste a token into chat or put a token in a remote URL. Do not make a private repository public. Record the fetched commit; pin a reviewed commit for repeatable deployments. Reuse an existing checkout only after inspecting its status and remote; never reset local work.
3. Prefer the host-native route below, or run `install.py` first without `--apply` and then with `--apply` for the already authorized installation. Do not run two installation methods for the same host. Existing unowned/modified installations must be reconciled, not deleted or overwritten.
4. Verify the installed `SKILL.md`, bundled references, schema, and script. Run the installed script's `--version` when Python is present, then confirm discovery in the host. A successful file copy is not proof of host discovery. Report exact location, source commit, invocation syntax, and any unverified step.
5. Stop. Source scope and model/data approval are separate from installation. Do not initialize a real environment, crawl a share, or run a mapping pass just because installation succeeded.

Do not execute `curl | sh`, elevate privileges, disable a sandbox, install hooks, add network connectors, edit `AGENTS.md`/`CLAUDE.md`, or broadly rewrite host configuration as a shortcut.

## Claude Code: native plugin

Inside Claude Code:

```text
/plugin marketplace add lpayt402/gyst
/plugin install gyst@gyst-marketplace
/reload-plugins
```

Invoke the installed skill:

```text
/gyst:gyst Map my approved source folder into a separate private workspace.
```

The manifest is `.claude-plugin/plugin.json`; the marketplace catalog is `.claude-plugin/marketplace.json`. The plugin payload uses the root `skills/` directory. Native plugin installation defaults to user scope. Use Claude Code's plugin interface or documented CLI `--scope` options when choosing project/local scope; native installation may update its own registry/settings as expected.

Private repositories require working credentials in Claude Code's Git environment. If direct access is unavailable but an authorized checkout exists, use a local marketplace path or the standalone installer rather than exposing credentials.

For development, from a reviewed checkout:

```bash
claude plugin validate .
claude --plugin-dir .
```

Do not simultaneously install the same skill as both a plugin and a standalone Claude skill. Native invocation is `/gyst:gyst`; standalone invocation is `/gyst`.

## Codex: native skill installer

In a Codex host that exposes `$skill-installer`:

```text
$skill-installer install the skill at https://github.com/lpayt402/gyst/tree/main/skills/gyst
```

Specify a reviewed commit instead of `main` for a pinned deployment. Use existing authorized Git credentials for this private repository. The whole `skills/gyst` directory is required; copying only `SKILL.md` loses the schema, references, and runtime.

Then invoke:

```text
$gyst Map my approved source folder into a separate private workspace.
```

Check `/skills` or the host's skill picker. Restart the host if it has not discovered the installation. GYST's `agents/openai.yaml` sets explicit invocation; it is not meant to scan company files merely because it appears relevant.

When the built-in installer is unavailable or blocked, use the included standalone installer below. Do not assume a ChatGPT web conversation has local Codex filesystem access.

## Standalone installer: Claude Code, Codex, or both

From the parent directory where you want a framework checkout:

```bash
git clone https://github.com/lpayt402/gyst.git
cd GYST
python3 install.py --agent both --scope user
python3 install.py --agent both --scope user --apply
```

On Windows PowerShell:

```powershell
git clone https://github.com/lpayt402/gyst.git
Set-Location GYST
py -3 install.py --agent both --scope user
py -3 install.py --agent both --scope user --apply
```

Use `--agent claude` or `--agent codex` to install only the current host. The first command is a dry run; the second writes the reviewed payload.

| Host | User location | Project location |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/gyst/` | `<project>/.claude/skills/gyst/` |
| Codex | `~/.agents/skills/gyst/` | `<project>/.agents/skills/gyst/` |

For a project installation, name an existing trusted directory explicitly:

```bash
python3 install.py --agent codex --scope project --target /absolute/path/to/trusted-project
python3 install.py --agent codex --scope project --target /absolute/path/to/trusted-project --apply
```

Quote paths containing spaces. Do not install into a raw dump whose instruction files may be loaded by the host. The source and installation paths must not use symlinks/junctions; use their reviewed physical paths where necessary.

The installer copies only `skills/gyst/`, records file hashes and the checkout commit when available, and leaves unrelated configuration untouched. Identical reinstallations are no-ops. It refuses to overwrite an installation it does not own or one with local modifications.

### Verify the standalone payload

For a Codex user installation on macOS/Linux:

```bash
python3 "$HOME/.agents/skills/gyst/scripts/gyst.py" --version
```

For Claude, substitute `.claude` for `.agents`. On Windows:

```powershell
py -3 "$HOME/.agents/skills/gyst/scripts/gyst.py" --version
```

Expected version: `0.1.0`. Also confirm actual discovery in the host. This repository's deterministic installer tests do not substitute for an end-to-end Claude/Codex session.

### Update or uninstall

Review/fetch the desired new framework commit without discarding local changes. Rerun the same installer arguments with `--update`; inspect the dry run, then add `--apply`. Untouched previous payloads are backed up beneath `~/.gyst-install-backups/<agent>/` or the project equivalent, outside the host skill search path. Review those backups before deleting them.

Installations created by the host-native installer may not have a GYST receipt. Update them with that same host-native method, or back up and explicitly reconcile before switching methods. Do not manufacture a receipt to bypass the ownership check.

There is no destructive uninstall command in v0.1. Use the host-native uninstall for plugins. For a copied skill, review the exact `gyst` directory and remove only that directory after preserving local modifications. Do not delete the parent `.agents`, `.claude`, user profile, or environment workspace.

## Other agents and chat products

An Agent Skills-compatible host can load the entire `skills/gyst` directory in its documented skill location. A host without discovery can explicitly read `SKILL.md` and its references using approved tools. Without Python, the workflow is instruction-only and validation must be described as manual.

Claude Desktop, ChatGPT, Cursor, Hermes, and other hosts have their own distribution and tool-access rules. This release does not claim automatic installation into all of them from a link. Do not guess a configuration path or claim shell/native-file capabilities the host lacks.

## Troubleshooting

**Private-repo access failed:** verify the current host's authorized Git access; a connection in another application does not necessarily carry over.

**Installed but not listed:** verify scope/path, complete directory contents, and host skill discovery; reload/restart before changing configuration.

**Existing installation refused:** identify its original installer and preserve edits; update with the owning method rather than forcing replacement.

**No source data was mapped:** that is expected. Invoke GYST with an approved source scope and a separate new workspace after installation.

Host conventions were checked against the official references in [HOSTS.md](docs/HOSTS.md) on September 15, 2026. Treat future host changes as requiring verification, not silent fallback guesses.
