# 4 · El script de Google (cómo llegan los datos a la web publicada)

La web publicada en GitHub no puede leer tu Google Drive por sí sola. Un pequeño **script de Apps Script dentro de tu hoja**
la exporta como .xlsx y se la entrega, solo si la petición trae **tu clave**. Plantilla lista: `apps-script/Code.gs.ejemplo`
(instrucciones de instalación dentro).

## El protocolo (lo que la web espera)
- Petición: `POST https://script.google.com/macros/s/<ID de implementación>/exec`, cuerpo de texto JSON `{"k":"<clave>"}`
  (la clave va en el cuerpo, nunca en la dirección).
- Respuesta correcta: `{"ok":true,"xlsx":"<base64 del .xlsx>"}`. Clave mala: `{"ok":false,"error":"clave"}` (la web vuelve a
  pedirla). Otro error: `{"ok":false,"error":"texto"}`.
- Calendario (opcional): `{"k":"…","q":"informe"}` → `{"ok":true,"ix":{…indice.json…},"emp":{}}`. Si el script no lo
  implementa, responde `{"ok":true}` sin `ix` y la web lo entiende.
- La web corta a los 45 s y entonces avisa «Google Drive no responde»; Google suele tardar de 2 a 6 s.

## El primer acceso en cada dispositivo
- Enlace personal: `https://<usuario>.github.io/<repo>/#d=<ID de implementación>&k=<clave>`. La web guarda ID y clave en
  ese dispositivo (localStorage) y borra el enlace de la barra. **Ese enlace es una contraseña**: no lo pegues en chats ni
  correos; mejor ábrelo una vez escribiéndolo o desde una nota privada.
- En el iPhone, la app de la pantalla de inicio no comparte lo guardado con Safari: la primera vez aparece un formulario
  para pegar el ID (empieza por `AKfy`) y la clave.
- Opciones → «Quitar clave» borra ID, clave y la copia de los datos de ese dispositivo.

## Cambiar la clave
Cambia `SECRETO` en el script, haz **una nueva versión** de la implementación y vuelve a meter la clave en cada dispositivo.

## Otras formas de cargar datos (ya incluidas en la web)
- **Archivo local:** si no hay script configurado, el aviso de acceso ofrece «Abrir un archivo .xlsx». Útil para probar.
- **Dentro de Claude:** la web funciona también como artefacto de Claude, leyendo la hoja con el conector de Google Drive
  (`FILE_ID` en el código; en la versión publicada va vacío).
- **Servida desde tu Google:** si la web se publica como aplicación de Apps Script (HtmlService), usa `google.script.run.getXlsx()`.
  Es más lento y con la barra de aviso de Google; no lo recomendamos.
