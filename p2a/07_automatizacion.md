# 07 · Automatización

**Estado:** borrador. Frecuencia decidida: lunes 09:00 (Chile). Hoy el disparador es **manual**: el comando `/respaldo-diario` en este chat (`.claude/commands/respaldo-diario.md`). La rutina automática queda como paso posterior (🚪D).

## Cómo se ejecuta hoy (manual)
1. Escribir `/respaldo-diario`.
2. `python3 scripts/respaldo.py preparar` → lee, valida, registra, verifica el adjunto, escribe `salidas/estado.json`.
   - Si `DETENIDO` → se informa el motivo y termina (sin escribir ni enviar).
3. Si `accion_correo = enviar` → (🚪C) el modelo redacta el cuerpo con `redactar-correo` y se envía con Gmail a `c.becar@udd.cl` (único), asunto «Respaldo diario Banco Central AAAA-MM-DD», con `historial.xlsx` adjunto.
4. Se confirma que el mensaje enviado tiene el adjunto; se registra con `respaldo.py marcar-enviado`.
5. Si `commit_y_push` → `git add historial.xlsx memoria` + commit + push. Si no hubo fila nueva, no hay commit.

## Diseño de la rutina automática (pendiente, 🚪D)
- **Gatillo (decidido 2026-11-13): los lunes a las 09:00 America/Santiago** (cron `CRON_TZ=America/Santiago 0 9 * * 1`; configurar con zona horaria, no con hora UTC fija, porque Chile cambia de horario). Un lunes a las 09:00 la fuente puede seguir mostrando el viernes: en ese caso la fila queda «sin cambio (último valor publicado: …)» y el correo se envía igual.
- **Entorno:** rutina en claude.ai con este repo y el conector de Gmail (con herramienta de envío y adjuntos), más acceso de red a `www.bcentral.cl` y `si3.bcentral.cl`.
- **Duplicados:** idempotente por fecha (`historial.xlsx`) y por `memoria/envios.json`.
- **Reintentos:** hasta 3 en la lectura (ya implementado); en el envío, ninguno automático (se avisa).
- **Supervisión y detención:** cualquier excepción de 02 detiene la ejecución y avisa; se desactiva la rutina desde claude.ai.
- **Pruebas de activación con evidencia:** `[PENDIENTE]` (no hay rutina activa).

## Ficha del agente operacional
Ver `README.md`.
## Supuestos y pendientes
`[PENDIENTE]` Gmail con envío (el alumno reconectará el conector); aprobación de 🚪C y 🚪D. Aprobadas: 🚪A y 🚪B. Aviso de falla: a `c.becar@udd.cl`.
## Retornos / Traspaso
Ninguno.
