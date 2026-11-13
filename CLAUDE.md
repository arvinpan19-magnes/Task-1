# Reglas del ramo para esta task

- Este repositorio corresponde a UNA sola task. No mezcles trabajo de otras tasks aquí.
- Al iniciar una sesión, antes de hacer cualquier otra cosa: ejecuta `git fetch --all` y revisa si hay ramas remotas `claude/...` (u `origin/main`) con commits que no estén en tu rama actual. Si las hay, intégralas en tu rama con `git merge`, de la más antigua a la más reciente, y avisa al alumno en una línea que recuperaste su trabajo anterior. Si hay conflictos, conserva la versión más reciente del trabajo, y en `reportes/` conserva todos los archivos. Nunca borres ramas.
- La carpeta `reportes/` se registra y se sube sola. No la borres, no la edites a mano y no la agregues a `.gitignore`.
- Haz commit y push del trabajo del alumno cada vez que completes un avance importante y antes de terminar una sesión.
- Usa Sonnet como modelo por defecto, salvo que el alumno pida otro.
- Cuando el alumno escriba "cerrar task" (o `/cerrar-task`), ejecuta el cierre descrito en `.claude/commands/cerrar-task.md`. No inicies el cierre por otras frases como "listo", "terminé" o "ya está": son parte normal de la conversación. Si el alumno parece haber terminado, puedes recordarle que escriba "cerrar task".
- Nunca guardes contraseñas, claves de API ni datos personales en el repositorio.

# Prompt2Agent: agente del respaldo diario del Banco Central

Este repo construye un agente con la metodología Prompt2Agent. El master prompt completo está en
`p2a/Prompt2Agent_MasterPrompt_Code.md`: es la guía de cómo trabajar (ciclos, tablero de madurez, puertas de aprobación A-D).

## Al iniciar cada sesión (recuperación de estado)
1. `git fetch --all` y revisar ramas `claude/...` (regla del ramo, arriba).
2. Leer `p2a/PROGRESO.md`, `memoria/decisiones.md`, `memoria/estado.md` y las instrucciones del agente `agent/INSTRUCCIONES.md`.
3. Mostrar el tablero de madurez antes de continuar.

## Reglas duras (no negociables)
- Lo exacto lo hace código (`scripts/`): leer la página, validar, escribir el Excel, generar el adjunto. El modelo solo redacta el correo.
- Nunca inventar valores. Dato faltante o fuera de rango = detenerse y avisar.
- Destinatario único: `c.becar@udd.cl`. Sin cc ni bcc. Está fijado en `agent/controles/config.json`.
- Nunca pegar el base64 del adjunto a mano ni de memoria: el base64 lo genera el código (`salidas/adjunto/historial.xlsx.b64`).
- Si el conector de Gmail no está disponible o no puede enviar con adjunto: detenerse y avisar al alumno. No usar otra vía sin preguntar.
- No hay envíos reales de correo hasta que el alumno apruebe la puerta C (sistemas reales).
- Comando de operación: `/respaldo-diario` (ver `.claude/commands/respaldo-diario.md`).
