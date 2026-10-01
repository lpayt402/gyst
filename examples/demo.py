#!/usr/bin/env python3
"""Seed a reference map from synthetic fixtures; not an autonomous agent benchmark."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gyst", ROOT / "skills/gyst/scripts/gyst.py")
gyst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gyst)


def run(workspace):
    work = Path(workspace).expanduser().resolve()
    gyst.init(work, domain="cybersecurity")
    for source in (ROOT / "examples/access-review/inbox").iterdir():
        shutil.copyfile(source, work / "inbox" / source.name)
    inventory = gyst.inventory(work)
    sources = {row["path"]: row for row in gyst.load(work / ".gyst/manifest.json")["sources"]}
    def evidence(name, line):
        row = sources[name]
        return {"source_id": row["id"], "sha256": row["sha256"], "method": "text", "locator": f"L{line}-L{line}"}
    entities = [
        {"id": "ent-benchboard", "name": "BenchBoard", "type": "system", "scope": "Rivet & Root Bicycle Cooperative", "aliases": [], "evidence": [evidence("access-policy.md", 3)]},
        {"id": "ent-operations-director", "name": "Operations Director", "type": "role", "scope": "Rivet & Root Bicycle Cooperative", "aliases": [], "evidence": [evidence("decision-record.md", 3)]},
        {"id": "ent-it-service-desk", "name": "IT Service Desk", "type": "role", "scope": "Rivet & Root Bicycle Cooperative", "aliases": [], "evidence": [evidence("ticket-export.csv", 2)]},
    ]
    def claim(identifier, predicate, value, statement, date, name, line, state="active", kind="literal"):
        return {"id": identifier, "subject": "ent-benchboard", "predicate": predicate, "object": {"kind": kind, "value": value}, "statement": statement, "scope": "Rivet & Root Bicycle Cooperative", "as_of": date, "basis": "documented", "state": state, "confidence": "medium", "rationale": "The source states this; status and implementation need separate evidence.", "contradicts": [], "evidence": [evidence(name, line)]}
    claims = [
        claim("clm-exception-recollection", "exception_expiry", "2026-10-15", "The August handoff recalls a possible extension to 2026-10-15 but has no written approval.", "2026-08-20", "handoff-2026.md", 3, "disputed"),
        claim("clm-exception-decision", "exception_expiry", "2026-09-30", "The signed decision says EX-041 was not extended and ends on 2026-09-30.", "2026-09-15", "decision-record.md", 3, "disputed"),
        claim("clm-mfa-required", "requires", "MFA for individual staff accounts", "The access standard requires MFA; deployment is not established by the policy, and the shared account's closure is not documented.", "2025-11-01", "access-policy.md", 3),
    ]
    claims[0]["contradicts"] = [claims[1]["id"]]
    claims[1]["contradicts"] = [claims[0]["id"]]
    questions = [
        {"id": "q-exception-implementation", "question": "Was the shared BenchBoard account retired or replaced with named MFA accounts by 2026-09-30, and what evidence shows that?", "why": "The signed decision sets an end date, but the reviewed files contain no configuration or closure evidence.", "priority": "P1", "state": "open", "related_ids": [claims[1]["id"], claims[2]["id"]], "suggested_respondent": "IT Service Desk and Operations Director", "resolution": ""},
        {"id": "q-ticket-device", "question": "Do SD-1842 and SD-1889 refer to one tablet or two?", "why": "Both tickets name the front-counter tablet but do not identify the same device conclusively.", "priority": "P2", "state": "open", "related_ids": [claims[0]["id"], claims[1]["id"]], "suggested_respondent": "IT Service Desk", "resolution": ""},
    ]
    knowledge = {"schema_version": "0.1", "entities": entities, "claims": claims, "questions": questions}
    proposal = {"base_revision": gyst.digest((work / "map/knowledge.json").read_bytes()), "knowledge": knowledge}
    path = work / "proposals/seeded-demo.json"
    gyst.write(path, proposal)
    applied = gyst.apply(work, path)
    rendered = gyst.report(work)
    return {"mode": "seeded-reference-not-agent-evaluation", "inventory": inventory, "validation": applied, **rendered}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, help="New or empty private output directory")
    args = parser.parse_args()
    print(json.dumps(run(args.workspace), indent=2))
