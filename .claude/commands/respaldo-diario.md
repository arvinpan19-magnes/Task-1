---
description: Respaldo diario del Banco Central (dólar, UF, cobre) -> historial.xlsx -> correo a c.becar@udd.cl
---

Ejecuta el respaldo diario. Lo exacto lo hace el código; tú solo redactas el correo y coordinas. Sé breve.
Procedimiento completo y justificación en `p2a/07_automatizacion.md` y `p2a/02_metodo.md`.

## 0. Arranque
- `git fetch --all`; si hay ramas `claude/...` con commits nuevos, intégralas (regla del ramo en CLAUDE.md).
- Confirma la hora de Chile: `TZ=America/Santiago date -Iseconds`.

## 1. Preparar (todo en código)
```bash
python3 scripts/respaldo.py preparar
```
Lee el home y la página de indicadores diarios del Banco Central (con navegador), valida rangos
(dólar 500–2000, UF 30000–60000, cobre 1–10), cruza home vs indicadores diarios, escribe la fila del día en
`historial.xlsx` SIN duplicar, prepara y verifica el adjunto (`cmp` + apertura con openpyxl) y escribe `salidas/estado.json`.

- **Código de salida 2 / `estado: DETENIDO`**: DETENTE. Informa al alumno el `motivo` en el chat. No envíes nada, no hagas commit, no
  inventes ni "corrijas" valores. (`aviso_falla` trae asunto, cuerpo y destinatario del correo `[ALERTA]`: único destinatario `c.becar@udd.cl`. Envíalo solo si Gmail está disponible con envío y la puerta C está aprobada; si no, solo avisa en el chat.)
- **Código 0 / `estado: LISTO`**: continúa.

## 2. Decidir si corresponde enviar (lee `salidas/estado.json`)
- `accion_correo = ya_enviado` → no envíes de nuevo. Dilo en una línea y termina (pasa al paso 5 solo si `commit_y_push` es true).
- `accion_correo = enviar` → sigue.

## 3. Enviar con Gmail (🚪 puerta C: solo si el alumno la aprobó; ver `memoria/decisiones.md`)
1. Verifica que el conector de Gmail está disponible **y** que tiene una herramienta para ENVIAR con adjunto (no solo `create_draft`).
   Si no, **detente y avisa al alumno**. No uses otra vía (SMTP, Drive, etc.) sin preguntarle.
2. Los parámetros salen de `salidas/estado.json` → `correo`: `para` = exactamente `["c.becar@udd.cl"]`, sin cc/bcc;
   `asunto` = el del JSON (formato «Respaldo diario Banco Central AAAA-MM-DD»). No los modifiques.
3. Cuerpo (lo redactas tú, en texto plano y breve): fecha, dólar observado, UF, libra de cobre (USD/lb), y la fuente (las dos URLs de
   `fuente_urls`). Si `nota` no está vacía, dilo («sin cambio: último valor publicado el …»). Usa SOLO los números del JSON.
4. Adjunto: `historial.xlsx`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`. El contenido base64 es EXACTAMENTE el
   archivo `salidas/adjunto/historial.xlsx.b64` generado por código. No lo escribas de memoria ni lo recortes. Si la herramienta
   permite referenciar un archivo, úsalo; si exige el texto en la llamada, léelo con Read y pásalo completo.
5. Antes de enviar, confirma que `estado.json → adjunto.verificado` es `true` y que `b64_caracteres` coincide con la longitud del archivo `.b64`.

## 4. Confirmar y registrar
- Tras enviar, busca el mensaje enviado (get_message / search en Enviados) y comprueba: destinatario único, asunto, y que **tiene el
  adjunto `historial.xlsx` con el tamaño `adjunto.bytes` del JSON**. Si falta o difiere, avisa al alumno; no reenvíes por tu cuenta.
- Si todo calza: `python3 scripts/respaldo.py marcar-enviado --fecha AAAA-MM-DD --mensaje-id <id>`.

## 5. Commit y push solo si hubo fila nueva (`commit_y_push: true`)
```bash
git add historial.xlsx memoria
git commit -m "Respaldo diario Banco Central AAAA-MM-DD"
git push -u origin HEAD
```
Si `fila_nueva` es false, no hagas commit de datos.

## 6. Cierre
Resume en 3 líneas: fecha, valores, si hubo «sin cambio», si el correo salió y se verificó, si hubo commit.
