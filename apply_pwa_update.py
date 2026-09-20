import json

# 1. INDEX.HTML
html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Schul-App: Lernstudio</title>
    <link rel="stylesheet" href="style.css">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#4A90E2">
</head>
<body>

    <!-- Audio-Unlock Overlay für Safari/iOS -->
    <div id="start-overlay" class="overlay">
        <div class="card start-card">
            <h1>Willkommen im Lernstudio! 🎈</h1>
            <p>Tippe auf den Knopf, um zu starten.</p>
            <button id="btn-start" class="btn-primary">Lernstudio Öffnen 🚀</button>
        </div>
    </div>

    <header>
        <div class="nav-tabs">
            <button id="tab-k1" class="tab-btn active">1. Klasse: Anlaute 🔊</button>
            <button id="tab-k3-math" class="tab-btn">3. Klasse: 1x1 🧮</button>
            <button id="tab-k3-lang" class="tab-btn">3. Klasse: Wortarten 📝</button>
        </div>
        <div id="score-display">Punkte: <span id="score">0</span></div>
    </header>

    <main class="container">
        <!-- MODUL 1. KLASSE: ANLAUTE -->
        <section id="module-k1" class="module-card">
            <div class="card game-card">
                <h2>Anlaute Hören</h2>
                <p class="instruction">Welcher Anlaut gehört zum Bild?</p>
                <button id="btn-play-audio" class="btn-audio" aria-label="Wort noch einmal anhören">
                    🔊 Wort anhören
                </button>
                <div class="image-container">
                    <span id="word-emoji" class="emoji-display">❓</span>
                </div>
                <div id="letter-options" class="options-grid"></div>
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
    </main>

    <script src="app.js"></script>
</body>
</html>"""

# 2. STYLE.CSS
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

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}

body {
    font-family: var(--font-family);
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
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

.nav-tabs {
    display: flex;
    gap: 0.4rem;
}

.tab-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 0.5rem 0.8rem;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.2s;
}

.tab-btn.active {
    background: white;
    color: var(--primary-color);
}

#score-display {
    font-weight: bold;
    font-size: 1.1rem;
    background: rgba(0,0,0,0.15);
    padding: 0.5rem 1rem;
    border-radius: 12px;
}

.container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
}

.module-card {
    width: 100%;
    max-width: 500px;
}

.hidden {
    display: none !important;
}

.card {
    background: var(--card-bg);
    border-radius: 20px;
    padding: 1.8rem;
    width: 100%;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    text-align: center;
}

.card h2 {
    margin-bottom: 0.8rem;
    color: var(--primary-color);
}

.instruction {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

.btn-audio {
    background-color: #FFE066;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 1.5rem;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    min-height: 50px;
    margin-bottom: 1rem;
}

.image-container {
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
}

.emoji-display {
    font-size: 4.5rem;
}

.options-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.8rem;
}

.btn-option {
    background-color: var(--bg-color);
    border: 3px solid var(--primary-color);
    border-radius: 16px;
    font-size: 2.2rem;
    font-weight: bold;
    color: var(--primary-color);
    padding: 0.8rem;
    min-height: 65px;
    cursor: pointer;
}

/* MATHE 1x1 */
.math-problem {
    font-size: 3rem;
    font-weight: bold;
    margin: 1rem 0 1.5rem 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.8rem;
}

.input-display {
    background: var(--bg-color);
    border: 3px solid var(--primary-color);
    border-radius: 12px;
    padding: 0.2rem 1rem;
    min-width: 90px;
    color: var(--primary-color);
}

.numpad-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    max-width: 320px;
    margin: 0 auto;
}

.btn-num {
    background-color: var(--bg-color);
    border: 2px solid #CBD5E1;
    border-radius: 14px;
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--text-color);
    min-height: 60px;
    cursor: pointer;
}

.btn-action { background-color: #FCA5A5; color: #991B1B; }
.btn-action-submit { background-color: var(--success-color); color: #065F46; }

/* WORTARTEN */
.sentence-box {
    background: var(--bg-color);
    padding: 1.2rem;
    border-radius: 12px;
    font-size: 1.3rem;
    margin-bottom: 1.5rem;
}

.highlight {
    color: var(--primary-color);
    text-decoration: underline;
}

.grammar-grid {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.btn-grammar {
    border: none;
    border-radius: 12px;
    padding: 1rem;
    font-size: 1.2rem;
    font-weight: bold;
    color: white;
    cursor: pointer;
}

.btn-nomen { background-color: var(--nomen-color); }
.btn-verb { background-color: var(--verb-color); }
.btn-adjektiv { background-color: var(--adjektiv-color); }

.shake { animation: shake 0.4s ease-in-out; }
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-8px); }
    40%, 80% { transform: translateX(8px); }
}

.overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6);
    display: flex; justify-content: center; align-items: center;
    z-index: 1000;
}

.btn-primary {
    background-color: var(--success-color);
    border: none; border-radius: 12px;
    padding: 1rem 2rem; font-size: 1.3rem; font-weight: bold;
    color: #1A3636; margin-top: 1.5rem; cursor: pointer;
}"""

# 3. APP.JS
js_content = """// Service Worker Registrierung für 100% Offline-Betrieb
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
        .then(() => console.log('Service Worker aktiv.'))
        .catch(err => console.log('SW Fehler:', err));
}

let score = parseInt(localStorage.getItem('school_app_score') || '0');

// Navigation
const tabK1 = document.getElementById('tab-k1');
const tabK3Math = document.getElementById('tab-k3-math');
const tabK3Lang = document.getElementById('tab-k3-lang');

const moduleK1 = document.getElementById('module-k1');
const moduleK3Math = document.getElementById('module-k3-math');
const moduleK3Lang = document.getElementById('module-k3-lang');

const scoreDisplay = document.getElementById('score');
scoreDisplay.textContent = score;

function updateScore(points) {
    score += points;
    localStorage.setItem('school_app_score', score);
    scoreDisplay.textContent = score;
}

function switchTab(activeTab, activeModule) {
    [tabK1, tabK3Math, tabK3Lang].forEach(t => t.classList.remove('active'));
    [moduleK1, moduleK3Math, moduleK3Lang].forEach(m => m.classList.add('hidden'));

    activeTab.classList.add('active');
    activeModule.classList.remove('hidden');
}

tabK1.addEventListener('click', () => switchTab(tabK1, moduleK1));
tabK3Math.addEventListener('click', () => { switchTab(tabK3Math, moduleK3Math); initMathTask(); });
tabK3Lang.addEventListener('click', () => { switchTab(tabK3Lang, moduleK3Lang); initGrammarTask(); });

// KLASSE 1: ANLAUTE
const taskDataK1 = [
    { word: 'Affe', letter: 'A', emoji: '🐒', audio: 'audio/Affe.mp3' },
    { word: 'Apfel', letter: 'A', emoji: '🍎', audio: 'audio/Apfel.mp3' },
    { word: 'Bär', letter: 'B', emoji: '🐻', audio: 'audio/Baer.mp3' },
    { word: 'Ball', letter: 'B', emoji: '⚽', audio: 'audio/Ball.mp3' },
    { word: 'Fisch', letter: 'F', emoji: '🐟', audio: 'audio/Fisch.mp3' },
    { word: 'Gitarre', letter: 'G', emoji: '🎸', audio: 'audio/Gitarre.mp3' },
    { word: 'Hase', letter: 'H', emoji: '🐰', audio: 'audio/Hase.mp3' },
    { word: 'Igel', letter: 'I', emoji: '🦔', audio: 'audio/Igel.mp3' },
    { word: 'Maus', letter: 'M', emoji: '🐭', audio: 'audio/Maus.mp3' },
    { word: 'Sonne', letter: 'S', emoji: '☀️', audio: 'audio/Sonne.mp3' },
    { word: 'Vogel', letter: 'V', emoji: '🐦', audio: 'audio/Vogel.mp3' },
    { word: 'Zebra', letter: 'Z', emoji: '🦓', audio: 'audio/Zebra.mp3' }
];

let indexK1 = 0;
let currentAudio = null;

const startOverlay = document.getElementById('start-overlay');
const btnStart = document.getElementById('btn-start');
const btnPlayAudio = document.getElementById('btn-play-audio');
const wordEmoji = document.getElementById('word-emoji');
const letterOptionsContainer = document.getElementById('letter-options');

btnStart.addEventListener('click', () => {
    startOverlay.style.display = 'none';
    loadTaskK1(indexK1);
});

function playAudioFile(path) {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
    currentAudio = new Audio(path);
    currentAudio.play().catch(e => console.log("Audio blockiert:", e));
}

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
        const card = document.querySelector('#module-k1 .game-card');
        card.classList.add('shake');
        playAudioFile(taskDataK1[indexK1].audio);
        setTimeout(() => card.classList.remove('shake'), 400);
    }
}

btnPlayAudio.addEventListener('click', () => playAudioFile(taskDataK1[indexK1].audio));

// KLASSE 3: MATHE 1x1 LOGIK
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

document.querySelectorAll('.btn-num').forEach(btn => {
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

// KLASSE 3: WORTARTEN LOGIK
const grammarTasks = [
    { sentence: 'Der schnelle Hund rennt.', target: 'schnelle', type: 'Adjektiv' },
    { sentence: 'Die Katze schläft auf dem Sofa.', target: 'Katze', type: 'Nomen' },
    { sentence: 'Wir fröhlichen Kinder singen laut.', target: 'singen', type: 'Verb' }
];
let indexGrammar = 0;

function initGrammarTask() {
    const task = grammarTasks[indexGrammar];
    const parts = task.sentence.split(task.target);
    document.getElementById('grammar-sentence').innerHTML = `${parts[0]}<strong class="highlight">${task.target}</strong>${parts[1]}`;
}

document.querySelectorAll('.btn-grammar').forEach(btn => {
    btn.addEventListener('click', () => {
        const selectedType = btn.getAttribute('data-type');
        if (selectedType === grammarTasks[indexGrammar].type) {
            updateScore(15);
            indexGrammar = (indexGrammar + 1) % grammarTasks.length;
            initGrammarTask();
        } else {
            const card = document.querySelector('#module-k3-lang .game-card');
            card.classList.add('shake');
            setTimeout(() => card.classList.remove('shake'), 400);
        }
    });
});"""

# 4. SW.JS (Service Worker)
sw_content = """const CACHE_NAME = 'schul-app-v1';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});"""

# Schreiben aller Dateien
open("index.html", "w", encoding="utf-8").write(html_content)
open("style.css", "w", encoding="utf-8").write(css_content)
open("app.js", "w", encoding="utf-8").write(js_content)
open("sw.js", "w", encoding="utf-8").write(sw_content)

print("✨ Offline-Update inkl. Service Worker & Wortarten-Modul erfolgreich geschrieben!")
