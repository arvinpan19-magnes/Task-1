#!/usr/bin/env python3
"""Ejecutor de pruebas (unidad 06). Cada caso corre en un directorio temporal aislado con un
fixture; NO toca el historial real, NO envía correos y NO usa la red.
Uso: python3 evals/ejecutar.py   -> escribe evals/reporte.md y sale con código 1 si algo falla."""
import copy
import datetime as dt
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import exportar_xlsx  # noqa: E402

BASE = json.loads((RAIZ / "evals/casos/lectura_real_2026-11-13.json").read_text(encoding="utf-8"))
REPETICIONES = 3  # los casos críticos se repiten 3 veces (instrucciones del ramo)
CASOS = json.loads((RAIZ / "evals/casos/casos.json").read_text(encoding="utf-8"))["casos"]


def mutar(obj, ruta, valor):
    ks = ruta.split(".")
    for k in ks[:-1]:
        obj = obj[k]
    obj[ks[-1]] = valor


def correr(raiz, fixture, hoy):
    r = subprocess.run([sys.executable, str(RAIZ / "scripts/respaldo.py"), "preparar", "--fixture", str(fixture),
                        "--hoy", hoy, "--raiz", str(raiz)], capture_output=True, text=True)
    est = json.loads((raiz / "salidas/estado.json").read_text(encoding="utf-8"))
    return r.returncode, est


def ejecutar_caso(c):
    fallas, evidencia = [], []
    with tempfile.TemporaryDirectory() as d:
        raiz = Path(d)
        (raiz / "memoria").mkdir()
        fx = copy.deepcopy(BASE)
        for k, v in (c.get("mut") or {}).items():
            mutar(fx, k, v)
        fxp = raiz / "fixture.json"
        fxp.write_text(json.dumps(fx), encoding="utf-8")
        e = c["esperado"]
        hist = raiz / "historial.xlsx"
        bytes_1 = None
        for i in range(c.get("ejecuciones", 1)):
            rc, est = correr(raiz, fxp, c["hoy"])
            if i == 0 and hist.exists():
                bytes_1 = hist.read_bytes()
            if i == 0 and c.get("marcar_enviado_tras_1"):
                subprocess.run([sys.executable, str(RAIZ / "scripts/respaldo.py"), "marcar-enviado", "--fecha", c["hoy"],
                                "--mensaje-id", "TEST", "--raiz", str(raiz)], capture_output=True, check=True)
        filas = exportar_xlsx.leer(hist) if hist.exists() else []
        evidencia.append(f"rc={rc} estado={est.get('estado')} filas={len(filas)} motivo={est.get('motivo', '')[:90]}")

        def chk(nombre, real, esperado):
            if real != esperado:
                fallas.append(f"{nombre}: esperado {esperado!r}, real {real!r}")

        if "rc" in e: chk("rc", rc, e["rc"])
        if "estado" in e: chk("estado", est.get("estado"), e["estado"])
        if "filas" in e: chk("filas", len(filas), e["filas"])
        if "fila_nueva" in e: chk("fila_nueva", est.get("fila_nueva"), e["fila_nueva"])
        if "commit_y_push" in e: chk("commit_y_push", est.get("commit_y_push"), e["commit_y_push"])
        if "accion_correo" in e: chk("accion_correo", est.get("accion_correo"), e["accion_correo"])
        if "historial_existe" in e: chk("historial_existe", hist.exists(), e["historial_existe"])
        if e.get("nota_vacia"): chk("nota_vacia", (filas[0]["nota"] or "") == "", True)
        if "nota_empieza" in e: chk("nota_empieza", (filas[0]["nota"] or "").startswith(e["nota_empieza"]), True)
        if e.get("bytes_historial_iguales"): chk("bytes_historial_iguales", hist.read_bytes() == bytes_1, True)
        if "adjunto_verificado" in e: chk("adjunto_verificado", (est.get("adjunto") or {}).get("verificado"), True)
        if "aviso_falla_asunto" in e: chk("aviso_falla_asunto", (est.get("aviso_falla") or {}).get("asunto"), e["aviso_falla_asunto"])
        if "para" in e: chk("para", est["correo"]["para"], e["para"]); chk("cc", est["correo"]["cc"], e["cc"]); chk("bcc", est["correo"]["bcc"], e["bcc"])
        if "asunto" in e: chk("asunto", est["correo"]["asunto"], e["asunto"])
        if "max_bytes" in e:
            tam = hist.stat().st_size
            evidencia.append(f"tamaño historial.xlsx={tam} B")
            chk(f"tamaño<={e['max_bytes']}", tam <= e["max_bytes"], True)
            with zipfile.ZipFile(hist) as z:
                nombres = z.namelist()
                evidencia.append("partes=" + ",".join(nombres))
                for p in e["sin_partes"]:
                    chk(f"sin {p}", any(p in n for n in nombres), False)
                chk("zip íntegro", z.testzip(), None)
    return fallas, "; ".join(evidencia)


def caso_url_invalida():
    """Usa el lector REAL (node) con URLs inexistentes: debe fallar con ok=false y el intérprete debe detenerse."""
    fallas = []
    r = subprocess.run(["node", str(RAIZ / "scripts/leer_bcch.js"), "--home", "http://127.0.0.1:59999/", "--diarios", "http://127.0.0.1:59999/"],
                       capture_output=True, text=True, timeout=120)
    crudo = json.loads(r.stdout)
    if crudo.get("ok") is not False: fallas.append("el lector debía devolver ok=false")
    if r.returncode != 3: fallas.append(f"rc del lector esperado 3, real {r.returncode}")
    import bcch
    try:
        bcch.interpretar(crudo); fallas.append("interpretar() debía lanzar ErrorDatos")
    except bcch.ErrorDatos:
        pass
    return fallas, f"lector rc={r.returncode} ok={crudo.get('ok')} error={" ".join(str(crudo.get("error")).split())[:70]}"


def main():
    filas_md, malos = [], 0
    for c in CASOS:
        fallas, ev = [], ""
        for rep in range(REPETICIONES):
            f, e = ejecutar_caso(c)
            fallas += [f"[rep {rep + 1}] {x}" for x in f]
            ev = e
        ev = f"{REPETICIONES}/{REPETICIONES} repeticiones · " + ev if not fallas else ev
        estado = "cumple" if not fallas else "FALLA"
        if c["id"].startswith(("C3", "C4", "C6")) and not fallas:
            estado = "control probado"
        malos += bool(fallas)
        filas_md.append(f"| {c['id']} | {c['desc']} | **{estado}** | {ev}{' — ' + ' | '.join(fallas) if fallas else ''} |")
    fallas, ev = caso_url_invalida()
    malos += bool(fallas)
    filas_md.append(f"| C9_url_invalida | Sin internet / URL inválida con el lector real: ok=false y se detiene | **{'control probado' if not fallas else 'FALLA'}** | {ev}{' — ' + ' | '.join(fallas) if fallas else ''} |")
    ahora = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    md = ["# Reporte de pruebas (unidad 06)", "", f"Ejecutado: {ahora}  ", "Entorno: fixtures aislados en directorio temporal; sin red, sin Gmail, sin tocar `historial.xlsx` real.", "",
          "| Caso | Qué prueba | Estado | Evidencia |", "|---|---|---|---|", *filas_md, "",
          f"**Resumen:** {len(CASOS) + 1 - malos}/{len(CASOS) + 1} casos (cada uno repetido {REPETICIONES} veces, salvo C9) con el resultado esperado.", "",
          "> Estos casos prueban el código determinista (lectura interpretada, validación, Excel, adjunto, estado). "
          "NO prueban el envío real por Gmail ni la lectura en vivo un día feriado: ver `p2a/06_validacion.md`.", ""]
    (RAIZ / "evals/reporte.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
