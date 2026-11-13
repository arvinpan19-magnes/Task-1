# 01 · Contrato (Planificación)

**Estado:** borrador — pendiente de 🚪 **Puerta A** (aprobación explícita del alumno). El alumno dictó estos términos en su encargo del 2026-11-13; falta su «sí» formal.

## Objetivo y audiencia
Dejar cada día un respaldo verificable de dólar observado, UF y libra de cobre del Banco Central, y entregarlo por correo a `c.becar@udd.cl`.

## Alcance
Leer 2 páginas oficiales · validar · registrar una fila por fecha en `historial.xlsx` · enviar correo con adjunto · commit/push si hay fila nueva.
**Exclusiones:** otras series; correcciones o estimaciones de valores; otros destinatarios; análisis de mercado; histórico anterior al primer día de operación.

## Autonomía
| Puede solo | Requiere aprobación | Prohibido |
|---|---|---|
| Leer las páginas; validar; escribir `historial.xlsx`; generar adjunto; commit/push de filas nuevas en su rama | Activar el envío real (🚪C); activar la rutina automática (🚪D); cambiar rangos, destinatario o remitente | Inventar o corregir valores; enviar a otra persona o con cc/bcc; usar una vía distinta de Gmail sin preguntar; enviar si el adjunto no se verificó |

## Responsable
El alumno (aprueba y responde). Destinatario del resultado: `c.becar@udd.cl`.

## Criterios verificables
| # | Criterio | Cómo se comprueba |
|---|---|---|
| K1 | Dólar 500–2000, UF 30000–60000, cobre 1–10 | `scripts/bcch.py` (casos C3a-C3c) |
| K2 | Ningún dato faltante o ilegible se registra | casos C3d-C3f, C4 |
| K3 | Una fila por fecha, sin duplicar | caso C2 |
| K4 | Fin de semana/feriado: fila «sin cambio» y correo igual | casos C5a, C5b |
| K5 | Adjunto = xlsx real, liviano, idéntico (`cmp`) y abre con openpyxl | caso C7 |
| K6 | Un solo destinatario `c.becar@udd.cl`; asunto «Respaldo diario Banco Central AAAA-MM-DD» | caso C8 + verificación posterior al envío |
| K7 | Tras enviar, el mensaje queda con el adjunto | verificación en Gmail (no probada aún) |
| K8 | Commit/push solo con fila nueva | campo `commit_y_push` + caso C2 |

## Resultado satisfactorio / incompleto / detención correcta
- **Satisfactorio:** K1-K8 cumplidos; correo enviado y verificado.
- **Incompleto:** fila registrada pero correo no enviado o sin adjunto verificado (se informa; no se reenvía a ciegas).
- **Detención correcta:** dato faltante/fuera de rango/inconsistente, o Gmail no disponible → no se escribe ni se envía nada y se avisa.

## Supuestos y pendientes
`[PENDIENTE]` ¿Aviso de falla por correo? y a quién (hoy solo chat). `[PENDIENTE]` Aprobación formal de la puerta A.
## Retornos
Ninguno. ## Traspaso
Rangos y destinatario en `agent/controles/config.json`.
