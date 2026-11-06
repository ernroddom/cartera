# 5 · Publicar la web (GitHub Pages) y ponerla en el móvil

## Una vez
1. Crea un repositorio en GitHub (p. ej. `cartera`). **Público** si tu cuenta es gratuita: GitHub Pages en repositorios
   privados exige un plan de pago. No pasa nada: lo publicado es solo el programa; tus datos nunca están ahí.
2. Sube **solo el contenido de `web/`** a la raíz de ese repositorio (o a una rama `gh-pages`). No subas `mi-hoja/`, ni
   `apps-script/` con tu clave, ni nada con tu ID de implementación (`AKfy…`).
3. Settings → Pages → Source: «Deploy from a branch», rama `main`, carpeta `/ (root)`. En un minuto estará en
   `https://<usuario>.github.io/<repo>/`.
4. La página lleva `noindex` (no sale en buscadores) y una política de seguridad que solo deja hablar con `script.google.com`.

## Cada cambio
1. Edita `fuente/cartera.html` y **sube el número de versión** (`VER="v1"` → `VER="v2"`).
2. `python3 herramientas/construir.py` (regenera `web/` con las huellas de seguridad nuevas; si no, la página no arranca).
3. Prueba (`node herramientas/probar.js mi-hoja/tu-hoja.xlsx` o servidor local).
4. Sube `web/` al repositorio. En los dispositivos, la web ve que `version.txt` ha cambiado y se recarga sola a los
   pocos segundos de abrirla (por eso, tras publicar, se ve un pequeño parpadeo una vez).
5. Si algo sale mal: vuelve a subir la versión anterior de `web/`.

## En el móvil
- iPhone: abre la dirección en Safari → Compartir → «Añadir a pantalla de inicio». Se abre a pantalla completa como una app.
- Android: Chrome → menú → «Añadir a pantalla de inicio» / «Instalar aplicación».
- El nombre bajo el icono es «Cartera» (`NOMBRE_APP=MiCartera python3 herramientas/construir.py` para cambiarlo).
- La primera vez pide el ID del script y la clave (ver `04-script-de-google.md`).
