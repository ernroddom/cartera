# 3 · Cómo adaptar la web a tu hoja

## La estrategia
1. **No reorganices tu hoja para la web.** Lo normal es adaptar `parse()` para que lea tu hoja tal como está y entregue el
   mismo objeto que entregaba con la hoja original (ver la forma del objeto más abajo). `model()` y el dibujo no se tocan.
2. Si alguna cosa es mucho más fácil de calcular en tu hoja (por ejemplo, un histórico mensual), la alternativa es una
   **pestaña auxiliar** en tu hoja (p. ej. «Web») con fórmulas que reordenan tus datos al formato del contrato. Tu hoja de
   siempre no se toca; solo se añade esa pestaña. Recuerda añadir su nombre a `const SHEETS=`.
3. Lo que no tengas, **se quita o se esconde** (ver «Quitar bloques»). La web aguanta bien que falten partes: probado con una
   hoja que solo tiene Transacciones, Aportaciones, Dividendos y Ajustes.

## Forma del objeto que debe devolver `parse()`
`{ kpi, pos, pre, comm, fxRef, tx, dv, ap, aj, ind, pais, divisa, evo, div, years, pays, wf, stats, tray, curYear, horizon, sinFecha }`
- `tx`: `[{ticker,name,cur,shares,broker,bd,bp,bt,bfee,sfee,sd,sp,st,pnl,note}]` — compra (`b*`) y venta (`s*`); `bd`/`sd` fechas
  (`Date`), `bt` total de compra en € con comisión, `st` total de venta en € neto, `sd=null` si sigue abierta.
- `dv`: `[{d,ticker,name,broker,cur,type,shares,dps,gross,net}]` (`gross`/`net` en €; fechas futuras = previstos).
- `ap`: `[{d,amt,broker,type,note}]` con `amt` **positivo** cuando aportas. `aj`: `[{d,amt,broker,note}]`.
- `pos` (de Cartera): `[{name,ticker,today,price,cur,shares,value,…}]`. `pre` (de Preselección): `[{ticker,name,today,price,cur,
  ind,country,fv,irrExp,req,mult,fvDate,status,w1,m1,m3,m6,ytd,y1,y3,dd,hi52,mm200,vol,…, inPf, weight, margin, val}]`.
- `kpi`, `wf`, `stats`: cifras de tu Dashboard para el cuadre (pueden ir vacías). `evo`: `[{d,v,a,i}]` mensual.
- Si dudas, pon temporalmente `console.log(pd)` en `load()` (justo después de `pd=parse(wb)`; o en el manejador de «Abrir un
  archivo .xlsx») y abre `plantilla/hoja-ejemplo.xlsx`: verás el objeto exacto en la consola. Las funciones no son globales,
  así que no se pueden llamar a mano desde la consola.

## Recetas para lo más habitual
| En tu hoja… | Qué hacer |
|---|---|
| Las pestañas o columnas se llaman distinto | Cambia los nombres en `parse()`. Truco limpio: un diccionario de alias (`{"Fecha compra":"Fecha", …}`) aplicado en `headerMap`. |
| Las aportaciones son positivas | Quita el signo menos en `out.ap` (`amt: g("Cantidad")`). |
| Compra y venta en filas distintas (no en la misma fila del lote) | Empareja en `parse()`: agrupa por ticker y reparte las ventas sobre los lotes (FIFO) para construir `tx` con `sd/sp/st`. |
| No apuntas lotes, solo posiciones | Crea un lote sintético por posición (acciones, invertido, fecha de primera compra). Se pierde el detalle de compras y la TIR será aproximada; avísalo. |
| Total de compra sin la comisión | Súmala en `parse()` (`bt = total + comisión`). |
| Importes en la divisa de cada empresa, no en € | Convierte en `parse()` con el tipo de cambio de la fecha si lo tienes, o con el de Referencias (aproximado, avísalo). |
| Tickers sin mercado (`KO` en vez de `NYSE:KO`) | Funciona si eres consistente en todas las pestañas; los logos se buscan también sin mercado. Preselección sí necesita `MERCADO:SÍMBOLO` para detectar la columna (o cambia ese detector). |
| Precios en otra pestaña (o con `GOOGLEFINANCE` en Transacciones) | Llévalos a `pos`/`pre` en `parse()`. Sin precio, la posición vale lo que costó. |
| Sin universo de candidatas | Construye `pre` con tus propias posiciones (industria/país si los tienes). Universo funcionará solo con tu cartera. |
| Moneda base que no es el euro | Hay que tocar los textos «€» y `eur()`, y el tipo de cambio `EUR:1` en `model()`. Es un cambio amplio: hazlo con calma. |
| Otro índice de referencia (S&P 500…) | En `parse()` busca tu columna en vez de `MSCI World` y cambia el texto «MSCI World» de la web. |

## Quitar bloques o pestañas
- Un bloque: añade al final del CSS `#id-del-bloque{display:none!important}` (ids en `01-que-hace.md`: `s-today`, `s-pos`,
  `s-check`, `s-divs`, `s-ret`, `s-tray`, `s-perf`, `s-plan`, `s-plist`, `s-cal`…), o quítalo del HTML con cuidado de no
  dejar código que lo busque (`$("id")` devolvería `null`).
- Una pestaña entera: quita su `<a>` de `#nav` (y, si quieres, su `<div class="view">`). La burbuja del menú se adapta sola.

## Añadir algo nuevo
Mismo camino que lo existente: leerlo en `parse()` → calcularlo en `model()` → una función que lo dibuje y su `<section>`
en la vista que toque. Reglas de diseño de la casa: en el móvil ninguna cifra pasa de 17 px; prueba siempre a 402 px de
ancho, en claro y oscuro; usa las variables de color (`--ink`, `--ink2`, `--ink3`, `--line`, `--pos`, `--neg`, `--panel`,
`--canvas`) para que el modo oscuro funcione solo.
