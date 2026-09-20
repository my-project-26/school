import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Oder mistral / phi3 / qwen2 je nach installierter Version

def generate_with_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            return json.loads(res["response"])
    except Exception as e:
        print(f"⚠️ Ollama-Verbindungsfehler ({e}). Nutze Fallback.")
        return None

def build_content_database():
    print("🧠 Generiere Wortarten-Aufgaben via Ollama...")
    prompt = """
    Du bist Grundschullehrer in Baden-Württemberg. Generiere ein JSON mit 3 Sätzen zur Wortarten-Bestimmung (3. Klasse).
    Antworte AUSSCHLIESSLICH im Format:
    {
      "tasks": [
        {"sentence": "Der schnelle Hund rennt.", "target": "schnelle", "type": "Adjektiv"},
        {"sentence": "Die Katze schläft auf dem Sofa.", "target": "Katze", "type": "Nomen"}
      ]
    }
    """
    ollama_data = generate_with_ollama(prompt)
    
    database = {
        "klasse3_wortarten": ollama_data.get("tasks", []) if ollama_data else []
    }
    
    with open("content.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    print("✨ 'content.json' wurde von Ollama aktualisiert!")

if __name__ == "__main__":
    build_content_database()
