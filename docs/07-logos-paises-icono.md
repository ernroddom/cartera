# 7 · Logos, banderas e icono de la app

## Cómo se guardan
- Las imágenes están en `fuente/logos/*.webp` (fondo transparente, 128 px por el lado largo; banderas 80×80).
- El diccionario que las une está dentro de `fuente/cartera.html`, en `<script type="application/json" id="logos">`:
  - `"T:NYSE:KO": "logos/….webp"` → logo de la empresa con ese ticker (tal cual aparece en tu hoja).
  - `"R:T:NYSE:KO": 3.048` → proporción ancho/alto (para colocarlo bien).
  - `"D:T:EPA:OR": 1` → logo negro: en modo oscuro se pinta en gris claro.
  - `"K:T:…": "logos/….webp"` → versión propia para el modo oscuro.
  - `"P:España": "logos/….webp"` → bandera; la clave es el texto exacto de la columna `País` de Preselección (`USA` se
    enseña como «EE. UU.»).
- Trae unos 140 logos de empresas conocidas y 23 banderas: si tus empresas están, salen solos.
- Si un ticker no tiene logo, la web enseña el nombre (o sus iniciales) en su lugar; no se rompe nada.
- Hay dos tablas opcionales de «peso visual» por ticker (`LOGO_F` y `LOGO_A`) para igualar logos finos y macizos en el
  mapa de Resumen. Para logos nuevos no hace falta tocarlas.

## Añadir o cambiar uno
`python3 herramientas/anadir_logo.py logo.png NYSE:XYZ` (opciones `--negro`, `--oscuro otro.png`, `--pais "Suiza"`), y
después `python3 herramientas/construir.py`. Busca logos en la web oficial de la empresa (sección de prensa) o en
Wikimedia Commons; SVG → conviértelo a PNG antes.

## El icono de la app
`fuente/icono/apple-touch-icon-180.png` (icono del iPhone, 180×180, sin transparencia), `favicon-32.png` y `favicon-64.png`.
**El que viene es el logo de la persona que te ha pasado la web: pon el tuyo.** Hay además una versión del logo dibujada
dentro de la web como icono de la pestaña Resumen del menú del móvil (busca `nav-logo` en `cartera.html`): cámbiala por el
tuyo o vuelve a un icono de trazo como los demás.
