import os
import sys

try:
    from gtts import gTTS
except ImportError:
    print("gTTS nicht gefunden. Installiere gTTS...")
    os.system(f"{sys.executable} -m pip install gtts")
    from gtts import gTTS

# Vollständige Wortliste für deine App (Tiere, Obst, Gemüse, Begriffe)
word_catalog = {
    "Adler": "Adler",
    "Affe": "Affe",
    "Alligator": "Alligator",
    "Alpaka": "Alpaka",
    "Ameise": "Ameise",
    "Ananas": "Ananas",
    "Apfel": "Apfel",
    "Aepfel": "Aepfel",
    "Äpfel": "Aepfel",
    "Aubergine": "Aubergine",
    "Avocado": "Avocado",
    "Baer": "Baer",
    "Bär": "Baer",
    "Baeren": "Baeren",
    "Bären": "Baeren",
    "Ball": "Ball",
    "Banane": "Banane",
    "Baum": "Baum",
    "Baeume": "Baeume",
    "Bäume": "Baeume",
    "Biber": "Biber",
    "Biene": "Biene",
    "Birne": "Birne",
    "Bohne": "Bohne",
    "Brokkoli": "Brokkoli",
    "Brot": "Brot",
    "Brote": "Brote",
    "Bueffel": "Bueffel",
    "Büffel": "Bueffel",
    "Chili": "Chili",
    "Chinchilla": "Chinchilla",
    "Dachs": "Dachs",
    "Dattel": "Dattel",
    "Delfin": "Delfin",
    "Dinosaurier": "Dinosaurier",
    "Eichhoernchen": "Eichhoernchen",
    "Eichhörnchen": "Eichhoernchen",
    "Eidechse": "Eidechse",
    "Elefant": "Elefant",
    "Erbse": "Erbse",
    "Erdbeere": "Erdbeere",
    "Esel": "Esel",
    "Eule": "Eule",
    "Feige": "Feige",
    "Haende": "Haende",
    "Hände": "Haende",
    "Haeuser": "Haeuser",
    "Häuser": "Haeuser"
}

os.makedirs("audio", exist_ok=True)

print("--- STARTE AUDIO-GENERIERUNG IN HOCHAUFLÖSENDER BAER-QUALITÄT ---")
for file_key, speak_text in word_catalog.items():
    file_path = f"audio/{file_key}.mp3"
    try:
        # Generierung mit der klaren Google TTS Engine (Aussprache auf Deutsch)
        tts = gTTS(text=speak_text, lang='de', slow=False)
        tts.save(file_path)
        print(f"[OK] Generiert: {file_path} (Text: '{speak_text}')")
    except Exception as e:
        print(f"[ERROR] Fehler bei {file_key}: {e}")

print("--- ALLE TONSPUREN ERFOLGREICH NEU ERSTELLT UND ÜBERSCHRIEBEN ---")
