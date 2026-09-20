if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js')
        .then(() => console.log('Service Worker aktiv.'))
        .catch(err => console.log('SW Fehler:', err));
}

let score = parseInt(localStorage.getItem('school_app_score') || '0');

let dynamicContent = null;
fetch('./content.json')
    .then(res => res.json())
    .then(data => {
        dynamicContent = data;
        if (data.obst_gemuese && data.tiere_weltweit) {
            mergeDynamicVocabulary(data.obst_gemuese, data.tiere_weltweit);
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
let taskDataK1 = [
    { word: 'Apfel', letter: 'A', emoji: '🍎', audio: 'audio/Apfel.mp3' },
    { word: 'Bär', letter: 'B', emoji: '🐻', audio: 'audio/Baer.mp3' },
    { word: 'Elefant', letter: 'E', emoji: '🐘', audio: 'audio/Elefant.mp3' },
    { word: 'Fisch', letter: 'F', emoji: '🐟', audio: 'audio/Fisch.mp3' },
    { word: 'Gitarre', letter: 'G', emoji: '🎸', audio: 'audio/Gitarre.mp3' },
    { word: 'Hase', letter: 'H', emoji: '🐰', audio: 'audio/Hase.mp3' },
    { word: 'Igel', letter: 'I', emoji: '🦔', audio: 'audio/Igel.mp3' },
    { word: 'Krokodil', letter: 'K', emoji: '🐊', audio: 'audio/Krokodil.mp3' },
    { word: 'Löwe', letter: 'L', emoji: '🦁', audio: 'audio/Loewe.mp3' },
    { word: 'Maus', letter: 'M', emoji: '🐭', audio: 'audio/Maus.mp3' },
    { word: 'Pilz', letter: 'P', emoji: '🍄', audio: 'audio/Pilz.mp3' },
    { word: 'Sonne', letter: 'S', emoji: '☀️', audio: 'audio/Sonne.mp3' }
];

function mergeDynamicVocabulary(obstList, tiereList) {
    const mapEntry = item => ({
        word: item.word,
        letter: item.letter,
        emoji: item.emoji,
        audio: `audio/${item.word}.mp3`
    });
    taskDataK1 = [...taskDataK1, ...obstList.map(mapEntry), ...tiereList.map(mapEntry)];
}

let indexK1 = 0;
const startOverlay = document.getElementById('start-overlay');
const btnStart = document.getElementById('btn-start');
const btnPlayAudio = document.getElementById('btn-play-audio');
const wordEmoji = document.getElementById('word-emoji');
const letterOptionsContainer = document.getElementById('letter-options');

btnStart.addEventListener('click', () => { startOverlay.style.display = 'none'; loadTaskK1(indexK1); });

function loadTaskK1(index) {
    const task = taskDataK1[index % taskDataK1.length];
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
        playAudioFile(taskDataK1[indexK1 % taskDataK1.length].audio);
        setTimeout(() => card.classList.remove('shake'), 400);
    }
}
btnPlayAudio.addEventListener('click', () => playAudioFile(taskDataK1[indexK1 % taskDataK1.length].audio));

// KLASSE 1: SILBEN
const silbenData = [
    { word: 'Bär', syllables: 1, emoji: '🐻', audio: 'audio/Baer.mp3' },
    { word: 'Affe', syllables: 2, emoji: '🐒', audio: 'audio/Affe.mp3' },
    { word: 'Elefant', syllables: 3, emoji: '🐘', audio: 'audio/Elefant.mp3' },
    { word: 'Krokodil', syllables: 3, emoji: '🐊', audio: 'audio/Krokodil.mp3' },
    { word: 'Maultasche', syllables: 3, emoji: '🥟', audio: 'audio/Maultasche.mp3' }
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
    { sentence: 'Wir fröhlichen Kinder singen laut.', target: 'singen', type: 'Verb' },
    { sentence: 'Oma kocht leckere Spätzle.', target: 'Spätzle', type: 'Nomen' },
    { sentence: 'Der große Bär wandert durch den Schwarzwald.', target: 'wandert', type: 'Verb' }
];
let indexGrammar = 0;

function initGrammarTask() {
    const tasks = (dynamicContent && dynamicContent.klasse3_wortarten) ? dynamicContent.klasse3_wortarten : fallbackGrammarTasks;
    const task = tasks[indexGrammar % tasks.length];
    const parts = task.sentence.split(task.target);
    document.getElementById('grammar-sentence').innerHTML = `${parts[0]}<strong class="highlight">${task.target}</strong>${parts[1]}`;
}

document.querySelectorAll('.btn-grammar').forEach(btn => {
    btn.addEventListener('click', () => {
        const tasks = (dynamicContent && dynamicContent.klasse3_wortarten) ? dynamicContent.klasse3_wortarten : fallbackGrammarTasks;
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

// KLASSE 3: RECHTSCHREIBSTRATEGIEN (BUGFIX STAMM & EXAKTE RECHTSCHREIBUNG)
const spellTasks = [
    { baseStem: 'B', gapQuestion: 'äume', choices: ['äume', 'ume'], correct: 'äume', fullWord: 'Bäume', strategy: 'Ableiten von: Baum', instruction: 'Leite ab von Baum:' },
    { baseStem: 'Hun', gapQuestion: 'd', choices: ['d', 't'], correct: 'd', fullWord: 'Hund', strategy: 'Verlängern: Hun-de', instruction: 'Verlängere das Wort:' },
    { baseStem: 'Hän', gapQuestion: 'de', choices: ['de', 'te'], correct: 'de', fullWord: 'Hände', strategy: 'Ableiten von: Hand', instruction: 'Leite ab von Hand:' },
    { baseStem: 'Wal', gapQuestion: 'd', choices: ['d', 't'], correct: 'd', fullWord: 'Wald', strategy: 'Verlängern: Wäl-der', instruction: 'Verlängere das Wort:' },
    { baseStem: 'Äp', gapQuestion: 'fel', choices: ['fel', 'pel'], correct: 'fel', fullWord: 'Äpfel', strategy: 'Ableiten von: Apfel', instruction: 'Leite ab von Apfel:' },
    { baseStem: 'Bro', gapQuestion: 't', choices: ['t', 'd'], correct: 't', fullWord: 'Brot', strategy: 'Verlängern: Bro-te', instruction: 'Verlängere das Wort:' }
];

let indexSpell = 0;
const spellInstructionEl = document.getElementById('spell-instruction');
const spellWordDisplayEl = document.getElementById('spell-word-display');
const spellHintEl = document.getElementById('spell-hint');
const spellOptionsEl = document.getElementById('spell-options');

function initSpellTask() {
    const task = spellTasks[indexSpell % spellTasks.length];
    spellInstructionEl.textContent = `${task.instruction} ${task.baseStem}...`;
    spellWordDisplayEl.innerHTML = `${task.baseStem}<span class="gap">?</span>`;
    spellHintEl.textContent = `💡 Tipp: ${task.strategy}`;

    spellOptionsEl.innerHTML = '';
    task.choices.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'btn-option';
        btn.textContent = opt;
        btn.addEventListener('click', () => {
            if (opt === task.correct) {
                updateScore(15);
                spellWordDisplayEl.innerHTML = `${task.baseStem}<strong style="color:var(--success-color);">${opt}</strong>`;
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
}