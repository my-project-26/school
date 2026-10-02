import os
import urllib.request
import urllib.parse

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Sämtliche Audio-Texte für Klasse 1 und Klasse 3
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

    # KLASSE 3: 1x1 Blitzrechnen
    {"filename": "3x4.mp3", "text": "Drei mal vier ist gleich zwölf"},
    {"filename": "5x5.mp3", "text": "Fünf mal fünf ist gleich fünfundzwanzig"},
    {"filename": "6x7.mp3", "text": "Sechs mal sieben ist gleich zweiundvierzig"},
    {"filename": "8x9.mp3", "text": "Acht mal neun ist gleich zweiundsiebzig"},
    {"filename": "4x8.mp3", "text": "Vier mal acht ist gleich zweiunddreißig"},

    # KLASSE 3: Halbschriftlich & Wortarten & Rechtschreibung
    {"filename": "halbschriftlich1.mp3", "text": "Dreihundertfünfundsiebzig"},
    {"filename": "laufen.mp3", "text": "Laufen ist ein Verb"},
    {"filename": "haende.mp3", "text": "Hände schreibt man mit Ä"},
    {"filename": "haeuser.mp3", "text": "Häuser schreibt man mit Ä U"}
]

def download_hd_audio():
    print("🎙 Generiere HD-Studio-Audiodateien für Klasse 1 & 3...")
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
            print(f"✅ Gespeichert: {filepath} ('{item['text']}')")
        except Exception as e:
            print(f"❌ Fehler bei {item['filename']}: {e}")

if __name__ == "__main__":
    download_hd_audio()
