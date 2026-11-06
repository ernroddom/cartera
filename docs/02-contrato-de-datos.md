# 2 · Qué espera encontrar la web en la hoja (el «contrato de datos»)

Todo esto lo hace `parse(wb)` en `fuente/cartera.html`. La hoja de ejemplo `plantilla/hoja-ejemplo.xlsx` lo cumple al pie
de la letra: ábrela al lado de esta guía.

## Cómo busca las cosas (importante para adaptar)
- Las pestañas se buscan **por su nombre exacto** (lista en `const SHEETS=`; solo se leen esas).
- Las tablas se encuentran buscando, en las **12 primeras filas**, una fila que tenga **todos** ciertos títulos de columna
  (`headerRow`). Las columnas se localizan **por el texto del título**, no por su posición: da igual el orden o que haya
  columnas de más. Los títulos se comparan exactos (sin espacios de sobra).
- Una tabla termina en la primera fila sin el dato clave (por ejemplo, Cartera termina en la primera fila sin «Empresa»;
  Transacciones, Dividendos, Aportaciones y Ajustes se saltan las filas vacías y siguen).
- Las etiquetas sueltas (Dashboard, Trayectoria) se buscan por texto en toda la pestaña, sin distinguir mayúsculas ni
  espacios (`find`/`norm`). El valor se coge **debajo** de la etiqueta (`below`) o **a su derecha** (el primer número en las
  12 columnas siguientes, `rightNum`).
- Números como números (no texto), porcentajes como **fracción** (12 % = 0,12), fechas como **fecha** de verdad.
- Importes en **euros** salvo donde se dice (la moneda base de la web es el euro; cambiarla es posible, ver 03).

## Lo mínimo para que arranque
**Transacciones** y **Aportaciones** con al menos una fila cada una (si no, la web dice «No encuentro las pestañas
Transacciones o Aportaciones»). Con eso calcula posiciones, liquidez, aportado, retorno y TIR. Para que las posiciones
tengan **precio** hace falta además **Cartera** o **Preselección** (sin precio, una posición se valora a lo que costó).

---

## Transacciones (obligatoria) — un lote por fila
Títulos obligatorios: `Ticker`, `Nombre`, `Acciones`. La tabla tiene **dos bloques de columnas con el mismo nombre**: el
primero es la compra y el segundo la venta.

| Columna | Qué es |
|---|---|
| `Ticker` | Formato `MERCADO:SÍMBOLO` como Google Finance (`NYSE:KO`, `BME:ITX`, `AMS:ASML`). Es la clave que une todo. |
| `Nombre`, `Divisa` | Nombre de la empresa y divisa de cotización (`EUR`, `USD`, `GBP`, `GBX`, `CHF`, `CAD`, `JPY`…). |
| `Acciones` | Número de acciones del lote. |
| `Bróker` | Texto libre (se usa para la liquidez por bróker y los filtros). En la hoja original «IB» se enseña como «Interactive Brokers». |
| 1.ª `Fecha`, `Precio`, `Total`, `Comisión` | Compra: fecha, precio por acción en su divisa, **total pagado en € comisión incluida**, comisión en €. |
| 2.ª `Fecha`, `Precio`, `Total`, `Comisión` | Venta (vacías si el lote sigue abierto): fecha, precio, **total cobrado en € ya sin comisión**, comisión. |
| `Benef. / Pérd.` | Resultado del lote vendido, en €. |
| `Comentarios` | Opcional. |

Un lote es **abierto** si su segunda `Fecha` está vacía. Si vendes parte de un lote, la hoja original lo parte en dos filas.
Las **opciones** se reconocen por el ticker con forma de contrato, p. ej. `XYZ C50 18DIC26` (se valoran a coste y se
excluyen del cuadre).

## Aportaciones (obligatoria)
Títulos: `Fecha`, `Cantidad`, `Tipo` (+ `Bróker`, `Comentario`). **Ojo al signo:** el dinero que **metes** va en
**negativo** (−1.000 = aportas 1.000 €) y lo que **sacas** en positivo. La web le da la vuelta (`amt = −Cantidad`).

## Dividendos
Títulos: `Fecha`, `Ticker`, `Div. EUR` (+ `Nombre`, `Bróker`, `Divisa`, `Tipo`, `Acciones`, `Div/Acc`, `Div. Broker`).
`Div. EUR` = bruto en €; `Div. Broker` = neto en € (lo que llega a la cuenta; la diferencia son retenciones). **Las filas con
fecha futura son los dividendos previstos**: alimentan «próximos 12 meses», «previsto del año que viene», el calendario y la
rentabilidad por dividendo.

## Ajustes
Títulos: `Fecha`, `Cantidad` (+ `Bróker`, `Comentario`). Cualquier movimiento de efectivo que no sea lo anterior
(intereses, diferencias de cambio, regalos de bróker, cuotas). Positivo = entra dinero.

## Cartera (recomendada) — una fila por posición abierta
Títulos obligatorios: `Empresa`, `Ticker`, `Valor`. Se usan sobre todo: `Precio` (en su divisa), `Hoy` (cambio del día en
fracción), `Divisa`, `Valor` (€). Opcionales que se comparan en el cuadre o se enseñan si están: `Acc.`, `Pr. Medio`,
`Invertido`, `Peso`, `Revaloriz.`, `FX`, `Dividendo`, `Total`, `Total €`, `TIR`, `Años`, `Anual`, `YoV`, `YoC`, `Cobrado`, `Próximo`.
El **tipo de cambio** de cada divisa se deduce de aquí (`Valor / (Precio × Acc.)`); si falta, sale de Referencias.

## Preselección (recomendada) — tu universo: posiciones + candidatas
Fila de títulos con al menos `Industria` y `País`. La columna de tickers se detecta sola (celdas con forma `ABC:XYZ` en
mayúsculas); el **nombre** de la empresa debe estar **en la columna justo a su izquierda**.
Columnas que usa: `Hoy`, `Precio`, `FX` (aquí es la **divisa**, p. ej. `USD`), `Múltiplo`, `Fecha` (de la última valoración),
`Cotiz.` (estado: `Previo` = aún no ha cotizado hoy), `1S`, `1M`, `3M`, `6M`, `YTD`, `1A`, `3A` (rendimientos en fracción),
`MM200`, `Volat.`, `Drawdown`, `Máx. 52s`, `Industria`, `País` (texto: `USA`, `España`, `Francia`…; da la bandera),
`Fair Value` (valor razonable), `Dist.`, `TIR esp.` (TIR esperada), `Exigido` (retorno exigido).
Sin esta pestaña: no hay Universo, ni industria/país en Análisis, ni pestaña Cotización en la ficha.

## Valor Mensual (opcional) — gráfica de Evolución
Una fila con los títulos `Fecha`, `Valor Cartera`, `Aportaciones` y `MSCI World` (en ese orden de izquierda a derecha;
`Fecha` a la izquierda de `MSCI World`). Debajo, una fila por mes: fecha, valor de la cartera, **aportado acumulado** y
el valor que tendría ese mismo dinero invertido en el MSCI World. También da la comparación «Frente al MSCI World».

## Dashboard (opcional) — solo para el «Cuadre con tu hoja» y algún dato suelto
Etiquetas con el valor **debajo**: `Valor de cartera`, `Retorno total`, `Hoy`, `TIR anualizada`, `Frente al MSCI World`
(en **puntos porcentuales**, p. ej. −0,5), `Rentas próximo año`; con número **a la derecha**: `Liquidez`, `Aportaciones`,
`Revalorización latente`, `Posiciones cerradas`, `Dividendos brutos`, `Retenciones`, `Comisiones de compra`, `Ajustes`.
Con el valor debajo: `Operaciones`, `Pos. cerradas`, `Comisiones`, `Comisión media`, `Antigüedad media`, `Aportaciones AAAA`,
`Total AAAA`, `CAGR…`, `Previsto…`, `Media mensual`, `YoV`, `YoC`.
Listas (título y debajo filas nombre + peso): `I N D U S T R I A S`, `P A Í S E S`, `D I V I S A S` (títulos con espacios
entre letras, tal cual; deja **9 columnas** entre una lista y otra).

## Trayectoria (opcional) — proyección a largo plazo
Tabla con `Año`, `Aportación`, `Acumulado`, `Valor final` (+ `Edad`, `Dividendos`, `Neto mes`, `TIR`). Etiquetas con número
a la derecha: `Año en curso`, `Edad`, `Patrimonio`, `Aportado`, `Neto mensual`, `Ahorro anual`, `Crecimiento anual`,
`Rentabilidad por dividendo`, `Dividendos apuntados hasta`, `Sin reinvertir desde` (0 = nunca). Tramos de impuestos: una
celda `Desde` y debajo pares (importe desde, tipo). Un título que empiece por `H O R I Z O N T E` da el nombre del bloque.

## Referencias (opcional)
- Título `M E R C A D O S` y en las filas siguientes `Prefijo`, `Fijo`, `%`, `Mínimo`, `Impuesto`: comisión de compra por
  mercado (el prefijo del ticker, `NYSE`, `BME`…). La usa la Calculadora de operaciones.
- Título `D I V I S A S` y `Divisa`, `En €`: cuántos euros vale una unidad de cada divisa (respaldo si Cartera no lo da).
  `GBX` (peniques) se deduce de `GBP` si falta.

## Valoración (opcional) — pestaña «Valoración» de la ficha
Un bloque por empresa, uno debajo de otro. Cada bloque empieza con el **nombre** en la columna B (igual que en
Preselección) y, en la fila justo debajo, la etiqueta `MÚLTIPLO SALIDA`, que es lo que la web busca para encontrar los bloques. Dentro del bloque (≤ 30 filas) busca por texto:
`MÚLTIPLO SALIDA`, `RETORNO EXIGIDO` (valor a la derecha); `Cotización`, `Deuda Neta`, `Múltiplo Actual`,
`Deuda Neta / Acción`, `Última Valoración`, `Caja Neta`, `Caja Neta / Acción` (valor debajo); `Notas`, `A favor`,
`En contra`, `Múltiplo`, `Retorno` (texto a la derecha); `DN / …` (deuda neta entre lo que elijas); una tabla `Año`,
`Precio`, `IRR`, `Dividendos`, `IRR (Div.)`; una proyección que empieza en `LTM` con filas como `Ventas`; y una matriz
`FAIR VALUE` (filas = múltiplos, columnas = retornos exigidos). Es lo más específico de la hoja original: si tu hoja no
lo tiene, la pestaña Valoración simplemente no aparece.

## Qué pasa si falta algo
| Falta | Efecto |
|---|---|
| Transacciones o Aportaciones | La web no arranca (mensaje claro). |
| Cartera y Preselección | Funciona, pero las posiciones se valoran a lo que costaron y «Hoy» sale a 0 (comprobado). |
| Preselección | Sin pestaña Universo útil, sin industria/país, sin Cotización en la ficha. |
| Dividendos | Todo lo de dividendos a cero; calendario solo con resultados. |
| Valor Mensual | La gráfica de Evolución y «Frente al MSCI World» se quedan sin datos. |
| Dashboard | Todo funciona; el Cuadre enseña las cifras de la web con la columna «Hoja» vacía (comprobado). |
| Trayectoria / Referencias / Valoración | Desaparece ese bloque o esa función. |
