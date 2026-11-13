# Estado del trabajo (checkpoint)

- **Fecha:** 2026-11-13 · **Rama:** `claude/respaldo-diario`
- **Versión de fuentes:** home y indicadores diarios del BCCh leídos el 2026-11-13 (`evals/casos/lectura_real_2026-11-13.json`); master prompt Prompt2Agent descargado el 2026-11-13.
- **Hecho:** repo estructurado; scripts de lectura/validación/registro/adjunto; 17 pruebas en `evals/` (x3 repeticiones) y captura de la página real en `evals/evidencia/`; primera fila real (2026-11-13: dólar 992,48 · UF 41.322,93 · cobre 6,30).
- **Correo del 2026-11-13:** NO enviado (D12).
- **Aprobado por el alumno (2026-11-13):** 🚪A y 🚪B; supuestos D9–D11; aviso `[ALERTA]` solo a c.becar@udd.cl; canal Gmail (reconectará el conector).
- **Pendiente:** autenticar el conector Gmail (hoy falla por registro de cliente) y que tenga envío con adjunto (🚪C); prueba del envío real; rutina lunes 09:00 (🚪D).
- **Gmail 2026-11-13:** sin herramienta de envío; `create_draft` falló por autenticación. Correo NO enviado ni dejado como borrador.
- **Ejecución real repetida (2026-11-13):** 2ª y 3ª corridas en vivo: una devolvió DETENIDO (motivo no capturado, posible corte de red) y otra LISTO con `fila_nueva: false` (sin duplicar).
- **Cómo retomar:** leer `p2a/PROGRESO.md`, `memoria/decisiones.md`; correr `python3 evals/ejecutar.py`; luego `/respaldo-diario`.
