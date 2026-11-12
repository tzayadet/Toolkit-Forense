#!/usr/bin/env python3
"""Generate a basic SHA-256 inventory for files in a directory.

For evidential work, operate on verified forensic copies and preserve chain of
custody. This utility is an inventory helper, not a forensic acquisition tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_dir(root: Path, extension: str | None = None) -> list[dict]:
    records = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if extension and path.suffix.lower() != extension.lower().lstrip(".") and path.suffix.lower() != "." + extension.lower().lstrip("."):
            continue
        try:
            stat = path.stat()
            records.append({
                "path": str(path),
                "size": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "sha256": hash_file(path),
            })
        except OSError as exc:
            records.append({"path": str(path), "error": f"{type(exc).__name__}: {exc}"})
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("-e", "--ext", help="Optional extension filter, e.g. pdf")
    args = parser.parse_args()
    if not args.path.is_dir():
        parser.error(f"not a directory: {args.path}")
    print(json.dumps(scan_dir(args.path, args.ext), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
