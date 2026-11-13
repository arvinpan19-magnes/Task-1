# 06 · Validación (Ejecución)

**Estado:** prototipo (parcial). Resultados esperados escritos antes de ejecutar en `evals/casos/casos.json`. Ejecutor: `python3 evals/ejecutar.py` → `evals/reporte.md`.

## Resultado de la ejecución (2026-11-13)
**16/16 casos con el resultado esperado** (ver `evals/reporte.md`). Cubren: caso normal; ejecución repetida el mismo día (sin duplicar, bytes idénticos); dólar/UF/cobre fuera de rango; dato faltante; formato ilegible; etiqueta cambiada; home≠diarios; falla de lectura + aviso de falla preparado; fin de semana; feriado; fecha futura; xlsx liviano; destinatario único.

Además, una **ejecución real** en vivo el 2026-11-13: lectura de ambas páginas, validación, fila registrada, adjunto verificado.

## Declaración de alcance validado
**Funciona (con evidencia):**
- Lectura en vivo de home e indicadores diarios con navegador (1 ejecución real, 2026-11-13).
- Interpretación del formato chileno, validación de rangos, detención ante datos malos (sin escribir nada).
- Registro sin duplicar; fila «sin cambio» cuando la fuente trae una fecha anterior a hoy (simulado con fixtures).
- xlsx de 1,7 KB que abre con openpyxl; copia y base64 idénticos al original (`cmp`).

**Condiciones:** Python 3.13 + openpyxl, Node + Playwright/Chromium, red con acceso a los hosts del BCCh.

**NO probado / pendiente:**
- **Envío real por Gmail** y la verificación posterior de que el mensaje trae el adjunto (K7). El conector principal falló al conectar y el alternativo no tiene herramienta de envío.
- **Correo de aviso de falla**: solo se probó que el código lo *prepara* (asunto/cuerpo); no tiene destinatario definido ni se envió.
- **Falla del conector de Gmail**: se *observó* (502 al iniciar) pero no hay prueba automatizada; el procedimiento es detenerse y avisar.
- Lectura **en vivo** un sábado, domingo o feriado (solo simulada con fixtures): puede que la fuente muestre otra fecha o estructura.
- Apertura del xlsx en Excel o LibreOffice (solo openpyxl).
- Ejecución a las 09:00 exactas (¿ya está publicado el dólar?).
- Rutina automática en la nube.
- Repeticiones de casos críticos en vivo (solo 1 ejecución real).

## Regresión
Ejecutar `python3 evals/ejecutar.py` tras cualquier cambio en `scripts/` o `config.json`.
## Retornos / Traspaso
Ninguno. Traspaso: `evals/reporte.md`.
