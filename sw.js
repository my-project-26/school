const CACHE_NAME = 'schulapp-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './audio/apfel.mp3',
  './audio/baer.mp3',
  './audio/fisch.mp3',
  './audio/loewe.mp3',
  './audio/robbe.mp3',
  './audio/eichhoernchen.mp3',
  './audio/ente.mp3',
  './audio/sonne.mp3',
  './audio/tomate.mp3',
  './audio/hund.mp3',
  './audio/katze.mp3',
  './audio/zehnerfeld7.mp3',
  './audio/zehnerfeld12.mp3',
  './audio/haende.mp3',
  './audio/haeuser.mp3',
  './audio/baeume.mp3',
  './audio/maeuse.mp3',
  './audio/laufen.mp3',
  './audio/hund_nomen.mp3',
  './audio/schnell_adj.mp3',
  './audio/halbschriftlich1.mp3'
];

for (let a = 1; a <= 10; a++) {
  for (let b = 1; b <= 10; b++) {
    ASSETS.push(`./audio/${a}x${b}.mp3`);
  }
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('📦 PWA ServiceWorker: Alle Assets & Audio-Dateien offline gecacht.');
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
