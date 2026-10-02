import os
import urllib.request
import urllib.parse

# Zielordner für glasklare Audio-Dateien
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Wortschatz-Liste für 1. und 3. Klasse (Anlaute & Rechtschreibung)
WORDS_TO_GENERATE = [
    {"filename": "apfel.mp3", "text": "A wie Apfel"},
    {"filename": "baer.mp3", "text": "B wie Bär"},
    {"filename": "fisch.mp3", "text": "F wie Fisch"},
    {"filename": "loewe.mp3", "text": "L wie Löwe"},
    {"filename": "robbe.mp3", "text": "R wie Robbe"},
    {"filename": "eichhoernchen.mp3", "text": "Eichhörnchen"},
    {"filename": "haende.mp3", "text": "Hände"},
    {"filename": "haeuser.mp3", "text": "Häuser"},
    {"filename": "baeume.mp3", "text": "Bäume"},
    {"filename": "maeuse.mp3", "text": "Mäuse"}
]

def download_hd_audio():
    print("🎙️️ Generiere HD-Audiodateien (Gemini-Qualitätslevel)...")
    for item in WORDS_TO_GENERATE:
        filepath = os.path.join(AUDIO_DIR, item["filename"])
        encoded_text = urllib.parse.quote(item["text"])
        # Nutzung der Google-Translate-TTS-Engine mit hoher Sprachqualität (de-DE)
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
