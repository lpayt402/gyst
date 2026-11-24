"""Exercise the local investigation through the public CLI."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/gyst/scripts/gyst.py"
ENTITY = "ent-benchboard"
QUESTION = "Was the shared BenchBoard account retired by September 30?"


class GoalTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        # macOS temporary paths can be rooted at the /var symlink.
        self.work = Path(folder.name).resolve()
        subprocess.run(
            [sys.executable, str(ROOT / "examples/demo.py"), "--workspace", str(self.work)],
            check=True, capture_output=True,
        )
        self.map = self.work / "map/knowledge.json"
        self.initial = hashlib.sha256(self.map.read_bytes()).hexdigest()

    def cli(self, command, *args, ok=True):
        result = subprocess.run(
            [sys.executable, str(CLI), command, str(self.work), *args],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0 if ok else 1, result.stderr)
        return json.loads(result.stdout if ok else result.stderr)

    def test_pause_resume_dispute_and_policy(self):
        self.cli("goal-start", "review", ENTITY, QUESTION, "--budget", "9")
        paused = self.cli("goal-run", "review", "--steps", "4")
        self.assertEqual(paused["status"], "paused")
        self.assertEqual(paused["board"]["spent"], 4)
        self.assertEqual(paused["board"]["next"]["action"], "link")
        self.assertEqual(self.cli("goal-show", "review"), paused)
        handoff = self.work / "inbox/handoff-2026.md"
        with handoff.open("a", encoding="utf-8") as stream:
            stream.write("\nSynthetic revision added between invocations.\n")
        completed = self.cli("goal-run", "review", "--steps", "9")
        self.assertEqual(completed["status"], "completed")
        self.assertEqual(completed["board"]["spent"], 9)
        self.assertEqual(completed, self.cli("goal-run", "review", "--steps", "9"))
        answer = completed["answer"]
        findings = {f["claim_id"]: f for f in answer["findings"]}
        self.assertEqual(len(findings), 3)
        self.assertEqual(findings["clm-mfa-required"]["interpretation"], "requirement")
        self.assertEqual(findings["clm-mfa-required"]["support"][0]["locator"], "L3-L3")
        self.assertEqual(findings["clm-exception-recollection"]["support"][0]["status"], "stale")
        self.assertEqual(findings["clm-exception-decision"]["support"][0]["status"], "citation_verified")
        self.assertIn("Implementation remains unverified", answer["summary"])
        self.assertTrue(any("retired or replaced" in q for q in answer["unresolved"]))
        self.assertEqual(hashlib.sha256(self.map.read_bytes()).hexdigest(), self.initial)

    def test_seeded_cli_workflow(self):
        self.assertEqual(self.cli("inventory")["status_counts"], {"ready": 8})
        validation = self.cli("validate")
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["warnings"], [])
        report = self.cli("report")
        self.assertIn("clm-mfa-required", Path(report["report"]).read_text(encoding="utf-8"))
        hits = self.cli("search", "EX-041", "--limit", "3")["hits"]
        self.assertTrue(hits)
        self.assertTrue(any(hit["path"] == "access-policy.md" for hit in hits))
        self.assertEqual(len(self.cli("trace", "clm-exception-decision")["claims"]), 2)
        started = self.cli("goal-start", "happy", ENTITY, QUESTION, "--budget", "9")
        self.assertEqual(started["board"]["spent"], 0)
        self.assertEqual(self.cli("goal-run", "happy", "--steps", "4")["status"], "paused")
        answer = self.cli("goal-run", "happy", "--steps", "9")
        self.assertEqual(answer["status"], "completed")
        self.assertEqual(answer, self.cli("goal-show", "happy"))
        self.assertEqual(answer["board"]["spent"], 9)
        self.assertEqual(len(answer["answer"]["findings"]), 3)
        self.assertTrue(all(
            citation["status"] == "citation_verified"
            for finding in answer["answer"]["findings"]
            for citation in finding["support"]
        ))
        self.assertEqual(hashlib.sha256(self.map.read_bytes()).hexdigest(), self.initial)

    def test_cli_rejects_aliased_workspace(self):
        with tempfile.TemporaryDirectory() as folder:
            alias = Path(folder).resolve() / "alias"
            try:
                alias.symlink_to(self.work, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Directory symlinks are unavailable on this host")
            result = subprocess.run(
                [sys.executable, str(CLI), "trace", str(alias), "clm-exception-decision"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Link/junction paths are not allowed", json.loads(result.stderr)["error"])

    def test_discovery_counts_toward_budget(self):
        self.cli("goal-start", "tiny", ENTITY, QUESTION, "--budget", "2")
        stopped = self.cli("goal-run", "tiny", "--steps", "200")
        self.assertEqual(stopped["status"], "budget_exhausted")
        self.assertEqual(stopped["board"]["spent"], 2)
        self.assertEqual(stopped["board"]["discovered"], 2)
        self.assertEqual(stopped["board"]["checks"], [])
        self.assertEqual(self.cli("goal-run", "tiny", "--steps", "200"), stopped)

    def test_trace_retains_both_sides_and_locators(self):
        trace = self.cli("trace", "clm-exception-decision")
        claims = {c["id"]: c for c in trace["claims"]}
        self.assertEqual(set(claims), {"clm-exception-decision", "clm-exception-recollection"})
        self.assertEqual(claims["clm-exception-recollection"]["reason"], "contradiction link")
        self.assertEqual(claims["clm-exception-recollection"]["support"][0]["path"], "handoff-2026.md")
        self.assertEqual(claims["clm-exception-decision"]["support"][0]["locator"], "L3-L3")

    def test_goal_revision_pin(self):
        self.cli("goal-start", "review", ENTITY, QUESTION, "--budget", "9")
        paused = self.cli("goal-run", "review", "--steps", "2")
        self.cli("inventory")
        blocked = self.cli("goal-run", "review", "--steps", "9", ok=False)
        self.assertIn("inventory changed", blocked["error"])
        self.assertEqual(self.cli("goal-show", "review"), paused)
