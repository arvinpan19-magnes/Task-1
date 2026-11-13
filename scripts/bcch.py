"""Interpretación y validación de los datos del Banco Central. Todo es código determinista:
el modelo no interviene aquí. Nunca se inventa un valor: si algo falta o no calza, se lanza
ErrorDatos y el proceso se detiene."""
import json
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = json.loads((RAIZ / "agent/controles/config.json").read_text(encoding="utf-8"))

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8,
         "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12,
         "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
         "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11,
         "diciembre": 12}
ETIQUETAS = {"uf": "unidad de fomento", "dolar": "dólar observado", "cobre": "libra de cobre"}


class ErrorDatos(Exception):
    """Dato faltante, ilegible, fuera de rango o inconsistente. Obliga a detenerse."""


def numero_cl(texto, nombre):
    """'41.322,93' -> 41322.93. Rechaza cualquier formato que no sea el esperado."""
    if texto is None:
        raise ErrorDatos(f"{nombre}: dato ausente")
    t = str(texto).replace("\xa0", " ").strip().lstrip("$").strip()
    if not re.fullmatch(r"\d{1,3}(\.\d{3})*(,\d+)?|\d+(,\d+)?", t):
        raise ErrorDatos(f"{nombre}: formato numérico no reconocido ({texto!r})")
    return float(t.replace(".", "").replace(",", "."))


def fecha_cl(texto, nombre="fecha_referencia"):
    """'13 Nov 2026' o '13 de noviembre de 2026' -> '2026-11-13'."""
    m = re.search(r"(\d{1,2})\s+(?:de\s+)?([A-Za-zÁÉÍÓÚáéíóú]+)\.?\s+(?:de\s+)?(\d{4})", texto or "")
    if not m or m.group(2).lower() not in MESES:
        raise ErrorDatos(f"{nombre}: fecha no reconocida ({texto!r})")
    return f"{int(m.group(3)):04d}-{MESES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"


def validar_rango(clave, valor):
    lo, hi = CONFIG["rangos"][clave]
    if not (lo <= valor <= hi):
        raise ErrorDatos(f"{clave}: {valor} fuera del rango razonable [{lo}, {hi}]")


def interpretar(crudo):
    """crudo = JSON de leer_bcch.js (o un fixture de prueba). Devuelve dict validado."""
    if not crudo.get("ok"):
        raise ErrorDatos(f"lectura fallida: {crudo.get('error', 'sin detalle')}")
    d = crudo.get("diarios") or {}
    h = crudo.get("home") or {}
    for clave, etiqueta in ETIQUETAS.items():
        e = ((d.get(clave) or {}).get("etiqueta") or "").lower()
        if etiqueta not in e:
            raise ErrorDatos(f"{clave}: la etiqueta de la página cambió ({e!r}); no se confía en el valor")
    v = {c: numero_cl((d.get(c) or {}).get("valor"), c) for c in ETIQUETAS}
    for c, x in v.items():
        validar_rango(c, x)
    fecha_fuente = fecha_cl(d.get("fecha_referencia"))

    # Cruce home vs indicadores diarios (dólar y UF deben coincidir)
    txt = h.get("texto_indicadores") or ""
    m_uf = re.search(r"\bUF\s+\$?\s*([\d.]+,\d+)", txt)
    m_do = re.search(r"Dólar Observado\s+\$?\s*([\d.]+,\d+)", txt, re.I)
    if not m_uf or not m_do:
        raise ErrorDatos("home: no se encontraron UF y/o dólar observado en la portada")
    for c, m in (("uf", m_uf), ("dolar", m_do)):
        vh = numero_cl(m.group(1), f"home.{c}")
        if abs(vh - v[c]) > CONFIG["tolerancia_cruce_home_vs_diarios"]:
            raise ErrorDatos(f"{c}: home ({vh}) distinto de indicadores diarios ({v[c]})")
    fecha_home = None
    try:
        fecha_home = fecha_cl(txt, "home.fecha")
    except ErrorDatos:
        pass
    return {"dolar": v["dolar"], "uf": v["uf"], "cobre": v["cobre"],
            "fecha_fuente": fecha_fuente, "fecha_home": fecha_home,
            "fuente": CONFIG["fuentes"]["home"] + " ; " + CONFIG["fuentes"]["indicadores_diarios"]}


def leer_en_vivo():
    r = subprocess.run(["node", str(RAIZ / "scripts/leer_bcch.js")], capture_output=True, text=True, timeout=300)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": f"salida ilegible del lector (rc={r.returncode}): {r.stderr[:200]}"}
