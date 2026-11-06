# Añade (o cambia) el logo de una empresa o la bandera de un país en la web.
#   python3 herramientas/anadir_logo.py logo.png NYSE:KO                 → logo de una empresa (clave = ticker tal cual en tu hoja)
#   python3 herramientas/anadir_logo.py logo.png NYSE:KO --negro         → logo negro: en modo oscuro se pinta en gris claro
#   python3 herramientas/anadir_logo.py claro.png NYSE:KO --oscuro oscuro.png   → con una versión propia para el modo oscuro
#   python3 herramientas/anadir_logo.py bandera.png --pais "España"      → bandera (el texto exacto de la columna País)
# El logo se recorta (bordes transparentes), se reduce a 128 px por el lado largo (banderas: 80×80) y se guarda en
# fuente/logos/ como .webp; después se apunta en el diccionario <script id="logos"> de fuente/cartera.html.
# Formatos: PNG, JPG o WebP (un SVG, conviértelo antes a PNG). Mejor con fondo transparente. Luego: construir.py.
import sys, os, re, json, hashlib, io, argparse
from PIL import Image
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
ap=argparse.ArgumentParser(); ap.add_argument("imagen"); ap.add_argument("ticker",nargs="?"); ap.add_argument("--pais"); ap.add_argument("--negro",action="store_true"); ap.add_argument("--oscuro")
a=ap.parse_args()
if not (a.ticker or a.pais): sys.exit("Indica el ticker (p. ej. NYSE:KO) o --pais \"España\"")
def prepara(p,bandera=False):
    im=Image.open(p).convert("RGBA"); bb=im.getchannel("A").getbbox()
    if bb: im=im.crop(bb)
    if bandera:
        s=min(im.size); l=(im.width-s)//2; t=(im.height-s)//2; im=im.crop((l,t,l+s,t+s)).resize((80,80),Image.LANCZOS)
    else:
        k=128/max(im.size); im=im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,"WEBP",quality=90,method=6); d=b.getvalue()
    ruta=f"logos/{hashlib.sha1(d).hexdigest()[:12]}.webp"; open(os.path.join(R,"fuente",ruta),"wb").write(d)
    return ruta, round(im.width/im.height,3)
H=os.path.join(R,"fuente","cartera.html"); t=open(H,encoding="utf-8").read()
m=re.search(r'(<script type="application/json" id="logos">)(.*?)(</script>)',t,flags=re.S); assert m, "no encuentro el diccionario de logos"
L=json.loads(m.group(2))
if a.pais:
    ruta,_=prepara(a.imagen,True); L["P:"+a.pais]=ruta; print("bandera",a.pais,"→",ruta)
else:
    k="T:"+a.ticker; ruta,ratio=prepara(a.imagen); L[k]=ruta; L["R:"+k]=ratio
    L.pop("D:"+k,None); L.pop("K:"+k,None)
    if a.negro: L["D:"+k]=1
    if a.oscuro: L["K:"+k]=prepara(a.oscuro)[0]
    print("logo",a.ticker,"→",ruta,"· proporción",ratio,("· negro" if a.negro else ""),("· versión oscura" if a.oscuro else ""))
t=t[:m.start(2)]+json.dumps(L,ensure_ascii=False,separators=(",",":"))+t[m.end(2):]
open(H,"w",encoding="utf-8").write(t); print("Hecho. Ahora: python3 herramientas/construir.py")
