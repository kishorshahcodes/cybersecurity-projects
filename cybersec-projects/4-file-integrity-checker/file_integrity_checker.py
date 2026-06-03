"""
File Integrity Checker
Author: [Your Name]
Description: Monitors files and directories for unauthorized changes using SHA-256 hashing.
             Detects modifications, deletions, and new files.
"""

import hashlib
import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


BASELINE_FILE = "integrity_baseline.json"
HASH_ALGORITHM = "sha256"


def compute_hash(filepath, algorithm="sha256"):
    """Compute the hash of a file."""
    h = hashlib.new(algorithm)
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except PermissionError:
        return "PERMISSION_DENIED"
    except Exception as e:
        return f"ERROR: {e}"


def get_file_metadata(filepath):
    """Get file metadata for additional context."""
    try:
        stat = os.stat(filepath)
        return {
            "size_bytes": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except Exception:
        return {}


def scan_target(target):
    """Scan a file or directory and return hash records."""
    records = {}
    target = Path(target)

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = [f for f in target.rglob("*") if f.is_file()]
    else:
        print(f"❌ Target not found: {target}")
        return records

    print(f"📂 Scanning {len(files)} file(s)...")

    for filepath in files:
        rel_path = str(filepath)
        file_hash = compute_hash(filepath)
        metadata = get_file_metadata(filepath)
        records[rel_path] = {
            "hash": file_hash,
            **metadata,
            "scanned_at": datetime.now().isoformat()
        }

    return records


def create_baseline(target, output=BASELINE_FILE):
    """Create a baseline snapshot of file hashes."""
    print(f"\n🔍 Creating baseline for: {target}")
    records = scan_target(target)

    baseline = {
        "created_at": datetime.now().isoformat(),
        "target": str(target),
        "algorithm": HASH_ALGORITHM,
        "files": records
    }

    with open(output, "w") as f:
        json.dump(baseline, f, indent=2)

    print(f"✅ Baseline created: {output}")
    print(f"   Files recorded: {len(records)}")
    print(f"   Timestamp     : {baseline['created_at']}")


def verify_integrity(target, baseline_file=BASELINE_FILE):
    """Compare current state against the baseline."""
    if not os.path.exists(baseline_file):
        print(f"❌ Baseline file not found: {baseline_file}")
        print("   Run with --create first to create a baseline.")
        return

    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    print(f"\n🔍 Verifying integrity for: {target}")
    print(f"   Baseline from : {baseline['created_at']}")
    print(f"   Algorithm     : {baseline['algorithm']}")
    print("-" * 55)

    current = scan_target(target)
    baseline_files = baseline["files"]

    modified = []
    deleted = []
    added = []

    # Check for modified or deleted files
    for filepath, info in baseline_files.items():
        if filepath not in current:
            deleted.append(filepath)
        elif current[filepath]["hash"] != info["hash"]:
            modified.append({
                "file": filepath,
                "old_hash": info["hash"][:16] + "...",
                "new_hash": current[filepath]["hash"][:16] + "...",
                "old_modified": info.get("modified_time", "unknown"),
                "new_modified": current[filepath].get("modified_time", "unknown"),
            })

    # Check for new files
    for filepath in current:
        if filepath not in baseline_files:
            added.append(filepath)

    # Report
    print(f"\n📊 Integrity Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    if not modified and not deleted and not added:
        print("✅ All files are INTACT. No changes detected.\n")
        return

    if modified:
        print(f"\n⚠️  MODIFIED FILES ({len(modified)}):")
        for f in modified:
            print(f"   📝 {f['file']}")
            print(f"      Hash : {f['old_hash']} → {f['new_hash']}")
            print(f"      Time : {f['old_modified']} → {f['new_modified']}")

    if deleted:
        print(f"\n🗑️  DELETED FILES ({len(deleted)}):")
        for f in deleted:
            print(f"   ❌ {f}")

    if added:
        print(f"\n🆕 NEW FILES ({len(added)}):")
        for f in added:
            print(f"   ➕ {f}")

    total_changes = len(modified) + len(deleted) + len(added)
    print(f"\n🚨 Total changes detected: {total_changes}")
    print("=" * 55 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🛡️ File Integrity Checker — Detect unauthorized file changes"
    )
    parser.add_argument("target", help="File or directory to monitor")
    parser.add_argument("--create", action="store_true", help="Create a new baseline")
    parser.add_argument("--verify", action="store_true", help="Verify against existing baseline")
    parser.add_argument("--baseline", default=BASELINE_FILE, help=f"Baseline file path (default: {BASELINE_FILE})")
    parser.add_argument("--hash-file", help="Compute and display hash of a single file")

    args = parser.parse_args()

    if args.hash_file:
        h = compute_hash(args.hash_file)
        print(f"\n🔐 SHA-256 Hash of '{args.hash_file}':\n   {h}\n")
        return

    if args.create:
        create_baseline(args.target, args.baseline)
    elif args.verify:
        verify_integrity(args.target, args.baseline)
    else:
        print("Please use --create to create a baseline or --verify to check integrity.")
        print("Use --help for more options.")


if __name__ == "__main__":
    main()
