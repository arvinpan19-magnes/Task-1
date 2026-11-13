# 04 · Memoria

**Estado:** borrador.

| Qué persiste | Dónde | Formato | Quién lo modifica |
|---|---|---|---|
| Historial de valores | `historial.xlsx` | xlsx liviano | `scripts/respaldo.py` |
| Envíos hechos (evita reenviar el mismo día) | `memoria/envios.json` | `{fecha: {mensaje_id, registrado_en}}` | `respaldo.py marcar-enviado` |
| Decisiones | `memoria/decisiones.md` | tabla | Claude + alumno |
| Estado del trabajo (checkpoint) | `memoria/estado.md` | markdown con versión de fuentes | Claude |
| Último resultado de ejecución | `salidas/estado.json` (regenerable, no se versiona) | JSON | código |

**Recuperación:** leer `p2a/PROGRESO.md` → `memoria/estado.md` → `memoria/decisiones.md` → verificar que `historial.xlsx` abre y que `git log` coincide → continuar.
**No se guarda:** contraseñas, tokens, contenido de correos recibidos, el HTML de las páginas.
## Supuestos y pendientes
`[PENDIENTE]` La rutina en la nube (claude.ai) arranca con un clon limpio: `memoria/envios.json` debe estar en el repo (lo está) para no reenviar.
## Retornos / Traspaso
Ninguno / el harness lee `memoria/envios.json` vía `respaldo.py`.
