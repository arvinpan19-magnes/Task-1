# Decisiones

| # | Fecha | Decisión | Motivo | Quién decidió |
|---|---|---|---|---|
| D1 | 2026-11-13 | Repo de trabajo: `arvinpan19-magnes/Task-1`; `udd-ia-2026/task1-arvinpan19-magnes` es solo guía (reglas del ramo) | Indicación del alumno | Alumno |
| D2 | 2026-11-13 | Seguir las reglas del repo guía: `CLAUDE.md`, hook de registro de sesión en `reportes/`, comando `/cerrar-task` | El alumno pidió seguir todo lo que pide ese repo | Alumno |
| D3 | 2026-11-13 | Usar Prompt2Agent con el master prompt oficial descargado de prompt2agent-metodologia.netlify.app (copia en `p2a/`) | Pedido del alumno | Alumno |
| D4 | 2026-11-13 | Permitir en la red del entorno los hosts `prompt2agent-metodologia.netlify.app`, `www.bcentral.cl`, `si3.bcentral.cl` | Estaban bloqueados (403); el alumno aprobó el cambio | Alumno (aprobó), Claude (propuso) |
| D5 | 2026-11-13 | Leer las páginas con navegador headless, no con curl | El sitio tiene protección anti-bot (Incapsula); curl recibe un desafío JS | Claude |
| D6 | 2026-11-13 | Dólar y UF desde el home; cobre y fecha de referencia desde indicadores diarios; además se cruzan dólar y UF entre ambas páginas y, si difieren, se detiene | El proceso lo define el alumno; el cruce es un control extra de Claude | Alumno (proceso), Claude (cruce) |
| D7 | 2026-11-13 | Lo exacto (leer, validar, Excel, adjunto) en código; el modelo solo redacta el correo | Regla de diseño del alumno; controles fuera del modelo (master prompt §6.3) | Alumno |
| D8 | 2026-11-13 | xlsx propio mínimo (zip+XML, sin estilos/metadatos, bytes deterministas) en vez de openpyxl al escribir | Adjunto liviano y comparable con `cmp`; pedido de `scripts/exportar_xlsx.py` | Alumno (pedido), Claude (técnica) |
| D9 | 2026-11-13 | El historial tiene 6 columnas: fecha, dólar, UF, cobre, fuente, **nota** | La marca «sin cambio» necesita un lugar; el alumno pidió 5 columnas base | Claude [SUPUESTO] — confirmar |
| D10 | 2026-11-13 | «Sin cambio» = la fecha de referencia de la fuente es anterior a hoy; se registra el último valor publicado | Cubre fines de semana y feriados sin lista de feriados | Claude [SUPUESTO] — confirmar |
| D11 | 2026-11-13 | Ejecución repetida el mismo día: no duplica fila; no reenvía si el envío ya quedó registrado en `memoria/envios.json` | Evitar correos duplicados | Claude [SUPUESTO] — confirmar |
| D12 | 2026-11-13 | **No se envía ningún correo real todavía.** Gmail principal falló al conectar (502); el conector alternativo solo tiene `create_draft`. Se detiene y se pregunta al alumno | Regla del alumno: si Gmail no está disponible, detenerse y avisar; master prompt: 🚪C y no hacer acciones reales sin autorización | Alumno (regla), Claude (aplicó) |
| D13 | 2026-11-13 | Remitente: `arvinpan@gmail.com` (cuenta distinta a la de UDD, aceptado) | Indicado por el alumno | Alumno |
| D14 | 2026-11-13 | Disparador manual con `/respaldo-diario`; la rutina 09:00 (America/Santiago) en claude.ai queda para después | Indicado por el alumno | Alumno |
| D15 | 2026-11-13 | Aviso de falla: solo en el chat por ahora (`destinatario_aviso_falla: null`) | La regla dice «destinatario: solo c.becar@udd.cl»; no se decidió si el aviso va a esa persona | Claude — **pendiente de decisión del alumno** |
| D16 | 2026-11-13 | Desarrollo en la rama `claude/respaldo-diario` | Convención del repo guía (`claude/...`); commit+push de datos solo con fila nueva | Claude |
| D17 | 2026-11-13 | Estados de madurez: ninguna unidad `acordado`/`implementado`/`validado` hasta que el alumno apruebe 🚪A y 🚪B y se pruebe el envío | Reglas de madurez del master prompt | Claude |
