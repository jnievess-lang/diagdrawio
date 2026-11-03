"""Genera ERD-Editronic-Dev.drawio (hoja completa y hojas por módulo) a partir de entidades.md.

Uso: python3 editronic/herramientas/generar_erd.py editronic/entidades.md editronic/ERD-Editronic-Dev.drawio
"""
import re, sys
from xml.sax.saxutils import quoteattr as q

md = open(sys.argv[1], encoding="utf8").read()

# ---------- 1. Leer tablas de entidades.md ----------
tablas = {}
for sec in re.split(r"\n## ", md)[1:]:
    nombre = sec.split("\n", 1)[0].strip()
    if not re.fullmatch(r"tb[a-z]+", nombre):
        continue
    filas = []
    for l in sec.split("\n"):
        if not l.startswith("|") or l.startswith("| Columna") or l.startswith("|---"):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 4:
            continue
        col, tipo, clave, nulo = c[0], c[1], c[2], c[3]
        tipo = "BIGINT IDENTITY" if tipo == "IDENTITY" else tipo
        clave = clave.replace(" ", "")
        filas.append((clave, col, tipo, "NULL" if nulo == "Sí" else ""))
    if filas:
        tablas[nombre] = filas
assert len(tablas) == 35, (len(tablas), sorted(tablas))

# ---------- 2. FK -> tabla referenciada ----------
FK = {
 "tipo_identificacion_id": "tbtiposidentificacion", "rol_id": "tbroles", "permiso_id": "tbpermisos",
 "usuario_id": "tbusuarios", "usuario_apertura_id": "tbusuarios", "usuario_cierre_id": "tbusuarios", "tecnico_id": "tbusuarios",
 "sesion_id": "tbsesiones", "reemplazado_por_id": "tbrefreshtokens", "tarifa_id": "tbtarifas", "cliente_id": "tbclientes",
 "tipo_equipo_id": "tbtiposequipo", "marca_id": "tbmarcas", "equipo_id": "tbequipos", "orden_garantia_id": "tbordenesreparacion",
 "pdf_ingreso_archivo_id": "tbarchivos", "pdf_archivo_id": "tbarchivos", "archivo_id": "tbarchivos", "logo_archivo_id": "tbarchivos",
 "orden_reparacion_id": "tbordenesreparacion", "estado_orden_id": "tbestadosorden", "categoria_producto_id": "tbcategoriasproducto",
 "tipo_iva_id": "tbtiposiva", "tipo_iva_predeterminado_id": "tbtiposiva", "producto_id": "tbproductos", "factura_id": "tbfacturas",
 "compra_id": "tbcompras", "proveedor_id": "tbproveedores", "proforma_id": "tbproformas", "sesion_caja_id": "tbsesionescaja",
 "metodo_pago_id": "tbmetodospago",
}
# Lado "muchos" obligatorio (1..N): el padre siempre tiene al menos un hijo
UNO_A_MUCHOS = {("tbfacturas", "tbdetallefactura"), ("tbproformas", "tbdetalleproforma"), ("tbcompras", "tbdetallecompra"),
                ("tbordenesreparacion", "tbhistorialestadosorden"), ("tbequipos", "tbordenesreparacion"),
                ("tbsesiones", "tbrefreshtokens")}

relaciones = []  # (hijo, col_fk, padre, lado_padre, lado_hijo)
for t, filas in tablas.items():
    for clave, col, tipo, nulo in filas:
        if "FK" not in clave:
            continue
        padre = FK[col]
        lado_padre = "0..1" if nulo else "1"
        if "UQ" in clave:
            lado_hijo = "0..1"
        elif (padre, t) in UNO_A_MUCHOS:
            lado_hijo = "1..N"
        else:
            lado_hijo = "0..N"
        relaciones.append((t, col, padre, lado_padre, lado_hijo))

FLECHA = {"1": "ERmandOne", "0..1": "ERzeroToOne", "1..N": "ERoneToMany", "0..N": "ERzeroToMany"}

# ---------- 3. Hojas (columnas; "*" = tabla de referencia de otro módulo) ----------
HOJAS = [
 ("seguridad", "1 · Seguridad", [["tbroles", "tbpermisos"], ["tbusuarios", "tbrolespermisos"], ["tbsesiones"], ["tbrefreshtokens"]]),
 ("servicio", "2 · Clientes y servicio técnico",
  [["tbtiposidentificacion", "tbtarifas*"], ["tbclientes", "tbtiposequipo", "tbmarcas*"], ["tbequipos", "tbusuarios*", "tbarchivos*"],
   ["tbordenesreparacion", "tbestadosorden"], ["tbhistorialestadosorden", "tbordenesarchivos"]]),
 ("tbproductos", "3 · Productos, inventario y compras",
  [["tbcategoriasproducto", "tbmarcas", "tbtiposiva", "tbtiposidentificacion*"],
   ["tbproductos", "tbtarifas", "tbarchivos*", "tbproveedores", "tbusuarios*"],
   ["tbpreciosproducto", "tbproductosarchivos", "tbcompras", "tbfacturas*"], ["tbdetallecompra", "tbmovimientosinventario"]]),
 ("ventas", "4 · Ventas y caja",
  [["tbclientes*", "tbordenesreparacion*", "tbarchivos*", "tbusuarios*"], ["tbproformas", "tbsesionescaja", "tbmetodospago", "tbproductos*"],
   ["tbfacturas", "tbdetalleproforma", "tbtarifas*", "tbcompras*"], ["tbdetallefactura", "tbmovimientoscaja"]]),
 ("tbarchivos", "5 · Archivos, correo y configuración",
  [["tbusuarios*"], ["tbarchivos", "tbfacturas*", "tbordenesreparacion*", "tbtiposiva*"], ["tbenvioscorreo", "tbconfiguracion"]]),
]
# Hoja completa: las 35 tablas, en columnas por dependencia (los padres siempre a la izquierda)
HOJA_COMPLETA = ("completo", "0 · Diagrama completo", [
  ["tbroles", "tbpermisos", "tbtiposidentificacion", "tbtarifas", "tbtiposequipo", "tbmarcas", "tbcategoriasproducto", "tbtiposiva", "tbmetodospago", "tbestadosorden"],
  ["tbusuarios", "tbrolespermisos", "tbclientes", "tbproveedores", "tbproductos"],
  ["tbsesiones", "tbarchivos", "tbequipos", "tbcompras", "tbpreciosproducto", "tbsesionescaja"],
  ["tbrefreshtokens", "tbconfiguracion", "tbordenesreparacion", "tbproformas", "tbproductosarchivos", "tbdetallecompra"],
  ["tbhistorialestadosorden", "tbordenesarchivos", "tbfacturas", "tbdetalleproforma"],
  ["tbenvioscorreo", "tbdetallefactura", "tbmovimientoscaja", "tbmovimientosinventario"],
])
assert sorted(t for c in HOJA_COMPLETA[2] for t in c) == sorted(tablas)
completas = [t for _, _, cols in HOJAS for c in cols for t in c if not t.endswith("*")]
assert sorted(completas) == sorted(tablas), set(tablas) ^ set(completas)

T = "shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
R = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom={b};html=1;"
C = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;whiteSpace=wrap;html=1;fontSize=11;"
E = "edgeStyle=orthogonalEdgeStyle;rounded=1;arcSize=10;fontSize=11;html=1;endFill=0;startFill=0;jumpStyle=arc;jumpSize=8;"
L = "edgeLabel;html=1;fontSize=11;fontStyle=1;labelBackgroundColor=#ffffff;resizable=0;"
W = [50, 190, 125, 45]; TW = sum(W); H = 26; GY = 50; PASO = 14; MARGEN = 40

def filas_de(t, ref):
    return [f for f in tablas[t] if "PK" in f[0]][:1] if ref else tablas[t]

def tabla_xml(pfx, nombre, filas, x, y, ref, hpk):
    st = T + ("dashed=1;" if ref else "")
    alt = [hpk] + [H] * (len(filas) - 1)
    o = [f'<mxCell id="{pfx}{nombre}" value={q(nombre)} style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{TW}" height="{30 + sum(alt)}" as="geometry"/></mxCell>']
    yy = 30; centros = {}
    for i, (clave, col, tipo, nulo) in enumerate(filas):
        rid = f"{pfx}{nombre}.{col}"; h = alt[i]
        o.append(f'<mxCell id="{rid}" value="" style="{R.format(b=1 if i == 0 else 0)}" vertex="1" parent="{pfx}{nombre}"><mxGeometry y="{yy}" width="{TW}" height="{h}" as="geometry"/></mxCell>')
        xx = 0
        for j, (v, w) in enumerate(zip((clave, col, tipo, nulo), W)):
            s = C + ("fontStyle=1;align=center;" if j == 0 else "align=left;spacingLeft=6;" + ("fontStyle=5;" if "PK" in clave and j == 1 else "") + ("fontColor=#666666;" if j >= 2 else ""))
            o.append(f'<mxCell id="{rid}.{j}" value={q(v)} style="{s}" vertex="1" parent="{rid}"><mxGeometry x="{xx}" width="{w}" height="{h}" as="geometry"><mxRectangle width="{w}" height="{h}" as="alternateBounds"/></mxGeometry></mxCell>')
            xx += w
        centros[col] = (y + yy, h)
        yy += h
    return o, 30 + sum(alt), centros

def hoja(pid, cols, fino=False):
    # fino=True (todas las hojas): más separación entre salidas, holgura junto a las tablas y etiquetas encima de la línea
    sep, holg = (28, 70) if fino else (18, 30)
    pfx = pid + "."
    col_de, es_ref = {}, {}
    for ci, c in enumerate(cols):
        for t in c:
            n = t.rstrip("*"); col_de[n] = ci; es_ref[n] = t.endswith("*")
    rels = [r for r in relaciones if r[0] in col_de and not es_ref[r[0]] and r[2] in col_de]
    faltan = {r[2] for r in relaciones if r[0] in col_de and not es_ref[r[0]] and r[2] not in col_de}
    assert not faltan, (pid, faltan)
    # uso de huecos entre columnas (hueco g = a la derecha de la columna g)
    uso = {g: [] for g in range(len(cols))}
    largas = []
    for r in rels:
        hijo, col, padre = r[0], r[1], r[2]
        i, j = col_de[padre], col_de[hijo]
        assert i <= j, (pid, padre, hijo)
        if hijo == padre or i == j:
            uso[i].append(r)
        else:
            uso[i].append(r)
            if j > i + 1:
                uso[j - 1].append(r); largas.append(r)
    carriles = len(largas)
    y0 = MARGEN + carriles * PASO + (20 if carriles else 0)
    # posiciones
    xcol, x = [], MARGEN
    for g in range(len(cols)):
        xcol.append(x); x += TW + 2 * holg + PASO * len(uso[g])
    salidas = {}
    for r in rels:
        salidas.setdefault(r[2], []).append(r)
    geo = {}; o = []; salida_y = {}
    for ci, c in enumerate(cols):
        y = y0
        for t in c:
            n = t.rstrip("*"); f = filas_de(n, es_ref[n])
            k = len(salidas.get(n, []))
            hpk = max(H, sep * k + 8)
            xml, alto, centros = tabla_xml(pfx, n, f, xcol[ci], y, es_ref[n], hpk)
            o += xml
            geo[n] = (xcol[ci], y, {col: top + h / 2 for col, (top, h) in centros.items()})
            # punto de salida propio para cada relación que sale de la PK, ordenado por destino
            top, h = centros[pk_col(n)]
            for m, r in enumerate(sorted(salidas.get(n, []), key=lambda r: (col_de[r[0]], r[0], r[1]))):
                fy = (m + 1) / (k + 1)
                salida_y[id(r)] = (top + h * fy, fy)
            y += alto + GY
    # carriles verticales asignados dentro de cada hueco, ordenados por y de origen
    pos_hueco = {}
    for g, lista in uso.items():
        lista_ord = sorted(lista, key=lambda r: salida_y[id(r)][0])
        for k, r in enumerate(lista_ord):
            pos_hueco[(id(r), g)] = xcol[g] + TW + holg + PASO * k
    carril = {id(r): MARGEN + PASO * k for k, r in enumerate(sorted(largas, key=lambda r: (col_de[r[0]] - col_de[r[2]])))}
    n = 0
    for r in rels:
        hijo, col, padre, lp, lh = r
        n += 1; eid = f"{pfx}rel{n}"
        i, j = col_de[padre], col_de[hijo]
        ys, fy = salida_y[id(r)]; yd = geo[hijo][2][col]
        src = f"{pfx}{padre}.{pk_col(padre)}"; dst = f"{pfx}{hijo}.{col}"
        if i == j:  # misma columna o autorreferencia: sale y entra por la derecha
            gx = pos_hueco[(id(r), i)]; pts = [(gx, ys), (gx, yd)]; ent = "entryX=1;entryY=0.5;"
        elif j == i + 1:
            gx = pos_hueco[(id(r), i)]; pts = [(gx, ys), (gx, yd)]; ent = "entryX=0;entryY=0.5;"
        else:
            g1 = pos_hueco[(id(r), i)]; g2 = pos_hueco[(id(r), j - 1)]; cy = carril[id(r)]
            pts = [(g1, ys), (g1, cy), (g2, cy), (g2, yd)]; ent = "entryX=0;entryY=0.5;"
        p = "".join(f'<mxPoint x="{a}" y="{b}"/>' for a, b in pts)
        o.append(f'<mxCell id="{eid}" style="{E}exitX=1;exitY={fy:.4f};{ent}startArrow={FLECHA[lp]};endArrow={FLECHA[lh]};" edge="1" parent="1" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"><Array as="points">{p}</Array></mxGeometry></mxCell>')
        if fino:  # texto encima de la línea, sin tapar el símbolo ni el borde de la tabla
            la = L + "align=left;verticalAlign=bottom;labelBackgroundColor=none;"
            lb = L + ("align=left;" if i == j else "align=right;") + "verticalAlign=bottom;labelBackgroundColor=none;"
            ax, ay, bx, by = 22, -3, (22 if i == j else -22), -3
        else:
            la = lb = L; ax, ay, by = 16, -7, -9; bx = 14 if i == j else -16
        o.append(f'<mxCell id="{eid}.a" value="{lp}" style="{la}" vertex="1" connectable="0" parent="{eid}"><mxGeometry x="-1" relative="1" as="geometry"><mxPoint x="{ax}" y="{ay}" as="offset"/></mxGeometry></mxCell>')
        o.append(f'<mxCell id="{eid}.b" value="{lh}" style="{lb}" vertex="1" connectable="0" parent="{eid}"><mxGeometry x="1" relative="1" as="geometry"><mxPoint x="{bx}" y="{by}" as="offset"/></mxGeometry></mxCell>')
    refs = [t for t in es_ref if es_ref[t]]
    return "".join(o), refs, n

def pk_col(t):
    return [f for f in tablas[t] if "PK" in f[0]][0][1]

out = '<mxfile host="Claude Code">\n'
for pid, nombre, cols in [HOJA_COMPLETA] + HOJAS:
    cuerpo, refs, n = hoja(pid, cols, fino=True)
    print(f"{nombre}: {sum(1 for c in cols for t in c if not t.endswith('*'))} tablas, referencias: {', '.join(refs) or '-'}; {n} relaciones", file=sys.stderr)
    out += f'  <diagram id="{pid}" name={q(nombre)}>\n    <mxGraphModel grid="1" gridSize="10" guides="1" connect="1" arrows="1" page="0" adaptiveColors="auto">\n      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        ' + cuerpo + '\n      </root>\n    </mxGraphModel>\n  </diagram>\n'
out += "</mxfile>\n"
open(sys.argv[2], "w", encoding="utf8").write(out)
