import os
import subprocess
import json

# 1. ORDNERSSTRUKTUR & DEPLOYMENT-WORKFLOW
os.makedirs(".github/workflows", exist_ok=True)

workflow_yaml = """name: Deploy Static PWA to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""

open(".github/workflows/static.yml", "w", encoding="utf-8").write(workflow_yaml)
open(".nojekyll", "w").write("")

gitignore_content = """venv/
__pycache__/
*.pyc
.DS_Store
"""
open(".gitignore", "w", encoding="utf-8").write(gitignore_content)

# 2. INDEX.HTML
html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Schul-App: Lernstudio BW</title>
    <link rel="stylesheet" href="./style.css?v=18">
    <link rel="manifest" href="./manifest.json">
    <meta name="theme-color" content="#4A90E2">
</head>
<body>

    <!-- Start-Overlay für Audio-Unlock (Safari/iOS Autoplay Policy Fix) -->
    <div id="start-overlay" class="overlay">
        <div class="card start-card">
            <h1>Willkommen im Lernstudio! 🎈</h1>
            <p>Tippe auf den Knopf, um das Lernspiel zu starten.</p>
            <button id="btn-start" class="btn-primary">Lernstudio Öffnen 🚀</button>
        </div>
    </div>

    <!-- Mobile Navigation Drawer / Modal -->
    <div id="mobile-menu-drawer" class="menu-drawer hidden">
        <div class="drawer-content">
            <div class="drawer-header">
                <h2>Modul wählen</h2>
                <button id="btn-close-menu" class="btn-close">✕</button>
            </div>
            <div class="drawer-section">
                <h3>1. Klasse</h3>
                <button class="drawer-btn active" data-target="k1-anlaut">🔊 Anlaute hören</button>
                <button class="drawer-btn" data-target="k1-silben">🌊 Silben schwingen</button>
                <button class="drawer-btn" data-target="k1-zehner">🔴 Zehnerfeld</button>
            </div>
            <div class="drawer-section">
                <h3>3. Klasse</h3>
                <button class="drawer-btn" data-target="k3-math">🧮 1x1 Blitzrechnen</button>
                <button class="drawer-btn" data-target="k3-halb">➕ Halbschriftlich</button>
                <button class="drawer-btn" data-target="k3-lang">📝 Wortarten bestimmen</button>
                <button class="drawer-btn" data-target="k3-spell">✍️ Rechtschreibung</button>
            </div>
        </div>
    </div>

    <header>
        <!-- Desktop Tabs -->
        <div class="nav-tabs desktop-only">
            <button id="tab-k1-anlaut" class="tab-btn active">1. Kl: Anlaute 🔊</button>
            <button id="tab-k1-silben" class="tab-btn">1. Kl: Silben 🌊</button>
            <button id="tab-k1-zehner" class="tab-btn">1. Kl: Zehnerfeld 🔴</button>
            <button id="tab-k3-math" class="tab-btn">3. Kl: 1x1 🧮</button>
            <button id="tab-k3-halb" class="tab-btn">3. Kl: Halbschriftlich ➕</button>
            <button id="tab-k3-lang" class="tab-btn">3. Kl: Wortarten 📝</button>
            <button id="tab-k3-spell" class="tab-btn">3. Kl: Rechtschreibung ✍️</button>
        </div>

        <!-- Mobile Menu Trigger -->
        <button id="btn-open-menu" class="mobile-menu-btn mobile-only">
            ☰ <span id="current-module-title">Anlaute</span>
        </button>

        <div id="score-display">Punkte: <span id="score">0</span></div>
    </header>

    <main class="container">
        <!-- MODUL 1. KLASSE: ANLAUTE -->
        <section id="module-k1-anlaut" class="module-card">
            <div class="card game-card">
                <h2>Anlaute Hören</h2>
                <p class="instruction">Welcher Anlaut gehört zum Bild?</p>
                <button id="btn-play-audio" class="btn-audio" aria-label="Wort noch einmal anhören">🔊 Wort anhören</button>
                <div class="image-container"><span id="word-emoji" class="emoji-display">❓</span></div>
                <div id="letter-options" class="options-grid"></div>
            </div>
        </section>

        <!-- MODUL 1. KLASSE: SILBEN SCHWINGEN -->
        <section id="module-k1-silben" class="module-card hidden">
            <div class="card game-card">
                <h2>Silben Schwingen</h2>
                <p class="instruction">Wie viele Silben hat das Wort?</p>
                <button id="btn-play-silben-audio" class="btn-audio">🔊 Wort anhören</button>
                <div class="image-container"><span id="silben-emoji" class="emoji-display">❓</span></div>
                <div id="silben-options" class="silben-grid">
                    <button class="btn-silbe" data-count="1">1 Silbe 0</button>
                    <button class="btn-silbe" data-count="2">2 Silben 🌊🌊</button>
                    <button class="btn-silbe" data-count="3">3 Silben 🌊🌊🌊</button>
                    <button class="btn-silbe" data-count="4">4 Silben 🌊🌊🌊🌊</button>
                </div>
            </div>
        </section>

        <!-- MODUL 1. KLASSE: ZEHNERFELD -->
        <section id="module-k1-zehner" class="module-card hidden">
            <div class="card game-card">
                <h2>Zehnerfeld: Mengen erfassen</h2>
                <p class="instruction">Wie viele Punkte siehst du?</p>
                <div id="ten-frame" class="ten-frame-grid"></div>
                <div id="zehner-options" class="numpad-grid" style="margin-top: 1.5rem;"></div>
            </div>
        </section>

        <!-- MODUL 3. KLASSE: 1x1 TRAINER -->
        <section id="module-k3-math" class="module-card hidden">
            <div class="card game-card">
                <h2>1x1 Blitzrechnen</h2>
                <div class="math-problem">
                    <span id="math-task">3 × 4 =</span>
                    <span id="math-input" class="input-display">?</span>
                </div>
                <div class="numpad-grid">
                    <button class="btn-num" data-val="1">1</button>
                    <button class="btn-num" data-val="2">2</button>
                    <button class="btn-num" data-val="3">3</button>
                    <button class="btn-num" data-val="4">4</button>
                    <button class="btn-num" data-val="5">5</button>
                    <button class="btn-num" data-val="6">6</button>
                    <button class="btn-num" data-val="7">7</button>
                    <button class="btn-num" data-val="8">8</button>
                    <button class="btn-num" data-val="9">9</button>
                    <button class="btn-num btn-action" data-val="clear">C</button>
                    <button class="btn-num" data-val="0">0</button>
                    <button class="btn-num btn-action-submit" id="btn-submit-math">OK</button>
                </div>
            </div>
        </section>

        <!-- MODUL 3. KLASSE: HALBSCHRIFTLICHES RECHNEN -->
        <section id="module-k3-halb" class="module-card hidden">
            <div class="card game-card">
                <h2>Halbschriftlich Addieren</h2>
                <p class="instruction">Löse Schritt für Schritt im ZR 1.000:</p>
                <div class="halb-problem">
                    <span id="halb-main-task">340 + 280 = ?</span>
                </div>
                <div class="step-container">
                    <div class="step-row">
                        <span id="step1-label">340 + 200 =</span>
                        <span id="step1-input" class="input-display active-field">?</span>
                    </div>
                    <div class="step-row">
                        <span id="step2-label">540 + 80 =</span>
                        <span id="step2-input" class="input-display">?</span>
                    </div>
                </div>
                <div class="numpad-grid" style="margin-top: 1rem;">
                    <button class="btn-num-halb" data-val="1">1</button>
                    <button class="btn-num-halb" data-val="2">2</button>
                    <button class="btn-num-halb" data-val="3">3</button>
                    <button class="btn-num-halb" data-val="4">4</button>
                    <button class="btn-num-halb" data-val="5">5</button>
                    <button class="btn-num-halb" data-val="6">6</button>
                    <button class="btn-num-halb" data-val="7">7</button>
                    <button class="btn-num-halb" data-val="8">8</button>
                    <button class="btn-num-halb" data-val="9">9</button>
                    <button class="btn-num-halb btn-action" data-val="clear">C</button>
                    <button class="btn-num-halb" data-val="0">0</button>
                    <button class="btn-num-halb btn-action-submit" id="btn-submit-halb">OK</button>
                </div>
            </div>
        </section>

        <!-- MODUL 3. KLASSE: WORTARTEN -->
        <section id="module-k3-lang" class="module-card hidden">
            <div class="card game-card">
                <h2>Wortarten Bestimmen</h2>
                <p class="instruction">Bestimme die Wortart des hervorgehobenen Worts:</p>
                <div class="sentence-box">
                    <p id="grammar-sentence">Der <strong id="target-word" class="highlight">schnelle</strong> Hund rennt.</p>
                </div>
                <div id="grammar-options" class="grammar-grid">
                    <button class="btn-grammar btn-nomen" data-type="Nomen">Nomen</button>
                    <button class="btn-grammar btn-verb" data-type="Verb">Verb</button>
                    <button class="btn-grammar btn-adjektiv" data-type="Adjektiv">Adjektiv</button>
                </div>
            </div>
        </section>

        <!-- MODUL 3. KLASSE: RECHTSCHREIBSTRATEGIEN -->
        <section id="module-k3-spell" class="module-card hidden">
            <div class="card game-card">
                <h2>Rechtschreibstrategien</h2>
                <p id="spell-instruction" class="instruction">Verlängere das Wort: Hun...</p>
                <div class="sentence-box">
                    <p id="spell-word-display" class="spell-display">Hun<span class="gap">?</span></p>
                    <p id="spell-hint" class="spell-hint">💡 Verlängerung: Hun-de</p>
                </div>
                <div id="spell-options" class="options-grid"></div>
            </div>
        </section>
    </main>

    <script src="./app.js?v=18"></script>
</body>
</html>"""

# 3. STYLE.CSS
css_content = """:root {
    --bg-color: #F0F4F8;
    --card-bg: #FFFFFF;
    --primary-color: #4A90E2;
    --success-color: #50E3C2;
    --text-color: #2C3E50;
    --font-family: system-ui, -apple-system, sans-serif;
    --nomen-color: #3B82F6;
    --verb-color: #EF4444;
    --adjektiv-color: #EAB308;
}

* { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
body { 
    font-family: var(--font-family); 
    background-color: var(--bg-color); 
    color: var(--text-color); 
    min-height: 100vh; 
    display: flex; 
    flex-direction: column; 
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
}

header { 
    background-color: var(--primary-color); 
    color: white; 
    padding: 0.8rem 1rem; 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
}

.mobile-only { display: none !important; }
.desktop-only { display: flex !important; }

@media (max-width: 700px) {
    .mobile-only { display: flex !important; }
    .desktop-only { display: none !important; }
}

.nav-tabs { display: flex; gap: 0.4rem; overflow-x: auto; }
.tab-btn { background: rgba(255, 255, 255, 0.2); border: none; color: white; padding: 0.5rem 0.8rem; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 0.85rem; white-space: nowrap; transition: background 0.2s; }
.tab-btn.active { background: white; color: var(--primary-color); }

.mobile-menu-btn {
    background: white;
    color: var(--primary-color);
    border: none;
    padding: 0.6rem 1rem;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.menu-drawer {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 2000;
    display: flex;
    justify-content: flex-start;
}

.drawer-content {
    background: white;
    width: 80%;
    max-width: 320px;
    height: 100%;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    box-shadow: 4px 0 16px rgba(0,0,0,0.2);
    overflow-y: auto;
}

.drawer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--bg-color);
    padding-bottom: 0.8rem;
}

.drawer-header h2 { color: var(--primary-color); font-size: 1.3rem; }
.btn-close { background: none; border: none; font-size: 1.8rem; color: #94A3B8; cursor: pointer; padding: 0.2rem 0.5rem; }

.drawer-section { display: flex; flex-direction: column; gap: 0.5rem; }
.drawer-section h3 { font-size: 0.9rem; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.5px; margin-bottom: 0.2rem; }

.drawer-btn {
    background: var(--bg-color);
    border: 2px solid transparent;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    font-size: 1rem;
    font-weight: bold;
    color: var(--text-color);
    text-align: left;
    cursor: pointer;
}

.drawer-btn.active {
    border-color: var(--primary-color);
    background: #EBF8FF;
    color: var(--primary-color);
}

#score-display { font-weight: bold; font-size: 1.1rem; background: rgba(0,0,0,0.15); padding: 0.5rem 1rem; border-radius: 12px; white-space: nowrap; }
.container { flex: 1; display: flex; justify-content: center; align-items: center; padding: 1rem; }
.module-card { width: 100%; max-width: 500px; }
.hidden { display: none !important; }
.card { background: var(--card-bg); border-radius: 20px; padding: 1.8rem; width: 100%; box-shadow: 0 8px 24px rgba(0,0,0,0.08); text-align: center; }
.card h2 { margin-bottom: 0.8rem; color: var(--primary-color); }
.instruction { font-size: 1.1rem; margin-bottom: 1rem; font-weight: 600; }
.btn-audio { background-color: #FFE066; border: none; border-radius: 12px; padding: 0.8rem 1.5rem; font-size: 1.1rem; font-weight: bold; cursor: pointer; min-height: 50px; margin-bottom: 1rem; }
.image-container { height: 100px; display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem; }
.emoji-display { font-size: 4.5rem; }
.options-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.8rem; }
.btn-option { background-color: var(--bg-color); border: 3px solid var(--primary-color); border-radius: 16px; font-size: 2.2rem; font-weight: bold; color: var(--primary-color); padding: 0.8rem; min-height: 65px; cursor: pointer; }

/* RECHTSCHREIBSTRATEGIEN STYLES */
.spell-display { font-size: 2.8rem; font-weight: bold; letter-spacing: 2px; }
.gap { color: var(--primary-color); border-bottom: 4px solid var(--primary-color); padding: 0 0.3rem; }
.spell-hint { font-size: 1rem; color: #64748B; font-weight: 600; margin-top: 0.8rem; }

.ten-frame-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; background: #E2E8F0; padding: 12px; border-radius: 16px; border: 3px solid #CBD5E1; max-width: 300px; margin: 0 auto; }
.ten-frame-cell { aspect-ratio: 1; background: white; border-radius: 50%; border: 2px dashed #94A3B8; display: flex; justify-content: center; align-items: center; }
.ten-frame-cell.dot { background: #EF4444; border: 2px solid #B91C1C; box-shadow: inset 0 -2px 4px rgba(0,0,0,0.2); }

.silben-grid { display: grid; grid-template-columns: repeat(1, 1fr); gap: 0.8rem; }
.btn-silbe { background-color: var(--bg-color); border: 2px solid var(--primary-color); border-radius: 14px; font-size: 1.2rem; font-weight: bold; color: var(--primary-color); padding: 0.9rem; min-height: 55px; cursor: pointer; }

.math-problem, .halb-problem { font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0 1rem 0; display: flex; justify-content: center; align-items: center; gap: 0.8rem; }
.step-container { display: flex; flex-direction: column; gap: 0.8rem; margin-bottom: 1rem; }
.step-row { font-size: 1.4rem; font-weight: bold; display: flex; justify-content: center; align-items: center; gap: 0.6rem; }

.input-display { background: var(--bg-color); border: 3px solid #CBD5E1; border-radius: 12px; padding: 0.2rem 0.8rem; min-width: 80px; color: var(--text-color); }
.input-display.active-field { border-color: var(--primary-color); background: #EBF8FF; color: var(--primary-color); }

.numpad-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; max-width: 320px; margin: 0 auto; }
.btn-num, .btn-num-halb { background-color: var(--bg-color); border: 2px solid #CBD5E1; border-radius: 14px; font-size: 1.8rem; font-weight: bold; color: var(--text-color); min-height: 55px; cursor: pointer; }
.btn-action { background-color: #FCA5A5; color: #991B1B; }
.btn-action-submit { background-color: var(--success-color); color: #065F46; }

.sentence-box { background: var(--bg-color); padding: 1.2rem; border-radius: 12px; font-size: 1.3rem; margin-bottom: 1.5rem; }
.highlight { color: var(--primary-color); text-decoration: underline; }
.grammar-grid { display: flex; flex-direction: column; gap: 0.8rem; }
.btn-grammar { border: none; border-radius: 12px; padding: 1rem; font-size: 1.2rem; font-weight: bold; color: white; cursor: pointer; }
.btn-nomen { background-color: var(--nomen-color); }
.btn-verb { background-color: var(--verb-color); }
.btn-adjektiv { background-color: var(--adjektiv-color); }

.shake { animation: shake 0.4s ease-in-out; }
@keyframes shake { 0%, 100% { transform: translateX(0); } 20%, 60% { transform: translateX(-8px); } 40%, 80% { transform: translateX(8px); } }
.overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.btn-primary { background-color: var(--success-color); border: none; border-radius: 12px; padding: 1rem 2rem; font-size: 1.3rem; font-weight: bold; color: #1A3636; margin-top: 1.5rem; cursor: pointer; }"""

# 4. APP.JS
js_content = """if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js')
        .then(() => console.log('Service Worker aktiv.'))
        .catch(err => console.log('SW Fehler:', err));
}

let score = parseInt(localStorage.getItem('school_app_score') || '0');

let dynamicGrammarTasks = [];
fetch('./content.json')
    .then(res => res.json())
    .then(data => {
        if (data.klasse3_wortarten && data.klasse3_wortarten.length > 0) {
            dynamicGrammarTasks = data.klasse3_wortarten;
        }
    }).catch(() => {});

// Navigation Mapping
const modules = {
    'k1-anlaut': { tab: document.getElementById('tab-k1-anlaut'), mod: document.getElementById('module-k1-anlaut'), title: 'Anlaute', init: null },
    'k1-silben': { tab: document.getElementById('tab-k1-silben'), mod: document.getElementById('module-k1-silben'), title: 'Silben', init: () => loadTaskSilben(indexSilben) },
    'k1-zehner': { tab: document.getElementById('tab-k1-zehner'), mod: document.getElementById('module-k1-zehner'), title: 'Zehnerfeld', init: initZehnerTask },
    'k3-math': { tab: document.getElementById('tab-k3-math'), mod: document.getElementById('module-k3-math'), title: '1x1 Blitz', init: initMathTask },
    'k3-halb': { tab: document.getElementById('tab-k3-halb'), mod: document.getElementById('module-k3-halb'), title: 'Halbschriftlich', init: initHalbTask },
    'k3-lang': { tab: document.getElementById('tab-k3-lang'), mod: document.getElementById('module-k3-lang'), title: 'Wortarten', init: initGrammarTask },
    'k3-spell': { tab: document.getElementById('tab-k3-spell'), mod: document.getElementById('module-k3-spell'), title: 'Rechtschreibung', init: initSpellTask }
};

const scoreDisplay = document.getElementById('score');
scoreDisplay.textContent = score;

function updateScore(points) {
    score += points;
    localStorage.setItem('school_app_score', score);
    scoreDisplay.textContent = score;
}

function selectModule(key) {
    Object.keys(modules).forEach(k => {
        if (modules[k].tab) modules[k].tab.classList.remove('active');
        if (modules[k].mod) modules[k].mod.classList.add('hidden');
    });

    const active = modules[key];
    if (active) {
        if (active.tab) active.tab.classList.add('active');
        if (active.mod) active.mod.classList.remove('hidden');
        document.getElementById('current-module-title').textContent = active.title;
        
        document.querySelectorAll('.drawer-btn').forEach(btn => {
            if (btn.getAttribute('data-target') === key) btn.classList.add('active');
            else btn.classList.remove('active');
        });

        if (active.init) active.init();
    }
}

Object.keys(modules).forEach(key => {
    if (modules[key].tab) {
        modules[key].tab.addEventListener('click', () => selectModule(key));
    }
});

const menuDrawer = document.getElementById('mobile-menu-drawer');
const btnOpenMenu = document.getElementById('btn-open-menu');
const btnCloseMenu = document.getElementById('btn-close-menu');

btnOpenMenu.addEventListener('click', () => menuDrawer.classList.remove('hidden'));
btnCloseMenu.addEventListener('click', () => menuDrawer.classList.add('hidden'));

document.querySelectorAll('.drawer-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const targetKey = btn.getAttribute('data-target');
        selectModule(targetKey);
        menuDrawer.classList.add('hidden');
    });
});

let currentAudio = null;
function playAudioFile(path) {
    if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; }
    currentAudio = new Audio(path);
    currentAudio.play().catch(e => console.log("Audio blockiert:", e));
}

// KLASSE 1: ANLAUTE
const taskDataK1 = [
    { word: 'Affe', letter: 'A', emoji: '🐒', audio: 'audio/Affe.mp3' },
    { word: 'Apfel', letter: 'A', emoji: '🍎', audio: 'audio/Apfel.mp3' },
    { word: 'Bär', letter: 'B', emoji: '🐻', audio: 'audio/Baer.mp3' },
    { word: 'Ball', letter: 'B', emoji: '⚽', audio: 'audio/Ball.mp3' },
    { word: 'Elefant', letter: 'E', emoji: '🐘', audio: 'audio/Elefant.mp3' },
    { word: 'Fisch', letter: 'F', emoji: '🐟', audio: 'audio/Fisch.mp3' },
    { word: 'Gitarre', letter: 'G', emoji: '🎸', audio: 'audio/Gitarre.mp3' },
    { word: 'Hase', letter: 'H', emoji: '🐰', audio: 'audio/Hase.mp3' },
    { word: 'Igel', letter: 'I', emoji: '🦔', audio: 'audio/Igel.mp3' },
    { word: 'Krokodil', letter: 'K', emoji: '🐊', audio: 'audio/Krokodil.mp3' },
    { word: 'Löwe', letter: 'L', emoji: '🦁', audio: 'audio/Loewe.mp3' },
    { word: 'Maus', letter: 'M', emoji: '🐭', audio: 'audio/Maus.mp3' },
    { word: 'Nase', letter: 'N', emoji: '👃', audio: 'audio/Nase.mp3' },
    { word: 'Oma', letter: 'O', emoji: '👵', audio: 'audio/Oma.mp3' },
    { word: 'Pinguin', letter: 'P', emoji: '🐧', audio: 'audio/Pinguin.mp3' },
    { word: 'Sonne', letter: 'S', emoji: '☀️', audio: 'audio/Sonne.mp3' },
    { word: 'Trommel', letter: 'T', emoji: '🥁', audio: 'audio/Trommel.mp3' },
    { word: 'Uhr', letter: 'U', emoji: '⏰', audio: 'audio/Uhr.mp3' },
    { word: 'Vogel', letter: 'V', emoji: '🐦', audio: 'audio/Vogel.mp3' },
    { word: 'Zebra', letter: 'Z', emoji: '🦓', audio: 'audio/Zebra.mp3' }
];

let indexK1 = 0;
const startOverlay = document.getElementById('start-overlay');
const btnStart = document.getElementById('btn-start');
const btnPlayAudio = document.getElementById('btn-play-audio');
const wordEmoji = document.getElementById('word-emoji');
const letterOptionsContainer = document.getElementById('letter-options');

btnStart.addEventListener('click', () => { startOverlay.style.display = 'none'; loadTaskK1(indexK1); });

function loadTaskK1(index) {
    const task = taskDataK1[index];
    wordEmoji.textContent = task.emoji;
    const choices = generateChoicesK1(task.letter);
    letterOptionsContainer.innerHTML = '';
    choices.forEach(letter => {
        const btn = document.createElement('button');
        btn.className = 'btn-option';
        btn.textContent = letter;
        btn.addEventListener('click', () => handleChoiceK1(letter, task.letter));
        letterOptionsContainer.appendChild(btn);
    });
    setTimeout(() => playAudioFile(task.audio), 300);
}

function generateChoicesK1(correct) {
    const all = ['A', 'B', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'S', 'T', 'U', 'V', 'Z'];
    const choices = new Set([correct]);
    while (choices.size < 4) choices.add(all[Math.floor(Math.random() * all.length)]);
    return Array.from(choices).sort(() => Math.random() - 0.5);
}

function handleChoiceK1(selected, correct) {
    if (selected === correct) {
        updateScore(10);
        indexK1 = (indexK1 + 1) % taskDataK1.length;
        loadTaskK1(indexK1);
    } else {
        const card = document.querySelector('#module-k1-anlaut .game-card');
        card.classList.add('shake');
        playAudioFile(taskDataK1[indexK1].audio);
        setTimeout(() => card.classList.remove('shake'), 400);
    }
}
btnPlayAudio.addEventListener('click', () => playAudioFile(taskDataK1[indexK1].audio));

// KLASSE 1: SILBEN
const silbenData = [
    { word: 'Bär', syllables: 1, emoji: '🐻', audio: 'audio/Baer.mp3' },
    { word: 'Affe', syllables: 2, emoji: '🐒', audio: 'audio/Affe.mp3' },
    { word: 'Elefant', syllables: 3, emoji: '🐘', audio: 'audio/Elefant.mp3' },
    { word: 'Krokodil', syllables: 3, emoji: '🐊', audio: 'audio/Krokodil.mp3' },
    { word: 'Pinguin', syllables: 2, emoji: '🐧', audio: 'audio/Pinguin.mp3' }
];

let indexSilben = 0;
const silbenEmoji = document.getElementById('silben-emoji');
function loadTaskSilben(index) {
    const task = silbenData[index];
    silbenEmoji.textContent = task.emoji;
    setTimeout(() => playAudioFile(task.audio), 300);
}

document.getElementById('btn-play-silben-audio').addEventListener('click', () => playAudioFile(silbenData[indexSilben].audio));

document.querySelectorAll('.btn-silbe').forEach(btn => {
    btn.addEventListener('click', () => {
        const count = parseInt(btn.getAttribute('data-count'), 10);
        if (count === silbenData[indexSilben].syllables) {
            updateScore(10);
            indexSilben = (indexSilben + 1) % silbenData.length;
            loadTaskSilben(indexSilben);
        } else {
            const card = document.querySelector('#module-k1-silben .game-card');
            card.classList.add('shake');
            playAudioFile(silbenData[indexSilben].audio);
            setTimeout(() => card.classList.remove('shake'), 400);
        }
    });
});

// KLASSE 1: ZEHNERFELD
let currentZehnerCount = 0;
const tenFrameEl = document.getElementById('ten-frame');
const zehnerOptionsEl = document.getElementById('zehner-options');

function initZehnerTask() {
    currentZehnerCount = Math.floor(Math.random() * 10) + 1;
    tenFrameEl.innerHTML = '';
    for (let i = 0; i < 10; i++) {
        const cell = document.createElement('div');
        cell.className = 'ten-frame-cell' + (i < currentZehnerCount ? ' dot' : '');
        tenFrameEl.appendChild(cell);
    }
    zehnerOptionsEl.innerHTML = '';
    const choices = new Set([currentZehnerCount]);
    while (choices.size < 4) choices.add(Math.floor(Math.random() * 10) + 1);
    Array.from(choices).sort((a,b) => a-b).forEach(num => {
        const btn = document.createElement('button');
        btn.className = 'btn-num';
        btn.textContent = num;
        btn.addEventListener('click', () => {
            if (num === currentZehnerCount) {
                updateScore(10);
                initZehnerTask();
            } else {
                const card = document.querySelector('#module-k1-zehner .game-card');
                card.classList.add('shake');
                setTimeout(() => card.classList.remove('shake'), 400);
            }
        });
        zehnerOptionsEl.appendChild(btn);
    });
}

// KLASSE 3: MATHE 1x1
let factorA = 0, factorB = 0, inputStr = "";
const mathTaskEl = document.getElementById('math-task');
const mathInputEl = document.getElementById('math-input');

function initMathTask() {
    factorA = Math.floor(Math.random() * 10) + 1;
    factorB = Math.floor(Math.random() * 10) + 1;
    inputStr = "";
    mathTaskEl.textContent = `${factorA} × ${factorB} =`;
    mathInputEl.textContent = "?";
}

document.querySelectorAll('#module-k3-math .btn-num').forEach(btn => {
    btn.addEventListener('click', () => {
        const val = btn.getAttribute('data-val');
        if (val === 'clear') { inputStr = ""; mathInputEl.textContent = "?"; }
        else if (val !== null && inputStr.length < 3) {
            inputStr += val;
            mathInputEl.textContent = inputStr;
        }
    });
});

document.getElementById('btn-submit-math').addEventListener('click', () => {
    if (!inputStr) return;
    if (parseInt(inputStr, 10) === factorA * factorB) {
        updateScore(15);
        initMathTask();
    } else {
        const card = document.querySelector('#module-k3-math .game-card');
        card.classList.add('shake');
        inputStr = ""; mathInputEl.textContent = "?";
        setTimeout(() => card.classList.remove('shake'), 400);
    }
});

// KLASSE 3: HALBSCHRIFTLICH
let halbNum1 = 0, halbNum2 = 0, h100 = 0, z10 = 0;
let currentStep = 1; 
let step1Str = "", step2Str = "";

const step1InputEl = document.getElementById('step1-input');
const step2InputEl = document.getElementById('step2-input');

function initHalbTask() {
    halbNum1 = (Math.floor(Math.random() * 40) + 10) * 10;
    h100 = (Math.floor(Math.random() * 3) + 1) * 100;
    z10 = (Math.floor(Math.random() * 8) + 1) * 10;
    halbNum2 = h100 + z10;

    document.getElementById('halb-main-task').textContent = `${halbNum1} + ${halbNum2} = ?`;
    document.getElementById('step1-label').textContent = `${halbNum1} + ${h100} =`;
    
    currentStep = 1;
    step1Str = ""; step2Str = "";
    step1InputEl.textContent = "?";
    step2InputEl.textContent = "?";
    
    step1InputEl.classList.add('active-field');
    step2InputEl.classList.remove('active-field');

    document.getElementById('step2-label').textContent = `... + ${z10} =`;
}

document.querySelectorAll('.btn-num-halb').forEach(btn => {
    btn.addEventListener('click', () => {
        const val = btn.getAttribute('data-val');
        if (val === 'clear') {
            if (currentStep === 1) { step1Str = ""; step1InputEl.textContent = "?"; }
            else { step2Str = ""; step2InputEl.textContent = "?"; }
        } else if (val !== null) {
            if (currentStep === 1 && step1Str.length < 4) {
                step1Str += val;
                step1InputEl.textContent = step1Str;
            } else if (currentStep === 2 && step2Str.length < 4) {
                step2Str += val;
                step2InputEl.textContent = step2Str;
            }
        }
    });
});

document.getElementById('btn-submit-halb').addEventListener('click', () => {
    const targetStep1 = halbNum1 + h100;
    const targetStep2 = targetStep1 + z10;

    if (currentStep === 1) {
        if (parseInt(step1Str, 10) === targetStep1) {
            currentStep = 2;
            step1InputEl.classList.remove('active-field');
            step2InputEl.classList.add('active-field');
            document.getElementById('step2-label').textContent = `${targetStep1} + ${z10} =`;
        } else {
            const card = document.querySelector('#module-k3-halb .game-card');
            card.classList.add('shake');
            step1Str = ""; step1InputEl.textContent = "?";
            setTimeout(() => card.classList.remove('shake'), 400);
        }
    } else if (currentStep === 2) {
        if (parseInt(step2Str, 10) === targetStep2) {
            updateScore(20);
            initHalbTask();
        } else {
            const card = document.querySelector('#module-k3-halb .game-card');
            card.classList.add('shake');
            step2Str = ""; step2InputEl.textContent = "?";
            setTimeout(() => card.classList.remove('shake'), 400);
        }
    }
});

// KLASSE 3: WORTARTEN
const fallbackGrammarTasks = [
    { sentence: 'Der schnelle Hund rennt.', target: 'schnelle', type: 'Adjektiv' },
    { sentence: 'Die Katze schläft auf dem Sofa.', target: 'Katze', type: 'Nomen' },
    { sentence: 'Wir fröhlichen Kinder singen laut.', target: 'singen', type: 'Verb' }
];
let indexGrammar = 0;

function initGrammarTask() {
    const tasks = dynamicGrammarTasks.length > 0 ? dynamicGrammarTasks : fallbackGrammarTasks;
    const task = tasks[indexGrammar % tasks.length];
    const parts = task.sentence.split(task.target);
    document.getElementById('grammar-sentence').innerHTML = `${parts[0]}<strong class="highlight">${task.target}</strong>${parts[1]}`;
}

document.querySelectorAll('.btn-grammar').forEach(btn => {
    btn.addEventListener('click', () => {
        const tasks = dynamicGrammarTasks.length > 0 ? dynamicGrammarTasks : fallbackGrammarTasks;
        const selectedType = btn.getAttribute('data-type');
        if (selectedType === tasks[indexGrammar % tasks.length].type) {
            updateScore(15);
            indexGrammar = (indexGrammar + 1) % tasks.length;
            initGrammarTask();
        } else {
            const card = document.querySelector('#module-k3-lang .game-card');
            card.classList.add('shake');
            setTimeout(() => card.classList.remove('shake'), 400);
        }
    });
});

// KLASSE 3: RECHTSCHREIBSTRATEGIEN (Verlängern & Ableiten)
const spellTasks = [
    { prefix: 'Hun', options: ['d', 't'], correct: 'd', strategy: 'Verlängern: Hun-de', instruction: 'Verlängere das Wort:' },
    { prefix: 'Hän', options: ['de', 'te'], correct: 'de', strategy: 'Ableiten von: Hand', instruction: 'Leite ab von Hand:' },
    { prefix: 'Gera', options: ['de', 'te'], correct: 'de', strategy: 'Verlängern: gera-de', instruction: 'Verlängere das Wort:' },
    { prefix: 'Bä', options: ['ume', 'ume'], correct: 'ume', strategy: 'Ableiten von: Baum', instruction: 'Leite ab von Baum:' },
    { prefix: 'Kro', options: ['g', 'k'], correct: 'g', strategy: 'Verlängern: Kro-ge', instruction: 'Verlängere das Wort:' }
];

let indexSpell = 0;
const spellInstructionEl = document.getElementById('spell-instruction');
const spellWordDisplayEl = document.getElementById('spell-word-display');
const spellHintEl = document.getElementById('spell-hint');
const spellOptionsEl = document.getElementById('spell-options');

function initSpellTask() {
    const task = spellTasks[indexSpell % spellTasks.length];
    spellInstructionEl.textContent = `${task.instruction} ${task.prefix}...`;
    spellWordDisplayEl.innerHTML = `${task.prefix}<span class="gap">?</span>`;
    spellHintEl.textContent = `💡 Tipp: ${task.strategy}`;

    spellOptionsEl.innerHTML = '';
    task.options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'btn-option';
        btn.textContent = opt;
        btn.addEventListener('click', () => {
            if (opt === task.correct) {
                updateScore(15);
                spellWordDisplayEl.innerHTML = `${task.prefix}<strong style="color:var(--success-color);">${opt}</strong>`;
                setTimeout(() => {
                    indexSpell = (indexSpell + 1) % spellTasks.length;
                    initSpellTask();
                }, 600);
            } else {
                const card = document.querySelector('#module-k3-spell .game-card');
                card.classList.add('shake');
                setTimeout(() => card.classList.remove('shake'), 400);
            }
        });
        spellOptionsEl.appendChild(btn);
    });
}"""

# 5. SW.JS
sw_content = """const CACHE_NAME = 'schul-app-v18';
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

open("index.html", "w", encoding="utf-8").write(html_content)
open("style.css", "w", encoding="utf-8").write(css_content)
open("app.js", "w", encoding="utf-8").write(js_content)
open("sw.js", "w", encoding="utf-8").write(sw_content)

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"[{'OK' if res.returncode==0 else 'ERR'}] {cmd}")
    if res.stderr and res.returncode != 0:
        print(f"    --> {res.stderr.strip()}")

print("🚀 Lade Rechtschreibstrategien-Modul zu GitHub hoch...")
run_cmd("git add .")
run_cmd("git commit -m 'Feat: Add Rechtschreibstrategien Module (Verlängern & Ableiten)'")
run_cmd("git branch -M main")
run_cmd("git push -u origin main")

print("\n✨ Deployment gestartet!")
