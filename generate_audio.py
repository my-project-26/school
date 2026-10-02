import os
import urllib.request
import urllib.parse

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

AUDIO_TASKS = [
    # KLASSE 1
    {"filename": "apfel.mp3", "text": "A wie Apfel"},
    {"filename": "baer.mp3", "text": "B wie Bär"},
    {"filename": "fisch.mp3", "text": "F wie Fisch"},
    {"filename": "loewe.mp3", "text": "L wie Löwe"},
    {"filename": "robbe.mp3", "text": "R wie Robbe"},
    {"filename": "tomate.mp3", "text": "To ma te hat drei Silben"},
    {"filename": "hund.mp3", "text": "Hund hat eine Silbe"},
    {"filename": "zehnerfeld7.mp3", "text": "Das sind sieben Punkte"},
    # KLASSE 3
    {"filename": "haende.mp3", "text": "Hände schreibt man mit Ä"},
    {"filename": "haeuser.mp3", "text": "Häuser schreibt man mit Ä U"},
    {"filename": "laufen.mp3", "text": "Laufen ist ein Verb"}
]

def download_hd_audio():
    print("🎙 Generiere HD-Studio-Audiodateien...")
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
