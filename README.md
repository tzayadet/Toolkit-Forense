<p align="center">
  <img src="https://img.shields.io/badge/DIGITAL_FORENSICS-FILE_INTEGRITY-101010?style=for-the-badge&labelColor=050805&color=00FF41" alt="Forensic File Integrity"/>
  <img src="https://img.shields.io/badge/PYTHON-CLI-101010?style=for-the-badge&logo=python&logoColor=00FF41" alt="Python CLI"/>
</p>

# Forensic File Integrity

Inventario técnico de archivos para copias de trabajo forense. Recorre un directorio, calcula hashes SHA-256 y registra tamaño y fecha de modificación en UTC. Sin dependencias externas y con salida JSON.

<p align="center">
  <a href="https://tzayadet.github.io/Toolkit-Forense/"><strong>LIVE SHOWCASE ↗</strong></a> ·
  <a href="https://github.com/tzayadet/Toolkit-Forense"><strong>SOURCE CODE</strong></a>
</p>

[![Python tests](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml) · [![Container build](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml)

> El showcase utiliza datos ficticios. El inventario real se ejecuta localmente; la página no procesa evidencias.

## What it does

- Recorre directorios y registra archivos.
- Calcula SHA-256 por archivo.
- Recoge tamaño y fecha de modificación en UTC.
- Permite filtrar por extensión.
- Registra errores de lectura por archivo.
- Excluye enlaces simbólicos para no seguir rutas fuera de la copia seleccionada.

## Quick start

**Requirements:** Python 3.10+. No external dependencies.

```bash
python forensic_inventory.py /path/to/evidence-copy
python forensic_inventory.py /path/to/evidence-copy --ext pdf
```

**Docker**

```bash
docker build -t forensic-file-integrity .
docker run --rm -v "/path/to/evidence-copy:/evidence:ro" forensic-file-integrity /evidence
```

La salida JSON se escribe en stdout. El contenedor ejecuta la utilidad sin privilegios y permite montar la copia en modo solo lectura.

## Project layout

| Path | Purpose |
|---|---|
| `forensic_inventory.py` | Inventario y cálculo de hashes |
| `docs/` | Showcase estático con datos de ejemplo |
| `tests/` | Pruebas automatizadas |
| `.github/workflows/` | CI, build de contenedor y Pages |

## Forensic considerations

Trabaja sobre copias verificadas, no sobre la evidencia original. Documenta adquisición, custodios, fechas, herramientas y versiones. Un hash permite comparar integridad frente a una referencia, pero no acredita por sí solo autenticidad ni cadena de custodia. Los metadatos de modificación dependen del sistema de archivos y no deben tratarse como fechas probatorias.

Esta utilidad no realiza adquisición forense, bloqueo de escritura ni preservación de cadena de custodia.

## Deployment

GitHub Pages publica el contenido de `docs/` mediante `.github/workflows/pages.yml`. Requiere configurar Pages con GitHub Actions y establecer la variable `ENABLE_PAGES=true`.

## License

See [LICENSE](LICENSE).
