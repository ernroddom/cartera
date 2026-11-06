# 6 · Calendario de resultados (opcional)

La pestaña Calendario junta dos cosas:
- **Dividendos previstos**: salen solos de tu pestaña Dividendos (filas con fecha futura). No hay que hacer nada.
- **Fechas de presentación de resultados** de tus empresas y del universo: no están en la hoja; las trae un archivo
  `indice.json` que prepara una **tarea semanal** (por ejemplo, una tarea programada de Claude cada lunes) y que el script
  de Google entrega a la web. Sin ese archivo, el calendario funciona solo con dividendos y lo dice.
- «Por revisar» (Universo y ficha) también usa estas fechas: una empresa está por revisar si presentó resultados después
  de la fecha de tu última valoración (o si la valoraste hace más de un año).

## Dónde se guarda
Una carpeta en tu Google Drive (p. ej. `Informes`) con una subcarpeta por semana con el nombre de su lunes (`2026-11-02`), y
dentro `indice.json`. En el script, pon el ID de esa carpeta en `CARPETA_CALENDARIO`. La web pide el más reciente.

## Formato de `indice.json` (ejemplo completo en `calendario/ejemplo-indice.json`)
```json
{ "semana": "2026-11-02", "generado": "2026-11-02T08:00:00+01:00", "tipo": "calendario",
  "empresas": [ { "ticker": "NYSE:KO", "nombre": "Coca-Cola",
      "ultimos":  { "fecha": "2026-10-21", "periodo": "3T 2026" },
      "proximos": { "fecha": "2027-02-10", "periodo": "4T 2026", "estado": "estimada", "hora": "" } } ] }
```
- `ticker` exactamente como en tu hoja. `fecha` en formato `AAAA-MM-DD`.
- `estado`: `"confirmada"` (la empresa la ha anunciado) o `"estimada"` (sale con un «?» en el calendario).
- `hora`: `"antes de la apertura"`, `"tras el cierre"` o `""` (sale con un sol o una luna).

## Instrucciones para la tarea semanal (pégalas en la tarea programada de tu Claude)
> Cada lunes, para cada empresa de mi hoja (pestañas Cartera y Preselección, sin opciones): busca la fecha de su última
> presentación de resultados y la de la próxima (web de relaciones con inversores primero; si no, calendarios fiables).
> Escribe `indice.json` con el formato de `docs/06-calendario.md`: `tipo: "calendario"`, `semana` = el lunes de esta semana,
> `generado` = ahora con zona horaria, `estado` `"confirmada"` solo si lo ha anunciado la empresa, `hora` solo si se conoce.
> Súbelo a mi carpeta de Drive `Informes/<AAAA-MM-DD>/indice.json` (si la semana ya existe, sustituye el archivo).
