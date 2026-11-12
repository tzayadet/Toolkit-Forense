# Forensic File Inventory

A Python utility for creating structured inventories of files in forensic working copies. It records file paths, sizes and modification timestamps, calculates SHA-256 hashes, and exports results as JSON.

<p align="center">
  <a href="https://github.com/tzayadet/Toolkit-Forense"><img src="https://img.shields.io/badge/SOURCE-GITHUB-161b22?style=flat-square&logo=github" alt="Source code"></a>
  <a href="docs/index.html"><img src="https://img.shields.io/badge/SHOWCASE-SOURCE-00a86b?style=flat-square" alt="Showcase source"></a>
</p>

[![Python tests](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml) · [![Container build](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml)

## What it does

- Recursively inventories files in a selected directory.
- Calculates a SHA-256 hash for each readable file.
- Records file size and modification time in UTC.
- Supports extension-based filtering.
- Captures per-file read errors without silently dropping them.
- Skips symbolic links to avoid following paths outside the selected working copy.

## Run locally

**Requirements:** Python 3.10 or later. No third-party Python packages are required.

```bash
python forensic_inventory.py /path/to/evidence-copy
python forensic_inventory.py /path/to/evidence-copy --ext pdf
```

## Docker

```bash
docker build -t forensic-file-inventory .
docker run --rm -v "/path/to/evidence-copy:/evidence:ro" forensic-file-inventory /evidence
```

The container runs the inventory against a read-only mount. JSON results are written to standard output.

## Project structure

| Path | Purpose |
|---|---|
| `forensic_inventory.py` | File inventory and SHA-256 calculation |
| `docs/` | Static showcase with synthetic data |
| `tests/` | Automated tests |
| `.github/workflows/` | CI, container build and Pages workflow |

## Showcase

The showcase source is available in [docs/index.html](docs/index.html). Its records are illustrative; the page does not access local files or process evidence. The deployment workflow is ready; GitHub Pages must first be enabled in repository settings with GitHub Actions as the source.

## Forensic considerations

Work on verified copies, not original evidence. Record acquisition details, custodians, timestamps, tool versions and handling procedures separately. A hash can help establish that a file has not changed relative to a trusted reference; by itself, it does not prove authenticity or establish chain of custody. The tool checks for changes during hashing, but it is not a substitute for write-blocking or a forensic acquisition process.

This utility does not acquire evidence, enforce write blocking or provide a chain-of-custody system. Filesystem timestamps may also reflect copying or filesystem behaviour rather than the time an event occurred.

## Tests

```bash
python -m pytest
```

## License

See [LICENSE](LICENSE) for the repository's licensing terms.
