#!/usr/bin/env python3
"""Genera un .xlsx REAL y liviano: una hoja, sin estilos, sin sharedStrings, sin docProps ni
metadatos de autor/fecha. Es determinista (misma entrada -> mismos bytes), así que el adjunto
puede compararse byte a byte con cmp. Abre con Excel, LibreOffice y openpyxl.

Uso como librería:  escribir(ruta, filas)  con filas = lista de dicts con las claves COLUMNAS
Uso como CLI:       exportar_xlsx.py ORIGEN.xlsx DESTINO.xlsx   (relee con openpyxl y recompacta)
"""
import sys
import zipfile
from xml.sax.saxutils import escape

COLUMNAS = [("fecha", "fecha"), ("dolar", "dólar observado (CLP)"), ("uf", "UF (CLP)"),
            ("cobre", "cobre (USD/lb)"), ("fuente", "fuente"), ("nota", "nota")]
NUMERICAS = {"dolar", "uf", "cobre"}
_FECHA_ZIP = (2026, 1, 1, 0, 0, 0)  # fija: bytes reproducibles


def _col(i):
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]


def _celda(ref, valor, numerica):
    if valor is None or valor == "":
        return ""
    if numerica:
        return f'<c r="{ref}"><v>{repr(float(valor))}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(str(valor))}</t></is></c>'


def _hoja(filas):
    xs = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    cab = "".join(_celda(f"{_col(i)}1", t, False) for i, (_, t) in enumerate(COLUMNAS))
    xs.append(f'<row r="1">{cab}</row>')
    for n, fila in enumerate(filas, start=2):
        cs = "".join(_celda(f"{_col(i)}{n}", fila.get(k), k in NUMERICAS) for i, (k, _) in enumerate(COLUMNAS))
        xs.append(f'<row r="{n}">{cs}</row>')
    xs.append("</sheetData></worksheet>")
    return "".join(xs)


def escribir(ruta, filas):
    partes = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '</Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>',
        "xl/workbook.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="historial" sheetId="1" r:id="rId1"/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '</Relationships>',
        "xl/worksheets/sheet1.xml": _hoja(filas),
    }
    tmp = str(ruta) + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for nombre, contenido in partes.items():
            zi = zipfile.ZipInfo(nombre, _FECHA_ZIP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, contenido.encode("utf-8"))
    import os
    os.replace(tmp, ruta)  # escritura atómica: nunca queda un archivo a medias


def leer(ruta):
    """Lee el historial con openpyxl. Devuelve lista de dicts con las claves de COLUMNAS."""
    from openpyxl import load_workbook
    wb = load_workbook(ruta, read_only=True, data_only=True)
    ws = wb.active
    filas = []
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        if not r or r[0] is None:
            continue
        filas.append({k: r[j] if j < len(r) else None for j, (k, _) in enumerate(COLUMNAS)})
    wb.close()
    return filas


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("uso: exportar_xlsx.py ORIGEN.xlsx DESTINO.xlsx")
    escribir(sys.argv[2], leer(sys.argv[1]))
    print(f"ok: {sys.argv[2]}")
