# Using GYST

## A folder is enough to begin

Install the skill, start the host in a trusted directory, and name the approved source root, new output workspace, domain, and permitted model/data boundary. The agent should ask only for missing authorization and then begin a bounded pass.

A SharePoint/Drive/wiki export can be the source folder. This does not provide live access to the originating platform or reconstruct its permissions. Keep separate workspaces for separate audiences/access boundaries.

## Helper commands

From a framework checkout, use `python3 skills/gyst/scripts/gyst.py`. From an installed skill, use its actual absolute `scripts/gyst.py` path. On Windows use `py -3`.

```bash
# Approved source is read-only; output must be new/empty and disjoint.
python3 skills/gyst/scripts/gyst.py init ../environment-map --source /approved/source-folder --domain cybersecurity
python3 skills/gyst/scripts/gyst.py inventory ../environment-map
python3 skills/gyst/scripts/gyst.py search ../environment-map "privileged access"
python3 skills/gyst/scripts/gyst.py validate ../environment-map
python3 skills/gyst/scripts/gyst.py report ../environment-map
```

`init` creates an empty map. `inventory` does not extract entities or answer questions. `report` renders whatever has been integrated; running it on an empty map should not be mistaken for a completed analysis. Invoke the agent skill for semantic work.

For text inspection, take the actual source ID and line count from `.gyst/manifest.json`:

```text
python <skill>/scripts/gyst.py show <workspace> <source-id> --start 1 --end 12
```

Choose an existing line range; at most 200 lines and 40,000 characters are returned. Search returns bounded lexical hits with IDs, hashes, and line locators; it is not semantic search or an exhaustive answer.

## Integrating a map

`map/knowledge.json` is canonical. The agent reads its bytes, computes their SHA-256, and proposes a complete next model:

```json
{
  "base_revision": "<SHA-256 of the current knowledge.json bytes>",
  "knowledge": {
    "schema_version": "0.1",
    "entities": [],
    "claims": [],
    "questions": []
  }
}
```

The empty arrays above illustrate the envelope, not an instruction to discard records. Preserve existing IDs. Entity and claim records require evidence. See the bundled schema and the executable synthetic example in `examples/demo.py` for complete valid records.

```text
python <skill>/scripts/gyst.py apply <workspace> <proposal-file>
python <skill>/scripts/gyst.py report <workspace>
```

`apply` rejects stale base revisions, invalid references/evidence structure, silent record deletion, and mutation of a claim's meaning/evidence under the same ID. It records previous map bytes in history. Add successor claims and update lifecycle state instead of rewriting past claims.

Warnings do not automatically block integration. Changed/missing evidence is not current verified support; native-file citations are hash-checked but need host/human locator verification. The agent must carry those qualifications into reports and answers. `valid: true` is a structural/evidence-mechanics result, not a truth/completeness guarantee.

## Document coverage

UTF-8 `.md`, `.txt`, `.csv`, `.tsv`, `.json`, `.yaml`, `.yml`, `.log`, and `.html` files can be searched as text. HTML is not rendered. CSV locators refer to physical file lines, not logical row numbers when values span lines.

`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.png`, `.jpg`, and `.jpeg` are inventoried as native files requiring extraction. Approved host readers may inspect them and create claims with original-file hashes and page/cell/slide locators. This CLI does not extract them or scan their contents for secrets. Legacy binary Office files, archives, unsupported encodings/formats, oversize files, and excluded locations must remain visible as coverage gaps.

Default limits are 16 MiB per file and 5,000 files per inventory; they are configurable in the private `gyst.json`. The limits are safety/performance bounds, not a tested corpus-size capacity promise. Narrow source scope before raising them. Metadata and source IDs are tied to one root; renames create a new ID rather than guessed identity continuity.

## Clarifications, refresh, and recovery

At each checkpoint, expect an overview, a coverage statement, changed facts/relationships, important contradictions, and no more than three questions. Additional reports or a proposed folder taxonomy are agent outputs, not physical reorganizations.

Record human answers as dated, scoped source notes only when adding new source material is authorized; otherwise the owner should add them. Inventory and cite those notes. Mark a claim `reported` when appropriate; an answer is not an audit.

To resume, ask the agent to read the private workspace's map, manifest, and latest checkpoint rather than restarting. To refresh, inventory again, compare source hashes with the checkpoint, and revisit affected claims. The helper flags drift but does not autonomously re-extract or schedule work.

A stale `.gyst/write.lock` is not permission to kill a process. Verify no writer is active before removing only that lock. Never solve a revision conflict by overwriting the entire map.
