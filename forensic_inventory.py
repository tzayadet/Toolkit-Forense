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
    if path.is_symlink():
        raise ValueError("Refusing to hash a symbolic link")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_dir(root: Path, extension: str | None = None) -> list[dict]:
    if root.is_symlink():
        raise ValueError("The evidence root must not be a symbolic link")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")

    records = []
    for path in sorted(root.rglob("*")):
        # Do not inventory linked files or directories that may lead outside
        # the selected evidence copy.
        if path.is_symlink() or not path.is_file():
            continue
        try:
            path.resolve(strict=True).relative_to(root)
        except (OSError, ValueError):
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
    if args.path.is_symlink() or not args.path.is_dir():
        parser.error(f"not a valid evidence directory (symbolic links are not accepted): {args.path}")
    print(json.dumps(scan_dir(args.path, args.ext), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
