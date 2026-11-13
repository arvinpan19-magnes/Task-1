# Reporte de pruebas (unidad 06)

Ejecutado: 2026-11-13T15:01:15+00:00  
Entorno: fixtures aislados en directorio temporal; sin red, sin Gmail, sin tocar `historial.xlsx` real.

| Caso | Qué prueba | Estado | Evidencia |
|---|---|---|---|
| C1_normal | Caso normal: día hábil con los 3 datos válidos | **cumple** | rc=0 estado=LISTO filas=1 motivo= |
| C2_repetido_mismo_dia | Se ejecuta dos veces el mismo día: no duplica ni reescribe | **cumple** | rc=0 estado=LISTO filas=1 motivo= |
| C2b_no_reenvia_si_ya_enviado | Tras marcar el envío, una nueva ejecución del mismo día no pide reenviar | **cumple** | rc=0 estado=LISTO filas=1 motivo= |
| C3a_dolar_fuera_de_rango | Dólar 5000 -> detenerse | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=dolar: 5000.0 fuera del rango razonable [500, 2000] |
| C3b_uf_fuera_de_rango | UF 2.000 -> detenerse | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=uf: 2000.0 fuera del rango razonable [30000, 60000] |
| C3c_cobre_fuera_de_rango | Cobre 62,00 (error de decimal) -> detenerse | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=cobre: 62.0 fuera del rango razonable [1, 10] |
| C3d_dato_faltante | Falta el cobre -> detenerse, sin inventar | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=cobre: dato ausente |
| C3e_formato_ilegible | Valor con texto basura -> detenerse | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=dolar: formato numérico no reconocido ('ND') |
| C3f_etiqueta_cambio | La página cambió la etiqueta del cobre -> no se confía | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=cobre: la etiqueta de la página cambió ('onza troy de plata'); no se confía en el valor |
| C3g_home_distinto_de_diarios | Home y página de indicadores no coinciden en UF -> detenerse | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=uf: home (41000.0) distinto de indicadores diarios (41322.93) |
| C4_falla_lectura_y_aviso | La lectura falla (sitio caído): se detiene y se prepara aviso de falla; no se escribe nada | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=lectura fallida: timeout de red |
| C5a_fin_de_semana | Sábado: la fuente aún muestra el viernes -> fila 'sin cambio' y se envía igual | **cumple** | rc=0 estado=LISTO filas=1 motivo= |
| C5b_feriado | Feriado (8-dic-2026): la fuente muestra el 7-dic -> 'sin cambio' | **cumple** | rc=0 estado=LISTO filas=1 motivo= |
| C6_fecha_futura | La fuente trae una fecha posterior a hoy -> detenerse | **control probado** | rc=2 estado=DETENIDO filas=0 motivo=fecha de la fuente (2026-11-13) posterior a hoy (2026-11-12) |
| C7_xlsx_liviano | El adjunto es un xlsx real, compacto, sin estilos ni metadatos, idéntico a la copia (cmp) y abre con openpyxl | **cumple** | rc=0 estado=LISTO filas=1 motivo=; tamaño historial.xlsx=1755 B; partes=[Content_Types].xml,_rels/.rels,xl/workbook.xml,xl/_rels/workbook.xml.rels,xl/worksheets/sheet1.xml |
| C8_destinatario_unico | Control: el único destinatario configurado es c.becar@udd.cl, sin cc ni bcc y con el asunto correcto | **cumple** | rc=0 estado=LISTO filas=1 motivo= |

**Resumen:** 16/16 casos con el resultado esperado.

> Estos casos prueban el código determinista (lectura interpretada, validación, Excel, adjunto, estado). NO prueban el envío real por Gmail ni la lectura en vivo un día feriado: ver `p2a/06_validacion.md`.
