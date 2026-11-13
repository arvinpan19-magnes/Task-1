# Respaldo diario Banco Central (Task-1)

Agente construido con la metodología **Prompt2Agent** (`p2a/`). Cada día lee dólar observado, UF y libra de cobre del Banco Central de Chile, los valida, los guarda en `historial.xlsx` (una fila por fecha) y envía un correo de respaldo con el Excel adjunto a `c.becar@udd.cl`.

## Ficha del agente operacional
| | |
|---|---|
| **Estado** | prototipo · lectura/validación/Excel probados · **envío por Gmail sin probar** (ver `p2a/PROGRESO.md`) |
| **Disparador** | manual: `/respaldo-diario` · rutina 09:00 America/Santiago: pendiente (🚪D) |
| **Entradas** | https://www.bcentral.cl/inicio · https://si3.bcentral.cl/Indicadoressiete/secure/Indicadoresdiarios.aspx |
| **Salidas** | `historial.xlsx` · correo (único destinatario `c.becar@udd.cl`) · commit/push solo con fila nueva |
| **Código** | `scripts/` (lectura, validación, registro, xlsx, adjunto) · el modelo solo redacta el correo |
| **Controles** | rangos y destinatario en `agent/controles/config.json` · se detiene ante dato faltante/fuera de rango/inconsistente |
| **Pruebas** | `python3 evals/ejecutar.py` → `evals/reporte.md` |
| **Requisitos** | Python 3 + openpyxl · Node + Playwright (Chromium) · acceso de red a `www.bcentral.cl` y `si3.bcentral.cl` |
| **Memoria** | `memoria/decisiones.md`, `memoria/estado.md`, `memoria/envios.json` |

Documentación: `p2a/00_baseline.md` … `p2a/07_automatizacion.md`.
