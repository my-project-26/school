import json

html = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Schul-App: 1. Klasse Anlaute</title>
    <link rel="stylesheet" href="style.css">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#4A90E2">
</head>
<body>
    <div id="start-overlay" class="overlay">
        <div class="card start-card">
            <h1>Willkommen! 🎈</h1>
            <p>Tippe auf den Knopf, um das Lernspiel zu starten.</p>
            <button id="btn-start" class="btn-primary">Spiel Starten 🔊</button>
        </div>
    </div>
    <header>
        <h1>Anlaute Hören (1. Klasse)</h1>
        <div id="score-display">Punkte: <span id="score">0</span></div>
    </header>
    <main class="container">
        <div class="card game-card">
            <p class="instruction">Welcher Anlaut gehört zum Bild?</p>
            <button id="btn-play-audio" class="btn-audio" aria-label="Wort noch einmal anhören">
                🔊 Wort anhören
            </button>
            <div class="image-container">
                <span id="word-emoji" class="emoji-display">❓</span>
            </div>
            <div id="letter-options" class="options-grid"></div>
        </div>
    </main>
    <script src="app.js"></script>
</body>
</html>"""

css = """:root {
    --bg-color: #F0F4F8;
    --card-bg: #FFFFFF;
    --primary-color: #4A90E2;
    --success-color: #50E3C2;
    --text-color: #2C3E50;
    --font-family: system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
body { font-family: var(--font-family); background-color: var(--bg-color); color: var(--text-color); min-height: 100vh; display: flex; flex-direction: column; }
header { background-color: var(--primary-color); color: white; padding: 1rem; display: flex; justify-content: space-between; align-items: center; }
.container { flex: 1; display: flex; justify-content: center; align-items: center; padding: 1rem; }
.card { background: var(--card-bg); border-radius: 20px; padding: 2rem; width: 100%; max-width: 500px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); text-align: center; }
.instruction { font-size: 1.2rem; margin-bottom: 1rem; font-weight: 600; }
.btn-audio { background-color: #FFE066; border: none; border-radius: 12px; padding: 0.8rem 1.5rem; font-size: 1.1rem; font-weight: bold; cursor: pointer; min-height: 50px; margin-bottom: 1.5rem; }
.image-container { height: 120px; display: flex; justify-content: center; align-items: center; margin-bottom: 2rem; }
.emoji-display { font-size: 5rem; }
.options-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.btn-option { background-color: var(--bg-color); border: 3px solid var(--primary-color); border-radius: 16px; font-size: 2.5rem; font-weight: bold; color: var(--primary-color); padding: 1rem; min-height: 70px; cursor: pointer; }
.shake { animation: shake 0.4s ease-in-out; }
@keyframes shake { 0%, 100% { transform: translateX(0); } 20%, 60% { transform: translateX(-8px); } 40%, 80% { transform: translateX(8px); } }
.overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.btn-primary { background-color: var(--success-color); border: none; border-radius: 12px; padding: 1rem 2rem; font-size: 1.3rem; font-weight: bold; color: #1A3636; margin-top: 1.5rem; cursor: pointer; }"""

js = """const taskData = [
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

let currentTaskIndex = 0;
let score = 0;
let currentAudio = null;

const startOverlay = document.getElementById('start-overlay');
const btnStart = document.getElementById('btn-start');
const btnPlayAudio = document.getElementById('btn-play-audio');
const wordEmoji = document.getElementById('word-emoji');
const letterOptionsContainer = document.getElementById('letter-options');
const scoreDisplay = document.getElementById('score');

btnStart.addEventListener('click', () => {
    startOverlay.style.display = 'none';
    loadTask(currentTaskIndex);
});

function playAudioFile(path) {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
    currentAudio = new Audio(path);
    currentAudio.play().catch(e => console.log("Audio abgefangen:", e));
}

function loadTask(index) {
    const task = taskData[index];
    wordEmoji.textContent = task.emoji;

    const letters = generateLetterChoices(task.letter);
    letterOptionsContainer.innerHTML = '';

    letters.forEach(letter => {
        const btn = document.createElement('button');
        btn.className = 'btn-option';
        btn.textContent = letter;
        btn.addEventListener('click', () => handleChoice(letter, task.letter));
        letterOptionsContainer.appendChild(btn);
    });

    setTimeout(() => { playAudioFile(task.audio); }, 300);
}

function generateLetterChoices(correctLetter) {
    const allLetters = ['A', 'B', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'S', 'T', 'U', 'V', 'Z'];
    const choices = new Set([correctLetter]);

    while (choices.size < 4) {
        const randomLetter = allLetters[Math.floor(Math.random() * allLetters.length)];
        choices.add(randomLetter);
    }

    return Array.from(choices).sort(() => Math.random() - 0.5);
}

function handleChoice(selectedLetter, correctLetter) {
    if (selectedLetter === correctLetter) {
        score += 10;
        scoreDisplay.textContent = score;
        currentTaskIndex = (currentTaskIndex + 1) % taskData.length;
        loadTask(currentTaskIndex);
    } else {
        const gameCard = document.querySelector('.game-card');
        gameCard.classList.add('shake');
        playAudioFile(taskData[currentTaskIndex].audio);
        setTimeout(() => { gameCard.classList.remove('shake'); }, 400);
    }
}

btnPlayAudio.addEventListener('click', () => {
    playAudioFile(taskData[currentTaskIndex].audio);
});"""

manifest = {
    "name": "Schul-App Klasse 1",
    "short_name": "SchulApp1",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "#F0F4F8",
    "theme_color": "#4A90E2"
}

open("index.html", "w", encoding="utf-8").write(html)
open("style.css", "w", encoding="utf-8").write(css)
open("app.js", "w", encoding="utf-8").write(js)
open("manifest.json", "w", encoding="utf-8").write(json.dumps(manifest, indent=2))

print("✨ Alle Frontend-Dateien wurden ohne Terminal-Hänger generiert!")
