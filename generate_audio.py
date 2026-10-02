import os
import urllib.request
import urllib.parse

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Sämtliche Audios für Klasse 1 und Klasse 3 im gleichen HD-Standard
AUDIO_TASKS = [
    # KLASSE 1: Anlaute
    {"filename": "apfel.mp3", "text": "A wie Apfel"},
    {"filename": "baer.mp3", "text": "B wie Bär"},
    {"filename": "fisch.mp3", "text": "F wie Fisch"},
    {"filename": "loewe.mp3", "text": "L wie Löwe"},
    {"filename": "robbe.mp3", "text": "R wie Robbe"},
    
    # KLASSE 1: Silben & Zehnerfeld
    {"filename": "tomate.mp3", "text": "To ma te hat drei Silben"},
    {"filename": "hund.mp3", "text": "Hund hat eine Silbe"},
    {"filename": "zehnerfeld7.mp3", "text": "Das sind sieben Punkte"},

    # KLASSE 3: Rechtschreibung & Wortarten
    {"filename": "haende.mp3", "text": "Hände schreibt man mit Ä"},
    {"filename": "haeuser.mp3", "text": "Häuser schreibt man mit Ä U"},
    {"filename": "baeume.mp3", "text": "Bäume schreibt man mit Ä U"},
    {"filename": "maeuse.mp3", "text": "Mäuse schreibt man mit Ä U"},
    {"filename": "laufen.mp3", "text": "Laufen ist ein Verb"},

    # KLASSE 3: Halbschriftlich
    {"filename": "halbschriftlich1.mp3", "text": "Dreihundertfünfundsiebzig"}
]

# 1x1 Aufgaben von 1x1 bis 10x10 dynamisch hinzufügen
for a in range(1, 11):
    for b in range(1, 11):
        res = a * b
        filename = f"{a}x{b}.mp3"
        text = f"{a} mal {b} ist gleich {res}"
        AUDIO_TASKS.append({"filename": filename, "text": text})

def download_hd_audio():
    print("🎙 Generiere 100% einheitliche Studio-Audiodateien für Klasse 1 & 3...")
    for item in AUDIO_TASKS:
        filepath = os.path.join(AUDIO_DIR, item["filename"])
        encoded_text = urllib.parse.quote(item["text"])
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl=de&client=tw-ob"
        
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            )
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ Gespeichert: {filepath}")
        except Exception as e:
            print(f"❌ Fehler bei {item['filename']}: {e}")

if __name__ == "__main__":
    download_hd_audio()
