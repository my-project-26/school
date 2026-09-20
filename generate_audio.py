import os
from gtts import gTTS

# Wortschatz für die 1. Klasse - Google liest jetzt direkt das saubere Wort
anlaut_words = [
    {"word": "Affe", "file": "Affe.mp3"},
    {"word": "Apfel", "file": "Apfel.mp3"},
    {"word": "Bär", "file": "Baer.mp3"},
    {"word": "Ball", "file": "Ball.mp3"},
    {"word": "Elefant", "file": "Elefant.mp3"},
    {"word": "Fisch", "file": "Fisch.mp3"},
    {"word": "Gitarre", "file": "Gitarre.mp3"},
    {"word": "Hase", "file": "Hase.mp3"},
    {"word": "Igel", "file": "Igel.mp3"},
    {"word": "Krokodil", "file": "Krokodil.mp3"},
    {"word": "Löwe", "file": "Loewe.mp3"},
    {"word": "Maus", "file": "Maus.mp3"},
    {"word": "Nase", "file": "Nase.mp3"},
    {"word": "Oma", "file": "Oma.mp3"},
    {"word": "Pinguin", "file": "Pinguin.mp3"},
    {"word": "Sonne", "file": "Sonne.mp3"},
    {"word": "Trommel", "file": "Trommel.mp3"},
    {"word": "Uhr", "file": "Uhr.mp3"},
    {"word": "Vogel", "file": "Vogel.mp3"},
    {"word": "Zebra", "file": "Zebra.mp3"}
]

output_dir = "audio"
os.makedirs(output_dir, exist_ok=True)

print("🎙️ Generiere saubere Wort-Audios ohne Buchstaben-Namen...")

for item in anlaut_words:
    file_path = os.path.join(output_dir, item["file"])
    tts = gTTS(text=item["word"], lang='de', slow=False)
    tts.save(file_path)
    print(f"  ✓ Generiert: {item['word']} -> {file_path}")

print("\n✨ Fertig! Sprachdateien wurden im Ordner 'audio/' erneuert.")
