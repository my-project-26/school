import json
import os
import urllib.request
import urllib.error

# Dateipfad zur words.json
WORDS_FILE = "words.json"

# --- REGELBASIERTER WORTSCHATZ-BAUSTEIN (Garantierte Qualität für Klasse 3) ---
RULE_BASED_WORDS = [
    # Kategorie: Familie & Haus
    {"category": "Familie & Haus", "strategy": "Ableiten", "baseWord": "Hand", "gapText": "H?", "fullWord": "Hände", "instruction": "Leite ab von Hand", "hint": "💡 Tipp: Ableiten von Hand", "options": ["ände", "ende"], "correctIndex": 0},
    {"category": "Familie & Haus", "strategy": "Ableiten", "baseWord": "Haus", "gapText": "H?", "fullWord": "Häuser", "instruction": "Leite ab von Haus", "hint": "💡 Tipp: Ableiten von Haus", "options": ["euser", "äuser"], "correctIndex": 1},
    {"category": "Familie & Haus", "strategy": "Verlängern", "baseWord": "Hund", "gapText": "Hun?", "fullWord": "Hund", "instruction": "Verlängere: Hunde", "hint": "💡 Tipp: Wir hören d bei Hun-de", "options": ["d", "t"], "correctIndex": 0},
    {"category": "Familie & Haus", "strategy": "Verlängern", "baseWord": "Kind", "gapText": "Kin?", "fullWord": "Kind", "instruction": "Verlängere: Kinder", "hint": "💡 Tipp: Wir hören d bei Kin-der", "options": ["d", "t"], "correctIndex": 0},
    {"category": "Familie & Haus", "strategy": "Merkwort", "baseWord": "Oma", "gapText": "Om?", "fullWord": "Oma", "instruction": "Familie: Oma", "hint": "💡 Tipp: Großmutter", "options": ["a", "ah"], "correctIndex": 0},
    {"category": "Familie & Haus", "strategy": "Merkwort", "baseWord": "Opa", "gapText": "Op?", "fullWord": "Opa", "instruction": "Familie: Opa", "hint": "💡 Tipp: Großvater", "options": ["a", "ah"], "correctIndex": 0},
    {"category": "Familie & Haus", "strategy": "Merkwort", "baseWord": "Bruder", "gapText": "Br?", "fullWord": "Bruder", "instruction": "Familie: Bruder", "hint": "💡 Tipp: Ein Familienmitglied", "options": ["uder", "ooder"], "correctIndex": 0},
    {"category": "Familie & Haus", "strategy": "Merkwort", "baseWord": "Schwester", "gapText": "Schw?", "fullWord": "Schwester", "instruction": "Familie: Schwester", "hint": "💡 Tipp: Ein Familienmitglied", "options": ["ester", "äster"], "correctIndex": 0},

    # Kategorie: Natur, Garten & Tiere
    {"category": "Natur & Tiere", "strategy": "Ableiten", "baseWord": "Maus", "gapText": "M?", "fullWord": "Mäuse", "instruction": "Leite ab von Maus", "hint": "💡 Tipp: Ableiten von Maus", "options": ["euse", "äuse"], "correctIndex": 1},
    {"category": "Natur & Tiere", "strategy": "Ableiten", "baseWord": "Baum", "gapText": "B?", "fullWord": "Bäume", "instruction": "Leite ab von Baum", "hint": "💡 Tipp: Ableiten von Baum", "options": ["äume", "eume"], "correctIndex": 0},
    {"category": "Natur & Tiere", "strategy": "Ableiten", "baseWord": "Wald", "gapText": "W?", "fullWord": "Wälder", "instruction": "Leite ab von Wald", "hint": "💡 Tipp: Ableiten von Wald", "options": ["älder", "elder"], "correctIndex": 0},
    {"category": "Natur & Tiere", "strategy": "Ableiten", "baseWord": "Garten", "gapText": "G?", "fullWord": "Gärtner", "instruction": "Leite ab von Garten", "hint": "💡 Tipp: Ableiten von Garten", "options": ["ertner", "ärtner"], "correctIndex": 1},

    # Kategorie: Alltag & Fahrzeuge
    {"category": "Alltag & Fahrzeuge", "strategy": "Ableiten", "baseWord": "Rad", "gapText": "R?", "fullWord": "Räder", "instruction": "Leite ab von Rad", "hint": "💡 Tipp: Gehört zum Auto (Rad -> Räder)", "options": ["äder", "eder"], "correctIndex": 0},
    {"category": "Alltag & Fahrzeuge", "strategy": "Verlängern", "baseWord": "Tag", "gapText": "Ta?", "fullWord": "Tag", "instruction": "Verlängere: Tage", "hint": "💡 Tipp: Wir hören g bei Ta-ge", "options": ["g", "k"], "correctIndex": 0},
    {"category": "Alltag & Fahrzeuge", "strategy": "Verlängern", "baseWord": "Gelb", "gapText": "gel?", "fullWord": "gelb", "instruction": "Verlängere: gelbe", "hint": "💡 Tipp: Wir hören b bei gel-be", "options": ["b", "p"], "correctIndex": 0}
]

def load_existing_words():
    """Lädt vorhandene Wörter aus der words.json Datei."""
    if os.path.exists(WORDS_FILE):
        try:
            with open(WORDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️️ Warnung: words.json war beschädigt. Erstelle neu.")
            return []
    return []

def save_words(words):
    """Speichert die Wortliste mit fortlaufender ID sauber formatiert ab."""
    for idx, item in enumerate(words, start=1):
        item["id"] = idx

    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print(f"✅ Erfolgreich {len(words)} Wörter in '{WORDS_FILE}' gespeichert.")

def generate_via_ollama(model="llama3", prompt_topic="Schule und Alltag"):
    """
    Versucht, über eine lokale Ollama-Instanz zusätzliche Wörter zu generieren.
    Voraussetzung: Ollama läuft lokal auf Port 11434.
    """
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
Du bist ein Grundschullehrer für die 3. Klasse in Baden-Württemberg.
Generiere 3 Wörter für die Rechtschreibübung zum Thema "{prompt_topic}".
Antworte AUSSCHLIESSLICH mit einem gültigen JSON-Array ohne Markdown-Codeblöcke.

Schema für jedes Objekt:
{{
  "category": "{prompt_topic}",
  "strategy": "Ableiten" oder "Verlängern" oder "Merkwort",
  "baseWord": "Grundwort",
  "gapText": "Wort mit Fragezeichen an der Lücke",
  "fullWord": "Vollständiges Wort",
  "instruction": "Kurze Anweisung für Grundschüler",
  "hint": "💡 Tipp: ...",
  "options": ["Option1", "Option2"],
  "correctIndex": 0 oder 1
}}
"""

    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        print(f"🤖 Anfrage an Ollama ({model}) läuft...")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            generated_json = json.loads(res_data["response"])
            return generated_json
    except urllib.error.URLError:
        print("ℹ️ Lokales Ollama nicht erreichbar. Nutze regelbasierte Wortschatz-Generierung.")
        return []
    except Exception as e:
        print(f"⚠️ Fehler bei der Ollama-Verarbeitung: {e}")
        return []

def main():
    print("🚀 Starte Wortschatz-Generator für Schul App...")
    
    existing_words = load_existing_words()
    existing_full_words = {item["fullWord"].lower() for item in existing_words}

    # 1. Regelbasierte Wörter hinzufügen (falls noch nicht vorhanden)
    added_count = 0
    for word_obj in RULE_BASED_WORDS:
        if word_obj["fullWord"].lower() not in existing_full_words:
            existing_words.append(word_obj)
            existing_full_words.add(word_obj["fullWord"].lower())
            added_count += 1

    print(f"📦 {added_count} neue Wörter aus dem vordefinierten Grundwortschatz ergänzt.")

    # 2. Versuch, über Ollama dynamisch zu erweitern
    ollama_words = generate_via_ollama()
    if ollama_words and isinstance(ollama_words, list):
        for word_obj in ollama_words:
            if "fullWord" in word_obj and word_obj["fullWord"].lower() not in existing_full_words:
                existing_words.append(word_obj)
                existing_full_words.add(word_obj["fullWord"].lower())
                print(f"✨ KI-Wort hinzugefügt: {word_obj['fullWord']}")

    # 3. Speichern
    save_words(existing_words)

if __name__ == "__main__":
    main()
