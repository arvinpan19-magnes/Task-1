# Tablero de madurez · Respaldo diario Banco Central

Actualizado: 2026-11-13 · Ciclo 0 + primer ciclo de construcción

```
Unidad              Estado        Vacíos clave
00 Baseline         borrador      tiempo manual y tasa de error actuales sin medir
01 Planificación    acordado      —  (🚪A aprobada 2026-11-13)
02 Método           acordado      hora de publicación del dólar sin confirmar  (🚪B aprobada)
03 Contexto         implementado  sin vigilancia automática de cambios en el sitio del BCCh
04 Memoria          implementado  la rutina en la nube no se probó con un clon limpio
05 Habilidad        prototipo     Gmail: sin herramienta de envío con adjunto (conector principal caído)
06 Ejecución        prototipo     17/17 en fixtures (x3) + 1 ejecución real contrastada; envío real y feriado en vivo sin probar
07 Automatización   borrador      manual con /respaldo-diario; rutina 09:00 pendiente (🚪D)
Próximo ciclo propuesto: reconectar Gmail con envío (🚪C), probar el envío real y un fin de semana en vivo
```

Reglas de madurez: 03 y 05 no pueden estar `implementado` sin 02 `acordado`; 06 no puede estar `validado` sin 01-05 `implementado`; 07 no puede ir a un entorno real sin 06 `validado`.
Hoy no hay nada `validado`: falta probar el envío real (05) y por eso 06 no puede validarse ni 07 activarse.
