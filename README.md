# Forensic Toolkit

Utilidad de inventario básico para análisis de archivos: recorre un directorio, calcula SHA-256 y registra tamaño y fecha de modificación.

## Requisitos

Python 3.10+. No requiere dependencias externas.

## Uso

```bash
python forensic.py /ruta/a/la/copia-forense
python forensic.py /ruta/a/la/copia-forense --ext pdf
```

La salida se genera en JSON e incluye la ruta, el tamaño, la fecha de modificación UTC y el hash SHA-256. Los errores de lectura se registran por archivo.

## Consideraciones forenses

- Trabaja sobre copias verificadas, no sobre la evidencia original.
- Monta los soportes en modo solo lectura cuando sea posible.
- Documenta adquisición, custodios, fechas, herramientas y versiones.
- Este script no realiza adquisición forense, bloqueo de escritura ni preservación de cadena de custodia.
- Los metadatos de creación dependen del sistema de archivos y no se incluyen como fecha probatoria.

## Licencia

Consulta [LICENSE](LICENSE).
