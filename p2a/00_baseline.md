# 00 · Baseline AS-IS — Respaldo diario del Banco Central

**Estado:** borrador · **Fecha:** 2026-11-13 · **Autor del contenido:** el alumno (encargo) + Claude (estructura)

## Proceso actual
1. Entrar al home del Banco Central de Chile (`https://www.bcentral.cl/inicio`) y leer **dólar observado** y **UF**.
2. Ir a la página de indicadores diarios (`https://si3.bcentral.cl/Indicadoressiete/secure/Indicadoresdiarios.aspx`) y leer la **libra de cobre (USD/lb)**.
3. Comprobar que los valores son razonables.
4. Anotar la fila del día en una planilla `historial.xlsx` (fecha, dólar, UF, cobre, fuente).
5. Enviar un correo con los 3 valores, la fuente y la planilla adjunta.

- **Quién recibe:** `c.becar@udd.cl` (solo esa persona). **Quién responde por el resultado:** el alumno.
- **Frecuencia:** el encargo original decía diaria 09:00; el 2026-11-13 el alumno fijó **los lunes a las 09:00** hora de Chile. **Inicio hoy:** manual, comando `/respaldo-diario`.
- **Fin:** correo enviado y verificado, fila registrada, commit+push si la fila es nueva.

## Hechos observados el 2026-11-13 (evidencia real)
- El home y la página de indicadores están detrás de una protección anti-bot: `curl` no sirve; se necesita un navegador (Chromium/Playwright).
- Home mostró UF `$41.322,93` y Dólar Observado `$992,48`; indicadores diarios mostró Libra de Cobre `6,30` y fecha de referencia `13 Nov 2026`. Evidencia: `evals/casos/lectura_real_2026-11-13.json`.
- Formato numérico chileno (`.` miles, `,` decimal).

## Conocimiento tácito convertido en regla
- «Nunca inventar valores» → ante dato faltante o fuera de rango, el proceso se detiene (02, 05).
- «Fines de semana y feriados: último valor publicado marcado "sin cambio" y se envía igual» → regla R6 de 02.
- «El adjunto debe ser xlsx real y liviano» y «no pegar el base64 a mano» → lecciones previas (el envío falló dos veces) → 05.

## Fricciones conocidas
- El base64 pegado a mano se cortó y Gmail rechazó el correo dos veces.
- Un adjunto con estilos/metadatos pesa más de lo necesario.

## Línea base
- Tiempo manual: `[PENDIENTE]` (el alumno no lo ha medido). Tasa de error actual: `[PENDIENTE]`.

## Supuestos y pendientes
- `[SUPUESTO]` Las páginas publican el valor del día antes de las 09:00 en días hábiles. No verificado (ver 06).
- `[PENDIENTE]` Calendario de feriados: no se mantiene una lista; se detecta por la fecha de referencia de la fuente.

## Retornos
Ninguno aún.

## Traspaso al harness
Las dos URLs, el formato numérico, la protección anti-bot y las dos lecciones sobre el adjunto.
