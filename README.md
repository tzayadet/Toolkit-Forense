# Forensic File Integrity

Utilidad de inventario de archivos para análisis técnico: recorre un directorio, calcula SHA-256 y registra tamaño y fecha de modificación en UTC.

[![Python tests](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/tests.yml) · [![Container build](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Toolkit-Forense/actions/workflows/container-build.yml)

## Requisitos

- Python 3.10 o superior.
- Sin dependencias externas.

## Uso local

```bash
python forensic_inventory.py /ruta/a/la/copia-forense
python forensic_inventory.py /ruta/a/la/copia-forense --ext pdf
```

La salida se genera en JSON e incluye la ruta, el tamaño, la fecha de modificación UTC y el hash SHA-256. Los errores de lectura se registran por archivo. Se excluyen enlaces simbólicos para evitar seguir rutas que salgan de la copia seleccionada.

## Docker

Construye la imagen:

```bash
docker build -t forensic-toolkit .
```

Monta la copia de trabajo en modo solo lectura:

```bash
docker run --rm \
  -v "/ruta/a/la/copia-forense:/evidence:ro" \
  forensic-toolkit /evidence
```

La imagen ejecuta la utilidad como usuario sin privilegios. La salida JSON se escribe en stdout.

## Publicar el showcase

La demo estática está en [docs/index.html](docs/index.html) y utiliza únicamente datos ficticios. Para publicarla:

1. En **Settings → Pages**, selecciona **GitHub Actions** como origen.
2. En **Settings → Secrets and variables → Actions → Variables**, crea `ENABLE_PAGES` con valor `true`.
3. Ejecuta **Deploy Toolkit-Forense showcase to GitHub Pages** desde Actions.

La página no procesa evidencias. El CLI inventaría archivos y calcula SHA-256; no realiza adquisición forense ni establece cadena de custodia.

## Consideraciones forenses

- Trabaja sobre copias verificadas, no sobre la evidencia original.
- Monta los soportes en modo solo lectura cuando sea posible.
- Documenta adquisición, custodios, fechas, herramientas y versiones.
- Este script no realiza adquisición forense, bloqueo de escritura ni preservación de cadena de custodia.
- Los metadatos de modificación dependen del sistema de archivos y no se incluyen como fecha probatoria.
- Un hash permite comprobar integridad respecto a una referencia, pero no acredita por sí solo la autenticidad ni la cadena de custodia.

## Licencia

Consulta [LICENSE](LICENSE).
