<p align="center">
  <img src="https://img.shields.io/badge/DFIR-FORENSIC_FILE_INVENTORY-101010?style=for-the-badge&labelColor=050805&color=00FF41" alt="Forensic File Inventory"/>
  <img src="https://img.shields.io/badge/PYTHON-SHA--256-101010?style=for-the-badge&labelColor=050805&logo=python&logoColor=00FF41" alt="Python SHA-256"/>
</p>

# Forensic File Inventory

A Python utility for creating structured inventories of files in forensic working copies. It records relative paths, file sizes and modification timestamps, calculates SHA-256 hashes, and exports JSON.

<p align="center">
  <a href="https://github.com/tzayadet/Toolkit-Forense/blob/main/docs/index.html"><strong>SHOWCASE SOURCE ↗</strong></a> ·
  <a href="https://github.com/tzayadet/Toolkit-Forense"><strong>SOURCE CODE</strong></a>
</p>

[![Python tests](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml) · [![Container build](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml) · [![Pages](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/pages.yml)

## Overview

- Recursively inventories files in a selected directory.
- Calculates a SHA-256 digest for each readable file.
- Records file size and modification time in UTC.
- Supports extension-based filtering.
- Reports per-file read and hashing errors.
- Skips symbolic links and uses relative paths in reports.
- Detects file metadata changes during hashing and discards unstable digests.

## Run locally

**Requirements:** Python 3.10+. No third-party Python packages are required.

```bash
python forensic_inventory.py /path/to/evidence-copy
python forensic_inventory.py /path/to/evidence-copy --ext pdf
```

The JSON inventory is written to standard output.

## Docker

```bash
docker build -t forensic-file-inventory .
docker run --rm -v "/path/to/evidence-copy:/evidence:ro" forensic-file-inventory /evidence
```

Use a verified working copy and mount it read-only.

## Project structure

| Path | Purpose |
|---|---|
| `forensic_inventory.py` | File inventory and SHA-256 calculation |
| `docs/` | Static showcase with synthetic records |
| `tests/` | Automated regression tests |
| `.github/workflows/` | Test, container and Pages automation |

## Showcase

The [showcase source](docs/index.html) contains illustrative records only. It does not access local files or process evidence. GitHub Pages deployment is configured, but Pages must be enabled in repository settings with GitHub Actions as the source before a public URL can be confirmed.

## Validation

Run the tests with:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the unit tests and container build.

## Forensic considerations

Work on verified copies, not original evidence. Record acquisition details, custodians, timestamps, tool versions and handling procedures separately. A hash can help establish that a file has not changed relative to a trusted reference; by itself, it does not prove authenticity or establish chain of custody.

This utility does not acquire evidence, enforce write blocking or provide a chain-of-custody system. Filesystem timestamps may reflect copying or filesystem behaviour rather than the time an event occurred. Relative paths avoid exposing local machine usernames in reports, but the inventory should still be handled as potentially sensitive case data.

## License

See [LICENSE](LICENSE).
