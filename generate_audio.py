import os
import urllib.request
import urllib.parse

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

AUDIO_TASKS = [
    # KLASSE 1: Anlaute
    {"filename": "apfel.mp3", "text": "A wie Apfel"},
    {"filename": "baer.mp3", "text": "B wie Bär"},
    {"filename": "fisch.mp3", "text": "F wie Fisch"},
    {"filename": "loewe.mp3", "text": "L wie Löwe"},
    {"filename": "robbe.mp3", "text": "R wie Robbe"},
    {"filename": "eichhoernchen.mp3", "text": "E wie Eichhörnchen"},
    {"filename": "ente.mp3", "text": "E wie Ente"},
    {"filename": "sonne.mp3", "text": "S wie Sonne"},

    # KLASSE 1: Silben Wortschatz
    {"filename": "tomate.mp3", "text": "To ma te hat drei Silben"},
    {"filename": "hund.mp3", "text": "Hund hat eine Silbe"},
    {"filename": "katze.mp3", "text": "Kat ze hat zwei Silben"},
    {"filename": "schokolade.mp3", "text": "Scho ko la de hat vier Silben"},
    {"filename": "schmetterling.mp3", "text": "Schmet ter ling hat drei Silben"},
    {"filename": "elefant.mp3", "text": "E le fant hat drei Silben"},
    {"filename": "haus.mp3", "text": "Haus hat eine Silbe"},
    {"filename": "blume.mp3", "text": "Blu me hat zwei Silben"},
    {"filename": "banane.mp3", "text": "Ba na ne hat drei Silben"},
    {"filename": "frosch.mp3", "text": "Frosch hat eine Silbe"},

    # KLASSE 3: Wortarten & Rechtschreibung
    {"filename": "hund_nomen.mp3", "text": "Hund ist ein Nomen"},
    {"filename": "laufen.mp3", "text": "Laufen ist ein Verb"},
    {"filename": "schnell_adj.mp3", "text": "Schnell ist ein Adjektiv"},
    {"filename": "katze_nomen.mp3", "text": "Katze ist ein Nomen"},
    {"filename": "spielen_verb.mp3", "text": "Spielen ist ein Verb"},
    {"filename": "schoen_adj.mp3", "text": "Schön ist ein Adjektiv"},
    {"filename": "haende.mp3", "text": "Hände schreibt man mit Ä"},
    {"filename": "haeuser.mp3", "text": "Häuser schreibt man mit Ä U"},
    {"filename": "baeume.mp3", "text": "Bäume schreibt man mit Ä U"},
    {"filename": "maeuse.mp3", "text": "Mäuse schreibt man mit Ä U"}
]

# Zehnerfeld Audio bis 20
for n in range(1, 21):
    AUDIO_TASKS.append({"filename": f"zehnerfeld{n}.mp3", "text": f"Das sind {n} Punkte"})

# 1x1 Aufgaben von 1x1 bis 10x10
for a in range(1, 11):
    for b in range(1, 11):
        res = a * b
        AUDIO_TASKS.append({"filename": f"{a}x{b}.mp3", "text": f"{a} mal {b} ist gleich {res}"})

def download_hd_audio():
    print("🎙 Generiere lückenlose HD-Studio-Audiodateien...")
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
