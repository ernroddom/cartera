# Construye la carpeta web/ (lista para GitHub Pages) a partir de fuente/.
#   python3 herramientas/construir.py
# Qué hace:
#  1. Pone la cabecera de la página (icono, nombre en el iPhone, colores de la barra, no indexar en buscadores).
#  2. Copia logos, fuentes (Inter y Newsreader), bibliotecas (SheetJS y Chart.js) e iconos junto a la página: nada se pide a otras webs.
#  3. Mete las reglas de las fuentes dentro de la página (en lugar de pedirlas a Google Fonts).
#  4. Añade la política de seguridad (CSP): solo se ejecutan los scripts de la propia página (por su huella sha256) y las dos
#     bibliotecas; los datos solo se piden a script.google.com. IMPORTANTE: la huella se calcula aquí, así que cada vez que
#     cambies cartera.html hay que volver a construir (si publicas el index.html viejo con código nuevo, la página no arranca).
#  5. Escribe version.txt (la app lo consulta para avisar de que hay versión nueva y recargarse).
#  6. Comprueba que no se cuela ningún ID de script (AKfy…), ni archivos .gs / appsscript.json.
import os, re, sys, shutil, hashlib, base64, glob
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
F=os.path.join(R,"fuente"); OUT=os.path.join(R,"web")
NOMBRE=os.environ.get("NOMBRE_APP","Cartera")   # el nombre bajo el icono en la pantalla de inicio del móvil
src=open(os.path.join(F,"cartera.html"),encoding="utf-8").read()
m=re.search(r'VER="(v\d+)"',src); assert m, "falta VER=\"vNNN\" en cartera.html"
os.makedirs(OUT,exist_ok=True)
cab="\n".join(['<!DOCTYPE html>','<html lang="es">','<meta charset="utf-8">',
 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
 '<meta name="robots" content="noindex, nofollow">','<meta name="referrer" content="no-referrer">',
 '<meta name="apple-mobile-web-app-capable" content="yes">','<meta name="mobile-web-app-capable" content="yes">',
 f'<meta name="apple-mobile-web-app-title" content="{NOMBRE}">',
 '<meta name="theme-color" content="#E4E2DC" media="(prefers-color-scheme: light)">',
 '<meta name="theme-color" content="#0F0F0E" media="(prefers-color-scheme: dark)">',
 '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">',
 '<link rel="icon" type="image/png" sizes="64x64" href="favicon-64.png">',
 '<link rel="apple-touch-icon" href="apple-touch-icon.png">',
 '<link rel="manifest" href="manifest.webmanifest">'])+"\n"
t=cab+src
open(os.path.join(OUT,"version.txt"),"w").write(m.group(1)+"\n")
shutil.copy(os.path.join(F,"icono","apple-touch-icon-180.png"),os.path.join(OUT,"apple-touch-icon.png"))
for f in ("favicon-32.png","favicon-64.png"): shutil.copy(os.path.join(F,"icono",f),os.path.join(OUT,f))
# Android: con el manifiesto, la web añadida a la pantalla de inicio se abre a pantalla completa, con su nombre e icono
for f in ("icon-192.png","icon-512.png"): shutil.copy(os.path.join(F,"icono",f),os.path.join(OUT,f))
import json
open(os.path.join(OUT,"manifest.webmanifest"),"w",encoding="utf-8").write(json.dumps({
 "name":NOMBRE,"short_name":NOMBRE,"start_url":"./","scope":"./","display":"standalone",
 "background_color":"#E4E2DC","theme_color":"#E4E2DC","lang":"es",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},ensure_ascii=False,indent=1))
for sub,pat in (("logos","*.webp"),("fonts","*.woff2"),("lib","*.js")):
    d=os.path.join(OUT,sub); shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    origen={"fonts":"fuentes"}.get(sub,sub)
    for p in glob.glob(os.path.join(F,origen,pat)): shutil.copy(p,d)
# los ID de Drive solo los usa la versión dentro de Claude: en la web van vacíos
t=re.sub(r'const FILE_ID = "[A-Za-z0-9_-]{25,}";','const FILE_ID = "";',t); t=re.sub(r'const INF_ID="[A-Za-z0-9_-]{25,}";','const INF_ID="";',t)
# fuentes propias en lugar de Google Fonts
G=re.search(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">\n',t)
if G:
    css=re.sub(r"/\*.*?\*/","",open(os.path.join(F,"fuentes","fuentes.css"),encoding="utf-8").read(),flags=re.S); css=re.sub(r"\s*\n\s*","",css)
    t=t[:G.start()]+"<style>/* fuentes propias */"+css+"</style>\n"+t[G.end():]
assert "fonts.googleapis" not in t and "fonts.gstatic" not in t, "queda alguna llamada a Google Fonts"
for b in ("lib/xlsx-0.20.3.full.min.js","lib/chart-4.4.1.umd.js"): assert f'src="{b}"' in t, f"falta la etiqueta de {b}: si cambias de versión, actualiza este script"
hs=" ".join("'sha256-%s'"%base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode() for s in re.findall(r"<script>(.*?)</script>",t,re.S))
csp=("default-src 'none'; script-src %s 'self'; worker-src blob:; "
     "connect-src 'self' https://script.google.com https://script.googleusercontent.com; img-src 'self' data: blob:; "
     "style-src 'self' 'unsafe-inline'; font-src 'self'; manifest-src 'self'; "
     "base-uri 'none'; form-action 'none'; object-src 'none'")%hs
assert t.count('<meta charset="utf-8">')==1
t=t.replace('<meta charset="utf-8">','<meta charset="utf-8">\n<meta http-equiv="Content-Security-Policy" content="%s">'%csp,1)
open(os.path.join(OUT,"index.html"),"w",encoding="utf-8").write(t)
# comprobaciones de seguridad
malos=[]
for root,ds,fs in os.walk(OUT):
    for f in fs:
        p=os.path.join(root,f)
        if f.endswith(".gs") or f=="appsscript.json": malos.append(p); continue
        if re.search(rb'AKfy[A-Za-z0-9_-]{30,}',open(p,"rb").read()): malos.append(p)
if malos: sys.exit("NO PUBLIQUES: hay un ID de script o un archivo del script en "+", ".join(malos))
print(f"web/ construida ({m.group(1)}): {len(re.findall(r'<script>',t))} scripts propios con huella · sin IDs de script")
