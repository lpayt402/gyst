"""Deterministic contracts, not a claim that model behavior is validated."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

g = module("gyst", ROOT / "skills/gyst/scripts/gyst.py")
installer = module("installer", ROOT / "install.py")
demo = module("demo", ROOT / "examples/demo.py")


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.work = self.root / "workspace"
        g.init(self.work)
        self.source = self.work / "inbox/source.md"
        self.source.write_text("# System\nAD supports the portal.\nSecurity owns remediation.\n", encoding="utf-8")
        g.inventory(self.work)
        self.row = g.load(self.work / ".gyst/manifest.json")["sources"][0]

    def model(self):
        evidence = {"source_id": self.row["id"], "sha256": self.row["sha256"], "method": "text", "locator": "L2-L2", "quote": "AD supports the portal."}
        return {"schema_version": "0.1", "entities": [{"id": "ent-ad", "name": "AD", "type": "system", "scope": "corporate", "aliases": [], "evidence": [copy.deepcopy(evidence)]}], "claims": [{"id": "clm-portal", "subject": "ent-ad", "predicate": "supports", "object": {"kind": "literal", "value": "portal"}, "statement": "AD supports the portal.", "scope": "corporate", "as_of": "unknown", "basis": "documented", "state": "active", "confidence": "medium", "rationale": "Explicit source statement; implementation unverified.", "contradicts": [], "evidence": [copy.deepcopy(evidence)]}], "questions": []}

    def apply(self, model, revision=None):
        path = self.work / "proposals/test.json"
        g.write(path, {"base_revision": revision or g.digest((self.work / "map/knowledge.json").read_bytes()), "knowledge": model})
        return g.apply(self.work, path)

    def test_init_preserves_existing(self):
        with self.assertRaises(ValueError): g.init(self.work)
        self.assertIn("Security", self.source.read_text())

    def test_inventory_readonly_and_stable_ids(self):
        before = self.source.read_bytes()
        g.inventory(self.work)
        again = g.load(self.work / ".gyst/manifest.json")["sources"][0]
        self.assertEqual(self.row["id"], again["id"])
        self.assertEqual(before, self.source.read_bytes())

    def test_duplicates_not_removed(self):
        shutil.copyfile(self.source, self.work / "inbox/copy.md")
        g.inventory(self.work)
        rows = g.load(self.work / ".gyst/manifest.json")["sources"]
        self.assertEqual(sum("duplicate_of" in r for r in rows), 1)
        self.assertEqual(len(rows), 2)

    def test_search_and_show(self):
        hits = g.search(self.work, "portal")["hits"]
        self.assertEqual(hits[0]["locator"], "L2-L2")
        self.assertEqual(g.show(self.work, self.row["id"], 2, 2)["lines"][0]["text"], "AD supports the portal.")

    def test_search_reports_changed_source(self):
        self.source.write_text("Changed source", encoding="utf-8")
        result = g.search(self.work, "portal")
        self.assertFalse(result["hits"])
        self.assertTrue(result["unavailable"])

    def test_show_bounds(self):
        with self.assertRaises(ValueError): g.show(self.work, self.row["id"], 1, 200)

    def test_valid_model_and_history(self):
        self.assertTrue(self.apply(self.model())["valid"])
        self.assertTrue(list((self.work / ".gyst/history").glob("*.json")))
        self.assertTrue(g.validate(self.work)["valid"])

    def test_bad_quote(self):
        model = self.model()
        model["claims"][0]["evidence"][0]["quote"] = "Not in the source"
        self.assertFalse(g.validate(self.work, model)["valid"])

    def test_bad_line_range(self):
        model = self.model()
        model["claims"][0]["evidence"][0]["locator"] = "L99-L100"
        self.assertFalse(g.validate(self.work, model)["valid"])

    def test_unknown_references(self):
        model = self.model()
        model["claims"][0]["subject"] = "ent-missing"
        self.assertFalse(g.validate(self.work, model)["valid"])

    def test_duplicate_ids(self):
        model = self.model()
        model["entities"].append(copy.deepcopy(model["entities"][0]))
        self.assertFalse(g.validate(self.work, model)["valid"])

    def test_schema_rejects_missing_or_unknown_fields(self):
        model = self.model()
        del model["claims"][0]["evidence"]
        self.assertFalse(g.validate(self.work, model)["valid"])
        model = self.model(); model["surprise"] = True
        self.assertFalse(g.validate(self.work, model)["valid"])

    def test_revision_conflict(self):
        with self.assertRaisesRegex(ValueError, "Revision conflict"):
            self.apply(self.model(), "0" * 64)

    def test_claim_immutable(self):
        model = self.model(); self.apply(model)
        model["claims"][0]["statement"] = "Changed meaning"
        with self.assertRaisesRegex(ValueError, "immutable"): self.apply(model)

    def test_no_silent_deletion(self):
        model = self.model(); self.apply(model)
        model["claims"] = []
        with self.assertRaisesRegex(ValueError, "delete"): self.apply(model)

    def test_lifecycle_can_change(self):
        model = self.model(); self.apply(model)
        model["claims"][0]["state"] = "needs_review"
        self.assertTrue(self.apply(model)["valid"])

    def test_stale_evidence_warns(self):
        self.apply(self.model())
        self.source.write_text("New version", encoding="utf-8")
        g.inventory(self.work)
        result = g.validate(self.work)
        self.assertTrue(result["valid"])
        self.assertIn("stale/missing", " ".join(result["warnings"]))

    def test_missing_source_retained(self):
        self.apply(self.model()); self.source.unlink(); g.inventory(self.work)
        self.assertEqual(g.load(self.work / ".gyst/manifest.json")["sources"][0]["status"], "missing")
        self.assertTrue(g.validate(self.work)["warnings"])

    def test_sensitive_source_and_map(self):
        self.source.write_text("password=synthetic-test-value", encoding="utf-8")
        g.inventory(self.work)
        self.assertEqual(g.load(self.work / ".gyst/manifest.json")["sources"][0]["status"], "blocked_sensitive")
        self.assertFalse(g.search(self.work, "password")["hits"])
        model = self.model(); model["claims"][0]["statement"] = "password=synthetic-test-value"
        self.assertFalse(g.validate(self.work, model)["valid"])

    def test_native_format_warns_not_parsed(self):
        (self.work / "inbox/file.pdf").write_bytes(b"%PDF-synthetic-not-a-real-document")
        g.inventory(self.work)
        row = next(r for r in g.load(self.work / ".gyst/manifest.json")["sources"] if r["path"] == "file.pdf")
        self.assertEqual(row["status"], "needs_extraction")
        model = self.model()
        model["claims"][0]["evidence"] = [{"source_id": row["id"], "sha256": row["sha256"], "method": "native", "locator": "page 1"}]
        self.assertTrue(g.validate(self.work, model)["warnings"])

    def test_limits_preserve_previous_inventory(self):
        before = (self.work / ".gyst/manifest.json").read_bytes()
        config = g.load(self.work / "gyst.json"); config["max_files"] = 0
        g.write(self.work / "gyst.json", config)
        with self.assertRaises(ValueError): g.inventory(self.work)
        self.assertEqual(before, (self.work / ".gyst/manifest.json").read_bytes())

    def test_unsupported_and_sensitive_names(self):
        (self.work / "inbox/archive.bin").write_bytes(b"binary")
        (self.work / "inbox/.env").write_text("do not read", encoding="utf-8")
        g.inventory(self.work)
        rows = g.load(self.work / ".gyst/manifest.json")["sources"]
        self.assertEqual(sum(r["status"] == "excluded" for r in rows), 2)

    def test_traversal_and_symlinks(self):
        for name in ("../elsewhere", "C:\\private", "/etc/passwd"):
            with self.assertRaises(ValueError): g.source_path(self.work / "inbox", name)
        link = self.work / "inbox/link.md"
        try: link.symlink_to(self.source)
        except OSError: return  # Windows may require privilege for symlink creation.
        with self.assertRaises(ValueError): g.source_path(self.work / "inbox", "link.md")

    def test_lock_and_external_scope(self):
        with g.lock(self.work):
            with self.assertRaises(ValueError): g.inventory(self.work)
        with self.assertRaises(ValueError): g.init(self.root / "nested", source=self.root)
        external = self.root / "external"; external.mkdir()
        work = self.root / "other"; g.init(work, source=external)
        external.rmdir()
        with self.assertRaises(ValueError): g.inventory(work)

    def test_demo_retains_dispute_and_policy_distinction(self):
        work = self.root / "demo"
        result = demo.run(work)
        model = g.load(work / "map/knowledge.json")
        self.assertTrue(result["validation"]["valid"])
        self.assertEqual(sum(c["state"] == "disputed" for c in model["claims"]), 2)
        self.assertIn("not established", model["claims"][2]["statement"])
        self.assertTrue(Path(result["report"]).is_file())


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project"; self.project.mkdir()

    def test_dry_run(self):
        result = installer.install(target=self.project)
        self.assertFalse(result["applied"])
        self.assertFalse((self.project / ".claude").exists())

    def test_scope_required(self):
        with self.assertRaises(ValueError): installer.install()
        with self.assertRaises(ValueError): installer.install(scope="user", target=self.project)

    def test_idempotent_and_preserves_configs(self):
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.project / name).write_text("Keep this", encoding="utf-8")
        installer.install(target=self.project, apply=True)
        result = installer.install(target=self.project, apply=True)
        self.assertTrue(all(a["action"] == "unchanged" for a in result["actions"]))
        self.assertEqual((self.project / "CLAUDE.md").read_text(), "Keep this")
        self.assertEqual((self.project / "AGENTS.md").read_text(), "Keep this")

    def test_unowned_or_modified_refused(self):
        path = self.project / ".agents/skills/gyst"; path.mkdir(parents=True)
        with self.assertRaises(ValueError): installer.install(agent="codex", target=self.project, apply=True)
        path.rmdir()
        installer.install(agent="codex", target=self.project, apply=True)
        (path / "SKILL.md").write_text("local edit", encoding="utf-8")
        with self.assertRaises(ValueError): installer.install(agent="codex", target=self.project, apply=True, update=True)

    def test_update_backup(self):
        installer.install(agent="codex", target=self.project, apply=True)
        source = self.root / "new-skill"; shutil.copytree(installer.SOURCE, source)
        with (source / "SKILL.md").open("a", encoding="utf-8") as handle: handle.write("\nUpdated test fixture\n")
        with patch.object(installer, "SOURCE", source):
            result = installer.install(agent="codex", target=self.project, apply=True, update=True)
        self.assertTrue(Path(result["actions"][0]["backup"]).is_dir())

    def test_user_scope_and_relocated_payload(self):
        with patch.object(Path, "home", return_value=self.project):
            installer.install(agent="codex", scope="user", apply=True)
        script = self.project / ".agents/skills/gyst/scripts/gyst.py"
        output = subprocess.run([sys.executable, str(script), "--version"], capture_output=True, text=True, check=True)
        self.assertEqual(output.stdout.strip(), "0.1.0")
        work = self.root / "portable-work"; g.init(work); g.inventory(work)
        output = subprocess.run([sys.executable, str(script), "validate", str(work)], capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(output.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
