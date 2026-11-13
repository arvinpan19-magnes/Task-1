#!/usr/bin/env python3
"""Orquestador determinista del respaldo diario. El modelo NO hace nada de esto.

  respaldo.py preparar   [--fixture F.json] [--hoy AAAA-MM-DD] [--raiz DIR]
      lee -> valida -> registra (sin duplicar) -> prepara y verifica adjunto -> escribe
      salidas/estado.json con todo lo que el correo necesita. Código de salida:
        0 = listo (revisar estado.json: accion_correo / fila_nueva)
        2 = DETENERSE: dato faltante, fuera de rango o inconsistente (no se escribió nada)
  respaldo.py marcar-enviado --fecha F --mensaje-id ID [--raiz DIR]
      registra en memoria/envios.json que el correo de esa fecha salió (evita reenvíos)
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bcch  # noqa: E402
import exportar_xlsx  # noqa: E402


def hoy_chile():
    return dt.datetime.now(ZoneInfo(bcch.CONFIG["zona_horaria"])).date().isoformat()


def cargar_json(ruta, defecto):
    try:
        return json.loads(Path(ruta).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return defecto


def guardar_json(ruta, obj):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    tmp = str(ruta) + ".tmp"
    Path(tmp).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, ruta)


def preparar_adjunto(historial, carpeta):
    """Copia el historial a salidas/adjunto/, genera el base64 con CÓDIGO y verifica:
    (1) copia idéntica con cmp, (2) base64 decodifica a bytes idénticos, (3) abre con openpyxl."""
    carpeta.mkdir(parents=True, exist_ok=True)
    copia = carpeta / "historial.xlsx"
    copia.write_bytes(Path(historial).read_bytes())
    datos = copia.read_bytes()
    b64 = base64.b64encode(datos).decode("ascii")
    (carpeta / "historial.xlsx.b64").write_text(b64, encoding="ascii")
    deco = carpeta / "_decodificado.xlsx"
    deco.write_bytes(base64.b64decode((carpeta / "historial.xlsx.b64").read_text(encoding="ascii")))
    ok_copia = subprocess.run(["cmp", str(historial), str(copia)]).returncode == 0
    ok_b64 = subprocess.run(["cmp", str(historial), str(deco)]).returncode == 0
    deco.unlink()
    try:
        n = len(exportar_xlsx.leer(copia))
        abre = True
    except Exception as e:  # noqa: BLE001
        n, abre = 0, False
        print(f"adjunto no abre con openpyxl: {e}", file=sys.stderr)
    return {"archivo": "historial.xlsx", "ruta_copia": str(copia), "ruta_b64": str(carpeta / "historial.xlsx.b64"),
            "bytes": len(datos), "b64_caracteres": len(b64), "sha256": hashlib.sha256(datos).hexdigest(),
            "cmp_copia_identica": ok_copia, "cmp_b64_identico": ok_b64, "abre_con_openpyxl": abre,
            "filas": n, "verificado": ok_copia and ok_b64 and abre}


def preparar(args):
    raiz = Path(args.raiz)
    hoy = args.hoy or hoy_chile()
    estado_ruta = raiz / "salidas/estado.json"
    try:
        crudo = json.loads(Path(args.fixture).read_text(encoding="utf-8")) if args.fixture else bcch.leer_en_vivo()
        d = bcch.interpretar(crudo)
        if d["fecha_fuente"] > hoy:
            raise bcch.ErrorDatos(f"fecha de la fuente ({d['fecha_fuente']}) posterior a hoy ({hoy})")
    except bcch.ErrorDatos as e:
        est = {"estado": "DETENIDO", "fecha": hoy, "motivo": str(e),
               "aviso_falla": aviso_falla(hoy, str(e)), "fila_nueva": False, "accion_correo": "no_enviar"}
        guardar_json(estado_ruta, est)
        print(json.dumps(est, ensure_ascii=False, indent=2))
        return 2

    sin_cambio = d["fecha_fuente"] < hoy
    nota = f"sin cambio (último valor publicado: {d['fecha_fuente']})" if sin_cambio else ""
    historial = raiz / bcch.CONFIG["archivos"]["historial"]
    filas = exportar_xlsx.leer(historial) if historial.exists() else []
    previa = next((f for f in filas if f["fecha"] == hoy), None)
    aviso_difiere = None
    if previa is None:
        filas.append({"fecha": hoy, "dolar": d["dolar"], "uf": d["uf"], "cobre": d["cobre"],
                      "fuente": d["fuente"], "nota": nota})
        filas.sort(key=lambda f: f["fecha"])
        exportar_xlsx.escribir(historial, filas)
        fila_nueva = True
    else:
        fila_nueva = False
        if (previa["dolar"], previa["uf"], previa["cobre"]) != (d["dolar"], d["uf"], d["cobre"]):
            aviso_difiere = "La fila de hoy ya existía con valores distintos a los leídos ahora; NO se modificó."
    fila = next(f for f in filas if f["fecha"] == hoy)

    adj = preparar_adjunto(historial, raiz / "salidas/adjunto")
    if not adj["verificado"]:
        est = {"estado": "DETENIDO", "fecha": hoy, "motivo": "el adjunto no pasó la verificación", "adjunto": adj,
               "fila_nueva": fila_nueva, "accion_correo": "no_enviar"}
        guardar_json(estado_ruta, est)
        print(json.dumps(est, ensure_ascii=False, indent=2))
        return 2

    envios = cargar_json(raiz / bcch.CONFIG["archivos"]["estado_envios"], {})
    cfg = bcch.CONFIG["correo"]
    est = {"estado": "LISTO", "fecha": hoy, "fila_nueva": fila_nueva, "sin_cambio": bool(fila.get("nota")),
           "valores": {"dolar": fila["dolar"], "uf": fila["uf"], "cobre": fila["cobre"]},
           "fecha_fuente": d["fecha_fuente"], "fuente_urls": bcch.CONFIG["fuentes"], "nota": fila.get("nota") or "",
           "aviso": aviso_difiere,
           "correo": {"para": cfg["destinatarios"], "cc": [], "bcc": [],
                      "asunto": f"{cfg['asunto_prefijo']} {hoy}", "remitente_esperado": cfg["remitente_esperado"]},
           "adjunto": adj,
           "accion_correo": "ya_enviado" if hoy in envios else "enviar",
           "commit_y_push": fila_nueva}
    guardar_json(estado_ruta, est)
    print(json.dumps(est, ensure_ascii=False, indent=2))
    return 0


def aviso_falla(hoy, motivo):
    return {"asunto": f"FALLA respaldo diario Banco Central {hoy}",
            "cuerpo": f"El respaldo diario del {hoy} se detuvo y no se registró ningún dato.\nMotivo: {motivo}\n"
                      "No se inventó ningún valor.",
            "para": bcch.CONFIG["correo"]["destinatario_aviso_falla"]}  # None = solo aviso en el chat


def marcar(args):
    raiz = Path(args.raiz)
    ruta = raiz / bcch.CONFIG["archivos"]["estado_envios"]
    envios = cargar_json(ruta, {})
    envios[args.fecha] = {"mensaje_id": args.mensaje_id,
                          "registrado_en": dt.datetime.now(ZoneInfo(bcch.CONFIG["zona_horaria"])).isoformat(timespec="seconds")}
    guardar_json(ruta, envios)
    print(f"envío del {args.fecha} registrado")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preparar")
    p.add_argument("--fixture")
    p.add_argument("--hoy")
    p.add_argument("--raiz", default=str(Path(__file__).resolve().parent.parent))
    m = sub.add_parser("marcar-enviado")
    m.add_argument("--fecha", required=True)
    m.add_argument("--mensaje-id", required=True)
    m.add_argument("--raiz", default=str(Path(__file__).resolve().parent.parent))
    a = ap.parse_args()
    sys.exit(preparar(a) if a.cmd == "preparar" else marcar(a))
