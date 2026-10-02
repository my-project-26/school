const CACHE_NAME = 'schulapp-v5';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

const silbenFiles = [
  "hund_silben", "haus_silben", "frosch_silben", "ball_silben", "baum_silben", "fisch_silben", "maus_silben", "uhr_silben", "brot_silben", "stern_silben",
  "katze_silben", "blume_silben", "sonne_silben", "vogel_silben", "wolke_silben", "lampe_silben", "apfel_silben", "kerze_silben", "schule_silben", "tafel_silben",
  "tasche_silben", "puppe_silben", "biene_silben", "eule_silben", "kirsche_silben", "tomate_silben", "banane_silben", "schmetterling_silben", "elefant_silben", "rakete_silben",
  "gitarre_silben", "zitrone_silben", "delfin_silben", "papagei_silben", "krokodil_silben", "pinguin_silben", "schokolade_silben", "marienkaefer_silben", "schneemann_silben", "regenbogen_silben"
];

silbenFiles.forEach(file => ASSETS.push(`./audio/${file}.mp3`));

for (let a = 1; a <= 10; a++) {
  for (let b = 1; b <= 10; b++) {
    ASSETS.push(`./audio/${a}x${b}.mp3`);
  }
}

for (let n = 1; n <= 20; n++) {
  ASSETS.push(`./audio/zehnerfeld${n}.mp3`);
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('📦 PWA ServiceWorker: Alle Assets & 40 Silben-Audios offline gecacht.');
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
