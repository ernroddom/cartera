# 9 · Seguridad y privacidad

- **Lo publicado en GitHub es solo el programa.** Tus datos no están en el repositorio: viajan de tu script de Google a tu
  dispositivo cuando abres la web, y solo si traes tu clave.
- **La clave** (y el ID de implementación `AKfy…`) se guardan únicamente en el dispositivo (localStorage). Nunca en el
  código, nunca en GitHub, nunca en un chat. El enlace personal `#d=…&k=…` es una contraseña.
- **`Code.gs` con la clave no se sube nunca** a GitHub. `construir.py` se niega a dar por buena una `web/` con un `AKfy…`
  o un `.gs`. Revisa también tú antes de cada subida (`git diff --stat`).
- La página lleva una **política de seguridad (CSP)**: solo ejecuta sus propios scripts (por su huella) y las dos
  bibliotecas incluidas, y solo puede conectarse a `script.google.com`. No carga nada de otras webs (fuentes y bibliotecas
  van junto a la página). Por eso, si cambias el código sin reconstruir, la página no arranca.
- `noindex` y `no-referrer`: no sale en buscadores ni filtra la dirección a terceros.
- En el dispositivo se guarda una copia de la última lectura (IndexedDB) para abrir al instante. «Quitar clave» en
  Opciones la borra junto con la clave. Si dejas el móvil a otra persona, el **modo privado** tapa los importes.
- El script de ejemplo compara la clave en tiempo constante y no entrega nada sin ella. Usa una clave larga y aleatoria y
  no la reutilices.
