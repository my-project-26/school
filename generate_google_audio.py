import os
import json
from gtts import gTTS

print("🎙️ Starte Generierung der kristallklaren Google-Audio-Dateien...")

os.makedirs("audio", exist_ok=True)

# Lade Begriffe aus content.json
if os.path.exists("content.json"):
    content = json.load(open("content.json", "r", encoding="utf-8"))
else:
    content = {"obst_gemuese": [], "tiere_weltweit": []}

words_to_generate = set([
    "Apfel", "Affe", "Bär", "Brot", "Elefant", "Fisch", "Gitarre", "Hase",
    "Igel", "Krokodil", "Kirsche", "Maus", "Milch", "Pilz", "Sonne", "Tanne",
    "Maultasche", "Spätzle", "Hund", "Hunde", "Hand", "Hände", "Baum", "Bäume",
    "Wald", "Wälder", "Brot", "Brote"
])

# Füge alle Wörter aus Obst, Gemüse und Tieren hinzu
for item in content.get("obst_gemuese", []):
    words_to_generate.add(item["word"])

for item in content.get("tiere_weltweit", []):
    words_to_generate.add(item["word"])

# Erzeuge Google TTS MP3 für jedes Wort
for word in words_to_generate:
    filename = f"audio/{word}.mp3"
    if not os.path.exists(filename):
        try:
            tts = gTTS(text=word, lang='de', tld='de', slow=False)
            tts.save(filename)
            print(f"  ✅ Generiert: {filename}")
        except Exception as e:
            print(f"  ❌ Fehler bei {word}: {e}")

print("✨ Audio-Generierung abgeschlossen!")
