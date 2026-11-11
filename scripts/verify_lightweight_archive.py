"""Inventory or verify the curated 2026-11-11 archive without simulator dependencies."""

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "archives/2026-11-11/manifest.json"
DIAGNOSTIC = ".cache/diagnose_warp_force.py"
TEXT_SUFFIXES = {".json", ".md", ".py", ".log", ".txt", ".in", ".lock"}
SKIP_PARTS = {".cache", "__pycache__", ".venv"}
COMPARISON_DIRS = {"full-comparison", "task02-comparison", "task02-comparison-preview"}


def selected(path):
    parts = path.relative_to(ROOT).parts
    if SKIP_PARTS.intersection(parts):
        return False
    if path.suffix in TEXT_SUFFIXES:
        return True
    if path.suffix == ".csv" and path.name != "raw.csv":
        return True
    if "source" in parts and "configs" in parts:
        return True
    return path.suffix == ".png" and (
        "comparison" in parts
        or path.parent.name in COMPARISON_DIRS
        or path.parent == ROOT / "results/full-recovery-20261009"
    )


def checked_path(relative):
    parts = PurePosixPath(relative)
    if parts.is_absolute() or ".." in parts.parts or "\\" in relative:
        raise ValueError(f"Unsafe archive path: {relative}")
    path = ROOT / parts
    if path.is_symlink() or path.resolve() != path.absolute():
        raise ValueError(f"Archive entries must be ordinary files: {relative}")
    return path


def build():
    entries, omitted, kinds = [], Counter(), Counter()
    for path in sorted((ROOT / "results").rglob("*")):
        if path.is_symlink():
            omitted["symlinks"] += 1
            continue
        if not path.is_file():
            continue
        if selected(path):
            entries.append(path)
        else:
            omitted["regular_files"] += 1
            omitted["regular_bytes"] += path.stat().st_size
            kinds[path.suffix or "[no extension]"] += 1
    entries.append(ROOT / DIAGNOSTIC)
    files = []
    for path in sorted(entries):
        relative = path.relative_to(ROOT).as_posix()
        content = checked_path(relative).read_bytes()
        files.append({
            "path": relative,
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        })
    payload_bytes = sum(item["bytes"] for item in files)
    if payload_bytes > 36 * 1024 * 1024:
        raise ValueError("Archive payload exceeds the reviewed approximate 34 MiB scope")
    manifest = {
        "schema_version": 1,
        "archive_date": "2026-11-11",
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "archive_kind": "summaries_and_historical_scripts_not_full_experiment_backup",
        "selection": {
            "text_suffixes": sorted(TEXT_SUFFIXES),
            "csv": "All metric/summary CSVs; raw.csv excluded",
            "source_configs": "All files under frozen source/configs directories",
            "png": "Comparison directories and full-recovery-20261009 root curves",
            "diagnostic": DIAGNOSTIC,
            "excluded": "All symlinks, source caches, bytecode, raw.csv, NPZ and other images",
        },
        "file_count": len(files),
        "payload_bytes": payload_bytes,
        "omitted_results": dict(omitted),
        "omitted_regular_files_by_extension": dict(sorted(kinds.items())),
        "files": files,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Inventoried {len(files)} files, {payload_bytes / 1048576:.2f} MiB")


def read_manifest():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = manifest["files"]
    paths = [item["path"] for item in files]
    if manifest["schema_version"] != 1 or len(paths) != len(set(paths)):
        raise ValueError("Invalid manifest schema or duplicate archive paths")
    if manifest["file_count"] != len(files):
        raise ValueError("Manifest file count mismatch")
    if manifest["payload_bytes"] != sum(item["bytes"] for item in files):
        raise ValueError("Manifest byte count mismatch")
    for path in paths:
        checked_path(path)
    return manifest


def verify(manifest):
    failures = []
    for item in manifest["files"]:
        path = checked_path(item["path"])
        if not path.is_file():
            failures.append(f"Missing: {item['path']}")
            continue
        content = path.read_bytes()
        if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
            failures.append(f"Modified: {item['path']}")
    if failures:
        raise ValueError("\n".join(failures))
    print(
        f"Verified {manifest['file_count']} files, "
        f"{manifest['payload_bytes'] / 1048576:.2f} MiB; all SHA-256 hashes match"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--build", action="store_true", help="Re-inventory the original local results")
    group.add_argument("--paths0", action="store_true", help="Print inventoried paths for Git staging")
    args = parser.parse_args()
    if args.build:
        build()
    manifest = read_manifest()
    if args.paths0:
        sys.stdout.buffer.write(
            b"".join(item["path"].encode("utf-8") + b"\0" for item in manifest["files"])
        )
    else:
        verify(manifest)


if __name__ == "__main__":
    main()
