# Crea plantilla/hoja-ejemplo.xlsx: una hoja de inversiones INVENTADA con exactamente la estructura que lee la web
# (pestañas, títulos de columna y etiquetas). Sirve para probar la web antes de conectarla a tu hoja y como referencia
# de qué espera encontrar cada parte. Uso:  python3 herramientas/crear_hoja_ejemplo.py
import datetime as dt, os
from openpyxl import Workbook
D=dt.datetime
HOY=D.now().replace(hour=0,minute=0,second=0,microsecond=0)
FX={"EUR":1.0,"USD":0.92}

# ---- datos inventados ----
# compras: (ticker, nombre, divisa, acciones, bróker, fecha, precio, comisión €)  · venta opcional (fecha, precio, comisión €)
COMPRAS=[
 ("NYSE:KO","Coca-Cola","USD",40,"Bróker A",D(2022,3,10),61.0,2.0,None),
 ("EPA:OR","L'Oréal","EUR",6,"Bróker A",D(2022,9,5),330.0,3.0,None),
 ("NASDAQ:MSFT","Microsoft","USD",8,"Bróker B",D(2023,2,14),262.0,2.0,None),
 ("BME:ITX","Inditex","EUR",60,"Bróker A",D(2023,6,1),33.0,4.0,None),
 ("AMS:ASML","ASML","EUR",3,"Bróker B",D(2024,1,20),760.0,3.0,None),
 ("NYSE:KO","Coca-Cola","USD",20,"Bróker A",D(2024,8,12),69.0,2.0,None),
 ("NYSE:NKE","Nike","USD",15,"Bróker B",D(2022,5,3),118.0,2.0,(D(2024,3,18),101.0,2.0)),
]
PRECIO={"NYSE:KO":(70.5,0.006),"EPA:OR":(372.0,-0.011),"NASDAQ:MSFT":(415.0,0.014),"BME:ITX":(48.2,0.004),"AMS:ASML":(690.0,-0.021)}  # precio, cambio de hoy
APORTACIONES=[(D(2022,1,15),-4000,"Bróker A"),(D(2022,4,20),-2500,"Bróker B"),(D(2023,1,10),-2500,"Bróker A"),(D(2023,2,1),-2000,"Bróker B"),
              (D(2024,1,5),-2500,"Bróker B"),(D(2024,7,1),-1500,"Bróker A"),(D(2025,1,8),-500,"Bróker A"),(D(HOY.year,1,9),-500,"Bróker A"),(D(2025,6,2),300,"Bróker B")]
AJUSTES=[(D(2024,12,31),-12.4,"Bróker A","Ajuste de divisa"),(D(2025,12,31),0.35,"Bróker B","Intereses")]
def div_rows():
    out=[]
    for y in range(2022,HOY.year+2):
        for m,d in ((4,1),(7,1),(10,1),(12,15)):
            f=D(y,m,d)
            if f<D(2022,3,15): continue
            sh=40 if f<D(2024,8,15) else 60
            if f>HOY+dt.timedelta(days=365): continue
            g=round(sh*0.485*FX["USD"],2); out.append((f,"NYSE:KO","Coca-Cola","Bróker A","USD","Dividendo",sh,0.485,g,round(g*0.85,2)))
        f=D(y,5,5)
        if D(2023,1,1)<f<=HOY+dt.timedelta(days=365): g=round(6*6.6,2); out.append((f,"EPA:OR","L'Oréal","Bróker A","EUR","Dividendo",6,6.6,g,round(g*0.7,2)))
        for m in (5,11):
            f=D(y,m,2)
            if D(2023,7,1)<f<=HOY+dt.timedelta(days=365): g=round(60*0.77,2); out.append((f,"BME:ITX","Inditex","Bróker A","EUR","Dividendo",60,0.77,g,round(g*0.81,2)))
    return sorted(out)
DIVS=div_rows()
PRESEL=[ # ticker, nombre, divisa, precio, hoy, industria, país, valor razonable, TIR esperada, exigido
 ("NYSE:KO","Coca-Cola","USD",70.5,0.006,"Bebidas","USA",74.0,0.095,0.09),
 ("EPA:OR","L'Oréal","EUR",372.0,-0.011,"Cuidado personal","Francia",410.0,0.105,0.10),
 ("NASDAQ:MSFT","Microsoft","USD",415.0,0.014,"Software","USA",450.0,0.11,0.10),
 ("BME:ITX","Inditex","EUR",48.2,0.004,"Ropa","España",52.0,0.10,0.10),
 ("AMS:ASML","ASML","EUR",690.0,-0.021,"Semiconductores","Países Bajos",820.0,0.13,0.11),
 ("NYSE:V","Visa","USD",280.0,0.003,"Servicios de pago","USA",300.0,0.105,0.10),
 ("NASDAQ:COST","Costco","USD",880.0,-0.004,"Retail","USA",700.0,0.07,0.10),
 ("EPA:RMS","Hermès","EUR",2250.0,0.008,"Lujo","Francia",2100.0,0.085,0.10),
]
INDUSTRIA={t:i for t,_,_,_,_,i,_,_,_,_ in PRESEL}; PAIS={t:p for t,_,_,_,_,_,p,_,_,_ in PRESEL}

wb=Workbook(); wb.remove(wb.active)
def hoja(n): return wb.create_sheet(n)
def fila(ws,r,c,vals):
    for i,v in enumerate(vals): ws.cell(row=r+1,column=c+1+i,value=v)   # r y c empiezan en 0, como en la web

# ---- Transacciones ----
T=hoja("Transacciones"); fila(T,0,0,["Ticker","Nombre","Divisa","Acciones","Bróker","Fecha","Precio","Total","Comisión","Fecha","Precio","Total","Comisión","Benef. / Pérd.","Comentarios"])
abiertas={}; cerradas_pnl=0; com_abiertas=0; com_total=0
for i,(t,n,cur,sh,br,f,p,fee,venta) in enumerate(COMPRAS):
    total=round(sh*p*FX[cur]+fee,2); row=[t,n,cur,sh,br,f,p,total,fee]
    com_total+=fee
    if venta:
        vf,vp,vfee=venta; vt=round(sh*vp*FX[cur]-vfee,2); pnl=round(vt-total,2); cerradas_pnl+=pnl; com_total+=vfee
        row+=[vf,vp,vt,vfee,pnl,"Vendida (ejemplo)"]
    else:
        row+=[None,None,None,None,None,""]; a=abiertas.setdefault(t,{"n":n,"cur":cur,"sh":0,"inv":0,"cost":0,"fee":0,"lots":[]}); a["sh"]+=sh; a["inv"]+=total-fee; a["cost"]+=sh*p; a["fee"]+=fee; a["lots"].append((f,total)); com_abiertas+=fee
    fila(T,i+1,0,row)

# ---- Dividendos ----
V=hoja("Dividendos"); fila(V,0,0,["Fecha","Ticker","Nombre","Bróker","Divisa","Tipo","Acciones","Div/Acc","Div. EUR","Div. Broker"])
for i,r in enumerate(DIVS): fila(V,i+1,0,list(r))
cobrados=[r for r in DIVS if r[0]<=HOY]; brutos=sum(r[8] for r in cobrados); netos=sum(r[9] for r in cobrados)

# ---- Aportaciones y Ajustes ----
A=hoja("Aportaciones"); fila(A,0,0,["Fecha","Cantidad","Tipo","Bróker","Comentario"])
for i,(f,c,br) in enumerate(APORTACIONES): fila(A,i+1,0,[f,c,"Aportación" if c<0 else "Retirada",br,""])
J=hoja("Ajustes"); fila(J,0,0,["Fecha","Cantidad","Bróker","Comentario"])
for i,r in enumerate(AJUSTES): fila(J,i+1,0,list(r))

# ---- cálculos para que el Dashboard y Cartera cuadren con lo que recalcula la web ----
valor=0; filas_cartera=[]
for t,a in abiertas.items():
    p,hoy=PRECIO[t]; v=round(a["sh"]*p*FX[a["cur"]],2); valor+=v; filas_cartera.append((t,a,p,hoy,v))
aport=sum(-c for _,c,_ in APORTACIONES)
liq=aport-sum(round(sh*p*FX[cur]+fee,2) for t,n,cur,sh,br,f,p,fee,vt in COMPRAS)+sum(round(c[3]*c[8][1]*FX[c[2]]-c[8][2],2) for c in COMPRAS if c[8])+netos+sum(r[1] for r in AJUSTES)
ret=valor+liq-aport

# ---- Cartera ----
C=hoja("Cartera"); cab=["Empresa","Ticker","Hoy","Precio","Divisa","Acc.","Pr. Medio","Invertido","Valor","Peso","Revaloriz.","FX","Dividendo","Total","Total €","TIR","Años","Anual","YoV","YoC","Cobrado","Próximo"]
fila(C,1,1,cab)
for i,(t,a,p,hoy,v) in enumerate(sorted(filas_cartera,key=lambda x:-x[4])):
    cob=sum(r[8] for r in cobrados if r[1]==t); fut=[r for r in DIVS if r[1]==t and r[0]>HOY]; anual=sum(r[8] for r in fut)
    tot=v-a["inv"]+cob
    fila(C,2+i,1,[a["n"],t,hoy,p,a["cur"],a["sh"],round(a["cost"]/a["sh"],2),round(a["inv"],2),v,round(v/valor,4),round(v/a["inv"]-1,4),None,round(cob/a["inv"],4),round(tot/a["inv"],4),round(tot,2),None,None,round(anual,2),round(anual/v,4),round(anual/a["inv"],4),round(cob,2),fut[0][0] if fut else None])

# ---- Preselección (tu universo: cartera + candidatas) ----
P=hoja("Preselección"); fila(P,0,0,["Empresa","Ticker","Hoy","Precio","FX","Múltiplo","Fecha","Cotiz.","1S","1M","3M","6M","YTD","1A","3A","MM200","Volat.","Drawdown","Máx. 52s","Industria","País","Fair Value","Dist.","TIR esp.","Exigido"])
for i,(t,n,cur,p,hoy,ind,pais,fv,tir,ex) in enumerate(PRESEL):
    fila(P,i+1,0,[n,t,hoy,p,cur,22.0,D(HOY.year,HOY.month,1),"Abierto",0.012,0.03,0.05,0.08,0.10,0.15,0.35,p*0.95,0.22,-0.08,p*1.08,ind,pais,fv,round(p/fv-1,4),tir,ex])

# ---- Valor Mensual (evolución frente al MSCI World) ----
M=hoja("Valor Mensual"); fila(M,0,0,["Fecha","Valor Cartera","Aportaciones","MSCI World"])
f=D(2022,1,31); r=1; acum=0; v_=0; idx=0
while f<=HOY:
    acum=sum(-c for d,c,_ in APORTACIONES if d<=f); meses=(f.year-2022)*12+f.month
    v_=round(acum*(1+0.006*meses**0.9),2); idx=round(acum*(1+0.0065*meses**0.9),2)
    fila(M,r,0,[f,v_,acum,idx]); r+=1
    f=(f.replace(day=1)+dt.timedelta(days=32)).replace(day=1)+dt.timedelta(days=31); f=f.replace(day=1)-dt.timedelta(days=1)

# ---- Dashboard (la web recalcula casi todo; esto se usa sobre todo para el «Cuadre con tu hoja») ----
Dh=hoja("Dashboard")
def et(r,c,label,valor,sub=None):
    Dh.cell(row=r+1,column=c+1,value=label); Dh.cell(row=r+2,column=c+1,value=valor)
    if sub is not None: Dh.cell(row=r+4,column=c+1,value=sub)
prox=sum(r[8] for r in DIVS if r[0].year==HOY.year+1)
et(0,1,"Valor de cartera",round(valor,2),f"{len(filas_cartera)} posiciones"); et(0,3,"Retorno total",round(ret,2),"sobre lo aportado"); et(0,5,"Hoy",round(sum(v*h/(1+h) for _,_,_,h,v in filas_cartera),2))
et(0,7,"TIR anualizada",0.08); et(0,9,"Frente al MSCI World",-0.5); et(0,11,"Rentas próximo año",round(prox,2),"previstas")
fila(Dh,6,1,["Liquidez",round(liq,2)]); fila(Dh,6,4,["Aportaciones",round(aport,2)])
for i,(l,v) in enumerate([("Revalorización latente",round(sum(v for *_,v in filas_cartera)-sum(a["inv"] for a in abiertas.values()),2)),("Posiciones cerradas",round(cerradas_pnl,2)),("Dividendos brutos",round(brutos,2)),("Retenciones",round(netos-brutos,2)),("Comisiones de compra",round(-com_abiertas,2)),("Ajustes",round(sum(r[1] for r in AJUSTES),2))]):
    fila(Dh,9+i,1,[l,v])
for c,(l,v) in enumerate([("Operaciones",len(COMPRAS)+1),("Pos. cerradas",1),("Comisiones",com_total),("Comisión media",round(com_total/(len(COMPRAS)+1),2)),("Antigüedad media",2.1),(f"Aportaciones {HOY.year}",500)]):
    et(17,1+c,l,v)
for c,(l,v) in enumerate([(f"Total {HOY.year}",round(sum(r[8] for r in cobrados if r[0].year==HOY.year),2)),("CAGR 2023-"+str(HOY.year),0.12),(f"Previsto {HOY.year+1}",round(prox,2)),("Media mensual",round(prox/12,2)),("YoV",0.021),("YoC",0.026)]):
    et(21,1+c,l,v)
def lista(c,titulo,items):
    Dh.cell(row=26,column=c+1,value=titulo)
    for i,(n,v) in enumerate(items): Dh.cell(row=27+i,column=c+1,value=n); Dh.cell(row=27+i,column=c+2,value=v)
pesos={}
for t,a,p,h,v in filas_cartera: pesos.setdefault(INDUSTRIA[t],0); pesos[INDUSTRIA[t]]+=v/valor
lista(1,"I N D U S T R I A S",sorted(pesos.items(),key=lambda x:-x[1]))
pp={}
for t,a,p,h,v in filas_cartera: pp.setdefault(PAIS[t],0); pp[PAIS[t]]+=v/valor
lista(10,"P A Í S E S",sorted(pp.items(),key=lambda x:-x[1]))
dd={}
for t,a,p,h,v in filas_cartera: dd.setdefault(a["cur"],0); dd[a["cur"]]+=v/valor
lista(19,"D I V I S A S",sorted(dd.items(),key=lambda x:-x[1]))

# ---- Trayectoria (proyección a largo plazo; opcional) ----
Tr=hoja("Trayectoria"); fila(Tr,0,1,["H O R I Z O N T E   ·   I N D E P E N D E N C I A"])
fila(Tr,2,1,["Año","Edad","Aportación","Acumulado","Valor final","Dividendos","Neto mes","TIR"])
acc=aport; val=valor+liq
for i,y in enumerate(range(HOY.year,HOY.year+20)):
    acc+=3000; val=val*1.07+3000; dvd=val*0.025
    fila(Tr,3+i,1,[y,40+i,3000,round(acc),round(val),round(dvd),round(dvd*0.81/12),0.07])
for i,(l,v) in enumerate([("Año en curso",HOY.year),("Edad",40),("Patrimonio",round(valor+liq)),("Aportado",round(aport)),("Neto mensual",round(val*0.025*0.81/12)),("Ahorro anual",3000),("Crecimiento anual",0.07),("Rentabilidad por dividendo",0.025),("Dividendos apuntados hasta",HOY.year+1),("Sin reinvertir desde",0)]):
    fila(Tr,3+i,11,[l,v])
fila(Tr,15,11,["Desde","Tipo"])
for i,r in enumerate([(0,0.19),(6000,0.21),(50000,0.23),(200000,0.27)]): fila(Tr,16+i,11,list(r))

# ---- Referencias (comisiones por mercado y tipo de cambio; opcional) ----
R=hoja("Referencias"); fila(R,0,1,["M E R C A D O S"]); fila(R,1,1,["Prefijo","Fijo","%","Mínimo","Impuesto"])
for i,r in enumerate([("NYSE",1.0,0,1.0,0),("NASDAQ",1.0,0,1.0,0),("EPA",2.0,0.0005,2.0,0.004),("BME",2.0,0.0005,2.0,0),("AMS",2.0,0.0005,2.0,0)]): fila(R,2+i,1,list(r))
fila(R,10,1,["D I V I S A S"]); fila(R,11,1,["Divisa","En €"])
for i,(k,v) in enumerate(FX.items()): fila(R,12+i,1,[k,v])

# (la pestaña «Valoración» es opcional: ver docs/02-contrato-de-datos.md)
dst=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","plantilla","hoja-ejemplo.xlsx"); wb.save(dst); print("creada",os.path.normpath(dst))
