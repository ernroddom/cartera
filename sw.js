// Service worker de la app Gastos. Su alcance es solo /gastos/,
// así que no toca la caché ni las peticiones de otras apps del dominio.
const CACHE = 'gastos-v10';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192-v4.png', './icon-512-v4.png', './apple-touch-icon-v4.png', './icon-maskable-512-v4.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('gastos-') && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  // Solo los archivos de la propia app; los datos del script van siempre a la red
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;
  e.respondWith(
    fetch(e.request, { cache: 'no-cache' })
      .then((r) => { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy)); return r; })
      .catch(() => caches.match(e.request).then((r) => r || caches.match('./index.html')))
  );
});
