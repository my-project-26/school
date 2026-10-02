import os
import urllib.request
import urllib.parse

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 40 SILBEN WÖRTER FÜR DIE 1. KLASSE
SILBEN_40 = [
    ("hund_silben", "Hund hat eine Silbe"),
    ("haus_silben", "Haus hat eine Silbe"),
    ("frosch_silben", "Frosch hat eine Silbe"),
    ("ball_silben", "Ball hat eine Silbe"),
    ("baum_silben", "Baum hat eine Silbe"),
    ("fisch_silben", "Fisch hat eine Silbe"),
    {"filename": "maus_silben.mp3", "text": "Maus hat eine Silbe"},
    {"filename": "uhr_silben.mp3", "text": "Uhr hat eine Silbe"},
    {"filename": "brot_silben.mp3", "text": "Brot hat eine Silbe"},
    {"filename": "stern_silben.mp3", "text": "Stern hat eine Silbe"},
    
    {"filename": "katze_silben.mp3", "text": "Kat ze hat zwei Silben"},
    {"filename": "blume_silben.mp3", "text": "Blu me hat zwei Silben"},
    {"filename": "sonne_silben.mp3", "text": "Son ne hat zwei Silben"},
    {"filename": "vogel_silben.mp3", "text": "Vo gel hat zwei Silben"},
    {"filename": "wolke_silben.mp3", "text": "Wol ke hat zwei Silben"},
    {"filename": "lampe_silben.mp3", "text": "Lam pe hat zwei Silben"},
    {"filename": "apfel_silben.mp3", "text": "Ap fel hat zwei Silben"},
    {"filename": "kerze_silben.mp3", "text": "Ker ze hat zwei Silben"},
    {"filename": "schule_silben.mp3", "text": "Schu le hat zwei Silben"},
    {"filename": "tafel_silben.mp3", "text": "Ta fel hat zwei Silben"},
    {"filename": "tasche_silben.mp3", "text": "Ta sche hat zwei Silben"},
    {"filename": "puppe_silben.mp3", "text": "Pup pe hat zwei Silben"},
    {"filename": "biene_silben.mp3", "text": "Bie ne hat zwei Silben"},
    {"filename": "eule_silben.mp3", "text": "Eu le hat zwei Silben"},
    {"filename": "kirsche_silben.mp3", "text": "Kir sche hat zwei Silben"},

    {"filename": "tomate_silben.mp3", "text": "To ma te hat drei Silben"},
    {"filename": "banane_silben.mp3", "text": "Ba na ne hat drei Silben"},
    {"filename": "schmetterling_silben.mp3", "text": "Schmet ter ling hat drei Silben"},
    {"filename": "elefant_silben.mp3", "text": "E le fant hat drei Silben"},
    {"filename": "rakete_silben.mp3", "text": "Ra ke te hat drei Silben"},
    {"filename": "gitarre_silben.mp3", "text": "Gi tar re hat drei Silben"},
    {"filename": "zitrone.mp3", "text": "Zi tro ne hat drei Silben"},
    {"filename": "delfin_silben.mp3", "text": "Del fin hat zwei Silben"},
    {"filename": "papagei_silben.mp3", "text": "Pa pa gei hat drei Silben"},
    {"filename": "krokodil_silben.mp3", "text": "Kro ko dil hat drei Silben"},
    {"filename": "pinguin_silben.mp3", "text": "Pin gu in hat drei Silben"},

    {"filename": "schokolade_silben.mp3", "text": "Scho ko la de hat vier Silben"},
    {"filename": "marienkaefer_silben.mp3", "text": "Ma ri en kä fer hat vier Silben"},
    {"filename": "schneemann_silben.mp3", "text": "Schnee mann hat zwei Silben"},
    {"filename": "regenbogen_silben.mp3", "text": "Re gen bo gen hat vier Silben"}
]

# Ergänzungs-Pipeline für 50 Anlaute
ANLAUTE_50 = [
    ("apfel", "A wie Apfel"), ("baer", "B wie Bär"), ("clown", "C wie Clown"), ("drache", "D wie Drache"),
    ("elefant", "E wie Elefant"), ("fisch", "F wie Fisch"), ("giraffe", "G wie Giraffe"), ("haus", "H wie Haus"),
    ("igel", "I wie Igel"), ("jacke", "J wie Jacke"), ("krokodil", "K wie Krokodil"), ("loewe", "L wie Löwe"),
    ("maus", "M wie Maus"), ("nadel", "N wie Nadel"), ("oma", "O wie Oma"), ("pinguin", "P wie Pinguin"),
    ("qualle", "Q wie Qualle"), ("robbe", "R wie Robbe"), ("sonne", "S wie Sonne"), ("tiger", "T wie Tiger"),
    ("uhr", "U wie Uhr"), ("vogel", "V wie Vogel"), ("wal", "W wie Wal"), ("xylophon", "X wie Xylophon"),
    ("yoga", "Y wie Yoga"), ("zebra", "Z wie Zebra"), ("ente", "E wie Ente"), ("eichhoernchen", "E wie Eichhörnchen"),
    ("insel", "I wie Insel"), ("otter", "O wie Otter"), ("uhustufe", "U wie Uhu"), ("ampel", "A wie Ampel"),
    ("ball", "B wie Ball"), ("delfin", "D wie Delfin"), ("eule", "E wie Eule"), ("frosch", "F wie Frosch"),
    ("gitarre", "G wie Gitarre"), ("hund", "H wie Hund"), ("indianer", "I wie Indianer"), ("kaefer", "K wie Käfer"),
    ("lampe", "L wie Lampe"), ("mond", "M wie Mond"), ("nuss", "N wie Nuss"), ("papagei", "P wie Papagei"),
    ("rakete", "R wie Rakete"), ("schaf", "S wie Schaf"), ("tomate", "T wie Tomate"), ("vulkan", "V wie Vulkan"),
    ("wolke", "W wie Wolke"), ("zitrone_anlaut", "Z wie Zitrone")
]

AUDIO_TASKS = [{"filename": f"{item[0]}.mp3", "text": item[1]} for item in SILBEN_40 if isinstance(item, tuple)]
for item in SILBEN_40:
    if isinstance(item, dict):
        AUDIO_TASKS.append(item)

for item in ANLAUTE_50:
    AUDIO_TASKS.append({"filename": f"{item[0]}.mp3", "text": item[1]})

# Wortarten & Rechtschreibung
AUDIO_TASKS.extend([
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
    print("🎙 Generiere HD-Audio für 40 Silben-Wörter & Gesamtsystem...")
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
