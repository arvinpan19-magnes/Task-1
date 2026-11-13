# 05 · Capacidades (Habilidad)

**Estado:** prototipo — los scripts están probados con fixtures y en vivo para la lectura; Gmail **no** está comprobado. (02 ya está `acordado`, pero 05 sigue en `prototipo` porque la capacidad crítica Gmail no está comprobada.)

| Capacidad | Cómo se resuelve | Acceso técnico | Permiso entorno | Autorizada | Prueba | Resultado | Alternativa |
|---|---|---|---|---|---|---|---|
| Leer home e indicadores del BCCh | Chromium headless (Playwright Node) | `scripts/leer_bcch.js` | hosts `www.bcentral.cl`, `si3.bcentral.cl` permitidos en el entorno (aprobado por el alumno 2026-11-13) | sí | lectura en vivo 2026-11-13 | ✅ valores correctos, cruce OK | si falla: detener y avisar |
| Leer el sitio de la metodología | HTTP simple | curl | host `prompt2agent-metodologia.netlify.app` permitido | sí | descarga del master prompt | ✅ | — |
| Validar y registrar | Python 3.13 + openpyxl 3.1.5 | `scripts/bcch.py`, `respaldo.py` | local | sí | 16 casos (`evals/reporte.md`) | ✅ | — |
| xlsx liviano | escritor propio (zip + XML, sin estilos) | `scripts/exportar_xlsx.py` | local | sí | C7: 1.755 B, sin styles/docProps/sharedStrings; abre con openpyxl | ✅ (openpyxl) · Excel/LibreOffice **no probado** | openpyxl estándar |
| Adjunto verificado | base64 por código + `cmp` + openpyxl | `respaldo.py` | local | sí | C1, C7 y ejecución real | ✅ | — |
| **Enviar correo con Gmail** | conector Gmail (MCP) | — | conector `Gmail`: **falló al conectar (502)** al iniciar la sesión. Conector `plugin:small-business:gmail`: solo expone `create_draft` (acepta adjuntos base64), **sin herramienta de envío** | **no** (🚪C pendiente) | **no probado** | ❌ no disponible para enviar | ninguna sin preguntar al alumno (regla) |
| Confirmar adjunto tras enviar | `get_message`/`get_thread` del conector | — | — | — | no probado | — | — |
| Git commit/push a `Task-1` | git + credenciales de la sesión | `git` | repo adjuntado con push | sí | ver `memoria/estado.md` | — | — |
| Rutina automática 09:00 en claude.ai | rutina con repo + Gmail | claude.ai | — | **no** (🚪D) | no probada | — | disparador manual |

## Controles implementados (en código/configuración, no solo en texto)
Rangos y destinatario único en `agent/controles/config.json` · verificación de etiquetas de la página · cruce home vs diarios · escritura atómica del Excel · idempotencia por fecha · estado de envíos en `memoria/envios.json`.

## Supuestos y pendientes
`[PENDIENTE]` Gmail: necesito (a) conector disponible, (b) herramienta de envío con adjunto. `[PENDIENTE]` abrir el xlsx en Excel/LibreOffice.
## Retornos / Traspaso
Retorno: el conector actual no envía → ver decisión D12. Traspaso: `agent/herramientas` = `scripts/`.
