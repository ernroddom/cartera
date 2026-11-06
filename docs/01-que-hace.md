# 1 · Qué hace la web (y qué no)

## La idea
Tu hoja es la fuente de verdad. La web la lee entera (como un .xlsx), **recalcula** la cartera a partir de los
movimientos (compras, ventas, dividendos, aportaciones, ajustes) y de las cotizaciones que pone la hoja, y lo enseña
ordenado, en PC y en el móvil. Las cifras resumen de tu hoja (Dashboard) solo se usan para **comprobar** que la web y la
hoja dicen lo mismo («Cuadre con tu hoja»).

## Las cinco pestañas (orden del menú)
### Resumen
- **Tarjeta oscura fija arriba**: Cartera (valor) con la liquidez debajo · Hoy (€ y %) · Total (€ y % sobre lo aportado).
  Tocarla oculta o enseña los importes (modo privado).
- **Tu cartera hoy**: mapa de rectángulos (tamaño = peso; color = lo que sube o baja hoy), con logos. Leyenda «X suben · Y bajan».
- **Posiciones**: lista con Hoy / Total; en PC, tabla con todas las columnas. Al tocar una empresa se abre su ficha.
- **Evolución**: gráfica del valor frente a lo aportado y frente al MSCI World (1 año, 3 años, todo).
- **Cuadre con tu hoja**: compara 20 cifras de la web con las de tu hoja y revisa los datos que metes a mano
  (acciones que no coinciden, dividendos sin compra, fechas imposibles, movimientos repetidos, empresas que faltan en el universo).

### Universo (tu lista de seguimiento, «Preselección»)
- **Franja** de cinco cifras: empresas, sobre lo exigido, margen, TIR esperada, por revisar.
- **Rendimiento**: mejores y peores del periodo (desplegable en el móvil: Hoy, Última sesión, 1 semana … 3 años, Desde máximos),
  y **Por industria** (casillas de color).
- **Calculadora de operaciones**: simula aportar/comprar/vender y calcula comisiones, nuevo precio medio y pesos.
- **Todas las empresas**: lista con buscador, botones (En cartera, Candidatas, Sobre lo exigido, Por revisar, Hoy), filtro por
  industria y orden; precio, valor razonable, margen sobre lo exigido y bandera del país.

### Calendario
- Mes con puntos por día: **resultados** (de la tarea semanal opcional, ver `06-calendario.md`) y **dividendos** previstos
  (de tu pestaña Dividendos, filas con fecha futura). Filtros Todo/Resultados/Dividendos y Mi cartera/Todo el universo.
- Al tocar un día: la lista de ese día (antes de la apertura / tras el cierre, fecha estimada).

### Análisis
- **Franja** de cinco cifras: dividendos del año que viene, fuera del euro, concentración, mayor país, mayor industria.
- **Dividendos**: año en curso (cobrado de previsto), crecimiento anual, cobrado total, rentabilidad sobre lo invertido y
  sobre el valor; próximos 12 meses (barras), mayores pagadores, próximos cobros (calendario), historial por año.
- **Diversificación**: industrias, países, divisas, concentración.
- **Anatomía del retorno**: de dónde sale lo ganado (revalorización, cerradas, dividendos, retenciones, comisiones, ajustes).
- **Trayectoria**: tu proyección a largo plazo (si tu hoja la tiene).

### Movimientos
- Cinco vistas (Movimientos/todos, Transacciones, Dividendos, Aportaciones, Ajustes), cada una con su bloque de cifras y su
  lista por meses; buscador y filtros (año, bróker, estado de la operación, orden).

## La ficha de cada empresa
Pestañas **Posición** (si la tienes), **Movimientos**, **Cotización** (precio, rangos, rendimientos, distancia al máximo)
y **Valoración** (si tu hoja tiene la pestaña Valoración: múltiplo, retorno exigido, proyección, valor razonable, notas a favor/en contra).

## Lo que hace en todas partes
- Claro / oscuro / automático. Modo privado (oculta importes). Buscador (⌘K en PC).
- Guarda una copia de la última lectura en el dispositivo: se abre al instante y luego se actualiza.
- En el móvil, **tirar hacia abajo** vuelve a leer la hoja (enseña la hora de los datos). En PC, botón Actualizar.
- Avisa si hay una versión nueva publicada y se recarga sola.
- Añadida a la pantalla de inicio del iPhone/Android se comporta como una app (sin barra del navegador).

## Lo que NO hace
- No se conecta a tu bróker ni tiene cotizaciones propias: los precios y el cambio del día salen de tu hoja.
- No escribe nunca en tu hoja ni manda tus datos a ningún sitio salvo a tu propio dispositivo.
- No es multiusuario: cada persona, su copia, su script y su clave.
- No da avisos ni notificaciones, ni calcula impuestos (salvo los tramos que pongas en la proyección).
- El calendario de resultados no se rellena solo: necesita la tarea semanal opcional (o que lo metas tú en un JSON).
- Sin conexión enseña la última copia guardada, pero no puede actualizar.
