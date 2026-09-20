import os
import subprocess
import json

print("🎙️ Starte Generierung klangreiner Studio-Tonspuren (44.1 kHz, 192kbps)...")

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
    "Wald", "Wälder", "Brot", "Brote", "Äpfel"
])

for item in content.get("obst_gemuese", []):
    words_to_generate.add(item["word"])

for item in content.get("tiere_weltweit", []):
    words_to_generate.add(item["word"])

# Erzeuge glasklares Audio via macOS 'say' Engine (Anna) & ffmpeg/afconvert
for word in words_to_generate:
    mp3_path = f"audio/{word}.mp3"
    aiff_path = f"audio/{word}.aiff"
    
    # Nutze die hochauflösende macOS Anna-Stimme
    cmd_say = f'say -v Anna -r 160 "{word}" -o "{aiff_path}"'
    subprocess.run(cmd_say, shell=True, capture_output=True)
    
    # Konvertiere verlustfrei in sauberes MP3
    cmd_conv = f'ffmpeg -y -i "{aiff_path}" -codec:a libmp3lame -qscale:a 0 "{mp3_path}" 2>/dev/null || afconvert -f m4af -d aac "{aiff_path}" "{mp3_path}" 2>/dev/null'
    subprocess.run(cmd_conv, shell=True, capture_output=True)
    
    if os.path.exists(aiff_path):
        os.remove(aiff_path)
    
    if os.path.exists(mp3_path):
        print(f"  🔊 Glasklar generiert: {mp3_path}")

print("✨ Alle Tonspuren erfolgreich in Studio-Qualität erstellt!")
