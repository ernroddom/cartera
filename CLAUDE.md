# Instrucciones para Claude: montar «Cartera» con la hoja de este usuario

Vas a adaptar una web de cartera de inversiones, ya hecha y muy pulida, a la hoja de cálculo de **tu usuario**. La web
salió de la hoja de otra persona (llamada aquí «la hoja original»). La hoja de tu usuario se parecerá en el fondo
(compras, dividendos, aportaciones, cotizaciones), pero sus pestañas, columnas y etiquetas **no tienen por qué coincidir**,
y puede que le falten partes (universo de candidatas, valoraciones, proyección…) o que tenga otras.

## Reglas
1. **La hoja del usuario es de solo lectura.** No la modifiques nunca sin su permiso explícito. Si para algo conviene una
   pestaña auxiliar con fórmulas, propónla y que la cree él o te autorice.
2. **Seguridad:** la clave del script y cualquier `Code.gs` con la clave **nunca** se suben a GitHub ni se escriben en
   archivos del repositorio. Antes de cada subida comprueba que no hay `AKfy…` (ID de implementación), ni la clave, ni
   `*.gs`, ni `appsscript.json` en lo que se publica (`construir.py` ya lo comprueba en `web/`). La carpeta `mi-hoja/`
   (su Excel) no se sube nunca: está en `.gitignore`.
3. **No cambies lo que no te pida.** Si ves una mejora, propónla. Pregunta antes de quitar bloques o cambiar el diseño.
4. **Mantén el contrato de datos.** El programa tiene tres capas: `parse()` lee la hoja → `model()` recalcula todo →
   las funciones `render*` dibujan. Para adaptarlo a otra hoja, lo normal es tocar **solo `parse()`** (y lo que haga falta
   alrededor) para que entregue **el mismo objeto** que entregaba con la hoja original. Así todo lo demás sigue funcionando.
5. **Cada cambio en `fuente/cartera.html`:** sube el número de `VER="vNNN"`, ejecuta `python3 herramientas/construir.py`
   y prueba (`herramientas/probar.js`). Sin reconstruir, la política de seguridad (huellas sha256 de los scripts) bloquea
   la página.
6. **Móvil primero:** el móvil de referencia es un iPhone de 402 px de ancho. Comprueba allí cada cambio visual (capturas).
7. Escribe en el idioma del usuario. Los textos de la web están en español de España.

## Plan de trabajo (en este orden)
1. **Entender la web.** Lee `docs/01-que-hace.md`, `docs/02-contrato-de-datos.md` y `docs/08-particularidades-hoja-original.md`.
   En `fuente/cartera.html`, busca `function parse(`, `function model(`, `const SHEETS=`, `const readSheet` y `function remPide`.
2. **Enseñársela con la hoja de ejemplo.** `cd web && python3 -m http.server 8000`, abre `http://localhost:8000` y, en el
   aviso «Conecta esta web con tu hoja», usa «Abrir un archivo .xlsx» con `plantilla/hoja-ejemplo.xlsx`. (O
   `node herramientas/probar.js plantilla/hoja-ejemplo.xlsx` para capturas de las cinco pestañas.)
3. **Analizar su hoja** (`mi-hoja/*.xlsx`): lista pestañas, filas de títulos de columna y etiquetas. Haz una **tabla de
   correspondencias** contra `docs/02-contrato-de-datos.md`: qué tiene igual, qué tiene con otro nombre, qué calcula de
   otra forma y qué no tiene. Enséñasela al usuario.
4. **Decidir con él** qué bloques quiere, cuáles no y si quiere añadir algo (ver `docs/03-adaptar-a-tu-hoja.md`).
5. **Adaptar `parse()`** (o, si el usuario lo prefiere, una pestaña auxiliar en su hoja que reordene sus datos al formato
   del contrato). Quitar o esconder los bloques que no tengan datos. Logos y banderas (`docs/07-logos-paises-icono.md`).
6. **Probar con su hoja** hasta que el bloque «Cuadre con tu hoja» salga sin diferencias (o explicar las que queden), en
   claro y oscuro, móvil y PC.
7. **Conectar y publicar:** script de Google (`docs/04-script-de-google.md`), GitHub Pages (`docs/05-publicar.md`) y el
   primer enlace personal en su móvil. Opcional: calendario de resultados (`docs/06-calendario.md`).
8. Al terminar, deja una nota en este archivo con las particularidades de **su** hoja, para la próxima sesión.

## Mapa rápido del código (`fuente/cartera.html`, un solo archivo de ~640 KB)
- **CSS** al principio (variables de color en `:root`, modo oscuro con `prefers-color-scheme` y `[data-theme="dark"]`;
  reglas del móvil en `@media (max-width:700.98px)` y `760.98px`). Muchas reglas se han ido añadiendo al final para
  ajustes finos: si algo no cambia, busca una regla posterior más específica.
- **HTML** de las cinco vistas: `#v-resumen`, `#v-preseleccion` (Universo), `#v-actualidad` (Calendario), `#v-analisis`,
  `#v-movimientos`; menú `#nav`; ficha de empresa `#sheet`; buscador `#kx`.
- **`<script id="logos" type="application/json">`**: diccionario de logos y banderas.
- **JS**: utilidades (`grid`, `find`, `rightNum`, `below`, `headerRow`, `listBelow`) → `parseVal` (Valoración) → `parse` →
  `xirr`, `dataChecks`, `model` → `render` y `render*` de cada bloque → carga de datos (`readSheet`, `load`, caché en
  IndexedDB) → Calendario (`loadAct`, `renderCal`) → menú, burbuja del menú, gesto de actualizar, modo privado.
- Hay código heredado de una pestaña antigua «Actualidad» (periódico semanal de noticias) que ya no se enseña: se puede
  dejar o quitar con cuidado.

## Lo que el usuario debe saber de entrada
- Las cotizaciones las pone **su hoja** (por ejemplo con `GOOGLEFINANCE`); la web no tiene una fuente de precios propia.
- La web **solo lee**: no escribe nunca en la hoja ni guarda nada fuera de su dispositivo.
- Funciona en PC, en el móvil (añadida a la pantalla de inicio se comporta como una app) y también dentro de Claude.

<!-- Notas de la hoja de este usuario (rellénalas al terminar): -->

### Notas de la hoja de este usuario (sesión de noviembre de 2026)
- **Formato:** su hoja («Cartera», en su Google personal) tiene **el mismo formato que la hoja original**: la web funciona sin
  adaptar `parse()`. Ojo: un Excel descargado de una versión antigua de su hoja traía otro formato; si algo no cuadra, pide
  primero una descarga reciente.
- **Código:** igual que el del amigo salvo el manifiesto de Android (`construir.py` genera `manifest.webmanifest` y copia
  `icon-192.png`/`icon-512.png`). Versión publicada: v426.
- **Publicación:** GitHub Pages sirve la rama **`gh-pages`**, que solo lleva el contenido de `web/` (+ `.nojekyll`). Tras cada
  `construir.py`, copia `web/` a esa rama, comprueba que no hay `AKfy…` y súbela. `main` lleva el paquete completo.
- **Script:** creado por él en su hoja con `Code.gs.ejemplo`. La copia de la hoja arrastró el script del amigo (`puerta.gs`) y su
  `appsscript.json` sin permiso de hojas de cálculo: se borró y se pusieron los permisos `spreadsheets`,
  `script.external_request` y `drive.readonly`. Nunca pidas ni guardes su ID ni su clave.
- **Arreglos hechos en su hoja (con su permiso):** formato de fecha en 4 dividendos futuros; Kraft Heinz como `NASDAQ:KHC` en
  Transacciones; «Cobrado» (Cartera, col. AE) reparte los dividendos según las acciones que conserva hoy, como la web;
  Vidrala 12/11/2025 = ampliación liberada (Div/Acc 0).
- **Diferencia aceptada:** «TradeRepublic Remunerada» (cuenta remunerada apuntada como lote con venta a 31/12 del año): el
  cuadre avisa de fecha futura; el usuario quiere dejarlo así.
- **Pendiente:** poner el bróker en cada aportación (ahora casi todas van a «Otros» en la liquidez por bróker) y escribir
  siempre «DeGiro»; cambiar el icono (aún es el del amigo).
- **App del hermano («Cartera de Inversión», `web/hermano/` → `…github.io/cartera/hermano/`):** 4 fondos por ISIN, aportaciones
  periódicas, hoja con el formato ANTIGUO del usuario. No hay segunda copia del programa: `herramientas/construir_hermano.py`
  parte de `fuente/cartera.html` y le aplica cambios al construir (3 pestañas Cartera/Aportaciones/Compras, lectura de su
  formato, «fondos/participaciones», sin cuadre ni avisos, solo sus pestañas, ID/clave/copia guardados como `fondos-…` para no
  mezclarse con la del usuario). Si un cambio en `cartera.html` rompe un parche, el script se para y dice cuál. Tras tocar
  `cartera.html`, construye las dos (`construir.py` y `construir_hermano.py`) y publica `web/` entera en `gh-pages`.
  Su «Valor Cartera»/«Invertido» de Valor Mensual son solo los fondos (sin liquidez): la gráfica compara eso. Su hoja lleva
  pestañas ocultas copiadas de la plantilla del usuario (Trayectoria, Preselección…) con datos del usuario: la app no las lee.
