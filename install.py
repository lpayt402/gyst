#!/usr/bin/env python3
"""Install only the self-contained GYST skill. Dry-run unless --apply is supplied."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "skills/gyst"
RECEIPT = ".gyst-install.json"


def safe(path):
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError(f"Refusing link/junction: {part}")
    return path


def hashes(folder):
    result = {}
    for path in sorted(folder.rglob("*")):
        safe(path)
        if path.is_file() and path.name != RECEIPT and "__pycache__" not in path.parts and path.suffix != ".pyc":
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def install(agent="both", scope="project", target=None, apply=False, update=False):
    if scope == "project" and not target:
        raise ValueError("Project installation requires an explicit --target directory")
    if scope == "user" and target:
        raise ValueError("--target is for project scope; user scope uses your home directory")
    base = safe(Path(target).expanduser() if target else Path.home())
    if not base.is_dir():
        raise ValueError("Install target must already exist")
    expected = hashes(SOURCE)
    if "SKILL.md" not in expected or "scripts/gyst.py" not in expected:
        raise ValueError("Incomplete skill payload")
    selected = ("claude", "codex") if agent == "both" else (agent,)
    actions = []
    for name in selected:
        dest = safe(base / (".claude" if name == "claude" else ".agents") / "skills/gyst")
        action = "install"
        if dest.exists():
            if not dest.is_dir() or not (dest / RECEIPT).is_file():
                raise ValueError(f"Existing unowned installation: {dest}. Back up and reconcile it manually.")
            receipt = json.loads(safe(dest / RECEIPT).read_text(encoding="utf-8"))
            current = hashes(dest)
            if receipt.get("tool") != "gyst" or current != receipt.get("files"):
                raise ValueError(f"Locally modified installation: {dest}. Preserve changes before updating.")
            if current == expected:
                action = "unchanged"
            elif update:
                action = "update"
            else:
                raise ValueError(f"An older installation exists: {dest}. Review changes and use --update.")
        actions.append({"agent": name, "destination": str(dest), "action": action})
    # Preflight every target before making any change. Never touch host configs.
    commit = None
    try:
        output = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=False, timeout=5)
        if output.returncode == 0 and len(output.stdout.strip()) == 40:
            commit = output.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    if apply:
        for action in actions:
            if action["action"] == "unchanged":
                continue
            dest = Path(action["destination"])
            dest.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix=".gyst-stage-", dir=dest.parent) as staging:
                staged = Path(staging) / "gyst"
                shutil.copytree(SOURCE, staged, ignore=shutil.ignore_patterns(RECEIPT, "__pycache__", "*.pyc"))
                (staged / RECEIPT).write_text(json.dumps({"tool": "gyst", "version": "0.1.0", "source_commit": commit, "installed_at": datetime.now(timezone.utc).isoformat(), "files": expected}, indent=2) + "\n", encoding="utf-8")
                if hashes(staged) != expected:
                    raise ValueError("Staged installation differs from the reviewed payload")
                backup = None
                if action["action"] == "update":
                    backup_root = safe(base / ".gyst-install-backups" / action["agent"])
                    backup_root.mkdir(parents=True, exist_ok=True)
                    backup = backup_root / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                    dest.rename(backup)
                    action["backup"] = str(backup)
                try:
                    staged.rename(dest)
                except OSError:
                    if backup is not None:
                        backup.rename(dest)
                    raise
    return {"applied": apply, "source_commit": commit, "actions": actions, "next": "Open the host skill list; invoke GYST explicitly. No workspace or source data was touched."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    parser.add_argument("--target")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(install(**vars(args)), indent=2))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
