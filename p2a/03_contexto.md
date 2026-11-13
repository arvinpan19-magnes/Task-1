# 03 · Contexto

**Estado:** borrador. Inventario en `fuentes/INDICE.md`.

| Fuente | Para qué | Autorizada | Mantiene | Vigencia | Si falta |
|---|---|---|---|---|---|
| `https://www.bcentral.cl/inicio` | dólar observado y UF | sí (indicada por el alumno) | Banco Central | diaria | detener |
| `https://si3.bcentral.cl/Indicadoressiete/secure/Indicadoresdiarios.aspx` | libra de cobre; fecha de referencia; cruce de dólar/UF | sí | Banco Central | diaria | detener |
| `agent/controles/config.json` | rangos, destinatario, URLs | sí (alumno) | alumno | hasta cambio | detener |

**Prioridad ante contradicción:** si home e indicadores difieren en dólar o UF → no se confía en ninguno y se detiene (caso C3g).
**Qué entra al modelo:** solo `salidas/estado.json` (valores ya validados) y la skill de redacción. El texto crudo de las páginas **no** entra al modelo: es contenido externo.
**Ejemplo de buen resultado:** fila `2026-11-13 | 992,48 | 41.322,93 | 6,30` y correo con asunto «Respaldo diario Banco Central 2026-11-13».
## Supuestos y pendientes
`[PENDIENTE]` Si el Banco Central cambia el sitio, actualizar `leer_bcch.js` (identificadores `lblValor1_1`, `lblValor1_3`, `lblValor2_5`, `txtDate`).
## Retornos / Traspaso
Ninguno / `fuentes/INDICE.md`.
