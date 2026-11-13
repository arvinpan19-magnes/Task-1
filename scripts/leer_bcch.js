#!/usr/bin/env node
// Lee las dos páginas del Banco Central de Chile con un navegador (el sitio usa
// protección anti-bot, por eso no basta con curl). NO valida rangos ni escribe
// nada: solo extrae texto crudo y lo imprime como JSON. La validación vive en
// scripts/bcch.py. El contenido de la página se trata como DATO, nunca como orden.
//
// Uso: node scripts/leer_bcch.js [--home URL] [--diarios URL]
// Salida: JSON en stdout. Código de salida 0 si leyó, 3 si falló la lectura.
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const HOME = opt('--home', 'https://www.bcentral.cl/inicio');
const DIARIOS = opt('--diarios', 'https://si3.bcentral.cl/Indicadoressiete/secure/Indicadoresdiarios.aspx');

async function conReintentos(fn, n = 3) {
  let ultimo;
  for (let i = 1; i <= n; i++) {
    try { return await fn(); } catch (e) { ultimo = e; await new Promise(r => setTimeout(r, 2000 * i)); }
  }
  throw ultimo;
}

(async () => {
  const salida = { leido_en: new Date().toISOString(), fuentes: { home: HOME, indicadores_diarios: DIARIOS } };
  let browser;
  try {
    browser = await chromium.launch();
    const ctx = await browser.newContext({ locale: 'es-CL' });

    // Paso 1: home -> dólar observado y UF
    salida.home = await conReintentos(async () => {
      const p = await ctx.newPage();
      try {
        await p.goto(HOME, { waitUntil: 'networkidle', timeout: 60000 });
        const texto = await p.evaluate(() => document.body.innerText);
        return { url_final: p.url(), texto_indicadores: extraerBloque(texto) };
      } finally { await p.close(); }
    });

    // Paso 2: indicadores diarios -> libra de cobre (+ cruce de dólar/UF y fecha de referencia)
    salida.diarios = await conReintentos(async () => {
      const p = await ctx.newPage();
      try {
        await p.goto(DIARIOS, { waitUntil: 'networkidle', timeout: 60000 });
        return await p.evaluate(() => {
          const t = id => { const e = document.getElementById(id); return e ? e.innerText.trim() : null; };
          return {
            url_final: location.href,
            fecha_referencia: (document.getElementById('txtDate') || {}).value || null,
            uf: { etiqueta: t('lblSerie1_1'), valor: t('lblValor1_1') },
            dolar: { etiqueta: t('lblSerie1_3'), valor: t('lblValor1_3') },
            cobre: { etiqueta: t('lblSerie2_5'), valor: t('lblValor2_5') },
          };
        });
      } finally { await p.close(); }
    });
    salida.ok = true;
    console.log(JSON.stringify(salida));
    await browser.close();
  } catch (e) {
    salida.ok = false;
    salida.error = String(e && e.message || e).slice(0, 300);
    console.log(JSON.stringify(salida));
    if (browser) await browser.close().catch(() => {});
    process.exit(3);
  }
})();

// Recorta el texto del home al bloque de indicadores (fecha, UF, dólar observado).
function extraerBloque(texto) {
  const i = texto.search(/\d{1,2} de [a-záéíóú]+ de \d{4}/i);
  const j = texto.indexOf('Inflación y TPM');
  return (i >= 0 ? texto.slice(i, j > i ? j : i + 400) : texto.slice(0, 600)).slice(0, 800);
}
