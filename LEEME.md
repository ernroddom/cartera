# Cartera · plantilla para montar tu propia web de inversiones

Esto es una web (que en el móvil funciona como una app) para ver tu cartera de inversiones a partir de **tu hoja de cálculo**.
La web no tiene datos dentro: lee tu hoja cada vez que la abres y lo calcula y lo dibuja todo. Viene de la web que usa
un amigo tuyo con su propia hoja; aquí no hay ni un dato suyo, solo el programa y una hoja de ejemplo inventada.

## Qué vas a necesitar
- **Claude Code** (en el ordenador o en claude.ai/code). Él hace el trabajo: tú le vas contestando.
- Tu hoja de inversiones en **Google Sheets** (si la tienes en Excel, súbela a Google Drive y ábrela con Hojas de cálculo).
- Una cuenta de **GitHub** (gratis) para publicar la web, y tu cuenta de **Google** para el script que le pasa tu hoja.
- Un par de horas la primera vez. Después, cada cambio es pedírselo a Claude.

## Cómo empezar (4 pasos)
1. Descomprime esta carpeta donde quieras y abre Claude Code **dentro de ella** (o súbela a un repositorio tuyo de GitHub y
   abre ahí una sesión de Claude Code).
2. Dile a Claude: **«Lee CLAUDE.md y ayúdame a montar esta web con mi hoja de inversiones»**.
3. Pásale tu hoja: descárgala como Excel (Archivo → Descargar → Microsoft Excel .xlsx) y déjala en la carpeta `mi-hoja/`
   (esa carpeta no se sube nunca a ningún sitio), o conéctale Google Drive si tu Claude lo tiene.
4. Claude te enseñará la web primero con la hoja de ejemplo, luego con la tuya, te preguntará qué partes quieres y cuáles
   no, y al final te guiará para crear el script de Google y publicarla.

## Qué hay en la carpeta
| Carpeta / archivo | Para qué |
|---|---|
| `CLAUDE.md` | Las instrucciones para tu Claude (léelas si quieres saber qué va a hacer). |
| `docs/` | La documentación completa: qué hace la web, qué espera de la hoja, cómo adaptarla, publicar, seguridad… |
| `fuente/` | El programa: `cartera.html` (toda la web en un archivo) más logos, fuentes, bibliotecas e iconos. |
| `herramientas/` | `construir.py` prepara la carpeta `web/` para publicar · `crear_hoja_ejemplo.py` · `probar.js`. |
| `plantilla/hoja-ejemplo.xlsx` | Una hoja inventada con la estructura que lee la web, para probar y para comparar con la tuya. |
| `apps-script/Code.gs.ejemplo` | El script de Google que entrega tu hoja a la web (lo pegas en tu hoja con tu clave). |
| `calendario/` | Opcional: formato e instrucciones para que una tarea semanal de Claude te rellene las fechas de resultados. |
| `web/` | La web ya construida con la versión de este paquete (la que se publica). Se regenera con `construir.py`. |

## Lo importante de la privacidad, en tres líneas
- Tu hoja **no se sube a GitHub**: lo publicado es solo el programa. Los datos viajan de tu script de Google a tu móvil, con tu clave.
- La clave y el código del script con la clave **nunca se suben a GitHub** ni se pegan en ningún sitio.
- El icono que trae es el de la persona que te lo pasa: Claude te ayudará a poner el tuyo.
