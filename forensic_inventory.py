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
        before = os.fstat(handle.fileno())
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(handle.fileno())

    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
    if identity_before != identity_after:
        raise OSError("File changed while hashing; digest discarded")
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
        if extension:
            expected_suffix = "." + extension.lower().lstrip(".")
            if path.suffix.lower() != expected_suffix:
                continue
        try:
            stat_before = path.stat()
            digest = hash_file(path)
            stat_after = path.stat()
            identity_before = (stat_before.st_dev, stat_before.st_ino, stat_before.st_size, stat_before.st_mtime_ns, stat_before.st_ctime_ns)
            identity_after = (stat_after.st_dev, stat_after.st_ino, stat_after.st_size, stat_after.st_mtime_ns, stat_after.st_ctime_ns)
            if identity_before != identity_after:
                raise OSError("File changed during inventory; record discarded")
            records.append({
                # Relative paths keep reports portable and avoid exposing local usernames.
                "path": path.relative_to(root).as_posix(),
                "size": stat_after.st_size,
                "modified_utc": datetime.fromtimestamp(stat_after.st_mtime, timezone.utc).isoformat(),
                "sha256": digest,
            })
        except OSError as exc:
            records.append({
                "path": path.relative_to(root).as_posix(),
                "error": f"{type(exc).__name__}: {exc}",
            })
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
