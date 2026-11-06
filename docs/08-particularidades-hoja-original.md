# 8 · Cómo es la hoja original (para que sepas qué hacía cada cosa y decidas)

La web se construyó para una hoja de Google Sheets llamada «Inversiones», de un inversor particular en acciones (largo
plazo, dividendos, varias divisas, dos brókers). Aquí se describe su **estructura**, sin ningún dato. Tu hoja no tiene por
qué parecerse: úsalo para entender de dónde sale cada número y qué te falta o te sobra.

## Pestañas y para qué servían
| Pestaña | Contenido |
|---|---|
| **Dashboard** | El cuadro de mando de la hoja: valor, retorno, TIR, comparación con el MSCI World, liquidez, aportaciones, desglose del retorno, estadísticas, dividendos (total del año, CAGR, previsto, media mensual, YoV/YoC), listas de industrias/países/divisas con títulos espaciados («I N D U S T R I A S»), rentas por año y próximos pagos (estos dos últimos ya no los usa la web). |
| **Cartera** | Una fila por posición abierta con fórmulas: precio (GOOGLEFINANCE), cambio de hoy, acciones, precio medio, invertido, valor, peso, revalorización, efecto divisa, dividendos, TIR, YoV/YoC, cobrado, próximo pago. |
| **Preselección** | El universo: las posiciones y las candidatas (más de un centenar), con precio y rendimientos (GOOGLEFINANCE), estado de la cotización («Previo» si aún no ha cotizado hoy), industria, país, valor razonable, distancia, TIR esperada y retorno exigido. Era su «radar». |
| **Valoración** | Un bloque por empresa con su modelo: múltiplo de salida, retorno exigido, deuda/caja neta, proyección (LTM y años), IRR con y sin dividendos, matriz de valor razonable (múltiplo × retorno) y notas de tesis (a favor, en contra). Es lo más personal de la hoja. |
| **Transacciones** | Un lote por fila, compra y venta en la misma fila (dos bloques de columnas Fecha/Precio/Total/Comisión), bróker y resultado. Opciones con ticker de contrato. El bróker principal aparece como «IB». |
| **Dividendos** | Cada cobro (bruto en €, neto del bróker, acciones, dividendo por acción) y, con fecha futura, los previstos. |
| **Aportaciones** | Ingresos (en negativo) y retiradas, por bróker. |
| **Ajustes** | Intereses, diferencias de cambio y otros movimientos de efectivo. |
| **Valor Mensual** | Una fila por mes: valor de la cartera, aportado acumulado y el mismo dinero invertido en el MSCI World. |
| **Trayectoria** | Proyección a largo plazo («horizonte de independencia»): por año, edad, aportación, acumulado, valor final, dividendos, neto al mes y TIR; supuestos (ahorro anual, crecimiento, rentabilidad por dividendo, año en que deja de reinvertir) y tramos de impuestos. |
| **Referencias** | Comisiones de compra por mercado (fijo, %, mínimo, impuesto) y tipo de cambio de cada divisa en €. |

## Particularidades que conviene conocer
- **La web recalcula** casi todo desde Transacciones, Dividendos, Aportaciones y Ajustes; el Dashboard solo sirve para
  comprobar (el bloque «Cuadre con tu hoja» marca cualquier diferencia de más de 1 €).
- **Liquidez** = aportaciones − compras + ventas + dividendos netos + ajustes, por bróker.
- **TIR** con los flujos de aportaciones (no con las compras); «Frente al MSCI World» con los mismos flujos invertidos en el índice.
- **Opciones**: se valoran a coste y no entran en el cuadre (la hoja original no las incluía en sus totales).
- **«Hoy»** se calcula con el cambio del día de cada posición. Antes de las 9:00 y en fin de semana se considera mercado
  cerrado y la web habla de «Última sesión».
- **Peniques (GBX)**: si una empresa británica cotiza en peniques, la web divide entre 100 usando el cambio de la libra.
- **Previstos**: lo que la hoja original apuntaba como dividendos futuros alimenta todo lo de «próximos 12 meses».
- La comparación con el **MSCI World** es una elección de esa hoja: cámbiala por tu índice si quieres.
- La **calculadora de operaciones** usa las comisiones de Referencias (si no las tienes, calcula sin comisión).

## Ideas de cosas que tu hoja puede tener y la original no
Fondos indexados o ETF (funcionan igual que acciones si tienen ticker y precio), cuentas remuneradas (como liquidez o
ajustes), criptomonedas (ticker propio y precio en tu hoja), varias carteras (habría que añadir un filtro por cartera),
objetivos de asignación por activo (sería un bloque nuevo). Todo se puede añadir siguiendo `03-adaptar-a-tu-hoja.md`.
