# Construye la app de fondos del hermano en web/hermano/ a partir de fuente/cartera.html (la del usuario).
#   python3 herramientas/construir_hermano.py
# No hay una segunda copia del programa: se parte de cartera.html y se le aplican estos cambios al construir, así que las
# mejoras de la app del usuario le llegan también a esta. Si un cambio deja de encajar (porque cartera.html ha cambiado),
# el script se para y dice cuál.
# Lo que cambia respecto a la del usuario:
#  1. Cuatro pestañas: Cartera (el Resumen, sin la columna de rentabilidad por dividendo), Aportaciones y Compras (las dos,
#     de Movimientos) e Índices (la pestaña «Índices» de su hoja: un bloque Fecha | precio por índice o fondo, con gráfica
#     de 1 año, 5 años o todo). Sin cuadre ni avisos de la hoja.
#  2. Lee el formato de su hoja: fondos por ISIN, «Participaciones»/«Part.», Cartera sin títulos Empresa/Ticker, «Var. %», «Rent.»…,
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
             f'<a href="#transacciones" data-v="transacciones">{icono("movimientos")}<span>Compras</span></a>'
             f'<a href="#indices" data-v="indices">{icono("preseleccion")}<span>Índices</span></a>')
cambia(nav, nuevo_nav)
# la pestaña marcada: en Movimientos, la sub-pestaña que se ve (Aportaciones o Compras)
cambia('document.querySelectorAll("#nav a").forEach(a=>a.setAttribute("aria-current",a.dataset.v===view?"page":"false"));',
       'document.querySelectorAll("#nav a").forEach(a=>a.setAttribute("aria-current",(view==="movimientos"?a.dataset.v===mtab:a.dataset.v===view)?"page":"false"));')
# fuera de estas cuatro, se abre la Cartera
cambia('const v = sub ? "movimientos" : (["resumen","analisis","movimientos","preseleccion","actualidad"].includes(token)?token:"resumen");',
       'if(sub&&!["aportaciones","transacciones"].includes(token)) token="aportaciones";\n  const v = token==="indices" ? "indices" : Object.keys(MOV).includes(token) ? "movimientos" : "resumen";')
cambia('const sub=Object.keys(MOV).includes(token);', 'const sub=Object.keys(MOV).includes(token)||token==="movimientos"; if(token==="movimientos") token="aportaciones";')

# --- 2. su hoja: solo sus pestañas, y sus títulos como los de la hoja original
cambia('const SHEETS=["Dashboard","Cartera","Preselección","Valoración","Transacciones","Dividendos","Aportaciones","Ajustes","Trayectoria","Valor Mensual","Referencias"];',
       'const SHEETS=["Dashboard","Cartera","Transacciones","Aportaciones","Ajustes","Valor Mensual","Índices"];')
cambia('''  const D = grid(wb,"Dashboard"), C = grid(wb,"Cartera"), V = grid(wb,"Valor Mensual"),
        T = grid(wb,"Trayectoria"), P = grid(wb,"Preselección"), TX = grid(wb,"Transacciones");''',
'''  // títulos de su hoja con el nombre que espera la web (solo en las 12 primeras filas, donde están los títulos)
  const ren=(g,m)=>{ for(let r=0;r<Math.min(g.length,12);r++) (g[r]||[]).forEach((v,c)=>{ if(typeof v==="string"&&m[v.trim()]) g[r][c]=m[v.trim()]; }); return g; };
  const D = ren(grid(wb,"Dashboard"),{"Variación hoy":"Hoy"}), V = ren(grid(wb,"Valor Mensual"),{"Invertido":"Aportaciones"}),
        T = [], P = [], TX = ren(grid(wb,"Transacciones"),{"Participaciones":"Acciones"});
  const C = ren(grid(wb,"Cartera"),{"Var. %":"Hoy","Part.":"Acc.","Rent.":"Revaloriz.","Rent. Tot.":"Total","Abs. Tot.":"Total €","IRR Tot.":"TIR"});
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
# Índices: bloques «Fecha | nombre» uno al lado de otro; encima, una nota (de dónde sale el precio)
cambia('  out.evo = [];', '''  out.idx = []; { const G=grid(wb,"Índices"), [h]=headerRow(G,["Fecha"]);
    if(h>=0) (G[h]||[]).forEach((v,c)=>{ if(norm(v)!=="FECHA") return; const name=celda(G,h,c+1); if(typeof name!=="string"||!name.trim()) return;
      const pts=[]; for(let r=h+1;r<G.length;r++){ const d=celda(G,r,c), x=celda(G,r,c+1); if(!(d instanceof Date)) break; if(isNum(x)&&x>0) pts.push({d:new Date(d.getFullYear(),d.getMonth(),d.getDate()),v:x}); }
      let note=null; for(let r=h-1;r>=0&&!note;r--){ const s=celda(G,r,c); if(typeof s==="string"&&s.trim()&&!/^(\\S\\s+)+\\S$/.test(s.trim())) note=s.trim(); }
      if(pts.length) out.idx.push({name:name.trim(),pts,note}); }); }
  out.evo = [];''')
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
/* sin dividendos: fuera la columna de rentabilidad por dividendo */
#t-pos [data-k="yov"],#t-pos td[data-l="Rent. div."]{display:none!important}
/* Índices */
#ix-list{display:grid;gap:16px}
@media (min-width:1000px){#ix-list{grid-template-columns:1fr 1fr}}
#v-indices .ix-k{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:2px 0 12px}
#v-indices .ix-v{font-size:26px;font-weight:300;letter-spacing:-.01em}
#v-indices .ix-s{font-size:var(--fs-12);color:var(--ink2)}
#v-indices .ix-n{margin:10px 0 0;font-size:var(--fs-11);color:var(--ink3)}
#v-indices .chartbox{height:210px}
#v-indices .ix-0{margin:0;padding:24px 0;color:var(--ink3);font-size:var(--fs-13);text-align:center}
@media (max-width:700.98px){#v-indices .chart-head{flex-direction:column;align-items:flex-start;gap:10px}}
body.hm3on #v-indices>#ix-list{margin-top:max(env(safe-area-inset-top,0px),10px)}
body.hm3on #v-movimientos>#s-mov{margin-top:max(env(safe-area-inset-top,0px),10px)}
.evo-leg span:nth-child(3){display:none}
"""
cambia('\n</style>\n\n<div class="wrap">', css + '</style>\n\n<div class="wrap">')

cambia('  <!-- Universo -->', """  <!-- Índices (app del hermano) -->
  <div class="view" id="v-indices" hidden><div id="ix-list"></div></div>

  <!-- Universo -->""")
cambia('function drawAll(){ if(view==="resumen") drawEvo();', 'function drawAll(){ if(view==="indices") renderIdx(); if(view==="resumen") drawEvo();')
cambia('const VER="', """// Índices: una tarjeta por serie (precio, variación en el periodo y gráfica de 1 año, 5 años o todo)
const ixN={};
function renderIdx(){ const box=$("ix-list"); if(!box||!DATA) return; const S=DATA.idx||[];
  if(!S.length){ box.innerHTML=`<section class="panel"><p class="nada">Tu hoja aún no tiene la pestaña «Índices».</p></section>`; return; }
  box.innerHTML=S.map((s,i)=>{ const n=ixN[i]??12; return `<section class="panel ixp"><div class="chart-head"><div><h2 class="st">${esc(s.name)}</h2></div>
    <div class="seg" role="group" aria-label="Periodo" data-ix="${i}">${[[12,"1 año"],[60,"5 años"],[0,"Todo"]].map(([v,l])=>`<button type="button" data-n="${v}" aria-pressed="${v===n}">${l}</button>`).join("")}</div></div>
    <div class="ix-k"><b class="ix-v num" id="ix-v-${i}"></b><span class="ix-s num" id="ix-s-${i}"></span></div>
    <div class="chartbox"><canvas id="ix-c-${i}" role="img" aria-label="Evolución de ${esc(s.name)}"></canvas></div>${s.note?`<p class="ix-n">${esc(s.note)}</p>`:""}</section>`; }).join("");
  S.forEach((_,i)=>drawIdx(i)); }
function drawIdx(i){ const s=DATA.idx[i], n=ixN[i]??12, all=s.pts, L=all[all.length-1];
  if(all.length<2){ $("ix-v-"+i).textContent=nf(2).format(L.v)+"\\u00A0€"; $("ix-s-"+i).textContent=fechaCorta(L.d);
    const cb=$("ix-c-"+i).parentElement; cb.outerHTML=`<p class="nada ix-0">La gráfica se irá completando cada día con el precio del fondo.</p>`; return; }
  let rows=all; if(n){ const st=new Date(L.d); st.setMonth(st.getMonth()-n); const r=all.filter(p=>p.d>=st); if(r.length>=2) rows=r; }
  const F=rows[0], ch=F.v?L.v/F.v-1:null, cubre=n&&+F.d<=+new Date(new Date(L.d).setMonth(new Date(L.d).getMonth()-n))+864e5*10;
  const per=n&&cubre?(n===12?"en 1 año":"en 5 años"):`desde ${fechaCorta(F.d)}`;
  $("ix-v-"+i).textContent=nf(2).format(L.v)+"\u00A0€"; $("ix-s-"+i).innerHTML=`<span class="${cls(ch)}">${pct(ch,1,true)}</span> ${per} · ${fechaCorta(L.d)}`;
  const a=+F.d, b=+L.d, corto=(b-a)<4e10, o=baseOpts();
  o.scales.y.ticks.callback=v=>nf(v<20?2:0).format(v); o.scales.y.ticks.maxTicksLimit=4;
  Object.assign(o.scales.x,{type:"linear",min:a,max:b,afterBuildTicks:sc=>{ const t=[], m=innerWidth<=MOVIL;
    if(corto){ const d=new Date(new Date(a).getFullYear(),new Date(a).getMonth()+1,1), st=(b-a)>2e10?(m?4:3):(m?2:1); for(;+d<=b;d.setMonth(d.getMonth()+st)) t.push({value:+d}); }
    else { const y=(b-a)/3.156e10, st=y>(m?8:14)?(m?5:4):y>(m?4:7)?2:1; for(let k=new Date(a).getFullYear()+1;+new Date(k,0,1)<=b;k+=st) t.push({value:+new Date(k,0,1)}); }
    sc.ticks=t; }});
  o.scales.x.ticks.callback=v=>{ const d=new Date(v); return corto?MES[d.getMonth()].toLowerCase()+(d.getMonth()===0?" "+d.getFullYear():""):String(d.getFullYear()); };
  o.plugins.tooltip.callbacks={title:it=>fechaCorta(new Date(it[0].parsed.x)),label:c=>" "+nf(2).format(c.parsed.y)+"\u00A0€"};
  const up=!(ch<0), col=varCss(up?"--pos-deep":"--neg");
  make("ix-c-"+i,{type:"line",data:{datasets:[{label:s.name,data:rows.map(p=>({x:+p.d,y:p.v})),borderColor:col,borderWidth:2,
    pointRadius:rows.map((_,k)=>k===rows.length-1?3.5:0),pointBackgroundColor:col,pointHoverRadius:4,tension:.25,
    fill:{target:"start"},backgroundColor:hexTok(up?"--pos":"--neg")+"1F"}]},options:o,plugins:[crosshair]}); }
document.addEventListener("click",e=>{ const b=e.target.closest("#ix-list .seg button"); if(!b) return; const g=b.parentElement, i=+g.dataset.ix;
  ixN[i]=+b.dataset.n; g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",String(x===b))); drawIdx(i); });
const VER=\"""")

with tempfile.TemporaryDirectory() as d:
    html = os.path.join(d, "cartera.html"); open(html, "w", encoding="utf-8").write(t)
    env = dict(os.environ, HTML=html, SALIDA=os.path.join(R, "web", "hermano"), NOMBRE_APP=NOMBRE)
    subprocess.run([sys.executable, os.path.join(R, "herramientas", "construir.py")], env=env, check=True)
