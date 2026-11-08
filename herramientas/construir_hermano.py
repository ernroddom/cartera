# Construye la app de fondos del hermano en web/hermano/ a partir de fuente/cartera.html (la del usuario).
#   python3 herramientas/construir_hermano.py
# No hay una segunda copia del programa: se parte de cartera.html y se le aplican estos cambios al construir, así que las
# mejoras de la app del usuario le llegan también a esta. Si un cambio deja de encajar (porque cartera.html ha cambiado),
# el script se para y dice cuál.
# Lo que cambia respecto a la del usuario:
#  1. Tres pestañas: Cartera (el Resumen), Aportaciones y Compras (las dos, de Movimientos). Sin cuadre ni avisos de la hoja.
#  2. Lee el formato de su hoja: fondos por ISIN, «Participaciones», Cartera sin títulos Empresa/Ticker, «Var. %», «Rent.»…,
#     Valor Mensual con «Invertido» y sin MSCI World. Solo lee sus pestañas (no las ocultas que vienen de la plantilla).
#  3. Habla de fondos y participaciones.
#  4. Guarda su ID, su clave y su copia de datos con otros nombres: en un mismo móvil no se mezcla con la app del usuario.
import os, re, subprocess, sys, tempfile
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NOMBRE = "Cartera de Inversión"
t = open(os.path.join(R, "fuente", "cartera.html"), encoding="utf-8").read()

def cambia(viejo, nuevo, todas=False, regex=False):
    global t
    n = len(re.findall(viejo, t)) if regex else t.count(viejo)
    if n == 0 or (n > 1 and not todas):
        sys.exit(f"construir_hermano: no encaja ({n} coincidencias): {viejo[:90]!r}")
    t = re.sub(viejo, nuevo, t) if regex else t.replace(viejo, nuevo)

# --- 1. título y menú: tres pestañas
cambia("<title>Cartera</title>", f"<title>{NOMBRE}</title>")
nav = re.search(r'<nav class="nav" id="nav" aria-label="Secciones">(.*?)</nav>', t, re.S).group(1)
a = dict(re.findall(r'(<a href="#[a-z]+" data-v="([a-z]+)">.*?</a>)', nav, re.S)[i][::-1] for i in range(5))
icono = lambda v: re.search(r"<svg.*?</svg>", a[v], re.S).group(0)
nuevo_nav = (f'<a href="#resumen" data-v="resumen">{icono("resumen")}<span>Cartera</span></a>'
             f'<a href="#aportaciones" data-v="aportaciones">{icono("analisis")}<span>Aportaciones</span></a>'
             f'<a href="#transacciones" data-v="transacciones">{icono("movimientos")}<span>Compras</span></a>')
cambia(nav, nuevo_nav)
# la pestaña marcada: en Movimientos, la sub-pestaña que se ve (Aportaciones o Compras)
cambia('document.querySelectorAll("#nav a").forEach(a=>a.setAttribute("aria-current",a.dataset.v===view?"page":"false"));',
       'document.querySelectorAll("#nav a").forEach(a=>a.setAttribute("aria-current",(view==="movimientos"?a.dataset.v===mtab:a.dataset.v===view)?"page":"false"));')
# fuera de estas tres, se abre la Cartera
cambia('const v = sub ? "movimientos" : (["resumen","analisis","movimientos","preseleccion","actualidad"].includes(token)?token:"resumen");',
       'if(sub&&!["aportaciones","transacciones"].includes(token)) token="aportaciones";\n  const v = Object.keys(MOV).includes(token) ? "movimientos" : "resumen";')
cambia('const sub=Object.keys(MOV).includes(token);', 'const sub=Object.keys(MOV).includes(token)||token==="movimientos"; if(token==="movimientos") token="aportaciones";')

# --- 2. su hoja: solo sus pestañas, y sus títulos como los de la hoja original
cambia('const SHEETS=["Dashboard","Cartera","Preselección","Valoración","Transacciones","Dividendos","Aportaciones","Ajustes","Trayectoria","Valor Mensual","Referencias"];',
       'const SHEETS=["Dashboard","Cartera","Transacciones","Aportaciones","Ajustes","Valor Mensual"];')
cambia('''  const D = grid(wb,"Dashboard"), C = grid(wb,"Cartera"), V = grid(wb,"Valor Mensual"),
        T = grid(wb,"Trayectoria"), P = grid(wb,"Preselección"), TX = grid(wb,"Transacciones");''',
'''  // títulos de su hoja con el nombre que espera la web (solo en las 12 primeras filas, donde están los títulos)
  const ren=(g,m)=>{ for(let r=0;r<Math.min(g.length,12);r++) (g[r]||[]).forEach((v,c)=>{ if(typeof v==="string"&&m[v.trim()]) g[r][c]=m[v.trim()]; }); return g; };
  const D = ren(grid(wb,"Dashboard"),{"Variación hoy":"Hoy"}), V = ren(grid(wb,"Valor Mensual"),{"Invertido":"Aportaciones"}),
        T = [], P = [], TX = ren(grid(wb,"Transacciones"),{"Participaciones":"Acciones"});
  const C = ren(grid(wb,"Cartera"),{"Var. %":"Hoy","Rent.":"Revaloriz.","Rent. Tot.":"Total","Abs. Tot.":"Total €","IRR Tot.":"TIR"});
  // Cartera sin títulos encima del ISIN y del nombre: se ponen al ver la primera fila
  { const [h]=headerRow(C,["Precio","Valor","Acc.","Invertido"]); if(h>=0){ const row=C[h+1]||[], tc=row.findIndex(v=>typeof v==="string"&&/^[A-Z]{2}[A-Z0-9]{9}\\d$/.test(v.trim()));
      if(tc>=0){ C[h][tc]="Ticker"; if(C[h][tc+1]==null||C[h][tc+1]==="") C[h][tc+1]="Empresa"; } } }''')
# valoración de empresas: no tiene
cambia('const VAL = parseVal(grid(wb,"Valoración"));', 'const VAL = {};')
# evolución: sin columna MSCI World, la tabla Fecha · Valor Cartera · Aportaciones más a la derecha (llega hasta hoy)
cambia('''        out.evo.push({d, v, a:celda(V,r,ac), i:celda(V,r,p[1])}); } } }''',
'''        out.evo.push({d, v, a:celda(V,r,ac), i:celda(V,r,p[1])}); } }
    else { const [h,m]=headerRow(V,["Fecha","Valor Cartera","Aportaciones"]); if(h>=0){ const fc=m["Fecha"][m["Fecha"].length-1], vc=m["Valor Cartera"].find(c=>c>fc), ac=m["Aportaciones"].find(c=>c>fc);
      for(let r=h+1;r<V.length;r++){ const d=celda(V,r,fc); if(!(d instanceof Date)) break; const v=celda(V,r,vc); if(!isNum(v)) break; out.evo.push({d, v, a:celda(V,r,ac), i:null}); } } } }''')
# aportaciones del Dashboard en positivo
cambia('    aport:rightNum(D,"Aportaciones") };', '    aport:(v=>isNum(v)&&v<0?-v:v)(rightNum(D,"Aportaciones")) };')

# evolución: su «Valor Cartera» es solo lo que valen los fondos y su «Invertido», lo invertido en ellos (sin la liquidez)
cambia('return [...e.slice(0,-1),{...L,v:k.value+(k.liquidez||0),a:isNum(k.aport)?k.aport:L.a}]; }', 'return [...e.slice(0,-1),{...L,v:k.value}]; }')
cambia('{label:"Aportado",data:rows.map', '{label:"Invertido",data:rows.map')
cambia('<i class="dash"></i>Aportado</span>', '<i class="dash"></i>Invertido</span>')

# --- 3. fondos y participaciones
# en el mapa, las iniciales del fondo en vez del principio del ISIN
cambia('const short=String(p.ticker).split(":").pop().split(" ")[0], lvl=',
       'const short=/^[A-Z]{2}[A-Z0-9]{9}\\d$/.test(String(p.ticker))?String(p.name||"").split(/\\s+/).filter(w=>/^[A-Za-zÁÉÍÓÚÑ]/.test(w)).map(w=>w[0]).join("").toUpperCase():String(p.ticker).split(":").pop().split(" ")[0], lvl=')
cambia('?"acción":"acciones"', '?"participación":"participaciones"', todas=True)
cambia('${shares(p.shares)} acciones`', '${shares(p.shares)} participaciones`')
cambia('class="thb">Empresa</button>', 'class="thb">Fondo</button>', todas=True)
cambia('l:"Empresa"', 'l:"Fondo"', todas=True)
cambia('data-l="Empresa"', 'data-l="Fondo"', todas=True)
cambia('"empresa":"empresas"', '"fondo":"fondos"', todas=True)
cambia('class="thb">Acciones</button>', 'class="thb">Particip.</button>')
cambia('data-l="Acciones"', 'data-l="Participaciones"', todas=True)
cambia('l:"Acciones"', 'l:"Participaciones"', todas=True)

# --- 4. su ID, su clave y su copia de datos, aparte de los del usuario
cambia('"cartera-', '"fondos-', todas=True)
cambia('indexedDB.open("cartera"', 'indexedDB.open("fondos"')
cambia('indexedDB.deleteDatabase("cartera")', 'indexedDB.deleteDatabase("fondos")')

# --- 5. lo que no usa: cuadre con la hoja, avisos de la hoja, sub-pestañas de Movimientos, MSCI World, buscador
css = """
/* app del hermano: solo Cartera, Aportaciones y Compras */
#s-check,#chk-show,#hoja-al,#mtabs,#kbtn,.hm5-mv{display:none!important}
body.hm3on #v-movimientos>#s-mov{margin-top:max(env(safe-area-inset-top,0px),10px)}
.evo-leg span:nth-child(3){display:none}
"""
cambia('\n</style>\n\n<div class="wrap">', css + '</style>\n\n<div class="wrap">')

with tempfile.TemporaryDirectory() as d:
    html = os.path.join(d, "cartera.html"); open(html, "w", encoding="utf-8").write(t)
    env = dict(os.environ, HTML=html, SALIDA=os.path.join(R, "web", "hermano"), NOMBRE_APP=NOMBRE)
    subprocess.run([sys.executable, os.path.join(R, "herramientas", "construir.py")], env=env, check=True)
