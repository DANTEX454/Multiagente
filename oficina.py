"""Oficina virtual animada: el gerente recibe el documento y se lo lleva al empleado del área."""
from html import escape

AREAS = {
    "contabilidad": {"nombre": "Contabilidad", "x": 130, "color": "#4F8EF7", "pelo": "#3b2a20"},
    "proyectos":    {"nombre": "Proyectos",    "x": 340, "color": "#43B581", "pelo": "#1f1f1f"},
    "diagnostico":  {"nombre": "Diagnóstico",  "x": 560, "color": "#F5A623", "pelo": "#7a4b21"},
    "proyecciones": {"nombre": "Proyecciones", "x": 770, "color": "#9B6BDE", "pelo": "#c4572f"},
}
GER_X, GER_Y = 450, 95
EMP_Y = 255


def _burbuja(x, y, texto, puntos=False):
    ancho = max(70, int(len(texto) * 6.4) + 26)
    t = escape(texto)
    dots = ""
    if puntos:
        dots = "".join(f'<circle class="dot" style="animation-delay:{i*0.2}s" cx="{ancho/2-12+i*12}" cy="12" r="3.2" fill="#555"/>' for i in range(3))
        t = ""
    return (f'<g transform="translate({x-ancho/2},{y})"><rect width="{ancho}" height="24" rx="12" fill="#fff" stroke="#c9c2b6"/>'
            f'<path d="M{ancho/2-6},24 l6,8 l6,-8 z" fill="#fff" stroke="#c9c2b6"/><rect x="{ancho/2-8}" y="22" width="16" height="3" fill="#fff"/>'
            f'<text x="{ancho/2}" y="16" text-anchor="middle" font-size="11" fill="#333">{t}</text>{dots}</g>')


def _persona(x, y, color, pelo, nombre, estado, bubble=""):
    """estado: idle | working | done"""
    brillo = "#8fd3ff" if estado == "working" else "#90a4ae"
    extra = ""
    if estado == "done":
        extra = (f'<g transform="translate(26,-52)"><circle r="11" fill="#2e9e5b"/>'
                 f'<path d="M-5,0 l4,4 l7,-8" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return f'''
<g transform="translate({x},{y})" class="{estado}">
  <ellipse cx="0" cy="70" rx="62" ry="8" fill="#000" opacity=".08"/>
  <g class="body"><rect x="-22" y="0" width="44" height="46" rx="14" fill="{color}"/>
    <g class="head"><circle cx="0" cy="-18" r="18" fill="#f2c9a0"/>
      <path d="M-18,-21 a18,18 0 0 1 36,0 q-18,-9 -36,0z" fill="{pelo}"/>
      <circle cx="-6" cy="-17" r="2" fill="#222"/><circle cx="6" cy="-17" r="2" fill="#222"/>
      <path d="M-5,-9 q5,4 10,0" stroke="#a0574a" stroke-width="1.6" fill="none" stroke-linecap="round"/></g>
    <rect class="arm armL" x="-31" y="14" width="10" height="26" rx="5" fill="{color}"/>
    <rect class="arm armR" x="21" y="14" width="10" height="26" rx="5" fill="{color}"/></g>
  <rect x="-58" y="38" width="116" height="16" rx="5" fill="#a67c52"/><rect x="-52" y="54" width="8" height="16" fill="#8b6540"/><rect x="44" y="54" width="8" height="16" fill="#8b6540"/>
  <rect x="-24" y="18" width="48" height="22" rx="3" fill="#cfd8dc"/><rect x="-20" y="21" width="40" height="15" rx="2" fill="{brillo}" class="pantalla"/>
  <text x="0" y="90" text-anchor="middle" font-size="13" font-weight="600" fill="#3a3a3a">{escape(nombre)}</text>
  {extra}
</g>{_burbuja(x, y - 62, bubble, puntos=(estado == "working" and not bubble)) if (bubble or estado == "working") else ""}'''


def _papel(x, y, extra_class=""):
    return (f'<g class="papel {extra_class}" transform="translate({x},{y})"><rect width="26" height="32" rx="3" fill="#fff" stroke="#9aa4b0"/>'
            '<rect x="5" y="7" width="16" height="2.5" fill="#b8c2cc"/><rect x="5" y="13" width="16" height="2.5" fill="#b8c2cc"/><rect x="5" y="19" width="10" height="2.5" fill="#b8c2cc"/></g>')


def html_oficina(estado="espera", area=None, mensaje=""):
    """estado: espera | gerente | area | listo"""
    partes = []
    g_estado = "working" if estado == "gerente" else "idle"
    g_burbuja = {"gerente": mensaje or "Revisando el documento…",
                 "area": "Enviado a " + (AREAS[area]["nombre"] if area else ""),
                 "listo": "¡Trabajo terminado!", "espera": "Sube un documento"}.get(estado, "")
    partes.append(_persona(GER_X, GER_Y, "#34495e", "#222", "Gerente", g_estado, g_burbuja))

    vuelo = ""
    for clave, a in AREAS.items():
        est, burb = "idle", ""
        if clave == area and estado == "area":
            est, burb = "working", mensaje
        elif clave == area and estado == "listo":
            est, burb = "done", mensaje or "¡Listo!"
        partes.append(_persona(a["x"], EMP_Y, a["color"], a["pelo"], a["nombre"], est, burb))
        if clave == area and estado == "area":
            tx, ty = a["x"] - 13, EMP_Y + 6
            vuelo = (f"@keyframes vuelo{{0%{{transform:translate({GER_X-13}px,{GER_Y+10}px) rotate(-8deg)}}"
                     f"45%{{transform:translate({(GER_X+tx)/2}px,{GER_Y+55}px) rotate(10deg)}}"
                     f"100%{{transform:translate({tx}px,{ty}px) rotate(0)}}}}")

    if estado == "gerente":
        partes.append(_papel(GER_X - 13, GER_Y + 10, "lee"))
    elif estado == "area" and area:
        partes.append(_papel(0, 0, "vuela"))

    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:transparent}}
svg{{width:100%;height:auto;display:block;border-radius:16px}}
.arm{{transform-box:fill-box;transform-origin:center}}
.working .armL{{animation:tip .3s infinite alternate ease-in-out}}
.working .armR{{animation:tip .3s .15s infinite alternate ease-in-out}}
.working .head{{animation:bob .5s infinite alternate ease-in-out}}
.idle .body{{animation:resp 3.2s infinite ease-in-out}}
.working .pantalla{{animation:pulso .7s infinite alternate}}
.dot{{animation:salto .9s infinite ease-in-out}}
.papel.lee{{animation:bob .8s infinite alternate}}
.papel.vuela{{animation:vuelo 1.3s ease-in-out forwards}}
@keyframes tip{{to{{transform:translateY(-6px)}}}}
@keyframes bob{{to{{transform:translateY(-2px)}}}}
@keyframes resp{{50%{{transform:translateY(-1.5px)}}}}
@keyframes pulso{{to{{fill:#d7f1ff}}}}
@keyframes salto{{0%,100%{{transform:translateY(0)}}40%{{transform:translateY(-4px)}}}}
{vuelo}
</style></head><body>
<svg viewBox="0 0 900 360" xmlns="http://www.w3.org/2000/svg">
<rect width="900" height="360" fill="#e8eef6"/><rect y="215" width="900" height="145" fill="#efe6d6"/>
<rect x="60" y="25" width="120" height="60" rx="6" fill="#cfe3f5" stroke="#b5cde4"/><line x1="120" y1="25" x2="120" y2="85" stroke="#b5cde4"/>
<rect x="720" y="25" width="120" height="60" rx="6" fill="#cfe3f5" stroke="#b5cde4"/><line x1="780" y1="25" x2="780" y2="85" stroke="#b5cde4"/>
{''.join(partes)}
</svg></body></html>'''
