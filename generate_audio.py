import os
import urllib.request
import urllib.parse

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 50 ANLAUT WÖRTER FÜR DIE 1. KLASSE
ANLAUTE_50 = [
    ("apfel", "A wie Apfel"), ("baer", "B wie Bär"), ("clown", "C wie Clown"), ("drache", "D wie Drache"),
    ("elefant", "E wie Elefant"), ("fisch", "F wie Fisch"), ("giraffe", "G wie Giraffe"), ("haus", "H wie Haus"),
    ("igel", "I wie Igel"), ("jacke", "J wie Jacke"), ("krokodil", "K wie Krokodil"), ("loewe", "L wie Löwe"),
    ("maus", "M wie Maus"), ("nadel", "N wie Nadel"), ("oma", "O wie Oma"), ("pinguin", "P wie Pinguin"),
    ("qualle", "Q wie Qualle"), ("robbe", "R wie Robbe"), ("sonne", "S wie Sonne"), ("tiger", "T wie Tiger"),
    ("uhr", "U wie Uhr"), ("vogel", "V wie Vogel"), ("wal", "W wie Wal"), ("xylophon", "X wie Xylophon"),
    ("yoga", "Y wie Yoga"), ("zebra", "Z wie Zebra"), ("ente", "E wie Ente"), ("eichhoernchen", "E wie Eichhörnchen"),
    ("insel", "I wie Igel"), ("otter", "O wie Otter"), ("uhustufe", "U wie Uhu"), ("ampel", "A wie Apfel"),
    ("ball", "B wie Bär"), ("delfin", "D wie Drache"), ("eule", "E wie Ente"), ("frosch", "F wie Fisch"),
    ("gitarre", "G wie Giraffe"), ("hund", "H wie Haus"), ("indianer", "I wie Igel"), ("kaefer", "K wie Krokodil"),
    ("lampe", "L wie Löwe"), ("mond", "M wie Maus"), ("nuss", "N wie Nadel"), ("papagei", "P wie Pinguin"),
    ("rakete", "R wie Robbe"), ("schaf", "S wie Sonne"), ("tomate", "T wie Tiger"), ("vulkan", "V wie Vogel"),
    ("wolke", "W wie Wal"), ("zitrone", "Z wie Zebra")
]

AUDIO_TASKS = [{"filename": f"{item[0]}.mp3", "text": item[1]} for item in ANLAUTE_50]

# Weitere Standard-Audios hinzufügen
AUDIO_TASKS.extend([
    {"filename": "tomate_silben.mp3", "text": "To ma te hat drei Silben"},
    {"filename": "hund_silben.mp3", "text": "Hund hat eine Silbe"},
    {"filename": "katze_silben.mp3", "text": "Kat ze hat zwei Silben"},
    {"filename": "hund_nomen.mp3", "text": "Hund ist ein Nomen"},
    {"filename": "laufen.mp3", "text": "Laufen ist ein Verb"},
    {"filename": "schnell_adj.mp3", "text": "Schnell ist ein Adjektiv"},
    {"filename": "haende.mp3", "text": "Hände schreibt man mit Ä"},
    {"filename": "haeuser.mp3", "text": "Häuser schreibt man mit Ä U"},
    {"filename": "baeume.mp3", "text": "Bäume schreibt man mit Ä U"},
    {"filename": "maeuse.mp3", "text": "Mäuse schreibt man mit Ä U"},
    {"filename": "halbschriftlich1.mp3", "text": "Dreihundertfünfundsiebzig"}
])

for n in range(1, 21):
    AUDIO_TASKS.append({"filename": f"zehnerfeld{n}.mp3", "text": f"Das sind {n} Punkte"})

for a in range(1, 11):
    for b in range(1, 11):
        res = a * b
        AUDIO_TASKS.append({"filename": f"{a}x{b}.mp3", "text": f"{a} mal {b} ist gleich {res}"})

def download_hd_audio():
    print("🎙 Generiere 50 Anlaut-Audios & gesamte Wörterbuch-Pipeline...")
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
