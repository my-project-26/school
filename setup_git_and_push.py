import subprocess
import json

# 1. SW.JS an GitHub Pages Unterpfad anpassen (Relative Pfade für Offline-Caching)
sw_content = """const CACHE_NAME = 'schul-app-v8';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './manifest.json',
  './content.json'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});"""

open("sw.js", "w", encoding="utf-8").write(sw_content)

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {cmd}")
    else:
        print(f"⚠️ {cmd}\n{result.stderr.strip()}")

print("🚀 Starte Git-Initialisierung und Push zu GitHub...")

run_cmd("git init")
run_cmd("git config user.name 'Kai Buhmeier'")
run_cmd("git add .")
run_cmd("git commit -m 'Initial commit: Schul-App PWA mit 6 Modulen & Service Worker'")
run_cmd("git branch -M main")
run_cmd("git remote remove origin 2>/dev/null")
run_cmd("git remote add origin https://github.com/my-project-26/school.git")
run_cmd("git push -u origin main")

print("\n🎉 Code erfolgreich auf GitHub hochgeladen!")
