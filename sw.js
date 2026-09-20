const CACHE_NAME = 'schulapp-v1';
const ASSETS = [
    './',
    './index.html',
    './manifest.json',
    './audio/Baer.mp3',
    './audio/Baeren.mp3',
    './audio/Baeume.mp3',
    './audio/Haende.mp3',
    './audio/Haeuser.mp3',
    './audio/Affe.mp3',
    './audio/Elefant.mp3',
    './audio/Ananas.mp3'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((res) => res || fetch(e.request))
    );
});
