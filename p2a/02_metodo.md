# 02 · Método

**Estado:** acordado — 🚪 **Puerta B** aprobada el 2026-11-13. Tecnología: **flujo programado** (pasos fijos en código; el modelo solo redacta), porque el orden de los pasos es conocido (master prompt §10).

## Ruta normal
| # | Paso | Ejecutor | Entrada → Salida | Verificación |
|---|---|---|---|---|
| 1 | Leer home y UF/dólar; leer indicadores diarios (cobre, fecha) | herramienta (`leer_bcch.js`) | URLs → JSON crudo | `ok: true` |
| 2 | Interpretar números/fechas; validar rango; comprobar etiquetas; cruzar home vs diarios | regla (`bcch.py`) | JSON → valores | falla = ErrorDatos |
| 3 | Registrar fila del día sin duplicar; marcar «sin cambio» | regla (`respaldo.py`) | valores → `historial.xlsx` | caso C2, C5 |
| 4 | Generar xlsx liviano, copia, base64; verificar `cmp` y openpyxl | regla | xlsx → `salidas/adjunto/*` | `verificado: true` |
| 5 | Redactar cuerpo | **modelo** | `estado.json` → texto | solo cifras del JSON |
| 6 | Enviar con Gmail | herramienta | correo + adjunto | 🚪C; destinatario único |
| 7 | Confirmar adjunto en el mensaje enviado; registrar envío | herramienta + regla | mensaje → `memoria/envios.json` | tamaño == `adjunto.bytes` |
| 8 | Commit y push | herramienta (git) | solo si `fila_nueva` | `commit_y_push` |

## Reglas fijas
R1 rangos · R2 nunca inventar · R3 una fila por fecha · R4 destinatario único · R5 adjunto generado por código, nunca a mano · R6 fin de semana/feriado: se registra el último valor publicado con nota «sin cambio (último valor publicado: AAAA-MM-DD)» y se envía igual · R7 mismo día ya enviado: no reenviar.

## Excepciones
| Condición | Acción | A quién |
|---|---|---|
| Dato ausente/ilegible/fuera de rango/etiqueta cambiada/home≠diarios/fecha futura | **Detener** (no escribir, no enviar) | alumno, en el chat |
| Sitio caído tras 3 reintentos | Detener | alumno |
| Fila de hoy ya existe con otros valores | No modificar; avisar | alumno |
| Gmail no disponible o sin envío con adjunto | **Detener**; no usar otra vía | alumno |
| Cualquier detención por falla | Preparar correo `[ALERTA]` a `c.becar@udd.cl` (único destinatario); enviarlo solo si Gmail funciona | c.becar@udd.cl + alumno en el chat |
| Adjunto no verificado | Detener | alumno |
| El mensaje enviado no trae el adjunto | Avisar; no reenviar solo | alumno |

## Fallas silenciosas a vigilar
Que la página cambie el orden o etiqueta de indicadores (mitigado: se verifican etiquetas) · que la fuente muestre una fecha vieja (mitigado: nota «sin cambio»).

## Supuestos y pendientes
Confirmado por el alumno (2026-11-13): «sin cambio» = la fecha de referencia de la fuente es anterior a hoy. Un día hábil muy temprano (antes de la publicación del dólar) se vería igual: `[PENDIENTE]` confirmar la hora de publicación.
## Retornos / Traspaso
Retorno 1 (2026-11-13): se agregó la columna `nota` al Excel (necesaria para «sin cambio»). Traspaso: todo el método está en `scripts/` y `.claude/commands/respaldo-diario.md`.
